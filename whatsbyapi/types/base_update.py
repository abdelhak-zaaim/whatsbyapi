"""This module contains the base types for all update types."""

from __future__ import annotations


__all__ = [
    "StopHandling",
]

import abc
import pathlib
import dataclasses
import datetime as dt
from typing import TYPE_CHECKING, BinaryIO, Iterable

from .others import Contact, Metadata, ProductsSection, User

if TYPE_CHECKING:
    from whatsbyapi.client import WhatsApp

    from .callback import Button, ButtonUrl, SectionList, FlowButton
    from .template import Template


class StopHandling(Exception):
    """
    Raise this exception to stop handling an update.

    You can call ``.stop_handling()`` on every update object to raise this exception.

    Example:

            >>> from whatsbyapi import WhatsApp
            >>> from whatsbyapi.types import Message
            >>> wa = WhatsApp(...)

            >>> @wa.on_message()
            ... def callback(_: WhatsApp, msg: Message):
            ...     msg.reply_text("Hello from whatsbyapi!")
            ...     msg.stop_handling()  # or raise StopHandling

            >>> @wa.on_message()
            ... def not_called(_: WhatsApp, msg: Message):
            ...     msg.reply_text("This message will not be sent")
    """

    pass


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class BaseUpdate(abc.ABC):
    """Base class for all update types."""

    _client: WhatsApp = dataclasses.field(repr=False, hash=False, compare=False)
    raw: dict = dataclasses.field(repr=False, hash=False, compare=False)

    @property
    @abc.abstractmethod
    def id(self) -> str:
        """The id of the update"""
        ...

    @property
    @abc.abstractmethod
    def timestamp(self) -> dt.datetime:
        """The timestamp the update was sent"""
        ...

    @classmethod
    @abc.abstractmethod
    def from_update(cls, client: WhatsApp, update: dict) -> BaseUpdate:
        """Create an update object from a raw update dict."""
        ...

    def __hash__(self):
        """Return the hash of the update ID."""
        return hash(self.id)

    def stop_handling(self) -> None:
        """
        Call this method to break out of the handler loop. other handlers will not be called.

        This method just raises :class:`StopHandling` which is caught by the handler loop and breaks out of it.

        Example:

            >>> from whatsbyapi import WhatsApp
            >>> from whatsbyapi.types import Message
            >>> wa = WhatsApp(...)

            >>> @wa.on_message()
            ... def callback(_: WhatsApp, msg: Message):
            ...     msg.reply_text("Hello from whatsbyapi!")
            ...     msg.stop_handling()

            >>> @wa.on_message()
            ... def callback_not_called(_: WhatsApp, msg: Message):
            ...     msg.reply_text("This message will not be sent")
        """
        raise StopHandling


@dataclasses.dataclass(frozen=True, slots=True, kw_only=True)
class BaseUserUpdate(BaseUpdate, abc.ABC):
    """Base class for all user-related update types (message, callback, etc.)."""

    @property
    @abc.abstractmethod
    def metadata(self) -> Metadata: ...

    @property
    @abc.abstractmethod
    def from_user(self) -> User: ...

    @property
    def sender(self) -> str:
        """
        The WhatsApp ID of the sender.
            - Shortcut for ``.from_user.wa_id``.
        """
        return self.from_user.wa_id

    @property
    def message_id_to_reply(self) -> str:
        """
        The ID of the message to reply to.

        If you want to ``wa.send_x`` with ``reply_to_message_id`` in order to reply to a message, use this property
        instead of ``id`` to prevent errors.
        """
        return self.id

    def reply_text(
        self,
        text: str,
        header: str | None = None,
        footer: str | None = None,
        buttons: Iterable[Button] | ButtonUrl | FlowButton | SectionList | None = None,
        quote: bool = False,
        preview_url: bool = False,
        keyboard: None = None,
    ) -> str:
        """
        Reply to the message with text.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_message` with ``to`` and ``reply_to_message_id``.

        Example:

            >>> msg.reply_text(
            ...     text="Hello from whatsbyapi! (https://github.com/abdelhak-zaaim/whatsbyapi)",
            ...     quote=True,
            ... )

        Example with keyboard buttons:

            >>> from whatsbyapi.types import Button
            >>> msg.reply_text(
            ...     header="Hello from whatsbyapi!",
            ...     text="What can I help you with?",
            ...     footer="Powered by whatsbyapi",
            ...     buttons=[
            ...         Button("Help", data="help"),
            ...         Button("About", data="about"),
            ...     ],
            ...     quote=True
            ... )

        Example with a section list:

            >>> from whatsbyapi.types import SectionList, Section, SectionRow
            >>> msg.reply_text(
            ...     header="Hello from whatsbyapi!",
            ...     text="What can I help you with?",
            ...     footer="Powered by whatsbyapi",
            ...     buttons=SectionList(
            ...         button_title="Choose an option",
            ...         sections=[
            ...             Section(
            ...                 title="Help",
            ...                 rows=[
            ...                     SectionRow(
            ...                         title="Help",
            ...                         callback_data="help",
            ...                         description="Get help with whatsbyapi",
            ...                     ),
            ...                     SectionRow(
            ...                         title="About",
            ...                         callback_data="about",
            ...                         description="Learn more about whatsbyapi",
            ...                     ),
            ...                 ],
            ...            ),
            ...            Section(
            ...                 title="Other",
            ...                 rows=[
            ...                     SectionRow(
            ...                         title="GitHub",
            ...                         callback_data="github",
            ...                         description="View the whatsbyapi GitHub repository",
            ...                     ),
            ...                 ],
            ...             ),
            ...         ],
            ...     ),
            ...     quote=True
            ... )

        Args:
            text: The text to reply with (markdown allowed, max 4096 characters).
            header: The header of the reply (if buttons are provided, optional, up to 60 characters,
             no markdown allowed).
            footer: The footer of the reply (if buttons are provided, optional, up to 60 characters,
             markdown has no effect).
            buttons: The buttons to send with the message (optional).
            quote: Whether to quote the replied message (default: False).
            preview_url: Whether to show a preview of the URL in the message (if any).
            keyboard: Deprecated and will be removed in a future version, use ``buttons`` instead.

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_message(
            to=self.sender,
            text=text,
            header=header,
            footer=footer,
            buttons=buttons,
            reply_to_message_id=self.message_id_to_reply if quote else None,
            preview_url=preview_url,
            keyboard=keyboard,
        )

    reply = reply_text  # alias

    def reply_image(
        self,
        image: str | pathlib.Path | bytes | BinaryIO,
        caption: str | None = None,
        body: None = None,
        footer: str | None = None,
        buttons: Iterable[Button] | ButtonUrl | FlowButton | None = None,
        quote: bool = False,
        mime_type: str | None = None,
    ) -> str:
        """
        Reply to the message with an image.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_image` with ``to`` and ``reply_to_message_id``.
            - Images must be 8-bit, RGB or RGBA.

        Example:

            >>> msg.reply_image(
            ...     image="https://example.com/image.png",
            ...     caption="This is an image!",
            ...     quote=True,
            ... )

        Args:
            image: The image to reply (either a media ID, URL, file path, bytes, or an open file object. When buttons are
             provided, only URL is supported).
            caption: The caption of the image (required when buttons are provided,
             `markdown <https://faq.whatsapp.com/539178204879377>`_ allowed).
            footer: The footer of the message (if buttons are provided, optional,
             `markdown <https://faq.whatsapp.com/539178204879377>`_ has no effect).
            buttons: The buttons to send with the image (optional).
            mime_type: The mime type of the image (optional, required when sending an image as bytes or a file object,
             or file path that does not have an extension).
            quote: Whether to quote the replied message (default: False).
            body: Deprecated and will be removed in a future version, use ``caption`` instead.

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_image(
            to=self.sender,
            image=image,
            caption=caption,
            body=body,
            footer=footer,
            buttons=buttons,
            reply_to_message_id=self.message_id_to_reply if quote else None,
            mime_type=mime_type,
        )

    def reply_video(
        self,
        video: str | pathlib.Path | bytes | BinaryIO,
        caption: str | None = None,
        body: None = None,
        footer: str | None = None,
        buttons: Iterable[Button] | ButtonUrl | FlowButton | None = None,
        quote: bool = False,
        mime_type: str | None = None,
    ) -> str:
        """
        Reply to the message with a video.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_video` with ``to`` and ``reply_to_message_id``.
            - Only H.264 video codec and AAC audio codec is supported.
            - Videos with a single audio stream or no audio stream are supported.

        Example:

            >>> msg.reply_video(
            ...     video="https://example.com/video.mp4",
            ...     caption="This is a video",
            ...     quote=True,
            ... )

        Args:
            video: The video to reply (either a media ID, URL, file path, bytes, or an open file object. When buttons
             are provided, only URL is supported).
            caption: The caption of the video (required when sending a video with buttons,
             `markdown <https://faq.whatsapp.com/539178204879377>`_ allowed).
            footer: The footer of the message (if ``buttons`` are provided, optional,
             `markdown <https://faq.whatsapp.com/539178204879377>`_ has no effect).
            buttons: The buttons to send with the video (optional).
            mime_type: The mime type of the video (optional, required when sending a video as bytes or a file object,
             or file path that does not have an extension).
            quote: Whether to quote the replied message (default: False).
            body: Deprecated and will be removed in a future version, use ``caption`` instead.

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_video(
            to=self.sender,
            video=video,
            caption=caption,
            reply_to_message_id=self.message_id_to_reply if quote else None,
            buttons=buttons,
            body=body,
            footer=footer,
            mime_type=mime_type,
        )

    def reply_document(
        self,
        document: str | pathlib.Path | bytes | BinaryIO,
        filename: str | None = None,
        caption: str | None = None,
        body: None = None,
        footer: str | None = None,
        buttons: Iterable[Button] | ButtonUrl | FlowButton | None = None,
        quote: bool = False,
        mime_type: str | None = None,
    ) -> str:
        """
        Reply to the message with a document.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_document` with ``to`` and ``reply_to_message_id``.

        Example:

            >>> msg.reply_document(
            ...     document="https://example.com/example_123.pdf",
            ...     filename="example.pdf",
            ...     caption="Example PDF",
            ...     quote=True,
            ... )


        Args:
            document: The document to reply (either a media ID, URL, file path, bytes, or an open file object. When
             buttons are provided, only URL is supported).
            filename: The filename of the document (optional, The extension of the filename will specify what format the
             document is displayed as in WhatsApp).
            caption: The caption of the document (required when sending a document with buttons,
             `markdown <https://faq.whatsapp.com/539178204879377>`_ allowed).
            footer: The footer of the message (if buttons are provided, optional,
             `markdown <https://faq.whatsapp.com/539178204879377>`_ has no effect).
            buttons: The buttons to send with the document (optional).
            mime_type: The mime type of the document (optional, required when sending a document as bytes or a file
             object, or file path that does not have an extension).
            body: Deprecated and will be removed in a future version, use ``caption`` instead.
            quote: Whether to quote the replied message (default: False).

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_document(
            to=self.sender,
            document=document,
            filename=filename,
            caption=caption,
            reply_to_message_id=self.message_id_to_reply if quote else None,
            buttons=buttons,
            body=body,
            footer=footer,
            mime_type=mime_type,
        )

    def reply_audio(
        self,
        audio: str | pathlib.Path | bytes | BinaryIO,
        mime_type: str | None = None,
    ) -> str:
        """
        Reply to the message with an audio.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_audio` with ``to`` and ``reply_to_message_id``.

        Example:

            >>> msg.reply_audio(
            ...     audio='https://example.com/audio.mp3',
            ... )

        Args:
            audio: The audio file to reply with (either a media ID, URL, file path, bytes, or an open file object).
            mime_type: The mime type of the audio (optional, required when sending a audio as bytes or a file object,
             or file path that does not have an extension).

        Returns:
            The ID of the sent message.
        """
        return self._client.send_audio(
            to=self.sender,
            audio=audio,
            mime_type=mime_type,
        )

    def reply_sticker(
        self,
        sticker: str | pathlib.Path | bytes | BinaryIO,
        mime_type: str | None = None,
    ) -> str:
        """
        Reply to the message with a sticker.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_sticker` with ``to`` and ``reply_to_message_id``.
            - A static sticker needs to be 512x512 pixels and cannot exceed 100 KB.
            - An animated sticker must be 512x512 pixels and cannot exceed 500 KB.

        Example:

            >>> msg.reply_sticker(
            ...     sticker='https://example.com/sticker.webp',
            ... )

        Args:
            sticker: The sticker to reply with (either a media ID, URL, file path, bytes, or an open file object).
            mime_type: The mime type of the sticker (optional, required when sending a sticker as bytes or a file
             object, or file path that does not have an extension).

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_sticker(
            to=self.sender,
            sticker=sticker,
            mime_type=mime_type,
        )

    def reply_location(
        self,
        latitude: float,
        longitude: float,
        name: str | None = None,
        address: str | None = None,
    ) -> str:
        """
        Reply to the message with a location.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_location` with ``to`` and ``reply_to_message_id``.

        Example:

            >>> msg.reply_location(
            ...     latitude=37.4847483695049,
            ...     longitude=--122.1473373086664,
            ...     name='WhatsApp HQ',
            ...     address='Menlo Park, 1601 Willow Rd, United States',
            ... )


        Args:
            latitude: The latitude of the location.
            longitude: The longitude of the location.
            name: The name of the location (optional).
            address: The address of the location (optional).

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_location(
            to=self.sender,
            latitude=latitude,
            longitude=longitude,
            name=name,
            address=address,
        )

    def reply_contact(
        self,
        contact: Contact | Iterable[Contact],
        quote: bool = False,
    ) -> str:
        """
        Reply to the message with a contact/s.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_contact` with ``to`` and ``reply_to_message_id``.

        Example:

            >>> from whatsbyapi.types import Contact
            >>> msg.reply_contact(
            ...     contact=Contact(
            ...         name=Contact.Name(formatted_name='David Lev', first_name='David'),
            ...         phones=[Contact.Phone(phone='1234567890', wa_id='1234567890', type='MOBILE')],
            ...         emails=[Contact.Email(email='test@test.com', type='WORK')],
            ...         urls=[Contact.Url(url='https://exmaple.com', type='HOME')],
            ...      ),
            ...     quote=True,
            ... )


        Args:
            contact: The contact/s to send.
            quote: Whether to quote the replied message (default: False).

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_contact(
            to=self.sender,
            contact=contact,
            reply_to_message_id=self.message_id_to_reply if quote else None,
        )

    def react(self, emoji: str) -> str:
        """
        React to the message with an emoji.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_reaction` with ``to`` and ``message_id``.

        Example:

            >>> msg.react('👍')

        Args:
            emoji: The emoji to react with.

        Returns:
            The ID of the sent reaction.
        """
        return self._client.send_reaction(
            to=self.sender,
            emoji=emoji,
            message_id=self.message_id_to_reply,
        )

    def unreact(self) -> str:
        """
        Remove the reaction from the message.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.remove_reaction` with ``to`` and ``message_id``.

        Example:

            >>> msg.unreact()

        Returns:
            The ID of the sent unreaction.
        """
        return self._client.remove_reaction(
            to=self.sender, message_id=self.message_id_to_reply
        )

    def reply_catalog(
        self,
        body: str,
        footer: str | None = None,
        thumbnail_product_sku: str | None = None,
        quote: bool = False,
    ) -> str:
        """
        Reply to the message with a catalog.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_catalog` with ``to`` and ``reply_to_message_id``.

        Example:

            >>> msg.reply_catalog(
            ...     body='This is a catalog',
            ...     footer='Powered by whatsbyapi',
            ...     thumbnail_product_sku='SKU123',
            ... )

        Args:
            body: Text to appear in the message body (up to 1024 characters).
            footer: Text to appear in the footer of the message (optional, up to 60 characters).
            thumbnail_product_sku: The thumbnail of this item will be used as the message's header image (optional, if
                not provided, the first item in the catalog will be used).
            quote: Whether to quote the replied message (default: False).

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_catalog(
            to=self.sender,
            body=body,
            footer=footer,
            thumbnail_product_sku=thumbnail_product_sku,
            reply_to_message_id=self.message_id_to_reply if quote else None,
        )

    def reply_product(
        self,
        catalog_id: str,
        sku: str,
        body: str | None = None,
        footer: str | None = None,
        quote: bool = False,
    ) -> str:
        """
        Reply to the message with a product.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_product` with ``to`` and ``reply_to_message_id``.
            - To reply with multiple products, use :py:func:`~BaseUserUpdate.reply_products`.

        Args:
            catalog_id: The ID of the catalog to send the product from. (To get the catalog ID use
             :py:func:`~whatsbyapi.client.WhatsApp.get_commerce_settings` or in the `Commerce Manager
             <https://business.facebook.com/commerce/>`_).
            sku: The product SKU to send.
            body: Text to appear in the message body (up to 1024 characters).
            footer: Text to appear in the footer of the message (optional, up to 60 characters).
            quote: Whether to quote the replied message (default: False).

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_product(
            to=self.sender,
            catalog_id=catalog_id,
            sku=sku,
            body=body,
            footer=footer,
            reply_to_message_id=self.message_id_to_reply if quote else None,
        )

    def reply_products(
        self,
        catalog_id: str,
        product_sections: Iterable[ProductsSection],
        title: str,
        body: str,
        footer: str | None = None,
        quote: bool = False,
    ) -> str:
        """
        Reply to the message with a product.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_products` with ``to`` and ``reply_to_message_id``.
            - To reply with multiple products, use :py:func:`~BaseUserUpdate.reply_products`.

        Example:

            >>> from whatsbyapi.types import ProductsSection
            >>> msg.reply_products(
            ...     catalog_id='1234567890',
            ...     title='Tech Products',
            ...     body='Check out our products!',
            ...     product_sections=[
            ...         ProductsSection(
            ...             title='Smartphones',
            ...             skus=['IPHONE12', 'GALAXYS21'],
            ...         ),
            ...         ProductsSection(
            ...             title='Laptops',
            ...             skus=['MACBOOKPRO', 'SURFACEPRO'],
            ...         ),
            ...     ],
            ...     footer='Powered by whatsbyapi',
            ...     quote=True,
            ... )


        Args:
            catalog_id: The ID of the catalog to send the product from (To get the catalog ID
             use :py:func:`~whatsbyapi.client.WhatsApp.get_commerce_settings` or in the `Commerce Manager <https://business.facebook.com/commerce/>`_).
            product_sections: The product sections to send (up to 30 products across all sections).
            title: The title of the product list (up to 60 characters).
            body: Text to appear in the message body (up to 1024 characters).
            footer: Text to appear in the footer of the message (optional, up to 60 characters).
            quote: Whether to quote the replied message (default: False).

        Returns:
            The ID of the sent reply.
        """
        return self._client.send_products(
            to=self.sender,
            catalog_id=catalog_id,
            product_sections=product_sections,
            title=title,
            body=body,
            footer=footer,
            reply_to_message_id=self.message_id_to_reply if quote else None,
        )

    def reply_template(
        self,
        template: Template,
        quote: bool = False,
    ) -> str:
        """
        Reply to the message with a template.

        -- Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.send_template` with ``to`` and ``reply_to_message_id``.

        Example:

            >>> from whatsbyapi.types import Template as Temp
            >>> wa = WhatsApp(...)
            >>> wa.send_template(
            ...     to='1234567890',
            ...         template=Temp(
            ...         name='buy_new_iphone_x',
            ...         language=Temp.Language.ENGLISH_US,
            ...         header=Temp.TextValue(value='15'),
            ...         body=[
            ...             Temp.TextValue(value='Abdelhak Zaaim'),
            ...             Temp.TextValue(value='WA_IPHONE_15'),
            ...             Temp.TextValue(value='15%'),
            ...         ],
            ...         buttons=[
            ...             Temp.UrlButtonValue(value='iphone15'),
            ...             Temp.QuickReplyButtonData(data='unsubscribe_from_marketing_messages'),
            ...             Temp.QuickReplyButtonData(data='unsubscribe_from_all_messages'),
            ...         ],
            ...     ),
            ... )

        Example for Authentication Template:

            >>> from whatsbyapi.types import Template as Temp
            >>> msg.reply_template(
            ...     template=Temp(
            ...         name='auth_with_otp',
            ...         language=Temp.Language.ENGLISH_US,
            ...         buttons=Temp.OTPButtonCode(code='123456'),
            ...     ),
            ...     quote=True
            ... )

        Args:
            template: The template to send.
            quote: Whether to quote the replied message (default: False).

        Returns:
            The ID of the sent reply.

        Raises:

        """
        return self._client.send_template(
            to=self.sender,
            template=template,
            reply_to_message_id=quote if quote else None,
        )

    def mark_as_read(self) -> bool:
        """
        Mark the message as read.
            - Shortcut for :py:func:`~whatsbyapi.client.WhatsApp.mark_message_as_read` with ``message_id``.

        Returns:
            Whether it was successful.
        """
        return self._client.mark_message_as_read(message_id=self.message_id_to_reply)
