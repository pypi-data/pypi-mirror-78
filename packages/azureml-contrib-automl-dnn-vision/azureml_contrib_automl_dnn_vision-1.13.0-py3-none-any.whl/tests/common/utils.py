import onnx
import onnxruntime as ort
import numpy as np


def _to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()


def check_exported_onnx_model(onnx_model_path, wrapper, input, device, get_torch_outputs_fn, check_output_parity):
    onnx_model = onnx.load(onnx_model_path)
    onnx.checker.check_model(onnx_model)

    ort_session = ort.InferenceSession(onnx_model_path)

    ort_inputs = {ort_session.get_inputs()[0].name: _to_numpy(input)}
    ort_outs = ort_session.run(None, ort_inputs)
    torch_outs = get_torch_outputs_fn(wrapper, input, device)

    # compare ONNX Runtime and PyTorch results
    if check_output_parity:
        np.testing.assert_allclose(_to_numpy(torch_outs), ort_outs[0], rtol=1e-03, atol=1e-05)
