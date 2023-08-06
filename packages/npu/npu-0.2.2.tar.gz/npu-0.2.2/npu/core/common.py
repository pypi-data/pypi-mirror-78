import hashlib

import requests

from .DataLoader import DataLoader
from .Dataset import Dataset
from .saving.saving import save_data
from .web.urls import TOKEN_URL, HASH_URL, UPLOAD_DATA_URL

VERBOSITY = 1
MIN_VERBOSITY = 1
MID_VERBOSITY = 2
FULL_VERBOSITY = 3


_token = ""


def api(token_, verbosity):
    global _token
    global VERBOSITY
    _token = token_
    VERBOSITY = verbosity
    if VERBOSITY != MIN_VERBOSITY:
        print("Verbosity level set to {}".format(VERBOSITY))
    params = {"token": _token}
    response = requests.get(TOKEN_URL, params=params)
    if response.status_code == 200:
        print("Token successfully authenticated")
        return response
    else:
        raise ValueError(response.text)
    # "API token not valid"


def getToken():
    return _token


def getVerbosity():
    return VERBOSITY


def getResponse(response):
    try:
        return response.json()
    except Exception as e:
        raise ConnectionError("Invalid response received. Error: {}".format(response.text))


def add_kwargs_to_params(params, **kwargs):
    params = {**params, **kwargs}
    return params


def checkModel(model):
    from .Task import Task
    from .Model import Model
    if not isinstance(model, Task) and not isinstance(model, str) and not isinstance(model, Model):
        raise ValueError("Model is not a valid format. Please make sure you've compiled it first.")


def checkData(data):
    if isinstance(data, (str, dict)):
        return data
    elif isinstance(data, Dataset):
        return data
    elif isinstance(data, DataLoader):
        response = uploadDataLoader(data)
    else:
        response = uploadData(data)
    return getResponse(response)


def sliceData(data):
    id = data["id"]
    x = data["indexes"]
    y = None
    if isinstance(x, slice):
        y = x.stop
        x = x.start
    return id, x, y


def uploadDataLoader(dl):
    length = len(dl)
    if VERBOSITY >= MID_VERBOSITY:
        print("Hashing data locally...")
    hash, size = dl.hash()
    params = {"token": getToken(), "hash": hash, "collection": 1, "chunked": True, "is_last": False, "size": size}
    print("Checking if data is on servers...")
    response = requests.get(HASH_URL, params=params)
    if response.status_code == 200:
        if VERBOSITY >= MID_VERBOSITY:
            print("Data already uploaded. Will not reupload.")
        return response
    print("Data not on servers. Starting to upload. Total size of data is {} bytes".format(size))
    print("{} chunks to upload...".format(length))
    for i, data_part in enumerate(dl.numpy()):
        if VERBOSITY >= MID_VERBOSITY:
            print("Uploading chunk {} out of {}...".format(i + 1, length))
        file = save_data(data_part)
        files = {'file': file}
        if i == length - 1:
            params["is_last"] = True
        response = requests.post(UPLOAD_DATA_URL, files=files, params=params)
    return response


def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def uploadData(data):
    if VERBOSITY >= FULL_VERBOSITY:
        print("Saving data locally...")
    if isinstance(data, str):
        file = open(data, "rb")
    else:
        file = save_data(data)
    if VERBOSITY >= FULL_VERBOSITY:
        print("Hashing...")
    hash = hashlib.md5()
    size = 0
    for piece in read_in_chunks(file):
        size += len(piece)
        hash.update(piece)
    hash = hash.hexdigest()
    print("Checking if data is on servers...")
    params = {"token": getToken(), "hash": hash, "collection": 1}
    response = requests.get(HASH_URL, params=params)
    if response.status_code == 200:
        if VERBOSITY >= MID_VERBOSITY:
            print("Data already on servers. Returning result...")
        file.close()
        return response
    print("Data not found on servers. Total size of data is {} bytes. Uploading now...".format(size))
    file.seek(0)
    files = {'file': file}
    response = requests.post(UPLOAD_DATA_URL, files=files, params=params)
    if isinstance(data, str):
        file.close()
    return response


def hashData(data):
    pass
