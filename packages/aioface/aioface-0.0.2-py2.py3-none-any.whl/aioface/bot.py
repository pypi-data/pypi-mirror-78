import typing

from aiohttp import web

from aioface.dispatcher import Dispatcher
from aioface.fb.facebook_request import FacebookRequest


class Bot:
    DEFAULT_HOST = '0.0.0.0'
    DEFAULT_PORT = 8080
    DEFAULT_WEBHOOK = '/'

    def __init__(self,
                 webhook_token: str,
                 page_token: str,
                 dispatcher: Dispatcher):
        self.webhook_token = webhook_token
        self.page_token = page_token
        self.dispatcher = dispatcher

    def verify_webhook(self, data: typing.Dict):
        if data['hub.mode'] == 'subscribe' and data['hub.verify_token'] == \
                self.webhook_token:
            return web.json_response(text=data['hub.challenge'])
        else:
            return web.json_response(status=403)

    async def handle_request(self, request):
        if request.method == 'GET':
            return self.verify_webhook(data=request.rel_url.query)
        elif request.method == 'POST':
            request_data = await request.json()
            print(request_data)
            if request_data['object'] == 'page':
                event_data = request_data['entry'][0]['messaging'][0]
                sender_psid = event_data['sender']['id']
                message_text = None
                payload = None
                if 'message' in event_data:
                    message_text = event_data['message']['text']
                if 'postback' in event_data:
                    payload = event_data['postback']['payload']
                fb_request = FacebookRequest(page_token=self.page_token,
                                             sender_psid=sender_psid,
                                             message_text=message_text,
                                             payload=payload)
                await self.dispatcher.notify_handler(fb_request=fb_request)
                return web.json_response()
            else:
                return web.json_response(status=404)

    def run(self,
            host: str = DEFAULT_HOST,
            port: int = DEFAULT_PORT,
            webhook: str = DEFAULT_WEBHOOK):
        bot_app = web.Application()
        bot_app.add_routes([web.get(webhook,
                                    self.handle_request),
                            web.post(webhook,
                                     self.handle_request)])
        web.run_app(app=bot_app,
                    host=host,
                    port=port)
