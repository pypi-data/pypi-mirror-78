import typing

from dataclasses import dataclass


@dataclass
class FacebookButton:
    type: str
    title: typing.Optional[str]
    payload: typing.Optional[str]
    url: typing.Optional[str]
    messenger_extensions: typing.Optional[bool]
    webview_height_ratio: typing.Optional[str]
    fallback_url: typing.Optional[str]


@dataclass
class FacebookAddress:
    street_1: str
    city: str
    postal_code: str
    state: str
    country: str
    street_2: typing.Optional[str]


@dataclass
class FacebookSummary:
    total_cost: float
    subtotal: typing.Optional[float]
    shipping_cost: typing.Optional[float]
    total_tax: typing.Optional[float]


@dataclass
class FacebookAdjustment:
    name: str
    amount: float


@dataclass
class FacebookTemplateElement:
    title: str
    subtitle: typing.Optional[str]
    image_url: typing.Optional[str]
    default_action: typing.Optional[FacebookButton]
    buttons: typing.Optional[typing.List[FacebookButton]]
    quantity: typing.Optional[float]
    price: typing.Optional[float]
    currency: typing.Optional[str]


@dataclass
class FacebookTemplate:
    template_type: str
    text: typing.Optional[str]
    elements: typing.Optional[typing.List[FacebookTemplateElement]]
    buttons: typing.Optional[typing.List[FacebookButton]]
    recipient_name: typing.Optional[str]
    merchant_name: typing.Optional[str]
    order_number: typing.Optional[str]
    currency: typing.Optional[str]
    payment_method: typing.Optional[str]
    order_url: typing.Optional[str]
    timestamp: typing.Optional[str]
    summary: typing.Optional[FacebookSummary]
    adjustments: typing.Optional[typing.List[FacebookAdjustment]]
    address: typing.Optional[FacebookAddress]


@dataclass
class FacebookQuickReply:
    content_type: str
    payload: typing.Optional[typing.Union[str, int]]
    title: typing.Optional[str]
    image_url: typing.Optional[str]


@dataclass
class FacebookFile:
    url: typing.Optional[str]
    is_reusable: typing.Optional[bool]
    attachment_id: typing.Optional[str]


@dataclass
class FacebookAttachment:
    type: str
    payload: typing.Any
