import typing
from dataclasses import dataclass

from aioface.storages.base_storage import BaseStorage
from aioface.fb.facebook_request import FacebookRequest
import aioface.dispatcher.utils as utils


@dataclass
class Filter:
    message: typing.Union[str, typing.List[str]]
    contains: typing.Union[str, typing.Set[str]]
    payload: typing.Union[str, typing.List[str]]


@dataclass
class Handler:
    callback: typing.Callable
    filter: Filter


class Dispatcher:
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.handlers: typing.List[Handler] = list()

    def message_handler(
            self,
            message: typing.Union[str, typing.List[str]] = None,
            contains: typing.Union[str, typing.List[str]] = None,
            payload: typing.Union[str, typing.List[str]] = None
    ):
        def decorator(callback):
            filter_obj = Filter(message=message,
                                contains=set(contains) if contains else None,
                                payload=payload)
            handler_obj = Handler(callback=callback, filter=filter_obj)
            self.handlers.append(handler_obj)
            return callback

        return decorator

    async def notify_handler(self, fb_request: FacebookRequest):
        for handler_obj in self.handlers:
            filter_obj = handler_obj.filter
            if not utils.check_full_text(
                    fb_full_text=fb_request.message_text,
                    filter_full_text=filter_obj.message):
                continue
            # if not utils.check_contains(fb_contains=fb_request.contains,
            #                             filter_contains=filter_obj.contains):
            #     continue
            if not utils.check_payload(fb_payload=fb_request.payload,
                                       filter_payload=filter_obj.payload):
                continue
            await handler_obj.callback(fb_request)
            break
