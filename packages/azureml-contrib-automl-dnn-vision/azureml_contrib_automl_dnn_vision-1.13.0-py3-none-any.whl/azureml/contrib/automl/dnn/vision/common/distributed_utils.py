# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Helper Utils for distributed mode."""

import pickle
import torch
import torch.distributed as dist


def dist_available_and_initialized():
    """ Check if distributed mode is available and is initialized.

    :return: distributed mode or not.
    :rtype: bool
    """
    return dist.is_available() and dist.is_initialized()


def get_world_size():
    """ Get the world size when running in distributed mode.
    Returns 1 if not in distributed mode.

    :return: world_size
    :rtype: int
    """
    if dist_available_and_initialized():
        return dist.get_world_size()
    return 1


def get_rank():
    """Get the rank of the current process when running in distributed mode.
    Returns 0 if not in distributed mode.

    :return: rank
    :rtype: int
    """
    if dist_available_and_initialized():
        return dist.get_rank()
    return 0


def master_process():
    """ Return if the current process is the master process.
    If in distributed mode, return true for process with rank 0.
    Else, return True.

    :return: If the current process is the master process.
    :rtype: bool
    """
    return get_rank() == 0


def all_gather(data):
    """Run distributed all_gather on pickle-able objects.

    Note (Important!!!):
        Make sure that "data" entirely resides in cpu memory. There are deadlocks otherwise.

        - Say Process P0 uses cuda:0 and P1 uses cuda:1. In this function, the data is pickled and converted
          to a tensor on current gpu before calling dist.all_gather(). Data from P0 (say D0) has device cuda:0 and
          data from P1 (say D1) has device cuda:1.
        - During the dist.all_gather() call, data is moved to the target gpu on which it is requested.
          After dist.all_gather() call, P0 gets [D0, D1] in tensor_list and both of them have device "cuda:0".
          P1 gets [D0, D1] in tensor_list and both of them have device "cuda:1".
        - When some values in data are on gpu, the dist.all_gather() does not move those values to the target gpu.
          This results in memory on a gpu being accessed by two processes, which results in deadlocks and stuck runs.

    Note: This code has been copied from PyTorch example code here:
    https://github.com/pytorch/vision/blob/master/references/detection/utils.py#L75

    :param data: data that has be to be gathered on all processes.
    :type data: any
    :return: List of data objects from all processes.
    :rtype: List
    """
    world_size = get_world_size()
    if world_size == 1:
        return [data]

    # serialized to a Tensor
    buffer = pickle.dumps(data)
    storage = torch.ByteStorage.from_buffer(buffer)
    tensor = torch.ByteTensor(storage).to("cuda")

    # obtain Tensor size of each rank
    local_size = torch.tensor([tensor.numel()], device="cuda")
    size_list = [torch.tensor([0], device="cuda") for _ in range(world_size)]
    dist.all_gather(size_list, local_size)
    size_list = [int(size.item()) for size in size_list]
    max_size = max(size_list)

    # receiving Tensor from all ranks
    # we pad the tensor because torch all_gather does not support
    # gathering tensors of different shapes
    tensor_list = []
    for _ in size_list:
        tensor_list.append(torch.empty((max_size,), dtype=torch.uint8, device="cuda"))
    if local_size != max_size:
        padding = torch.empty(size=(max_size - local_size,), dtype=torch.uint8, device="cuda")
        tensor = torch.cat((tensor, padding), dim=0)
    dist.all_gather(tensor_list, tensor)

    data_list = []
    for size, tensor in zip(size_list, tensor_list):
        buffer = tensor.cpu().numpy().tobytes()[:size]
        data_list.append(pickle.loads(buffer))

    return data_list


def reduce_dict(input_dict, average=True):
    """Reduce a dictionary of tensors from all processes and return a dictionary with
    same keys as input_dict and reduced values.

    To be used with similar tensors from all processes with the below restrictions.
        1) Restrictions on input_dict within a process
            - Tensors for all the keys should already be on the current gpu device.
            - Tensors for all the keys in input_dict should have same size. This is because tensors for all keys
              are stacked using torch.stack before calling dist.all_reduce() and
              stack only works with tensors of same size.
        2) Restrictions on input_dict across processes.
            - input_dict on all processes should have same set of keys.
            - Tensors should have same size across processes i.e. tensors from process 1 should have
              same size as tensors from process 2 and so on.

    Note: The tensors in return dict will not have grad_fn as the below code is executed in torch.no_grad block.

    Note: This code has been copied from PyTorch example code here:
    https://github.com/pytorch/vision/blob/master/references/detection/utils.py#L118

    :param input_dict: Dictionary of tensors to be reduced.
    :type input_dict: Dict
    :param average: Whether to do average or sum for reduce.
    :type average: Boolean
    :return: Dictionary with same keys as data and reduced tensors as values.
    :rtype data: Dict
    """
    world_size = get_world_size()
    if world_size < 2:
        return input_dict

    with torch.no_grad():
        keys = []
        values = []
        # sort the keys so that they are consistent across processes.
        for key in sorted(input_dict.keys()):
            keys.append(key)
            values.append(input_dict[key])
        # Combine the tensors into a single tensor.
        values = torch.stack(values, dim=0)
        dist.all_reduce(values)
        if average:
            values /= world_size

        result = dict(zip(keys, values))
    return result
