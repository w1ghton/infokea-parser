from aiogram.utils.keyboard import InlineKeyboardBuilder
from .parser import parse

template = [
    {"school_class": "5", "tasks": []},
    {"school_class": "7", "tasks": []},
    {"school_class": "8", "tasks": []},
    {"school_class": "9", "tasks": []},
    {"school_class": "10", "tasks": []},
    {"school_class": "11", "tasks": []},
]


async def classes() -> KeyboardInterrupt:
    keyboard = InlineKeyboardBuilder()
    for i in template:
        keyboard.button(text=i["school_class"], callback_data=i["school_class"])
    return keyboard.adjust(3).as_markup()


async def tasks(school_class: str) -> KeyboardInterrupt:
    keyboard = InlineKeyboardBuilder()
    parsed_data = parse()
    for i in parsed_data:
        if i["school_class"] == school_class:
            for j in i["tasks"]:
                keyboard.button(text=j["name"], url=j["url"])
    keyboard.button(text="🔙Назад", callback_data="back")
    keyboard.button(text="🔄Обновить", callback_data="update")
    return keyboard.adjust(2).as_markup()
