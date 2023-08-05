# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" Helper classes and functions for creating dataloaders """

from ..common import constants
from ..common.constants import DataLoaderParameterLiterals
from ...common.dataloaders import RobustDataLoader


class DataLoaderParameters:
    """Class that encodes all the parameters used to define a dataloader
    behavior.
    """

    def __init__(self, **kwargs):
        """
        :param kwargs: Optional parameters to define dataloader behavior.
            Currently supports:
            -batch_size: (Int) Number of records in each batch
            -shuffle: (Bool) Whether to shuffle the data in between each epoch
            -num_workers: (Int or None) Number of workers if specified
        :type kwargs: dict
        """
        # TODO: move to constant.py
        self._batch_size = kwargs.get(
            DataLoaderParameterLiterals.BATCH_SIZE, constants.DataLoaderParameters.DEFAULT_BATCH_SIZE)
        self._shuffle = kwargs.get(
            DataLoaderParameterLiterals.SHUFFLE, constants.DataLoaderParameters.DEFAULT_SHUFFLE)
        self._num_workers = kwargs.get(
            DataLoaderParameterLiterals.NUM_WORKERS, constants.DataLoaderParameters.DEFAULT_NUM_WORKERS)

    @property
    def batch_size(self):
        """Get batch size

        :return: Batch size
        :rtype: Int
        """
        return self._batch_size

    @property
    def shuffle(self):
        """Get whether dataset is shuffled between epoch

        :return: Dataset will be shuffled
        :rtype: Bool
        """
        return self._shuffle

    @property
    def num_workers(self):
        """Get number of workers if specified

        :return: Number of workers
        :rtype: Int or None
        """
        return self._num_workers


def setup_dataloader(dataset, **kwargs):
    """Helper function to create dataloader

    :param dataset: Dataset used to create dataloader
    :type dataset: CommonObjectDetectionDatasetWrapper or class derived from CommonObjectDetectionDatasetWrapper
        (see object_detection.data.datasets
    :param kwargs: Optional keyword arguments, currently supported:
        -batch_size: (Int) Number of records per batch
        -shuffle: (Bool) Whether to shuffle the data between epochs
        -num_workers: (Int) Number of workers to use
    :type kwargs: dict
    :return: Dataloader
    :rytpe: Pytorch Dataloader
    """
    parameters = DataLoaderParameters(**kwargs)

    loader = RobustDataLoader(dataset,
                              batch_size=parameters.batch_size,
                              shuffle=parameters.shuffle,
                              num_workers=parameters.num_workers,
                              pin_memory=True,
                              collate_fn=dataset.collate_fn)
    return loader
