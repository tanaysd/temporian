# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Subtract a scalar from an event"""
from typing import Union, List

from temporian.core import operator_lib
from temporian.core.data import dtype as dtype_lib
from temporian.core.data.event import Event
from temporian.core.operators.arithmetic_scalar.base import (
    BaseArithmeticScalarOperator,
)


class SubtractScalarOperator(BaseArithmeticScalarOperator):
    """
    Subtract a scalar from an event, feature to feature according to their
    position.
    """

    @classmethod
    @property
    def operator_def_key(cls) -> str:
        return "SUBTRACTION_SCALAR"

    @property
    def prefix(self) -> str:
        return "sub"

    @property
    def supported_value_dtypes(self) -> List[dtype_lib.DType]:
        return [
            dtype_lib.FLOAT32,
            dtype_lib.FLOAT64,
            dtype_lib.INT32,
            dtype_lib.INT64,
        ]


operator_lib.register_operator(SubtractScalarOperator)


SCALAR = Union[float, int]


def subtract_scalar(
    minuend: Union[Event, SCALAR],
    subtrahend: Union[Event, SCALAR],
) -> Event:
    """
    Subtracts the subtrahend from the minuend and returns the difference.

    Args:
        minuend: The number or event being subtracted from.
        subtrahend: The number or event being subtracted.

    Returns:
        Event: Event with the difference between the minuend and subtrahend.
    """
    scalars_types = (float, int)

    if isinstance(minuend, Event) and isinstance(subtrahend, scalars_types):
        return SubtractScalarOperator(
            event=minuend,
            value=subtrahend,
            is_value_first=False,
        ).outputs["event"]

    if isinstance(minuend, scalars_types) and isinstance(subtrahend, Event):
        return SubtractScalarOperator(
            event=subtrahend,
            value=minuend,
            is_value_first=True,
        ).outputs["event"]

    raise ValueError(
        "Invalid input types for subtract_scalar. "
        "Expected (Event, SCALAR) or (SCALAR, Event), "
        f"got ({type(minuend)}, {type(subtrahend)})."
    )
