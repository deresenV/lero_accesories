from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def site_info_keyboard(site_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="История", callback_data=f"history_site:{site_id}"),
                InlineKeyboardButton(text="Статистика", callback_data=f"site_stats:{site_id}")
            ],
            [
                InlineKeyboardButton(text="Редактировать", callback_data=f"edit_site:{site_id}"),
                InlineKeyboardButton(text="Удалить", callback_data=f"delete_site:{site_id}")
            ],
            [InlineKeyboardButton(text="Назад", callback_data="back_to_my_sites")]
        ]
    )
    return keyboard


def edit_site_keyboard(site_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Редактировать URL", callback_data=f"edit_site_url:{site_id}")],
            [InlineKeyboardButton(text="Редактировать интервал", callback_data=f"edit_site_interval:{site_id}")],
            [InlineKeyboardButton(text="Назад", callback_data=f"site:{site_id}")]
        ]
    )
    return keyboard

def remove_site_keyboard(site_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Удалить", callback_data=f"delete_site_succesful:{site_id}")],
            [InlineKeyboardButton(text="Отмена", callback_data=f"site:{site_id}")]
        ]
    )
    return keyboard

def history_keyboard(site_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data=f"site:{site_id}")
            ],
            [
                InlineKeyboardButton(text="Скачать полный лог", callback_data=f"download_log:{site_id}")
            ]
        ]
    )
    return keyboard

def back_statistic_keyboard(site_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data=f"site:{site_id}")]
        ]
    )
    return keyboard