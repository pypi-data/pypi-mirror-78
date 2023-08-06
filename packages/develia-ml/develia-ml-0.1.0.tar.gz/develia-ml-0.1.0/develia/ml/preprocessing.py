from abc import abstractmethod as _abstractmethod
from functools import partial
from typing import (Iterable as _Iterable,
                    Union as _Union,
                    Sequence as _Sequence, Optional as _Optional, Tuple as _Tuple, List, Any, Union, Tuple, Callable)

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, FunctionTransformer, OneHotEncoder


class BaseTransformer(BaseEstimator, TransformerMixin):
    @_abstractmethod
    def fit(self, x, y=None, **fit_params) -> "BaseTransformer":
        pass

    @_abstractmethod
    def transform(self, x) -> np.ndarray:
        pass

    @_abstractmethod
    def inverse_transform(self, x) -> np.ndarray:
        pass


class CompositeTransformer(BaseTransformer):
    def __init__(self, transformers):
        self.transformers = transformers

    def fit(self, x, y=None, **fit_params) -> "BaseTransformer":

        if len(self.transformers) == 0:
            return self

        data = x
        for i in range(len(self.transformers) - 1):
            scaler = self.transformers[i]
            scaler.fit(data)
            data = scaler.transform(data)

        self.transformers[-1].fit(data)

        return self

    def transform(self, x):
        output = x
        for scaler in self.transformers:
            output = scaler.transform(output)

        return output

    def inverse_transform(self, x):
        output = x
        for scaler in reversed(self.transformers):
            output = scaler.inverse_transform(output)

        return output


def difference(x):
    diff = []
    for i in range(len(x) - 1):
        diff.append(x[i + 1] - x[i])

    return diff


def revert_difference(x, initial_value):
    last = initial_value
    inverse = [last]

    for i in range(len(x)):
        inverse.append(x[i] + last)
        last = x[i] + last

    return inverse


class Difference(BaseTransformer):
    _initial_value: object

    def fit(self, x, y=None, **fit_params) -> "BaseTransformer":
        self._initial_value = x[0]
        return self

    def transform(self, x):
        if self._initial_value is None:
            self.fit(x)

        output = difference(x)
        output.insert(0, [0])
        return np.array(output)

    def inverse_transform(self, x):
        output = revert_difference(x, self._initial_value)
        output.pop(0)
        return np.array(output)


class Reshaper(BaseTransformer):
    original_shape_: _Union[_Iterable, _Tuple[int]]

    def __init__(self, shape: _Tuple):
        self.shape = shape

    def fit(self, x, y=None, **fit_params) -> "BaseTransformer":
        self.original_shape_ = np.shape(x)
        return self

    def transform(self, x) -> np.ndarray:
        return np.array(x).reshape(self.shape)

    def inverse_transform(self, x) -> np.ndarray:
        return np.array(x).reshape(self.original_shape_)


def to_supervised(data: _Union[np.ndarray, _Sequence],
                  n_features: int = 1,
                  n_timesteps: _Optional[int] = None,
                  n_samples: _Optional[int] = -1) -> np.ndarray:
    if not isinstance(data, np.ndarray):
        data = np.array(data)

    if n_timesteps is None:
        return data.reshape((n_samples, n_features))
    else:
        return data.reshape((n_samples, n_timesteps, n_features))


def get_sliding_window(data: _Union[np.ndarray, _Sequence],
                       x_window_size: int,
                       y_window_size: int,
                       step: int = 1,
                       overlap: int = 0,
                       x_preprocessor=None,
                       y_preprocessor=None) -> (np.ndarray, np.ndarray):
    # noinspection PyPep8Naming
    X = []
    y = []

    length = len(data)
    start = length % step

    for i in range(start, length - (x_window_size + y_window_size) + 1, step):

        start_x = i
        end_x = i + x_window_size + overlap
        start_y = i + x_window_size - overlap
        end_y = i + x_window_size + y_window_size

        data_x = np.array(data[start_x:end_x])
        data_y = np.array(data[start_y:end_y])

        if x_preprocessor is not None:
            data_x = x_preprocessor.fit_transform(data_x)

        if y_preprocessor is not None:
            data_y = y_preprocessor.fit_transform(data_y)

        X.append(data_x)
        y.append(data_y)

    return np.array(X), np.array(y)


class InverseTransformer(BaseTransformer):
    def __init__(self, transformer):
        self.transformer = transformer

    def fit(self, x, y=None, **fit_params) -> "BaseTransformer":
        return self

    def transform(self, x) -> np.ndarray:
        return self.transformer.inverse_transform(x)

    def inverse_transform(self, x) -> np.ndarray:
        return self.transformer.transform(x)


class DateTimeEncoder(BaseTransformer):
    getters_: List[str]
    column_transformer_: ColumnTransformer

    def __init__(self,
                 month_encoder=None,
                 day_of_month_encoder=None,
                 day_of_week_encoder=None,
                 hour_encoder=None,
                 minute_encoder=None,
                 second_encoder=None):

        self.second_encoder = second_encoder
        self.minute_encoder = minute_encoder
        self.hour_encoder = hour_encoder
        self.day_of_week_encoder = day_of_week_encoder
        self.day_of_month_encoder = day_of_month_encoder
        self.month_encoder = month_encoder

    @staticmethod
    def _fit_transformer(transformer, rang):
        if transformer:
            transformer.fit(np.reshape(rang, (-1, 1)))

    @staticmethod
    def _apply_transformation(transformer, x, getter, output):
        if transformer:
            tmp = np.array(list(map(lambda row: [getter(row[0])], x)))
            tmp = transformer.transform(tmp)
            output = np.append(output, tmp, 1)

        return output

    def fit(self, x, y=None, **fit_params) -> "BaseTransformer":

        self._fit_transformer(self.second_encoder, range(0, 60), )
        self._fit_transformer(self.minute_encoder, range(0, 60), )
        self._fit_transformer(self.hour_encoder, range(0, 24), )
        self._fit_transformer(self.day_of_week_encoder, range(0, 7), )
        self._fit_transformer(self.day_of_month_encoder, range(1, 32), )
        self._fit_transformer(self.month_encoder, range(1, 13), )

        return self

    def transform(self, x) -> np.ndarray:

        output = np.empty((len(x), 0))
        output = self._apply_transformation(self.second_encoder, x, lambda date: date.second, output)
        output = self._apply_transformation(self.minute_encoder, x, lambda date: date.minute, output)
        output = self._apply_transformation(self.hour_encoder, x, lambda date: date.hour, output)
        output = self._apply_transformation(self.day_of_week_encoder, x, lambda date: date.weekday(), output)
        output = self._apply_transformation(self.day_of_month_encoder, x, lambda date: date.day, output)
        output = self._apply_transformation(self.month_encoder, x, lambda date: date.month, output)
        return output

    def inverse_transform(self, x):
        return None
