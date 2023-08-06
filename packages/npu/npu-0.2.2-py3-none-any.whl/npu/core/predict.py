# @wait_task
import requests

from .common import getToken, checkData, sliceData, add_kwargs_to_params, checkModel
from .Task import Task
from .web.urls import PREDICT_URL
from .Dataset import Dataset
from .Model import Model


def predict(model, data, asynchronous=False, callback=None, **kwargs):
    checkModel(model)
    inference_data = checkData(data)
    task_id = model.task_id if isinstance(model, Task) else ""
    resp = predictApi(model, inference_data, task_id, **kwargs)
    task = Task(resp.json(), callback)
    if not asynchronous:
        task.wait()
    return task


def predictApi(model, data_id, task_id, **kwargs):
    start = end = None
    data_name = ""
    if isinstance(data_id, dict):
        data_id, start, end = sliceData(data_id)
    if isinstance(data_id, Dataset):
        data_name = data_id.id
        data_id = ""
    params = {"dataId": data_id, "token": getToken(), "task_id": task_id, "start": start, "end": end, "data_name": data_name}
    if isinstance(model, Model):
        params["model_name"] = model.name
    elif model != "" and not isinstance(model, Task):
        params["modelId"] = model
    params = add_kwargs_to_params(params, **kwargs)
    response = requests.get(PREDICT_URL, params=params)
    if response.status_code != 200:
        raise ValueError(response.text)
    return response


