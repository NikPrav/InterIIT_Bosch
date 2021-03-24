import typing as t
from werkzeug.datastructures import Headers
from werkzeug.wrappers import BaseResponse

_str_bytes = t.Union[str, bytes]
_data_type = t.Union[
    _str_bytes,
    BaseResponse,
    t.Dict[str, t.Any],
    t.Callable[
        [t.Dict[str, t.Any], t.Callable[[str, t.List[t.Tuple[str, str]]], None]],
        t.Iterable[bytes],
    ],
]
_status_type = t.Union[int, _str_bytes]
_headers_type = t.Union[
    Headers,
    t.Dict[_str_bytes, _str_bytes],
    t.Iterable[t.Tuple[_str_bytes, _str_bytes]],
]

view_return_type = t.Union[
    _data_type,
    t.Tuple[_data_type],
    t.Tuple[_data_type, _status_type],
    t.Tuple[_data_type, _headers_type],
    t.Tuple[_data_type, _status_type, _headers_type],
]
