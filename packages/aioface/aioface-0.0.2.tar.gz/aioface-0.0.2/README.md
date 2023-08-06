# aioface

aioface is a powerful and simple asynchronous framework for the Facebook Messenger API written in Python 3.7.

## Installation

```console
$ pip install aioface
```

## Examples

### Echo bot

```Python
from aioface import Bot, Dispatcher, BaseStorage, FacebookRequest


dispatcher = Dispatcher(BaseStorage())
bot = Bot(webhook_token='your_webhook_token',
          page_token='your_page_token',
          dispatcher=dispatcher)


@dispatcher.message_handler()
async def echo_handler(fb_request: FacebookRequest):
    await fb_request.send_message(message=fb_request.message_text)
    
    
if __name__ == '__main__':
    bot.run()
```
