import glob
import hashlib
import tarfile
import os
from io import BytesIO
from tempfile import TemporaryFile
import numpy as np


def convert_to_numpy(data):
    if isinstance(data, (tuple, list)):
        return [framework_to_numpy(d) for d in data]
    else:
        return framework_to_numpy(data)


def save_model(model, library: str):
    model_path = model
    if not isinstance(model, str):
        if not os.path.isdir("tmp"):
            os.mkdir("tmp")
        model_path = "tmp/tmp_model"
        if library == "pytorch":
            from torch import save
            import dill
            model_path += ".pt"
            save(model, model_path, pickle_module=dill)
        elif library == "keras":
            model_path += ".h5"
            import keras
            with keras.backend.get_session().graph.as_default():
                model.save_model(model_path)
        elif library == "mxnet":
            model_path += ".tar"
            model.export(model_path)
            with tarfile.open(model_path, "w") as tar:
                jsonname = model_path + "-symbol.json"
                paramname = model_path + "-0000.params"
                tar.add(jsonname, arcname=os.path.basename(jsonname))
                tar.add(paramname, arcname=os.path.basename(paramname))
        elif library == "TF":
            from tensorflow.keras.models import save_model
            model_path += ".tar"
            model.save(model_path + "dir")
            # save_model(model, model_path + "dir", include_optimizer=True, save_format='tf')
            with tarfile.open(model_path, "w") as tar:
                for file in glob.glob(model_path + "dir/*"):
                    tar.add(file, arcname=os.path.basename(file))
        elif library == "TF1":
            model_path += ".pb"
        else:
            raise ValueError("Model type: " + str(library) + " not defined")
    return model_path

    # if model_type is ModelType.ONNX:
    #     onnx.save(model, file_path)
    # elif model_type is ModelType.TF1:
    #     pass
    # tf.saved_model.save(model, "./dd.pb")
    # tf.compat.v1.saved_model.save(model, "tmp")
    # raise ValueError("Tensorflow 1 incompatible. Please use .pb file directly if using Tensorflow 1.")


def utf_str(obj):
    return str(obj).encode("utf-8")


def hash_model(model, library):
    hash = hashlib.md5()
    if isinstance(model, str):
        with open(model, "rb") as file:
            return hashlib.md5(file.read()).hexdigest()
    elif library == "pytorch":
        hash.update(utf_str(model))
        for p in model.parameters():
            hash.update(utf_str(p))
    elif library == "mxnet":
        from mxnet import sym
        x = sym.var('data')
        x = model(x).tojson()
        hash.update(utf_str(x))
        for param in sorted(model.collect_params().items()):
            hash.update(utf_str(param[1].data()))
    elif library == "TF":
        hash.update(utf_str(model.to_json()))
        for param in model.trainable_variables:
            hash.update(utf_str(param))
    else:
        raise ValueError("Cannot hash... Model type: {} not defined.".format(library))
    return hash.hexdigest()


def framework_to_numpy(data):
    try:
        if isinstance(data, np.ndarray):
            return data
    finally:
        pass
    try:
        from torch import Tensor
        if isinstance(data, Tensor):
            return data.numpy()
    finally:
        pass
    try:
        from tensorflow import is_tensor, make_ndarray
        if is_tensor(data):
            return make_ndarray(data)
    finally:
        pass
    try:
        from mxnet import nd
        if isinstance(data, nd.NDArray):
            return data.asnumpy()
    finally:
        pass
    raise ValueError("Could not determine framework data is from. Try pass in numpy array directly.")


def save_data(data):
    file = BytesIO()
    data = convert_to_numpy(data)
    if isinstance(data, (tuple, list)):
        dict_data = {str(i): data[i] for i in range(0, len(data))}
        np.savez(file, **dict_data)
    else:
        np.savez(file, data)
    file.seek(0)
    return file


def determine_model(model):
    try:
        from torch.nn import Module
        if isinstance(model, Module):
            return "pytorch"
    except:
        pass
    finally:
        pass
    try:
        from tensorflow.keras import Model
        if isinstance(model, Model):
            return "TF"
    except:
        pass
    finally:
        pass
    try:
        from mxnet.gluon.nn import Block
        if isinstance(model, Block):
            return "mxnet"
    except:
        pass
    finally:
        pass
    raise ValueError("Could not determine framework model is from. Please specify explicitly.")
