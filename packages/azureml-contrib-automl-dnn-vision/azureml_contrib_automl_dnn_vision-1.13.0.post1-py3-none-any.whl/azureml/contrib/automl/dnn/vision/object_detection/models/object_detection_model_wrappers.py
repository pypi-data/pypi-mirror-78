# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper functions to build model wrappers."""
import torch
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.transform import GeneralizedRCNNTransform
from torchvision.transforms import functional

from .base_model_wrapper import BaseObjectDetectionModelWrapper
from .customrcnn import CustomRCNNWrapper, CustomRCNNSpecifications
from ..common.constants import ModelNames, RCNNBackbones
from ...common.constants import PretrainedModelNames
from ...common.pretrained_model_utilities import PretrainedModelFactory
from ...common.logging_utils import get_logger

DEFAULT_MODEL = ModelNames.FASTER_RCNN_RESNET50_FPN

logger = get_logger(__name__)


class CallableGeneralizedRCNNTransform:
    """Wrapper that exposes transforms extracted from GeneralizedRCNNTransform
    to be used when loading data on cpu."""
    def __init__(self, model):
        """Init method.

        :param model: a FasterRCNN model
        """
        self._gen_rcnn_transform = GeneralizedRCNNTransform(min_size=model.transform.min_size,
                                                            max_size=model.transform.max_size,
                                                            image_mean=model.transform.image_mean,
                                                            image_std=model.transform.image_std)

    @staticmethod
    def identity_batch(images):
        """A NOP batch method.

        :param images: images to batch
        :return: same images
        """
        return images

    def inference_transform(self, image):
        """Apply the transform from the model on a single image at inference time.

        :param image: the image to prepare for inference
        :type image: PIL Image
        :return: transformed image
        :rtype: Tensor
        """
        self._gen_rcnn_transform.training = False
        # No need for batching here, as this function is called for each image
        self._gen_rcnn_transform.batch_images = self.identity_batch
        image_tensor = functional.to_tensor(image)
        new_image, _ = self._gen_rcnn_transform(torch.unsqueeze(image_tensor, 0))  # transform expects a batch

        # remove the batch dimension
        return new_image.tensors[0]

    def train_validation_transform(self, is_train, image, boxes):
        """Exposes model specific transformations.

        :param is_train: True if the transformations are for training, False otherwise.
        :param image: image tensor, 3 dimensions
        :param boxes: boxes tensor
        :return: a tuple with new image, boxes, height and width
        """

        self._gen_rcnn_transform.training = is_train
        new_image, new_boxes = self._gen_rcnn_transform(torch.unsqueeze(image, 0),  # transform expects a batch
                                                        [{"boxes": boxes}])
        # remove the batch dimension
        new_image = torch.squeeze(new_image.tensors, 0)
        # the first element of the list contains the boxes for the image,
        # as the batch only has one entry
        new_boxes = new_boxes[0]["boxes"]

        new_height = new_image.shape[1]
        new_width = new_image.shape[2]

        return new_image, new_boxes, new_height, new_width


class FasterRCNNResnet50FPNWrapper(BaseObjectDetectionModelWrapper):
    """Model wrapper for Faster RCNN with Resnet50 FPN backbone."""

    def __init__(self, number_of_classes=None, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param kwargs: Optional keyword arguments to define model specifications
        :type kwargs: dict
        """

        model = self._create_model(number_of_classes, **kwargs)
        super().__init__(model=model, number_of_classes=number_of_classes)

    def _create_model(self, number_of_classes, specs=None, **kwargs):
        model = PretrainedModelFactory.fasterrcnn_resnet50_fpn(pretrained=True, **kwargs)

        if number_of_classes is not None:
            input_features = model.roi_heads.box_predictor.cls_score.in_features
            model.roi_heads.box_predictor = FastRCNNPredictor(input_features,
                                                              number_of_classes)

        return model

    def get_inference_transform(self):
        """Get the transformation function to use at inference time."""
        return CallableGeneralizedRCNNTransform(self.model).inference_transform

    def get_train_validation_transform(self):
        """Get the transformation function to use at training and validation time."""
        return CallableGeneralizedRCNNTransform(self.model).train_validation_transform

    def disable_model_transform(self):
        """Disable resize and normalize from the model."""

        self.model.transform.resize = self.identity_resize
        self.model.transform.normalize = self.identity_normalize

    @staticmethod
    def identity_normalize(image):
        """A NOP normalization method.

        :param image: image to normalize
        :return: same image
        """
        return image

    @staticmethod
    def identity_resize(image, target_index):
        """A NOP resize method.

        :param image: image to resize.
        :param target_index: target index to resize.
        :return: tuple with same image and target_index.
        """
        return image, target_index


class FasterRCNNResnet18FPNWrapper(CustomRCNNWrapper):
    """Model wrapper for Faster RCNN with Resnet 18 FPN backbone."""

    _specifications = CustomRCNNSpecifications(
        backbone=RCNNBackbones.RESNET_18_FPN_BACKBONE)

    def __init__(self, number_of_classes, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param kwargs: Optional keyword arguments to define model specifications
        :type kwargs: dict
        """

        super().__init__(number_of_classes, self._specifications, **kwargs)


class FasterRCNNMobilenetV2Wrapper(CustomRCNNWrapper):
    """Model wrapper for Faster RCNN with MobileNet v2 w/o FPN backbone."""

    _specifications = CustomRCNNSpecifications(
        backbone=RCNNBackbones.MOBILENET_V2_BACKBONE)

    def __init__(self, number_of_classes, **kwargs):
        """
        :param number_of_classes: Number of object classes
        :type number_of_classes: Int
        :param kwargs: Optional keyword arguments to define model specifications
        :type kwargs: dict
        """

        super().__init__(number_of_classes, self._specifications, **kwargs)


class ObjectDetectionModelFactory:
    """Factory function to create models."""

    _models_dict = {
        ModelNames.FASTER_RCNN_RESNET50_FPN: FasterRCNNResnet50FPNWrapper,
        ModelNames.FASTER_RCNN_RESNET18_FPN: FasterRCNNResnet18FPNWrapper,
        ModelNames.FASTER_RCNN_MOBILENETV2: FasterRCNNMobilenetV2Wrapper
    }

    _pre_trained_model_names_dict = {
        ModelNames.FASTER_RCNN_RESNET50_FPN: PretrainedModelNames.FASTERRCNN_RESNET50_FPN_COCO,
        ModelNames.FASTER_RCNN_RESNET18_FPN: PretrainedModelNames.RESNET18,
        ModelNames.FASTER_RCNN_MOBILENETV2: PretrainedModelNames.MOBILENET_V2
    }

    @staticmethod
    def _get_model_wrapper(number_of_classes=None, model_name=None, **kwargs):

        if model_name is None:
            model_name = DEFAULT_MODEL

        if model_name not in ObjectDetectionModelFactory._models_dict:
            raise ValueError('Unsupported model')

        return ObjectDetectionModelFactory._models_dict[model_name](number_of_classes=number_of_classes, **kwargs)

    @staticmethod
    def _download_model_weights(model_name=None):

        if model_name is None:
            model_name = DEFAULT_MODEL

        if model_name not in ObjectDetectionModelFactory._pre_trained_model_names_dict:
            raise ValueError("Unsupported model")

        PretrainedModelFactory.download_pretrained_model_weights(
            ObjectDetectionModelFactory._pre_trained_model_names_dict[model_name], progress=True)
