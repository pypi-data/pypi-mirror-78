# This file was generated automatically by filter-stubs.py

import urllib3
from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence
class ConcurrentWriteFailure(RequestFailure):
    """
    A write failed due to another concurrent writer
    """
    ...

class Error(Exception):
    """Base class for blobfile exceptions."""

    def __init__(self, message: str):
        self.message = ...

class Request:

    def __init__(self, method: str, url: str, params: Optional[Mapping[str,
        str]]=..., headers: Optional[Mapping[str, str]]=..., data: Any=...,
        preload_content: bool=..., success_codes: Sequence[int]=...,
        retry_codes: Sequence[int]=...) ->None:
        self.url = ...
        self.method = ...
        self.params = ...
        self.headers = ...
        self.data = ...
        self.preload_content = ...
        self.success_codes = ...
        self.retry_codes = ...

    def __repr__(self):
        ...

class RequestFailure(Error):
    """
    A request failed, possibly after some number of retries
    """

    def __init__(self, message: str, request: Request, response: urllib3.
        HTTPResponse):
        self.message = ...
        self.request = ...
        self.response = ...

class RestartableStreamingWriteFailure(RequestFailure):
    """
    A streaming write failed in a permanent way that requires restarting from the beginning of the stream
    """
    ...

