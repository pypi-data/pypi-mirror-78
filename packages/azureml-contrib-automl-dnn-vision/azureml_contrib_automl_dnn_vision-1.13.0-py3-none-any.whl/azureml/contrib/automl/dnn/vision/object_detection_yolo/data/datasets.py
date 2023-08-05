# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" Classes and functions to inject data for object detection """

import cv2
import json
import numpy as np
import os
import random
import torch

from abc import ABC, abstractmethod
from collections import defaultdict
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset

from azureml.automl.core.shared import logging_utilities
from azureml.contrib.automl.dnn.vision.common.logging_utils import get_logger
from azureml.core import Dataset as AmlDataset

from ..utils.utils import load_mosaic, load_image, letterbox, random_affine, xyxy2xywh, convert_to_yolo_labels
from ..common.constants import DatasetFieldLabels
from ...common.labeled_dataset_helper import AmlLabeledDatasetHelper
from ...common.exceptions import AutoMLVisionDataException

logger = get_logger(__name__)


class ObjectDetectionDatasetBaseWrapper(ABC, Dataset):
    """Class the establishes interface for object detection datasets"""

    @abstractmethod
    def __getitem__(self, index):
        """Get item by index

        :param index: Index of object
        :type index: Int
        :return: Item at Index
        :rtype: Object Detection Record
        """
        pass

    @abstractmethod
    def __len__(self):
        """Get the number of items in dataset

        :return: Number of items in dataset
        :rtype: Int
        """
        pass

    @property
    @abstractmethod
    def num_classes(self):
        """Get the number of classes in dataset

        :return: Number of classes
        :rtype: Int
        """
        pass

    @abstractmethod
    def label_to_index_map(self, label):
        """Get the index associated with a given class

        :param label: Label name
        :type: String
        :return: Index associated with label
        :rtype: Int
        """
        pass

    @abstractmethod
    def index_to_label(self, index):
        """Get the label associated with a certain index

        :param index: Index
        :type index: Int
        :return: Class name
        :rtype: String
        """
        pass

    @property
    @abstractmethod
    def classes(self):
        """Get a list of classes ordered by index.

        :return: List of classes
        :rtype: List of Strings
        """
        pass


class ObjectAnnotation:
    """Class that contains all of the information associated with
    a single bounding box."""

    def __init__(self, labels):
        """
        :param labels: Information about the bounding box in
        the image, must contain label, topX, topY, bottomX, bottomY.
        :type labels: Dictionary
        """
        self._bounding_box = None
        self._label = None
        self._iscrowd = 0

        self._init_labels(labels)

    @property
    def bounding_box(self):
        """Get bounding box coordinates

        :return: Bounding box in form [top, left, bottom, right] in pixel coordinates
        :rtype: List of floats
        """
        return self._bounding_box

    @property
    def label(self):
        """Get bounding box classification

        :return: Classification for bounding box object
        :rtype: String
        """
        return self._label

    @property
    def iscrowd(self):
        """Get image is iscrowd

        :return: 0 for not crowd, 1 for crowd
        :rtype: int
        """
        return self._iscrowd

    def _init_labels(self, labels):

        if (DatasetFieldLabels.CLASS_LABEL not in labels or
            DatasetFieldLabels.X_0_PERCENT not in labels or
            DatasetFieldLabels.Y_0_PERCENT not in labels or
            DatasetFieldLabels.X_1_PERCENT not in labels or
                DatasetFieldLabels.Y_1_PERCENT not in labels):
            raise AutoMLVisionDataException("Incomplete Record", has_pii=False)

        self._label = labels[DatasetFieldLabels.CLASS_LABEL]

        if DatasetFieldLabels.IS_CROWD in labels:
            self._iscrowd = int(labels[DatasetFieldLabels.IS_CROWD] == "true")

        self._x0_percentage = float(labels[DatasetFieldLabels.X_0_PERCENT])
        self._y0_percentage = float(labels[DatasetFieldLabels.Y_0_PERCENT])
        self._x1_percentage = float(labels[DatasetFieldLabels.X_1_PERCENT])
        self._y1_percentage = float(labels[DatasetFieldLabels.Y_1_PERCENT])

        self._bounding_box = [self._label,
                              self._x0_percentage, self._y0_percentage,
                              self._x1_percentage, self._y1_percentage]


class CommonObjectDetectionDatasetWrapper(ObjectDetectionDatasetBaseWrapper):
    """Wrapper for object detection dataset"""

    def __init__(self, is_train=False, ignore_data_errors=True):
        """
        :param is_train: which mode (training, inference) is the network in?
        :type is_train: boolean
        :param ignore_data_errors: boolean flag on whether to ignore input data errors
        :type ignore_data_errors: bool
        """
        self._is_train = is_train
        self._ignore_data_errors = ignore_data_errors

    def __len__(self):
        """Get number of records in dataset

        :return: Number of records
        :rtype: Int
        """
        return len(self._image_urls)

    def __getitem__(self, index):
        """Get dataset item by index

        :return: Image, bounding box information, and image information, with form:
                 -Image: Torch tensor
                 -Labels: Dictionary with keys "boxes" and "labels", where boxes is a list of lists of
                          pixel coordinates, and "labels" is a list of integers with the class of each bounding box,
                 -Image Information: is a dictionary with the image url, image width and height,
                                     and a list of areas of the different bounding boxes
        :rtype: Tuple of form (Torch Tensor, Dictionary, Dictionary)
        """
        hyp = self.hyp
        if self.mosaic:
            # Load mosaic
            img, labels = load_mosaic(self, index)

        else:
            # Load image
            img, (h0, w0), (h, w) = load_image(self, index)

            # Letterbox
            shape = self.img_size  # final letterboxed shape
            img, ratio, pad = letterbox(img, shape, auto=False, scaleup=self.augment)

            # Load labels
            labels = []
            x = self.labels[index]
            if x.size > 0:
                # Normalized xywh to pixel xyxy format
                labels = x.copy()
                labels[:, 1] = ratio[0] * w * (x[:, 1] - x[:, 3] / 2) + pad[0]  # pad width
                labels[:, 2] = ratio[1] * h * (x[:, 2] - x[:, 4] / 2) + pad[1]  # pad height
                labels[:, 3] = ratio[0] * w * (x[:, 1] + x[:, 3] / 2) + pad[0]
                labels[:, 4] = ratio[1] * h * (x[:, 2] + x[:, 4] / 2) + pad[1]

        if self.augment:
            # Augment imagespace
            if not self.mosaic:
                img, labels = random_affine(img, labels,
                                            degrees=hyp['degrees'],
                                            translate=hyp['translate'],
                                            scale=hyp['scale'],
                                            shear=hyp['shear'])

        nL = len(labels)  # number of labels
        if nL:
            # convert xyxy to xywh
            labels[:, 1:5] = xyxy2xywh(labels[:, 1:5])

            # Normalize coordinates 0 - 1
            labels[:, [2, 4]] /= img.shape[0]  # height
            labels[:, [1, 3]] /= img.shape[1]  # width

        if self.augment:
            # random left-right flip
            lr_flip = True
            if lr_flip and random.random() < 0.5:
                img = np.fliplr(img)
                if nL:
                    labels[:, 1] = 1 - labels[:, 1]

            # random up-down flip
            ud_flip = False
            if ud_flip and random.random() < 0.5:
                img = np.flipud(img)
                if nL:
                    labels[:, 2] = 1 - labels[:, 2]

        labels_out = torch.zeros((nL, 6))
        if nL:
            labels_out[:, 1:] = torch.from_numpy(labels)

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        return torch.from_numpy(img), labels_out, self._image_urls[index]

    @property
    def num_classes(self):
        """Get number of classes in dataset

        :return: Number of classes in dataset
        :rtype: Int
        """
        return len(self._object_classes)

    @property
    def classes(self):
        """Get list of classes in dataset

        :return: List of classses
        :rtype: List of strings
        """
        return self._object_classes

    def label_to_index_map(self, label):
        """Get mapping from class name to numeric
        class index.

        :param label: Class name
        :type label: String
        :return: Numeric class index
        :rtype: Int
        """
        return self._class_to_index_map[label]

    def index_to_label(self, index):
        """Get the class name associated with numeric index

        :param index: Numeric class index
        :type index: Int
        :return: Class name
        :rtype: String
        """
        return self._object_classes[index]

    def train_val_split(self, valid_portion=0.2):
        """Splits a dataset into two datasets, one for training and and for validation.

        :param valid_portion: (optional) Portion of dataset to use for validation. Defaults to 0.2.
        :type valid_portion: Float between 0.0 and 1.0
        :return: Training dataset and validation dataset
        :rtype: Tuple of form (CommonObjectDetectionSubsetWrapper, CommonObjectDetectionSubsetWrapper)
        """
        number_of_samples = len(self._image_urls)
        indices = np.arange(number_of_samples)
        training_indices, validation_indices = train_test_split(indices, test_size=valid_portion)

        train_dataset = CommonObjectDetectionSubsetWrapper(self, training_indices)
        validation_dataset = CommonObjectDetectionSubsetWrapper(self, validation_indices)
        # Update flags for validation dataset
        validation_dataset._is_train = False
        validation_dataset.augment = False
        validation_dataset.mosaic = False

        return train_dataset, validation_dataset

    def reset_classes(self, classes):
        """Update dataset wrapper with a list of new classes

        :param classes: classes
        :type classes: string list
        """
        self._object_classes = sorted(classes, reverse=False)
        self._class_to_index_map = {object_class: i for
                                    i, object_class in
                                    enumerate(self._object_classes)}

    @staticmethod
    def collate_fn(batch):
        """Custom collate function for training and validation

        :param batch: list of samples (image, label and path)
        :type batch: list
        :return: Images, Labels and Image Paths
        :rtype: tuple of (image pixels), tuple of (bbox information), tuple of (image path)
        """
        img, label, path = zip(*batch)  # transposed
        for i, l in enumerate(label):
            l[:, 0] = i  # add target image index for build_targets()
        return torch.stack(img, 0), torch.cat(label, 0), path


class FileObjectDetectionDatasetWrapper(CommonObjectDetectionDatasetWrapper):
    """Wrapper for object detection dataset"""

    def __init__(self, annotations_file=None, image_folder=".", is_train=False, hyp=None, ignore_data_errors=True):
        """
        :param annotations_file: Annotations file
        :type annotations_file: str
        :param image_folder: target image path
        :type image_folder: str
        :param is_train: which mode (training, inferencing) is the network in?
        :type is_train: boolean
        :param hyp:
        :type hyp:
        :param ignore_data_errors:
        :type ignore_data_errors:
        """
        self._image_urls = []
        self._annotations = defaultdict(list)
        self._object_classes = []
        self._class_to_index_map = {}
        # specific for yolo
        self.labels = []
        self.hyp = hyp
        self.img_size = hyp['img_size'] if hyp else 640
        self.augment = is_train
        self.mosaic = is_train  # load 4 images at a time into a mosaic (only during training)
        self.mosaic_border = [-self.img_size // 2, -self.img_size // 2]
        super().__init__(is_train, ignore_data_errors)

        if annotations_file is not None:
            annotations = self._read_annotations_file(annotations_file, ignore_data_errors=ignore_data_errors)
            self._init_dataset(annotations, image_folder, ignore_data_errors=ignore_data_errors)

    def _init_dataset(self, annotations, image_folder, ignore_data_errors=True):

        image_urls = set()
        object_classes = set()

        if not annotations:
            raise AutoMLVisionDataException("No annotations to initialize datasets.", has_pii=False)

        for annotation in annotations:
            if (DatasetFieldLabels.IMAGE_URL not in annotation or
                DatasetFieldLabels.IMAGE_DETAILS not in annotation or
                    DatasetFieldLabels.IMAGE_LABEL not in annotation):
                missing_required_fields_message = "Missing required fields in annotation"
                if ignore_data_errors:
                    logger.warning(missing_required_fields_message)
                else:
                    raise AutoMLVisionDataException(missing_required_fields_message, has_pii=False)

            try:
                object_info = ObjectAnnotation(annotation[DatasetFieldLabels.IMAGE_LABEL])
            except AutoMLVisionDataException as ex:
                if ignore_data_errors:
                    logging_utilities.log_traceback(ex, logger)
                    continue
                else:
                    raise

            image_url = os.path.join(image_folder, annotation[DatasetFieldLabels.IMAGE_URL])
            if not os.path.exists(image_url):
                file_missing_message = "File missing for image"
                if ignore_data_errors:
                    logger.warning(file_missing_message)
                    continue
                else:
                    raise AutoMLVisionDataException(file_missing_message, has_pii=False)

            image_urls.add(image_url)
            self._annotations[image_url].append(object_info)
            object_classes.add(annotation[DatasetFieldLabels.IMAGE_LABEL][DatasetFieldLabels.CLASS_LABEL])

        self._object_classes = list(sorted(object_classes))
        # Use sorted to make sure all workers get the same order of data in distributed training/validation
        self._image_urls = sorted(image_urls)
        self._class_to_index_map = {label: i for i, label in enumerate(self._object_classes)}
        self.labels = convert_to_yolo_labels(self._image_urls, self._annotations, self._class_to_index_map)

    def _read_annotations_file(self, annotations_file, ignore_data_errors=True):
        annotations = []
        line_no = 0
        with open(annotations_file, "r") as json_file:
            for line in json_file:
                try:
                    try:
                        line_no += 1
                        annotations.append(json.loads(line))
                    except json.JSONDecodeError as ex:
                        raise AutoMLVisionDataException("Json decoding error in line no: {}".format(line_no),
                                                        has_pii=False)
                except AutoMLVisionDataException as ex:
                    if ignore_data_errors:
                        logging_utilities.log_traceback(ex, logger)
                    else:
                        raise

        return annotations


class CommonObjectDetectionSubsetWrapper(CommonObjectDetectionDatasetWrapper):
    """Creates a subset of a larger CommonObjectDetectionDatasetWrapper"""

    def __init__(self, parent_dataset, indices):
        """
        :param parent_dataset: Dataset to take a subset of
        :type parent_dataset: CommonObjectDetectionDatasetWrapper
        :param indices: Indices to use in subset
        :type indices: List of Ints
        """
        self._image_urls = parent_dataset._image_urls
        self._annotations = parent_dataset._annotations
        self._object_classes = parent_dataset._object_classes
        self._class_to_index_map = parent_dataset._class_to_index_map
        self._indices = indices
        self._is_train = parent_dataset._is_train
        self._ignore_data_errors = parent_dataset._ignore_data_errors
        # specific for yolo
        self.labels = parent_dataset.labels
        self.hyp = parent_dataset.hyp
        self.img_size = parent_dataset.hyp['img_size'] if parent_dataset.hyp else 640
        self.augment = parent_dataset._is_train
        self.mosaic = parent_dataset._is_train  # load 4 images at a time into a mosaic (only during training)
        self.mosaic_border = [-self.img_size // 2, -self.img_size // 2]

    def _set_indices(self, indices):
        self._indices = indices

    def __len__(self):
        """Get the number of records in subset

        :return: Number of records
        :rtype: Int
        """
        return len(self._indices)

    def __getitem__(self, idx):
        """Get a record at a certain subset index

        :return: Dataset record (see __getitem__
        of CommonObjectDetectionDatasetWrapper)
        :rtype: Tuple (see __getitem__ of
        CommonObjectDetectionDatasetWrapper)
        """

        index = self._indices[idx]

        return super().__getitem__(index)


class AmlDatasetObjectDetectionWrapper(CommonObjectDetectionDatasetWrapper):
    """Wrapper for Aml labeled dataset for object detection dataset"""

    def __init__(self, dataset_id, is_train=False, hyp=None,
                 workspace=None, ignore_data_errors=False, datasetclass=AmlDataset,
                 download_files=True):
        """
        :param dataset_id: dataset id
        :type dataset_id: str
        :param is_train: which mode (training, inferencing) is the network in?
        :type is_train: boolean
        :param hyp:
        :type hyp:
        :param ignore_data_errors: Setting this ignores and files in the labeled dataset that fail to download.
        :type ignore_data_errors: bool
        :param datasetclass: The source dataset class.
        :type datasetclass: class
        :param download_files: Flag to download files or not.
        :type download_files: bool
        """
        self._image_urls = []
        self._annotations = defaultdict(list)
        self._object_classes = []
        self._class_to_index_map = {}
        # specific for yolo
        self.labels = []
        self.hyp = hyp
        self.img_size = hyp['img_size'] if hyp else 640
        self.augment = is_train
        self.mosaic = is_train  # load 4 images at a time into a mosaic (only during training)
        self.mosaic_border = [-self.img_size // 2, -self.img_size // 2]
        super().__init__(is_train, ignore_data_errors)

        self._labeled_dataset_helper = AmlLabeledDatasetHelper(dataset_id, workspace, ignore_data_errors,
                                                               datasetclass, download_files=download_files)
        self._label_column_name = self._labeled_dataset_helper.label_column_name
        images_df = self._labeled_dataset_helper.images_df

        self._init_dataset(images_df, ignore_data_errors=ignore_data_errors)

    def _init_dataset(self, images_df, ignore_data_errors=True):

        image_urls = set()
        object_classes = set()

        for index, label in enumerate(images_df[self._label_column_name]):

            image_url = self._labeled_dataset_helper.get_image_full_path(index)

            if not os.path.exists(image_url):
                mesg = "File missing for image"
                raise AutoMLVisionDataException(mesg, has_pii=False)

            image_urls.add(image_url)

            for annotation in label:
                try:
                    object_info = ObjectAnnotation(annotation)
                except AutoMLVisionDataException as ex:
                    if ignore_data_errors:
                        logging_utilities.log_traceback(ex, logger)
                        continue
                    else:
                        raise

                self._annotations[image_url].append(object_info)
                object_classes.add(annotation[DatasetFieldLabels.CLASS_LABEL])

        self._object_classes = list(sorted(object_classes))
        # Use sorted to make sure all workers get the same order of data in distributed training/validation
        self._image_urls = sorted(image_urls)
        self._class_to_index_map = {label: i for i, label in enumerate(self._object_classes)}
        self.labels = convert_to_yolo_labels(self._image_urls, self._annotations, self._class_to_index_map)

    def get_images_df(self):
        """Return images dataframe

        :param images_df: DataFrame containing images.
        :type images_df: Pandas DataFrame
        """
        return self._labeled_dataset_helper.images_df


class PredictionDataset_yolo(Dataset):
    """Dataset file so that score.py can process images in batches.

    """

    def __init__(self, root_dir=None, image_list_file=None, ignore_data_errors=True,
                 input_dataset_id=None, ws=None, datasetclass=AmlDataset):
        """
        :param root_dir: prefix to be added to the paths contained in image_list_file
        :type root_dir: str
        :param image_list_file: path to file containing list of images
        :type image_list_file: str
        :param ignore_data_errors: boolean flag on whether to ignore input data errors
        :type ignore_data_errors: bool
        :param input_dataset_id: The input dataset id.  If this is specified image_list_file is not required.
        :type input_dataset_id: str
        :param ws: The Azure ML Workspace
        :type ws: Workspace
        :param datasetclass: The Azure ML Datset class
        :type datasetclass: Dataset

        """
        self._files = []

        if input_dataset_id is not None:
            dataset_helper = AmlLabeledDatasetHelper(input_dataset_id, ws, ignore_data_errors,
                                                     image_column_name=AmlLabeledDatasetHelper.PATH_COLUMN_NAME,
                                                     datasetclass=datasetclass)
            self._files = dataset_helper.get_file_name_list()
            self._files = [f.strip("/") for f in self._files]
            self._root_dir = dataset_helper._data_dir
        else:
            for filename in open(image_list_file):
                self._files.append(filename.strip())

            # Size of image list file before removing blank strings
            logger.info('Image list file contains {} lines before removing blank '
                        'strings'.format(len(self._files)))

            # Remove blank strings
            self._files = [f for f in self._files if f]
            self._root_dir = root_dir

        # Length of final dataset
        logger.info('Size of dataset: {}'.format(len(self._files)))
        self._ignore_data_errors = ignore_data_errors

    def __len__(self):
        """Size of the dataset."""
        return len(self._files)

    def __getitem__(self, idx):
        """
        :param idx: index
        :type idx: int
        :return: item and label at index idx
        :rtype: tuple[str, image]
        """
        filename = self._files[idx]
        if self._root_dir and filename:
            filename = filename.lstrip('/')
        full_path = os.path.join(self._root_dir, filename)

        _, image, pad = self._read_image(full_path)
        return filename, image, pad

    def _read_image(self, image_url, img_size=640):
        img0 = cv2.imread(image_url)  # BGR
        assert img0 is not None, 'Image Not Found ' + image_url

        img, ratio, pad = letterbox(img0, new_shape=img_size, auto=False, scaleup=False)

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x640x640
        img = np.ascontiguousarray(img)
        return image_url, torch.from_numpy(img), pad

    @staticmethod
    def collate_fn(batch):
        """Custom collate function for inference

        :param batch: list of samples (path, image and pad)
        :type batch: list
        :return: Paths, Images and Pads
        :rtype: tuple of (image path), tuple of (image pixels), tuple of (pad used in letterbox image)
        """
        fname, imgs, pad = zip(*batch)
        return fname, torch.stack(imgs, 0), pad
