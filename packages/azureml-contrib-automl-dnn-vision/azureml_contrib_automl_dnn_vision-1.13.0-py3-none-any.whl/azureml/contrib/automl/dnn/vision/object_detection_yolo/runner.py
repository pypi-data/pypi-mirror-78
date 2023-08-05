# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Entry script that is invoked by the driver script from automl."""

import argparse
import logging
import os

import torch.optim as optim
import torch.utils.data

from azureml.automl.core.shared.exceptions import ClientException
from azureml.contrib.automl.dnn.vision.common.constants import SettingsLiterals
from azureml.contrib.automl.dnn.vision.common.utils import _merge_settings_args_defaults, _set_logging_parameters, \
    _make_arg, _save_image_df, _save_od_image_files, init_tensorboard
from azureml.core.run import Run
from azureml.train.automl import constants

from .common.constants import ArtifactLiterals, yolo_hyp_defaults, training_settings_defaults, TrainingLiterals, \
    TrainingParameters, YoloLiterals, YoloParameters
from .data import datasets, loaders
from .models.yolo import Model
from .trainer.train import train
from .utils.utils import check_img_size, init_seeds, WarmupCosineSchedule, check_file
from .utils.ema import ModelEMA
from .writers import modelsaver
from ..common.system_meter import SystemMeter

azureml_run = Run.get_context()

logger = logging.getLogger(__name__)


def read_aml_dataset(dataset_id, validation_dataset_id, settings, ignore_data_errors, output_dir):
    """Read the training and validation datasets from AML datasets.

    :param dataset_id: Training dataset id
    :type dataset_id: str
    :param validation_dataset_id: Validation dataset id
    :type dataset_id: str
    :param settings:
    :type settings:
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dir: where to save train and val files
    :type output_dir: str
    :return: Training dataset and validation dataset
    :rtype: Tuple of form (AmlDatasetObjectDetectionWrapper, AmlDatasetObjectDetectionWrapper)
    """

    ws = Run.get_context().experiment.workspace

    if validation_dataset_id is not None:
        training_dataset = datasets.AmlDatasetObjectDetectionWrapper(dataset_id,
                                                                     is_train=True,
                                                                     hyp=settings,
                                                                     ignore_data_errors=ignore_data_errors,
                                                                     workspace=ws)
        validation_dataset = datasets.AmlDatasetObjectDetectionWrapper(validation_dataset_id,
                                                                       is_train=False,
                                                                       hyp=settings,
                                                                       ignore_data_errors=ignore_data_errors,
                                                                       workspace=ws)
        _save_image_df(train_df=training_dataset.get_images_df(),
                       val_df=validation_dataset.get_images_df(),
                       output_dir=output_dir)

    else:
        dataset = datasets.AmlDatasetObjectDetectionWrapper(dataset_id,
                                                            is_train=True,
                                                            hyp=settings,
                                                            ignore_data_errors=ignore_data_errors,
                                                            workspace=ws)
        training_dataset, validation_dataset = dataset.train_val_split()

        _save_image_df(train_df=dataset.get_images_df(), train_index=training_dataset._indices,
                       val_index=validation_dataset._indices, output_dir=output_dir)

    return training_dataset, validation_dataset


def read_file_dataset(image_folder, train_labels_file, val_labels_file, settings,
                      ignore_data_errors, output_dir):
    """Read the training and validation datasets from annotation files.

    :param image_folder: target image path
    :type image_folder: str
    :param train_labels_file: Training labels file
    :type train_labels_file: str
    :param val_labels_file: Validation labels file
    :type val_labels_file: str
    :param settings:
    :type settings:
    :param ignore_data_errors: boolean flag on whether to ignore input data errors
    :type ignore_data_errors: bool
    :param output_dir: where to save train and val files
    :type output_dir: str
    :return: Training dataset and validation dataset
    :rtype: Tuple of form (FileObjectDetectionDatasetWrapper, FileObjectDetectionDatasetWrapper)
    """

    if val_labels_file:
        training_dataset = datasets.FileObjectDetectionDatasetWrapper(train_labels_file, image_folder,
                                                                      is_train=True,
                                                                      hyp=settings,
                                                                      ignore_data_errors=ignore_data_errors)
        validation_dataset = datasets.FileObjectDetectionDatasetWrapper(val_labels_file, image_folder,
                                                                        is_train=False,
                                                                        hyp=settings,
                                                                        ignore_data_errors=ignore_data_errors)
        _save_od_image_files(train_ds=train_labels_file, val_ds=val_labels_file, output_dir=output_dir)

    else:
        dataset = datasets.FileObjectDetectionDatasetWrapper(train_labels_file, image_folder,
                                                             is_train=True,
                                                             hyp=settings,
                                                             ignore_data_errors=ignore_data_errors)
        training_dataset, validation_dataset = dataset.train_val_split()
        _save_od_image_files(train_ds=training_dataset, val_ds=validation_dataset, output_dir=output_dir)

    return training_dataset, validation_dataset


def setup_dataloaders(settings, output_directory):
    """Settings for (file and aml) datasets and data loaders

    :param settings: Dictionary with all training and model settings
    :type settings: Dictionary
    :param output_directory: Name of dir to save files for training/validation dataset
    :type output_directory: String
    :return: train_loader and validation_loader
    :rtype: Tuple of form (dataloaders.RobustDataLoader, dataloaders.RobustDataLoader)
    """

    image_folder = settings.get(SettingsLiterals.IMAGE_FOLDER, None)
    if image_folder is not None:
        image_folder = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)
    train_labels_file = settings.get(SettingsLiterals.LABELS_FILE, None)
    if train_labels_file is not None:
        train_labels_file = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], train_labels_file)
    val_labels_file = settings.get(SettingsLiterals.VALIDATION_LABELS_FILE, None)
    if val_labels_file is not None:
        val_labels_file = os.path.join(settings[SettingsLiterals.LABELS_FILE_ROOT], val_labels_file)

    # Settings for Aml dataset
    dataset_id = settings.get(SettingsLiterals.DATASET_ID, None)
    validation_dataset_id = settings.get(SettingsLiterals.VALIDATION_DATASET_ID, None)

    # Settings for both
    ignore_data_errors = settings.get(SettingsLiterals.IGNORE_DATA_ERRORS, True)
    settings['img_size'] = check_img_size(settings['img_size'], settings['gs'])

    # Setup Dataset
    if dataset_id is not None:
        train_dataset, validation_dataset = read_aml_dataset(dataset_id,
                                                             validation_dataset_id,
                                                             settings,
                                                             ignore_data_errors,
                                                             output_directory)
        logger.info("[train dataset_id: {}, validation dataset_id: {}]".format(dataset_id, validation_dataset_id))
    else:
        if image_folder is None:
            raise ClientException("images_folder or dataset_id needs to be specified", has_pii=False)

        if train_labels_file is None:
            raise ClientException("labels_file needs to be specified", has_pii=False)

        train_dataset, validation_dataset = read_file_dataset(image_folder,
                                                              train_labels_file,
                                                              val_labels_file,
                                                              settings,
                                                              ignore_data_errors,
                                                              output_directory)
        logger.info("[train file: {}, validation file: {}]".format(train_labels_file, val_labels_file))

    # Update classes
    if train_dataset.classes != validation_dataset.classes:
        all_classes = list(set(train_dataset.classes + validation_dataset.classes))
        train_dataset.reset_classes(all_classes)
        validation_dataset.reset_classes(all_classes)

    logger.info("[# train images: {}, # validation images: {}, # labels: {}, image size: {}]".format(
        len(train_dataset), len(validation_dataset), train_dataset.num_classes, train_dataset.img_size))

    # Setup Dataloaders
    train_dataloader_settings = {'batch_size': settings[TrainingLiterals.TRAINING_BATCH_SIZE],
                                 'shuffle': True,
                                 'num_workers': settings[SettingsLiterals.NUM_WORKERS]}
    val_dataloader_settings = {'batch_size': settings[TrainingLiterals.VALIDATION_BATCH_SIZE],
                               'shuffle': False,
                               'num_workers': settings[SettingsLiterals.NUM_WORKERS]}

    train_loader = loaders.setup_dataloader(train_dataset, **train_dataloader_settings)
    validation_loader = loaders.setup_dataloader(validation_dataset, **val_dataloader_settings)

    return train_loader, validation_loader


def run(automl_settings):
    """Invoke training by passing settings and write the resulting model.

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    """

    settings = _parse_argument_settings(automl_settings)

    task_type = constants.Tasks.IMAGE_OBJECT_DETECTION
    _set_logging_parameters(task_type, settings)

    logger.info("Final settings: \n {}".format(settings))

    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    tb_writer = init_tensorboard()

    # Set random seed
    init_seeds(1)

    epochs = settings['number_of_epochs']
    weights = settings['weights']
    device = settings['device']
    output_directory = ArtifactLiterals.OUTPUT_DIR

    # Set data loaders
    train_loader, validation_loader = setup_dataloaders(settings, output_directory)

    # Update # of class
    nc = train_loader.dataset.num_classes

    # Create model
    model = Model(settings['cfg'], nc=nc).to(device)
    num_params = sum(x.numel() for x in model.parameters())  # number parameters
    logger.info("[model: {}, # layers: {}, # param: {}]".format(settings[TrainingLiterals.MODEL_NAME],
                                                                len(list(model.parameters())), num_params))

    # TODO: move all model weights in cdn
    # TODO: support resume
    # Load pre-trained model
    if weights is not None:
        ckpt = torch.load(weights, map_location=device)
        try:
            new_ckpt = {}
            for k, v in ckpt.items():
                if model.state_dict()[k].numel() == v.numel():
                    new_ckpt[k] = v
            model.load_state_dict(new_ckpt, strict=False)
        except KeyError as e:
            logger.info('%s: could not load the pretrained model: %s' % (e, weights))
            pass
        del ckpt

    # Model parameters
    settings['cls'] *= nc / 80.  # scale coco-tuned hyp['cls'] to current dataset
    model.nc = nc  # attach number of classes to model
    model.hyp = settings  # attach hyperparameters to model
    model.gr = 1.0  # giou loss ratio (obj_loss = 1.0 or giou)
    model.names = train_loader.dataset.classes
    model.device = device
    # Exponential moving average
    ema = ModelEMA(model)

    # Optimizer
    pg0, pg1, pg2 = [], [], []  # optimizer parameter groups
    for k, v in model.named_parameters():
        if v.requires_grad:
            if '.bias' in k:
                pg2.append(v)  # biases
            elif '.weight' in k and '.bn' not in k:
                pg1.append(v)  # apply weight decay
            else:
                pg0.append(v)  # all else

    optimizer = optim.SGD(pg0, lr=settings['lr0'], momentum=settings['momentum'], nesterov=True)
    optimizer.add_param_group({'params': pg1, 'weight_decay': settings['weight_decay']})  # add pg1 with weight_decay
    optimizer.add_param_group({'params': pg2})  # add pg2 (biases)
    del pg0, pg1, pg2

    # Scheduler
    nb = len(train_loader)  # number of batches
    lf_warmpcosine = WarmupCosineSchedule(warmup_steps=nb * 2, t_total=epochs * nb)
    scheduler = optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lf_warmpcosine.lr_lambda)

    # Train
    train(model, ema, optimizer, scheduler, train_loader, validation_loader, tb_writer, run=azureml_run)

    # Save Model
    modelsaver.write_model(model, output_dir=output_directory, device=device,
                           enable_onnx_norm=settings[SettingsLiterals.ENABLE_ONNX_NORMALIZATION])

    # Upload outputs
    folder_name = os.path.basename(output_directory)
    if azureml_run is not None:
        azureml_run.upload_folder(name=folder_name, path=output_directory)


def _parse_argument_settings(automl_settings):
    """Parse all arguments and merge settings

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    :return: automl settings dictionary with all settings filled in
    :rtype: dict
    """

    parser = argparse.ArgumentParser(description="Object detection - Yolo")

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

    # Yolov5 Settings

    current_file_path = os.path.dirname(__file__)

    parser.add_argument(_make_arg(YoloLiterals.IMG_SIZE), type=int,
                        help='image size for train and val',
                        default=YoloParameters.DEFAULT_IMG_SIZE)
    parser.add_argument(_make_arg(YoloLiterals.CFG), type=str,
                        help='model.yaml path',
                        default=os.path.join(current_file_path, 'models', YoloParameters.DEFAULT_CFG))
    parser.add_argument(_make_arg(YoloLiterals.WEIGHTS), type=str,
                        help='initial weights path',
                        default=os.path.join(current_file_path, 'weights', YoloParameters.DEFAULT_WEIGHTS))
    parser.add_argument(_make_arg(YoloLiterals.MULTI_SCALE),
                        help='vary img-size +/- 50%%', action="store_true")

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
    script_args = parser.parse_args()
    script_args.cfg = check_file(script_args.cfg)
    script_args.weights = check_file(script_args.weights)

    # Update training default settings with yolo specific hyper-parameters
    training_settings_defaults.update(yolo_hyp_defaults)

    # Training settings
    return _merge_settings_args_defaults(automl_settings, script_args, training_settings_defaults)
