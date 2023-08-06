import typing
from dataclasses import asdict

from aioface import config
from aioface.fb import types
from aioface.fb.utils import fb_dict_factory

import aiohttp


class FacebookRequest:
    def __init__(self,
                 sender_psid: str,
                 page_token: str,
                 message_text: str = None,
                 payload: str = None):
        self.page_token = page_token
        self.sender_psid = sender_psid
        self.message_text = message_text
        self.payload = payload

    async def send_message(
            self,
            message: str = None,
            attachment: types.FacebookAttachment = None,
            quick_replies: typing.List[types.FacebookQuickReply] = None
    ) -> None:
        await self._send(data=self._build_request_body(
            text=message,
            attachment=attachment,
            quick_replies=quick_replies
        ))

    async def _send(self, data: typing.Dict):
        async with aiohttp.ClientSession() as session:
            await session.post(
                url=config.GRAPH_API_URL,
                params={'access_token': self.page_token},
                json=data
            )

    def _build_request_body(
            self,
            text: str = None,
            attachment: types.FacebookAttachment = None,
            quick_replies: typing.List[types.FacebookQuickReply] = None
    ) -> typing.Dict:
        body = {'recipient': {'id': self.sender_psid},
                'message': {}}
        if text is not None:
            body['message']['text'] = text
        if attachment is not None:
            body['message']['attachment'] = asdict(
                obj=attachment,
                dict_factory=fb_dict_factory
            )
        if quick_replies is not None:
            body['message']['quick_replies'] = [
                asdict(obj=reply, dict_factory=fb_dict_factory)
                for reply in quick_replies
            ]
        print(body)
        return body
