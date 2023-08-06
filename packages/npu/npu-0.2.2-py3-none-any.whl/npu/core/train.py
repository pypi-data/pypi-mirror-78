import time

import requests

from .Dataset import Dataset
from .common import getToken, checkData, sliceData, add_kwargs_to_params, checkModel
from .Task import Task
from .web.urls import TRAIN_URL
from .Model import Model
import base64
import dill


def train(model, training_data, test_data, batch_size, epochs, optimiser, loss, asynchronous, callback, **kwargs):
    checkModel(model)
    training_data = checkData(training_data)
    test_data = checkData(test_data)
    task_id = model.task_id if isinstance(model, Task) else ""
    task = Task(trainApi(model, training_data, test_data, optimiser, loss, batch_size, epochs, task_id, **kwargs).json(),
                callback)
    if not asynchronous:
        task.wait(show_progress=True)
        print("Model finished training")
    return task


def trainApi(model_id, train_data, test_data, optimiser, loss, batch_size, epochs, task_id="", **kwargs):
    train_start = train_end = test_start = test_end = None
    train_name = ""
    test_name = ""
    if isinstance(train_data, dict):
        train_data, train_start, train_end = sliceData(train_data)
    if isinstance(test_data, dict):
        test_data, test_start, test_end = sliceData(test_data)
    if isinstance(train_data, Dataset):
        train_name = train_data.id
        train_data = ""
    if isinstance(test_data, Dataset):
        test_name = test_data.id
        test_data = ""
    if callable(loss):
        print("Using custom loss function...")
        loss = base64.urlsafe_b64encode(dill.dumps(loss))
    params = {"trainId": train_data, "testId": test_data, "loss": loss,
              "token": getToken(), "batch_size": batch_size, "epochs": epochs, "task_id": task_id, "train_start": train_start,
              "train_end": train_end, "test_start": test_start, "test_end": test_end, "train_name": train_name, "test_name": test_name}
    if isinstance(model_id, Model):
        params["model_name"] = model_id.name
    elif model_id != "" and not isinstance(model_id, Task):
        params["modelId"] = model_id
    params = add_kwargs_to_params(params, **kwargs)
    response = requests.get(TRAIN_URL, params=params, json=optimiser)
    if response.status_code != 200:
        raise ValueError(response.text)
    return response
