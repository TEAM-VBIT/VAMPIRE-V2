# Copyright (c) 2025 TheHamkerAlone
# Licensed under the MIT License.
# This file is part of AloneXMusic


import random

from pyrogram import types
from pyrogram.enums import ButtonStyle

from AloneX import app, config, lang
from AloneX.core.lang import lang_codes


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton
        self.styles = [ButtonStyle.PRIMARY, ButtonStyle.DANGER, ButtonStyle.SUCCESS]

    def _get_style(self):
        return random.choice(self.styles)

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=text,
                        callback_data=f"cancel_dl",
                        style=ButtonStyle.DANGER,
                    )
                ]
            ]
        )

    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []

        # Priority: timer > status
        if timer:
            keyboard.append(
                [
                    self.ikb(
                        text=timer,
                        callback_data=f"controls status {chat_id}",
                        style=self._get_style(),
                        icon_custom_emoji_id=5204046146955153467,
                    )
                ]
            )
        elif status:
            keyboard.append(
                [
                    self.ikb(
                        text=status,
                        callback_data=f"controls status {chat_id}",
                        style=self._get_style(),
                    )
                ]
            )

        if not remove:
            keyboard.append(
                [
                    self.ikb(
                        text="",
                        callback_data=f"controls resume {chat_id}",
                        icon_custom_emoji_id=5348125953090403204,
                        style=self._get_style(),
                    ),
                    self.ikb(
                        text="",
                        callback_data=f"controls pause {chat_id}",
                        icon_custom_emoji_id=5359543311897998264,
                        style=self._get_style(),
                    ),
                    self.ikb(
                        text="",
                        callback_data=f"controls skip {chat_id}",
                        icon_custom_emoji_id=5368509223632118184,
                        style=self._get_style(),
                    ),
                    self.ikb(
                        text="",
                        callback_data=f"controls stop {chat_id}",
                        icon_custom_emoji_id=5240241223632954241,
                        style=self._get_style(),
                    ),
                ]
            )
            keyboard.append(
                [
                    self.ikb(
                        text="⪻ -𝟸𝟶s",
                        callback_data=f"controls seek_back {chat_id}",
                        style=self._get_style(),
                    ),
                    self.ikb(
                        text="",
                        callback_data=f"controls replay {chat_id}",
                        icon_custom_emoji_id=5386367538735104399,
                        style=self._get_style(),
                    ),
                    self.ikb(
                        text="+𝟸𝟶s ⪼",
                        callback_data=f"controls seek_forward {chat_id}",
                        style=self._get_style(),
                    ),
                ]
            )
            keyboard.append(
                [
                    self.ikb(
                        text="𝐀ᴅᴅ 𝐌є",
                        url=f"https://t.me/{app.username}?startgroup=true",
                        icon_custom_emoji_id=5395476176527447827,
                        style=self._get_style(),
                    ),
                    self.ikb(
                        text="𝐔ᴘᴅᴧᴛєs",
                        url=config.SUPPORT_CHANNEL,
                        icon_custom_emoji_id=5438600169325095982,
                        style=self._get_style(),
                    ),
                ]
            )

        return self.ikm(keyboard)

    def help_markup(
        self, _lang: dict, back: bool = False
    ) -> types.InlineKeyboardMarkup:
        if back:
            rows = [
                [
                    self.ikb(text=_lang["back"], callback_data="help back"),
                    self.ikb(text=_lang["close"], callback_data="help close"),
                ]
            ]
        else:
            cbs = ["admins", "auth", "blist", "lang", "ping", "play", "queue", "stats", "sudo"]
            buttons = [
                self.ikb(text=_lang[f"help_{i}"], callback_data=f"help {cb}")
                for i, cb in enumerate(cbs)
            ]
            rows = [buttons[i : i + 3] for i in range(0, len(buttons), 3)]

        return self.ikm(rows)

    def lang_markup(self, _lang: str) -> types.InlineKeyboardMarkup:
        langs = lang.get_languages()

        buttons = [
            self.ikb(
                text=f"{name} ({code}) {'✔️' if code == _lang else ''}",
                callback_data=f"lang_change {code}",
                style=ButtonStyle.PRIMARY,
            )
            for code, name in langs.items()
        ]

        rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        return self.ikm(rows)

    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=text, url=config.SUPPORT_CHAT, style=ButtonStyle.SUCCESS
                    )
                ]
            ]
        )

    def play_queued(
        self, chat_id: int, item_id: str, _text: str
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=_text,
                        callback_data=f"controls force {chat_id} {item_id}",
                        style=self._get_style(),
                    )
                ]
            ]
        )

    def queue_markup(
        self, chat_id: int, _text: str, playing: bool
    ) -> types.InlineKeyboardMarkup:
        _action = "pause" if playing else "resume"
        return self.ikm(
            [
                [
                    self.ikb(
                        text=_text,
                        callback_data=f"controls {_action} {chat_id} q",
                        style=ButtonStyle.PRIMARY,
                    )
                ]
            ]
        )

    def settings_markup(
        self,
        lang: dict,
        admin_only: bool,
        language: str,
        chat_id: int,
        autoplay: bool = False,
    ) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text=lang["play_mode"] + " ➜",
                        callback_data=f"controls status {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text=admin_only,
                        callback_data="playmode",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
                [
                    self.ikb(
                        text="𝐀ᴜᴛᴏ 𝐏ʟᴀʏ ➜",
                        callback_data=f"controls status {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text=lang["enabled"] if autoplay else lang["disabled"],
                        callback_data=f"autoplay_setting {not autoplay}",
                        style=ButtonStyle.SUCCESS if autoplay else ButtonStyle.DANGER,
                    ),
                ],
                [
                    self.ikb(
                        text=lang["language"] + " ➜",
                        callback_data=f"controls status {chat_id}",
                        style=ButtonStyle.PRIMARY,
                    ),
                    self.ikb(
                        text=lang_codes[language],
                        callback_data="language",
                        style=ButtonStyle.PRIMARY,
                    ),
                ],
            ]
        )

    def close_markup(self) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(
                        text="⌯ 𝐂ʟσsє ⌯",
                        callback_data="help close",
                        style=ButtonStyle.DANGER,
                    )
                ]
            ]
        )

    def autoplay_markup(self, status: bool, lang: dict) -> types.InlineKeyboardMarkup:
        text = lang["enabled"] if status else lang["disabled"]
        style = ButtonStyle.SUCCESS if status else ButtonStyle.DANGER
        return self.ikm(
            [
                [
                    self.ikb(
                        text=text,
                        callback_data=f"autoplay {not status}",
                        style=style,
                    )
                ],
                [
                    self.ikb(
                        text=lang["close"],
                        callback_data="help close",
                        style=ButtonStyle.DANGER,
                    )
                ],
            ]
        )

    def start_key(
        self, lang: dict, private: bool = False
    ) -> types.InlineKeyboardMarkup:
        rows = [
            [
                self.ikb(
                    text=lang["add_me"],
                    url=f"https://t.me/{app.username}?startgroup=true",
                )
            ],
            [self.ikb(text=lang["help"], callback_data="help")],
            [
                self.ikb(text=lang["support"], url=config.SUPPORT_CHAT),
                self.ikb(text=lang["channel"], url=config.SUPPORT_CHANNEL),
            ],
        ]
        if private:
            rows += [
                [
                    self.ikb(text=lang["aloneowner"], user_id=config.OWNER_ID),
                    self.ikb(
                        text=lang["source"],
                        url="https://github.com/TeamAloneOp/AloneX",
                    )
                ]
            ]
        else:
            rows += [[self.ikb(text=lang["language"], callback_data="language")]]
        return self.ikm(rows)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm(
            [
                [
                    self.ikb(text="Copy Link", copy_text=link, style=ButtonStyle.PRIMARY),
                    self.ikb(text="Open in YouTube", url=link, style=ButtonStyle.PRIMARY),
                ],
            ]
        )
