__all__ = ['LoggerMiddleware']

import logging
import sys

from starlette.types import ASGIApp, Receive, Scope, Send

from rollbar.contrib.asgi import ReporterMiddleware as ASGIReporterMiddleware
from rollbar.contrib.starlette.requests import store_current_request

log = logging.getLogger(__name__)


class LoggerMiddleware(ASGIReporterMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        if sys.version_info < (3, 7):
            log.error('LoggerMiddleware requires Python 3.7+')
            raise RuntimeError('LoggerMiddleware requires Python 3.7+')

        super().__init__(app)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        store_current_request(scope, receive)

        await self.app(scope, receive, send)
