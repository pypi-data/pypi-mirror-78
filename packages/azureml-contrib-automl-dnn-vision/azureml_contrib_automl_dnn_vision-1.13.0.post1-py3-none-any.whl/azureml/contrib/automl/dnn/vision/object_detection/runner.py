# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Entry script that is invoked by the driver script from automl."""

import argparse
import os
import torch

from azureml.automl.core.shared import log_server
from azureml.automl.core.shared.exceptions import ClientException
from azureml.contrib.automl.dnn.vision.common.utils import _safe_exception_logging, _merge_settings_args_defaults, \
    _make_arg, _save_image_df, _save_od_image_files, _set_random_seed, _set_logging_parameters, \
    _set_deterministic

from azureml.train.automl import constants
from .data import datasets, loaders
from .models import detection
from .trainer import optimize, lrschedule, criterion, train
from .eval import cocotools, vocmap
from .writers import modelsaver
from .common.constants import TrainingParameters, LearningParameters, SchedulerParameters, \
    ArtifactLiterals, training_settings_defaults, TrainingLiterals, FasterRCNNLiterals, FasterRCNNParameters, \
    DistributedLiterals, DistributedParameters, DataLoaderParameterLiterals, LRSchedulerNames
from ..common import distributed_utils
from ..common.constants import SettingsLiterals
from ..common.exceptions import AutoMLVisionSystemException
from ..common.logging_utils import get_logger

from azureml.core.run import Run

from ..common.system_meter import SystemMeter

azureml_run = Run.get_context()

logger = get_logger(__name__)


def read_aml_dataset(dataset_id, validation_dataset_id, ignore_data_errors, output_dir, master_process):
    """Read the training and validation datasets from AML datasets.

    :param dataset_id: Training dataset id
    :type dataset_id: str
    :param validation_dataset_id: Validation dataset id
    :type dataset_id: str
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dir: where to save train and val files
    :type output_dir: str
    :param master_process: boolean flag indicating whether current process is master or not.
    :type master_process: bool
    :return: Training dataset and validation dataset
    :rtype: Tuple of form (AmlDatasetObjectDetectionWrapper, AmlDatasetObjectDetectionWrapper)
    """
    ws = Run.get_context().experiment.workspace

    # Assumption is that aml dataset files are already downloaded to local path
    # by a call to cache_required_files()
    download_files = False

    if validation_dataset_id is not None:
        training_dataset = datasets.AmlDatasetObjectDetectionWrapper(dataset_id, is_train=True,
                                                                     ignore_data_errors=ignore_data_errors,
                                                                     workspace=ws, download_files=download_files)
        validation_dataset = datasets.AmlDatasetObjectDetectionWrapper(validation_dataset_id, is_train=False,
                                                                       ignore_data_errors=ignore_data_errors,
                                                                       workspace=ws, download_files=download_files)

        if master_process:
            _save_image_df(train_df=training_dataset.get_images_df(),
                           val_df=validation_dataset.get_images_df(),
                           output_dir=output_dir)

    else:
        dataset = datasets.AmlDatasetObjectDetectionWrapper(dataset_id, is_train=True,
                                                            ignore_data_errors=ignore_data_errors,
                                                            workspace=ws, download_files=download_files)
        training_dataset, validation_dataset = dataset.train_val_split()
        if master_process:
            _save_image_df(train_df=dataset.get_images_df(), train_index=training_dataset._indices,
                           val_index=validation_dataset._indices, output_dir=output_dir)

    return training_dataset, validation_dataset


def read_file_dataset(image_folder, annotations_file, annotations_test_file, ignore_data_errors,
                      output_dir, master_process):
    """Read the training and validation datasets from annotation files.

    :param image_folder: target image path
    :type image_folder: str
    :param annotations_file: Training annotations file
    :type annotations_file: str
    :param annotations_test_file: Validation annotations file
    :type annotations_test_file: str
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dir: where to save train and val files
    :type output_dir: str
    :param master_process: boolean flag indicating whether current process is master or not.
    :type master_process: bool
    :return: Training dataset and validation dataset
    :rtype: Tuple of form (FileObjectDetectionDatasetWrapper, FileObjectDetectionDatasetWrapper)
    """
    if image_folder is None:
        raise ClientException("images_folder or dataset_id needs to be specified", has_pii=False)

    if annotations_file is None:
        raise ClientException("labels_file needs to be specified", has_pii=False)

    if annotations_test_file:
        training_dataset = datasets.FileObjectDetectionDatasetWrapper(annotations_file, image_folder,
                                                                      is_train=True,
                                                                      ignore_data_errors=ignore_data_errors)
        validation_dataset = datasets.FileObjectDetectionDatasetWrapper(annotations_test_file,
                                                                        image_folder, is_train=False,
                                                                        ignore_data_errors=ignore_data_errors)
    else:
        dataset = datasets.FileObjectDetectionDatasetWrapper(annotations_file, image_folder, is_train=True,
                                                             ignore_data_errors=ignore_data_errors)
        training_dataset, validation_dataset = dataset.train_val_split()
        if master_process:
            _save_od_image_files(train_ds=training_dataset, val_ds=validation_dataset, output_dir=output_dir)

    return training_dataset, validation_dataset


def download_required_files(settings):
    """ Download files required for Aml dataset and model setup.

    This step needs to be done before launching distributed training so that there are no concurrency issues
    where multiple processes are downloading the same file.

    :param settings: Dictionary with all training and model settings
    :type settings: Dict
    """

    # Download aml dataset to local disk
    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)

    if dataset_id is not None:
        ws = Run.get_context().experiment.workspace
        logger.info("Downloading training dataset files to local disk.")
        datasets.AmlDatasetObjectDetectionWrapper.download_image_files(dataset_id, ws)
        if validation_dataset_id is not None:
            logger.info("Downloading validation dataset files to local disk.")
            datasets.AmlDatasetObjectDetectionWrapper.download_image_files(validation_dataset_id, ws)

    # Download pretrained model weights and cache on local disk
    logger.info("Downloading pretrained model weights to local disk.")
    model_name = settings[TrainingLiterals.MODEL_NAME]
    detection.download_model_weights(model_name=model_name)


@_safe_exception_logging
def run(automl_settings):
    """Invoke training by passing settings and write the resulting model.

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    """
    settings, unknown = _parse_argument_settings(automl_settings)

    task_type = constants.Tasks.IMAGE_OBJECT_DETECTION
    _set_logging_parameters(task_type, settings)

    # TODO JEDI
    # When we expose the package to customers we need to revisit. We should not log any unknown
    # args when the customers send their hp space.
    if unknown:
        logger.info("Got unknown args, will ignore them: {}".format(unknown))

    # TODO JEDI
    # This is ok to log now because it can only be system metadata. When we expose the package to customers
    # we need to revisit.
    logger.info("Final settings: \n {}".format(settings))

    # Download required files before launching train_worker to avoid concurrency issues in distributed mode
    download_required_files(settings)

    # Decide to train in distributed mode or not based on gpu device count and distributed flag
    distributed = settings[DistributedLiterals.DISTRIBUTED]
    device_count = torch.cuda.device_count() if torch.cuda.is_available() else 0
    if distributed and device_count > 1:
        logger.info("Starting distributed training with world_size: {}.".format(device_count))
        os.environ[log_server.HOST_ENV_NAME] = log_server.server_host
        os.environ[log_server.PORT_ENV_NAME] = str(log_server.server_port)
        settings.update({
            DistributedLiterals.WORLD_SIZE: device_count
        })
        # Launch multiple processes
        torch.multiprocessing.spawn(train_worker, args=(True, settings), nprocs=device_count, join=True)
    else:
        if distributed:
            logger.warning("Distributed flag is {}, but is not supported as the device_count is {}. "
                           "Training using a single process.".format(distributed, device_count))
        train_worker(0, False, settings)


def train_worker(rank, distributed, settings):
    """Invoke training on a single device and write the resulting model.

    :param rank: Rank of the process if invoked in distributed mode. 0 otherwise.
    :type rank: int
    :param distributed: Distributed mode or not.
    :type distributed: bool
    :param settings: Dictionary with all training and model settings
    :type settings: Dictionary
    """
    if distributed:
        world_size = settings.get(DistributedLiterals.WORLD_SIZE, None)
        if world_size is None:
            msg = "{} parameter is missing from settings in distributed mode.".format(DistributedLiterals.WORLD_SIZE)
            logger.error(msg)
            raise AutoMLVisionSystemException(msg, has_pii=False)

        # init process group
        logger.info("Setting up process group for worker {}".format(rank))
        os.environ[DistributedLiterals.MASTER_ADDR] = settings[DistributedLiterals.MASTER_ADDR]
        os.environ[DistributedLiterals.MASTER_PORT] = settings[DistributedLiterals.MASTER_PORT]
        torch.cuda.set_device(rank)
        torch.distributed.init_process_group(backend=DistributedParameters.DEFAULT_BACKEND,
                                             rank=rank, world_size=world_size)

    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    model_name = settings[TrainingLiterals.MODEL_NAME]
    device = torch.device("cuda:" + str(rank)) if distributed else settings[SettingsLiterals.DEVICE]
    master_process = distributed_utils.master_process()

    training_settings = {"number_of_epochs": settings[TrainingLiterals.NUMBER_OF_EPOCHS],
                         "lr": settings[TrainingLiterals.LEARNING_RATE] * distributed_utils.get_world_size(),
                         "momentum": settings[TrainingLiterals.MOMENTUM],
                         "weight_decay": settings[TrainingLiterals.WEIGHT_DECAY],
                         "max_patience_iterations": settings[TrainingLiterals.MAX_PATIENCE_ITERATIONS],
                         "primary_metric": settings[TrainingLiterals.PRIMARY_METRIC],
                         "enable_coco_validation": settings[TrainingLiterals.ENABLE_COCO_VALIDATION],
                         "early_stop_delay_iterations": settings[TrainingLiterals.EARLY_STOP_DELAY_ITERATIONS]}

    fasterrcnn_settings = {"min_size": settings[FasterRCNNLiterals.MIN_SIZE],
                           "box_score_thresh": settings[FasterRCNNLiterals.BOX_SCORE_THRESH],
                           "box_nms_thresh": settings[FasterRCNNLiterals.BOX_NMS_THRESH],
                           "box_detections_per_img": settings[FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG]}

    # Set dataloaders' num_workers
    num_workers = settings.get(SettingsLiterals.NUM_WORKERS, None)

    train_data_loader_settings = {
        DataLoaderParameterLiterals.BATCH_SIZE: settings[TrainingLiterals.TRAINING_BATCH_SIZE],
        DataLoaderParameterLiterals.SHUFFLE: True,
        DataLoaderParameterLiterals.NUM_WORKERS: num_workers,
        DataLoaderParameterLiterals.DISTRIBUTED: distributed,
        DataLoaderParameterLiterals.DROP_LAST: False}

    validation_data_loader_settings = {
        DataLoaderParameterLiterals.BATCH_SIZE: settings[TrainingLiterals.VALIDATION_BATCH_SIZE],
        DataLoaderParameterLiterals.SHUFFLE: False,
        DataLoaderParameterLiterals.NUM_WORKERS: num_workers,
        DataLoaderParameterLiterals.DISTRIBUTED: distributed,
        DataLoaderParameterLiterals.DROP_LAST: False}

    # Set randomization seed for deterministic training.
    random_seed = settings.get(SettingsLiterals.RANDOM_SEED, None)
    if distributed and random_seed is None:
        # Set by default for distributed training to ensure
        # all workers have same random parameters.
        random_seed = DistributedParameters.DEFAULT_RANDOM_SEED
    _set_random_seed(random_seed)
    _set_deterministic(settings.get(SettingsLiterals.DETERMINISTIC, False))

    # Extract Automl Settings

    image_folder = settings.get(SettingsLiterals.IMAGE_FOLDER, None)

    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)

    annotations_file = settings.get(SettingsLiterals.LABELS_FILE, None)
    if annotations_file is not None:
        annotations_file = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], annotations_file)

    ignore_data_errors = settings.get(SettingsLiterals.IGNORE_DATA_ERRORS, True)
    output_directory = ArtifactLiterals.OUTPUT_DIR
    annotations_test_file = None
    resume_file = settings.get(SettingsLiterals.RESUME, None)

    if SettingsLiterals.VALIDATION_LABELS_FILE in settings:
        annotations_test_file = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT],
                                             settings[SettingsLiterals.VALIDATION_LABELS_FILE])

    # Setup Dataset

    if dataset_id is not None:
        training_dataset, validation_dataset = read_aml_dataset(dataset_id,
                                                                validation_dataset_id,
                                                                ignore_data_errors,
                                                                output_directory,
                                                                master_process)
        logger.info("[train dataset_id: {}, validation dataset_id: {}]".format(dataset_id, validation_dataset_id))
    else:
        if image_folder is None:
            raise ClientException("Image folder path needs to be specified", has_pii=False)
        else:
            image_folder = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)

        training_dataset, validation_dataset = read_file_dataset(image_folder,
                                                                 annotations_file,
                                                                 annotations_test_file,
                                                                 ignore_data_errors,
                                                                 output_directory,
                                                                 master_process)

    if training_dataset.classes != validation_dataset.classes:
        all_classes = list(set(training_dataset.classes + validation_dataset.classes))
        training_dataset.reset_classes(all_classes)
        validation_dataset.reset_classes(all_classes)

    logger.info("# train images: {}, # validation images: {}, # labels: {}".format(
        len(training_dataset), len(validation_dataset), training_dataset.num_classes - 1))  # excluding "--bg--" class

    # Setup Model
    model = detection.setup_model(model_name=model_name, number_of_classes=training_dataset.num_classes,
                                  **fasterrcnn_settings)

    # TODO: Both classes and device should not be set here but in initialization
    model.classes = training_dataset.classes
    model.device = device

    # Move base model to device
    model.to_device(device)

    # if the model exposes some transformations
    # enable those in the datasets.
    training_dataset.transform = model.get_train_validation_transform()
    validation_dataset.transform = model.get_train_validation_transform()
    # Replace model.transform resize and normalize with identity methods
    # so that we avoid re-doing the transform in the model
    model.disable_model_transform()

    if distributed:
        model.model = torch.nn.parallel.DistributedDataParallel(model.model, device_ids=[rank], output_device=rank)
    model.distributed = distributed

    num_params = sum([p.data.nelement() for p in model.parameters()])
    logger.info("[model: {}, #param: {}]".format(model_name, num_params))

    # Resume

    if resume_file:
        checkpoint = torch.load(resume_file, map_location="cpu")
        model.model.load_state_dict(checkpoint)  # TODO: Fix this in case of Distributed training.

    # Setup Dataloaders

    train_loader = loaders.setup_dataloader(
        training_dataset, **train_data_loader_settings)
    validation_loader = loaders.setup_dataloader(
        validation_dataset, **validation_data_loader_settings)

    # Setup Optimizer

    optimizer = optimize.setup_optimizer(model, **training_settings)
    num_batches_per_epoch = len(train_loader)
    lr_scheduler_settings = {
        "warmup_steps": num_batches_per_epoch * 2,
        "total_steps": num_batches_per_epoch * training_settings["number_of_epochs"]
    }
    lr_scheduler = lrschedule.setup_lr_scheduler(
        optimizer, LRSchedulerNames.WARMUP_COSINE, **lr_scheduler_settings)
    loss_function = criterion.setup_criterion("FASTER_RCNN")

    # Setup Evaluation Tools

    coco_index = None
    if training_settings["enable_coco_validation"]:
        coco_index = cocotools.create_coco_index(validation_dataset)
    val_vocmap = vocmap.VocMap(validation_dataset)

    # Train Model

    train_settings = train.TrainSettings(**training_settings)
    logger.info("[start training: train batch_size: {}, val batch_size: {}, train_settings {}]".format(
        train_data_loader_settings["batch_size"], validation_data_loader_settings["batch_size"], vars(train_settings)))

    system_meter.log_system_stats()

    train.train(model=model,
                optimizer=optimizer,
                scheduler=lr_scheduler,
                train_data_loader=train_loader,
                device=device,
                criterion=loss_function,
                train_settings=train_settings,
                val_data_loader=validation_loader,
                val_coco_index=coco_index,
                val_vocmap=val_vocmap,
                enable_coco_validation=training_settings["enable_coco_validation"],
                val_index_map=model.classes,
                run=azureml_run,
                ignore_data_errors=ignore_data_errors)

    if master_process:
        # Save model

        modelsaver.write_model(model, labels=training_dataset.classes, output_dir=output_directory, device=device,
                               train_datafile=annotations_file, val_datafile=annotations_test_file,
                               enable_onnx_norm=settings[SettingsLiterals.ENABLE_ONNX_NORMALIZATION])

        folder_name = os.path.basename(output_directory)
        if azureml_run is not None:
            azureml_run.upload_folder(name=folder_name, path=output_directory)


def _parse_argument_settings(automl_settings):
    """Parse all arguments and merge settings

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    :return: tuple of the automl settings dictionary with all settings filled in and a list of any unknown args
    :rtype: tuple
    """

    parser = argparse.ArgumentParser(description="Object detection")

    # Model and Device Settings

    parser.add_argument(_make_arg(TrainingLiterals.MODEL_NAME), type=str,
                        help="model_name",
                        default=training_settings_defaults[TrainingLiterals.MODEL_NAME])

    parser.add_argument(_make_arg(SettingsLiterals.DEVICE), type=str,
                        help="Device to train on (cpu/cuda:0/cuda:1,...)",
                        default=training_settings_defaults[SettingsLiterals.DEVICE])

    # Training Related Settings

    parser.add_argument(_make_arg(TrainingLiterals.NUMBER_OF_EPOCHS), type=int,
                        help="number of training epochs",
                        default=TrainingParameters.DEFAULT_NUMBER_EPOCHS)
    parser.add_argument(_make_arg(TrainingLiterals.MAX_PATIENCE_ITERATIONS), type=int,
                        help="max number of epochs with no validation improvement",
                        default=TrainingParameters.DEFAULT_PATIENCE_ITERATIONS)
    parser.add_argument(_make_arg(TrainingLiterals.ENABLE_COCO_VALIDATION),
                        help="enable coco validation and evaluation", action="store_true")
    parser.add_argument(_make_arg(TrainingLiterals.EARLY_STOP_DELAY_ITERATIONS), type=int,
                        help="number of epochs to wait before validation improvement is tracked for early stopping",
                        default=TrainingParameters.DEFAULT_EARLY_STOP_DELAY_ITERATIONS)

    parser.add_argument(_make_arg(TrainingLiterals.LEARNING_RATE), type=float,
                        help="learning rate for optimizer",
                        default=LearningParameters.SGD_DEFAULT_LEARNING_RATE)
    parser.add_argument(_make_arg(TrainingLiterals.MOMENTUM), type=float,
                        help="momentum for optimizer",
                        default=LearningParameters.SGD_DEFAULT_MOMENTUM)
    parser.add_argument(_make_arg(TrainingLiterals.WEIGHT_DECAY), type=float,
                        help="optimizer weight decay",
                        default=LearningParameters.SGD_DEFAULT_WEIGHT_DECAY)

    parser.add_argument(_make_arg(TrainingLiterals.STEP_SIZE), type=int,
                        help="step size for learning rate scheduler",
                        default=SchedulerParameters.DEFAULT_STEP_LR_STEP_SIZE)
    parser.add_argument(_make_arg(TrainingLiterals.GAMMA), type=float,
                        help="decay rate for learning rate scheduler",
                        default=SchedulerParameters.DEFAULT_STEP_LR_GAMMA)

    # Faster-rcnn Settings

    parser.add_argument(_make_arg(FasterRCNNLiterals.MIN_SIZE), type=int,
                        help="minimum size of the image to be rescaled before feeding it to the backbone",
                        default=FasterRCNNParameters.DEFAULT_MIN_SIZE)
    parser.add_argument(_make_arg(FasterRCNNLiterals.BOX_SCORE_THRESH), type=float,
                        help="during inference, only return proposals with a classification score \
                        greater than box_score_thresh",
                        default=FasterRCNNParameters.DEFAULT_BOX_SCORE_THRESH)
    parser.add_argument(_make_arg(FasterRCNNLiterals.BOX_NMS_THRESH), type=float,
                        help="NMS threshold for the prediction head. Used during inference",
                        default=FasterRCNNParameters.DEFAULT_BOX_NMS_THRESH)
    parser.add_argument(_make_arg(FasterRCNNLiterals.BOX_DETECTIONS_PER_IMG), type=int,
                        help="maximum number of detections per image, for all classes.",
                        default=FasterRCNNParameters.DEFAULT_BOX_DETECTIONS_PER_IMG)

    # Dataloader Settings

    parser.add_argument(_make_arg(TrainingLiterals.TRAINING_BATCH_SIZE), type=int,
                        help="training batch size",
                        default=TrainingParameters.DEFAULT_TRAINING_BATCH_SIZE)

    parser.add_argument(_make_arg(TrainingLiterals.VALIDATION_BATCH_SIZE), type=int,
                        help="validation batch size",
                        default=TrainingParameters.DEFAULT_VALIDATION_BATCH_SIZE)

    parser.add_argument(_make_arg(SettingsLiterals.DATA_FOLDER),
                        _make_arg(SettingsLiterals.DATA_FOLDER.replace("_", "-")),
                        type=str,
                        help="root of the blob store",
                        default="")

    parser.add_argument(_make_arg(SettingsLiterals.LABELS_FILE_ROOT),
                        _make_arg(SettingsLiterals.LABELS_FILE_ROOT.replace("_", "-")),
                        type=str,
                        help="root relative to which label file paths exist",
                        default="")

    # Extract Commandline Settings

    args, unknown = parser.parse_known_args()

    return _merge_settings_args_defaults(automl_settings, args, training_settings_defaults), unknown
