# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Functions for inference using a trained model"""

import json
import logging
import os
import pickle
import time
import torch

from azureml.contrib.automl.dnn.vision.common.dataloaders import RobustDataLoader
from azureml.contrib.automl.dnn.vision.common.labeled_dataset_helper import AmlLabeledDatasetHelper
from azureml.contrib.automl.dnn.vision.common.utils import _data_exception_safe_iterator, log_end_scoring_stats
from azureml.contrib.dataset.labeled_dataset import _LabeledDatasetFactory
from azureml.core.experiment import Experiment
from azureml.core.run import Run, _OfflineRun

from ..data.datasets import PredictionDataset_yolo
from ..utils.utils import non_max_suppression, unpad_bbox
from ..common.constants import ArtifactLiterals, ScoringParameters, YoloLiterals
from ...common.average_meter import AverageMeter
from ...common.system_meter import SystemMeter

logger = logging.getLogger(__name__)


def _load_model_wrapper(torch_model_file, model_wrapper_pkl, **model_settings):
    with open(model_wrapper_pkl, 'rb') as fp:
        model_wrapper = pickle.load(fp)

    model_weights = torch.load(torch_model_file)
    model_wrapper.restore_model(model_weights, **model_settings)

    return model_wrapper


def _distill_run_from_experiment(run_id, experiment_name=None):
    current_experiment = Run.get_context().experiment
    experiment = current_experiment

    if experiment_name is not None:
        workspace = current_experiment.workspace
        experiment = Experiment(workspace, experiment_name)

    return Run(experiment=experiment, run_id=run_id)


def _fetch_model_from_artifacts(run_id, experiment_name=None, **model_settings):
    logger.info("Start fetching model from artifacts")
    run = _distill_run_from_experiment(run_id, experiment_name)

    run.download_file(os.path.join(ArtifactLiterals.OUTPUT_DIR, ArtifactLiterals.MODEL_FILE_NAME),
                      ArtifactLiterals.MODEL_FILE_NAME)
    run.download_file(os.path.join(ArtifactLiterals.OUTPUT_DIR, ArtifactLiterals.PICKLE_FILE_NAME),
                      ArtifactLiterals.PICKLE_FILE_NAME)

    logger.info("Finished downloading files from artifacts")

    return _load_model_wrapper(ArtifactLiterals.MODEL_FILE_NAME, ArtifactLiterals.PICKLE_FILE_NAME,
                               **model_settings)


def _get_box_dims(image_shape, box):
    box_keys = ['topX', 'topY', 'bottomX', 'bottomY']
    height, width = image_shape[0], image_shape[1]

    box_dims = dict(zip(box_keys, [coordinate.item() for coordinate in box]))

    box_dims['topX'] = box_dims['topX'] * 1.0 / width
    box_dims['bottomX'] = box_dims['bottomX'] * 1.0 / width
    box_dims['topY'] = box_dims['topY'] * 1.0 / height
    box_dims['bottomY'] = box_dims['bottomY'] * 1.0 / height

    return box_dims


def _write_prediction_file_line(fw, filename, label, image_shape, classes):
    bounding_boxes = []
    for box, label_index, score in zip(label['boxes'], label['labels'], label['scores']):
        box_dims = _get_box_dims(image_shape, box)

        box_record = {'box': box_dims,
                      'label': classes[label_index],
                      'score': score.item()}

        bounding_boxes.append(box_record)

    annotation = {'filename': filename,
                  'boxes': bounding_boxes}

    fw.write('{}\n'.format(json.dumps(annotation)))


def _write_dataset_file_line(fw, filename, label, image_shape, classes):
    labels = []
    scores = []
    for box, label_index, score in zip(label['boxes'], label['labels'], label['scores']):
        label_record = _get_box_dims(image_shape, box)
        label_record['label'] = classes[label_index]

        labels.append(label_record)
        scores.append(score.item())

    AmlLabeledDatasetHelper.write_dataset_file_line(
        fw,
        filename,
        scores,
        labels)


def _convert_to_rcnn_output(output, image, pad):
    # output: nx6 (x1, y1, x2, y2, conf, cls)
    rcnn_label = {"boxes": [], "labels": [], "scores": []}

    # Adjust bbox to effective image bounds
    _, height, width = image.shape
    img_height, img_width = unpad_bbox(output[:, :4] if output is not None else None, (height, width), pad)

    if output is not None:
        rcnn_label["boxes"] = output[:, :4]
        rcnn_label["labels"] = output[:, 5:6].long()
        rcnn_label["scores"] = output[:, 4:5]

    return rcnn_label, (img_height, img_width)


def _get_workspace(run):
    return None if isinstance(run, _OfflineRun) else run.experiment.workspace


def _score_with_model(model, run, target_path, output_file, root_dir,
                      image_list_file, batch_size=1,
                      ignore_data_errors=True,
                      labeled_dataset_factory=_LabeledDatasetFactory,
                      labeled_dataset_file="labeled_dataset.json",
                      input_dataset_id=None, always_create_dataset=False,
                      num_workers=None):

    classes = model.names
    model.eval()

    score_start = time.time()

    ws = _get_workspace(run)
    logger.info("Building the prediction dataset")

    # TODO: use PIL instead of CV, similar to faster-rcnn
    dataset = PredictionDataset_yolo(root_dir=root_dir, image_list_file=image_list_file,
                                     ignore_data_errors=ignore_data_errors,
                                     input_dataset_id=input_dataset_id, ws=ws)

    dataloader = RobustDataLoader(dataset, batch_size=batch_size, collate_fn=dataset.collate_fn,
                                  num_workers=num_workers)

    batch_time = AverageMeter()
    end = time.time()
    system_meter = SystemMeter()

    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    model.to(device)

    logger.info("Starting the inference")

    with torch.no_grad():
        try:
            with open(output_file, "w") as fw, open(labeled_dataset_file, "w") as ldsf:
                # count number of lines written to prediction
                prediction_num_lines = 0
                for i, (filenames, image_batch, pads) in enumerate(_data_exception_safe_iterator(iter(dataloader))):
                    image_batch = image_batch.to(device).float() / 255.0
                    inf_out, _ = model(image_batch)

                    # Run NMS
                    outputs = non_max_suppression(inf_out,
                                                  conf_thres=model.settings[YoloLiterals.BOX_SCORE_THRESH],
                                                  iou_thres=model.settings[YoloLiterals.BOX_IOU_THRESH])

                    for filename, output, image, pad in zip(filenames, outputs, image_batch, pads):
                        prediction_num_lines += 1
                        # convert yolo output to faster-rcnn output format
                        label, image_shape = _convert_to_rcnn_output(output, image, pad)

                        _write_prediction_file_line(fw, filename, label, image_shape, classes)
                        _write_dataset_file_line(ldsf, filename,
                                                 label, image_shape, classes)

                    batch_time.update(time.time() - end)
                    end = time.time()
                    if i % 100 == 0 or i == len(dataloader) - 1:
                        mesg = "Epoch: [{0}/{1}]\t" "Time {batch_time.value:.4f}" \
                               " ({batch_time.avg:.4f})\t".format(i, len(dataloader), batch_time=batch_time)
                        mesg += system_meter.get_gpu_stats()
                        logger.info(mesg)
                        system_meter.log_system_stats(True)

                logger.info("Number of lines written to prediction file: {}".format(prediction_num_lines))

            if always_create_dataset or input_dataset_id is not None:
                datastore = ws.get_default_datastore()
                AmlLabeledDatasetHelper.create(run, datastore, labeled_dataset_file, target_path,
                                               'ObjectDetection', labeled_dataset_factory)

        finally:
            os.remove(labeled_dataset_file)

    # measure total scoring time
    score_time = time.time() - score_start
    log_end_scoring_stats(score_time, batch_time, system_meter)


def score(run_id, experiment_name=None, output_file=None, root_dir=None, image_list_file=None, batch_size=16,
          ignore_data_errors=True, output_dataset_target_path=None, input_dataset_id=None, **model_settings):
    """Load model and infer on new data.

    :param run_id: Name of the run to load model from
    :type run_id: String
    :param experiment_name: Name of experiment to load model from
    :type experiment_name: String
    :param output_file: Name of file to write results to
    :type output_file: String
    :param root_dir: prefix to be added to the paths contained in image_list_file
    :type root_dir: str
    :param image_list_file: path to file containing list of images
    :type image_list_file: str
    :batch_size: Inference batch size
    :type batch_size: Int
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dataset_target_path: path on Datastore for the output dataset files.
    :type output_dataset_target_path: str
    :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
    :type input_dataset_id: str
    :param model_settings: Optional keyword arguments to define model specifications
    :type model_settings: Dictionary
    """
    logger.info("[start prediction: batch_size: {}]".format(batch_size))
    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    model_wrapper = _fetch_model_from_artifacts(run_id, experiment_name, **model_settings)
    logger.info("Model restored successfully")

    current_scoring_run = Run.get_context()

    if output_dataset_target_path is None:
        output_dataset_target_path = AmlLabeledDatasetHelper.get_default_target_path()

    num_workers = ScoringParameters.DEFAULT_NUM_WORKERS

    _score_with_model(model_wrapper, current_scoring_run, output_dataset_target_path, output_file=output_file,
                      root_dir=root_dir, image_list_file=image_list_file,
                      batch_size=batch_size, ignore_data_errors=ignore_data_errors,
                      input_dataset_id=input_dataset_id, num_workers=num_workers)
