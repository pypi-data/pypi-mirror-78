"""
最小模型系统
"""

import abc
from abc import ABC
from typing import Union
from contextlib import contextmanager
from threading import Lock
import uuid


class MinimumModel(abc.ABC):
    def __init__(self):
        super(MinimumModel, self).__init__()
        self._model = None

    @property
    def model(self):
        assert self._model  # please load_model first
        return self._model

    @model.setter
    def model(self, value):
        print("set model", value)
        self._model = value

    @abc.abstractmethod
    def _load_model(self, *args, **kwargs):
        """
        you should set your model here. for example:
        this model can be abstract: it could be pytorch, tf-graph, or even a func handler.
        Example:
            >>> self.model = ...
        """

    @abc.abstractmethod
    def _forward(self, *args, **kwargs):
        """
        you need you implement your one time forwarding.
        :param args:
        :param kwargs:
        :return:
        Example:
            >>> x: Union[...]
            >>> return self.model(x)
        """

    def _reload_model(self, *args, **kwargs):
        """
        reload model by exec the load_model function.
        :return:
        """
        print("""reload model""")
        self.model = self._load_model(*args, **kwargs)


class AbstractModel(MinimumModel, ABC):
    def __init__(self, *args, **kwargs):
        super(AbstractModel, self).__init__()
        self.inference_lock = Lock()
        # load model immediately
        self._load_model(*args, **kwargs)
        self.load_model_args = args
        self.load_model_kwargs = kwargs

        self.analysis_args = ()
        self.analysis_kwargs = {}

    def analysis(self, *args, **kwargs):
        with self.lock():
            # refresh the args and kwargs if given new.
            if args:
                self.analysis_args = args
            if kwargs:
                self.analysis_kwargs = kwargs
            result = self._forward(*self.analysis_args, **self.analysis_kwargs)
            return result

    def reload(self, *args, **kwargs):
        with self.lock():
            # refresh the args and kwargs if given new.
            if args:
                self.load_model_args = args
            if kwargs:
                self.load_model_kwargs = kwargs
            self._reload_model(*self.load_model_args, **self.load_model_kwargs)

    @contextmanager
    def lock(self):
        try:
            self.inference_lock.acquire(blocking=True)
            yield uuid.uuid1()
        finally:
            if self.inference_lock.locked():
                self.inference_lock.release()
