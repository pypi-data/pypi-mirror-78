import typing

from aioface.fb import types


class FacebookFactory:
    @staticmethod
    def _create_attachment(
            attachment_type: str,
            payload
    ) -> types.FacebookAttachment:
        return types.FacebookAttachment(type=attachment_type,
                                        payload=payload)

    @staticmethod
    def _create_template(
            template_type: str,
            text: str = None,
            elements: typing.List[types.FacebookTemplateElement] = None,
            buttons: typing.List[types.FacebookButton] = None,
            recipient_name: str = None,
            order_number: str = None,
            currency: str = None,
            payment_method: str = None,
            order_url: str = None,
            timestamp: str = None,
            summary: types.FacebookSummary = None,
            merchant_name: str = None,
            adjustments: typing.List[types.FacebookAdjustment] = None,
            address: types.FacebookAddress = None
    ) -> types.FacebookTemplate:
        return types.FacebookTemplate(
            template_type=template_type,
            text=text,
            elements=elements,
            buttons=buttons,
            recipient_name=recipient_name,
            order_number=order_number,
            currency=currency,
            payment_method=payment_method,
            order_url=order_url,
            timestamp=timestamp,
            summary=summary,
            merchant_name=merchant_name,
            adjustments=adjustments,
            address=address
        )

    @staticmethod
    def _create_template_element(
            title: str,
            subtitle: str = None,
            image_url: str = None,
            default_action: types.FacebookButton = None,
            buttons: typing.List[types.FacebookButton] = None,
            price: float = None,
            quantity: float = None,
            currency: str = None) -> types.FacebookTemplateElement:
        return types.FacebookTemplateElement(title=title,
                                             subtitle=subtitle,
                                             image_url=image_url,
                                             default_action=default_action,
                                             buttons=buttons,
                                             price=price,
                                             quantity=quantity,
                                             currency=currency)

    @staticmethod
    def _create_button(button_type: str,
                       title: str = None,
                       payload: str = None,
                       url: str = None,
                       messenger_extensions: bool = None,
                       webview_height_ratio: str = None,
                       fallback_url: str = None) -> types.FacebookButton:
        return types.FacebookButton(type=button_type,
                                    title=title,
                                    payload=payload,
                                    url=url,
                                    messenger_extensions=messenger_extensions,
                                    webview_height_ratio=webview_height_ratio,
                                    fallback_url=fallback_url)

    @staticmethod
    def _create_file_attachment(
            file_type: str,
            url: str = None,
            is_reusable: bool = False,
            attachment_id: str = None
    ) -> types.FacebookAttachment:
        if url is None and attachment_id is None:
            raise AttributeError
        if attachment_id is not None:
            if url is not None:
                raise AttributeError
            is_reusable = None
        facebook_file = types.FacebookFile(url=url,
                                           is_reusable=is_reusable,
                                           attachment_id=attachment_id)
        return types.FacebookAttachment(type=file_type,
                                        payload=facebook_file)

    def create_url_button(self,
                          title: str,
                          url: str) -> types.FacebookButton:
        return self._create_button(button_type='web_url',
                                   title=title,
                                   url=url)

    def create_postback_button(self,
                               title: str,
                               payload: str) -> types.FacebookButton:
        return self._create_button(button_type='postback',
                                   title=title,
                                   payload=payload)

    def create_phone_number_button(self,
                                   title: str,
                                   payload: str) -> types.FacebookButton:
        return self._create_button(button_type='phone_number',
                                   title=title,
                                   payload=payload)

    def create_log_in_button(self, url: str) -> types.FacebookButton:
        return self._create_button(button_type='account_link', url=url)

    def create_log_out_button(self) -> types.FacebookButton:
        return self._create_button(button_type='account_unlink')

    def create_image_attachment(
            self,
            url: str = None,
            is_reusable: bool = False,
            attachment_id: str = None
    ) -> types.FacebookAttachment:
        return self._create_file_attachment(file_type='image',
                                            url=url,
                                            is_reusable=is_reusable,
                                            attachment_id=attachment_id)

    def create_video_attachment(
            self,
            url: str = None,
            is_reusable: bool = False,
            attachment_id: str = None
    ) -> types.FacebookAttachment:
        return self._create_file_attachment(file_type='video',
                                            url=url,
                                            is_reusable=is_reusable,
                                            attachment_id=attachment_id)

    def create_audio_attachment(
            self,
            url: str = None,
            is_reusable: bool = False,
            attachment_id: str = None
    ) -> types.FacebookAttachment:
        return self._create_file_attachment(file_type='audio',
                                            url=url,
                                            is_reusable=is_reusable,
                                            attachment_id=attachment_id)

    def create_file_attachment(
            self,
            url: str = None,
            is_reusable: bool = False,
            attachment_id: str = None
    ) -> types.FacebookAttachment:
        return self._create_file_attachment(file_type='file',
                                            url=url,
                                            is_reusable=is_reusable,
                                            attachment_id=attachment_id)

    @staticmethod
    def _create_quick_reply(content_type: str,
                            title: str = None,
                            payload: typing.Union[str, int] = None,
                            image_url: str = None) -> types.FacebookQuickReply:
        return types.FacebookQuickReply(content_type=content_type,
                                        title=title,
                                        payload=payload,
                                        image_url=image_url)

    def create_text_quick_reply(
            self,
            title: str,
            payload: typing.Union[str, int],
            image_url: str = None
    ) -> types.FacebookQuickReply:
        return self._create_quick_reply(content_type='text',
                                        title=title,
                                        payload=payload,
                                        image_url=image_url)

    def create_user_phone_number_quick_reply(
            self,
            title: str = None,
            payload: typing.Union[str, int] = None,
            image_url: str = None
    ) -> types.FacebookQuickReply:
        return self._create_quick_reply(content_type='user_phone_number',
                                        title=title,
                                        payload=payload,
                                        image_url=image_url)

    def create_user_email_quick_reply(
            self,
            title: str = None,
            payload: typing.Union[str, int] = None,
            image_url: str = None
    ) -> types.FacebookQuickReply:
        return self._create_quick_reply(content_type='user_email',
                                        title=title,
                                        payload=payload,
                                        image_url=image_url)

    def create_generic_template_element(
            self,
            title: str,
            subtitle: str = None,
            image_url: str = None,
            default_action: types.FacebookButton = None,
            buttons: typing.List[types.FacebookButton] = None
    ) -> types.FacebookTemplateElement:
        return self._create_template_element(title=title,
                                             subtitle=subtitle,
                                             image_url=image_url,
                                             default_action=default_action,
                                             buttons=buttons)

    def create_generic_template(
            self,
            elements: typing.List[types.FacebookTemplateElement]
    ) -> types.FacebookAttachment:
        template = self._create_template(
            template_type='generic',
            elements=elements
        )
        return self._create_attachment(attachment_type='template',
                                       payload=template)

    def create_button_template_attachment(
            self,
            text: str,
            buttons: typing.List[types.FacebookButton]
    ) -> types.FacebookAttachment:
        template = self._create_template(
            template_type='button',
            text=text,
            buttons=buttons
        )
        return self._create_attachment(attachment_type='template',
                                       payload=template)

    def create_receipt_template_element(
            self,
            title: str,
            price: float,
            subtitle: str = None,
            quantity: float = None,
            currency: str = None,
            image_url: str = None
    ) -> types.FacebookTemplateElement:
        return self._create_template_element(title=title,
                                             price=price,
                                             subtitle=subtitle,
                                             quantity=quantity,
                                             currency=currency,
                                             image_url=image_url)

    @staticmethod
    def create_receipt_template_adjusment(
            name: str,
            amount: float
    ) -> types.FacebookAdjustment:
        return types.FacebookAdjustment(name=name,
                                        amount=amount)

    @staticmethod
    def create_receipt_template_summary(
            total_cost: float,
            subtotal: float = None,
            shipping_cost: float = None,
            total_tax: float = None,
    ) -> types.FacebookSummary:
        return types.FacebookSummary(subtotal=subtotal,
                                     shipping_cost=shipping_cost,
                                     total_tax=total_tax,
                                     total_cost=total_cost)

    @staticmethod
    def create_receipt_template_address(
            street_1: str,
            city: str,
            postal_code: str,
            state: str,
            country: str,
            street_2: str = None
    ) -> types.FacebookAddress:
        return types.FacebookAddress(street_1=street_1,
                                     street_2=street_2,
                                     city=city,
                                     postal_code=postal_code,
                                     state=state,
                                     country=country)

    def create_receipt_template(
            self,
            recipient_name: str,
            order_number: str,
            currency: str,
            payment_method: str,
            summary: types.FacebookSummary,
            merchant_name: str = None,
            timestamp: str = None,
            elements: typing.List[types.FacebookTemplateElement] = None,
            address: types.FacebookAddress = None,
            adjustments: typing.List[types.FacebookAdjustment] = None
    ):
        template = self._create_template(
            template_type='receipt',
            recipient_name=recipient_name,
            order_number=order_number,
            currency=currency,
            payment_method=payment_method,
            summary=summary,
            merchant_name=merchant_name,
            timestamp=timestamp,
            elements=elements,
            address=address,
            adjustments=adjustments
        )
        return self._create_attachment(attachment_type='template',
                                       payload=template)
