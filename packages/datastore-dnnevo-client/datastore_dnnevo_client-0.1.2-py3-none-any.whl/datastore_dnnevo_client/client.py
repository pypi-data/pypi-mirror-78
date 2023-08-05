import json
import logging
import pickle
import subprocess
from time import sleep
from functools import reduce

import requests
import os

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("dnnevo")

MASTER_ADDRESS = "http://master:5000"


class DatasetDescriptor(object):

    def __init__(
            self,
            dataset_name,
            input_shape,
            output_shape,
            samples_count,
            samples_train,
            samples_test
    ):
        self.__dataset_name = dataset_name
        self.__input_shape = input_shape
        self.__output_shape = output_shape
        self.__samples_count = samples_count
        self.__samples_train = samples_train
        self.__samples_test = samples_test
        self.__input_size = reduce(lambda l, r: l * r, input_shape)
        self.__output_size = reduce(lambda l, r: l * r, output_shape)

    @property
    def dataset_name(self):
        return self.__dataset_name

    @property
    def input_shape(self):
        return self.__input_shape

    @property
    def output_shape(self):
        return self.__output_shape

    @property
    def samples_count(self):
        return self.__samples_count

    @property
    def samples_train(self):
        return self.__samples_train

    @property
    def samples_test(self):
        return self.__samples_test

    @property
    def input_size(self):
        return self.__input_size

    @property
    def output_size(self):
        return self.__output_size


class DataStoreClient(object):
    def __init__(self, dataset_name, indices=None, batch_size=1, is_train=True, dir="./"):
        if indices is None or indices == []:
            self.indices = list(range(10000))
        else:
            self.indices = indices
        self.dataset_name = dataset_name.lower()
        self.batch_size = batch_size
        self.prefix = self.dataset_name + "_"
        self.suffix = "_" + ("train" if is_train else "test")
        self.dir = dir
        self._size = None

    def format_id(self, id):
        if len(id.split("_")) > 1:
            id = id.split("_")[1]
        return "{}{}{}".format(self.prefix, id, self.suffix)

    def _chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def _url(self, url):
        return "http://" + url

    def get_by_id(self, datapoint_id):
        datapoint_id = self.format_id(str(datapoint_id))
        id_mapping = requests.get('{}/get/{}'.format(MASTER_ADDRESS, datapoint_id)).json()
        response = requests.get('{}/get/{}'.format(self._url(id_mapping["worker"]), datapoint_id))
        try:
            return pickle.loads(response.content)
        except IOError:
            logger.error("Failed saving result for datapoint id: {}".format(datapoint_id))
            return ""

    def get_by_ids(self, ids):
        paths = []
        ids = list(map(lambda x: self.format_id(x), ids))
        for chunk in self._chunks(ids, self.batch_size):
            response = requests.post('{}/batch/get'.format(MASTER_ADDRESS),
                                     json.dumps({"ids": chunk}),
                                     headers={'content-type': 'Application/json'})
            batches = response.json()
            for batch in batches:
                url = "{}/batch/get/{}".format(self._url(batch["addr"]), batch["id"])
                try:
                    response = requests.get(url)
                    while response.status_code == 202:
                        response = requests.get(url)
                        sleep(5)
                    path = self.dir
                    total_path = path + batch["id"] + ".tar.gz"
                    with open(total_path, "wb+") as file:
                        file.write(response.content)
                    subprocess.run(["tar", "-zxf", total_path])
                    subprocess.run(["rm", total_path])
                    paths.append(path + batch["id"])
                except IOError as ex:
                    logger.error("Failed saving result: {}".format(ex))
        data = []
        target = []
        for path in paths:
            files = [f for f in os.listdir(path)]
            for file in files:
                with open(path + "/" + file, "rb") as f:
                    (dt, trgt) = pickle.load(f)
                    data.append(dt)
                    target.append(trgt)
            subprocess.run(["rm", "-r", path])
        return data, target

    def dataset_size(self):
        if self._size is None:
            # removing first element from suffix to get rid of _
            response = requests.get('{}/size/{}/{}'.format(MASTER_ADDRESS, self.dataset_name, self.suffix[1:]))
            self._size = response.json()["size"]
        return self._size

    def get_descriptor(self):
        response = requests.get('{}/descriptor/{}'.format(MASTER_ADDRESS, self.dataset_name))
        jsn = response.json()
        return DatasetDescriptor(
            self.dataset_name,
            tuple(list(map(lambda x: int(x), jsn["input_shape"]))),
            tuple(list(map(lambda x: int(x), jsn["output_shape"]))),
            int(jsn["size"]),
            int(jsn["size_train"]),
            int(jsn["size_test"])
        )
