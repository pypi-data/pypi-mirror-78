from typing import Any, Iterable, Mapping, Optional, Text
from wsgiref.types import StartResponse, WSGIApplication, WSGIEnvironment

class DispatcherMiddleware(object):
    app: WSGIApplication
    mounts: Mapping[Text, WSGIApplication]
    def __init__(self, app: WSGIApplication, mounts: Optional[Mapping[Text, WSGIApplication]] = ...) -> None: ...
    def __call__(self, environ: WSGIEnvironment, start_response: StartResponse) -> Iterable[bytes]: ...
