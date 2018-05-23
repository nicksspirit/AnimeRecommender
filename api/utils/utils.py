from marshmallow import Schema
from typing import Dict
from types import FunctionType
from functools import wraps


def marshall_with(schema: Schema, many=True) -> FunctionType:
    def _marshall(f_query: FunctionType) -> FunctionType:
        def wrapper(self, limit, *args, **kwargs) -> Dict:
            data = f_query(self, limit, *args, **kwargs)
            result = schema(many=many).load(data)

            return result.data
        return wraps(f_query)(wrapper)
    return _marshall
