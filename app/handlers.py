from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from .keyboards import classes, tasks

router = Router()
user_class = []


@router.message(CommandStart)
async def cmd_start(message: Message) -> None:
    """
    Первичный выбор класса
    """
    user_class.append({"id": message.from_user.id, "class": str})
    await message.reply("Выберите класс:", reply_markup=await classes())


@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery) -> None:
    """
    Возврат в меню выбора класса
    """
    await callback.answer()
    await callback.message.edit_text("Выберите класс:", reply_markup=await classes())


@router.callback_query(F.data == "update")
async def update(callback: CallbackQuery) -> None:
    """
    Обновление заданий
    """
    for i in user_class:
        if i["id"] == callback.from_user.id:
            current_user_class = i["class"]
    try:
        await callback.message.edit_text(
            "Задания для %s класса" % current_user_class,
            reply_markup=await tasks(current_user_class),
        )
        await callback.answer("Задания обновлены.")
    except Exception:
        await callback.answer("Обновлений не найдено.")


@router.callback_query(F.data)
async def get_tasks(callback: CallbackQuery) -> None:
    """
    Отображение заданий для данного класса
    """
    await callback.answer()
    for i in user_class:
        if i["id"] == callback.from_user.id:
            i["class"] = callback.data
    try:
        await callback.message.edit_text(
            "Задания для %s класса" % callback.data,
            reply_markup=await tasks(callback.data),
        )
    except Exception:
        print("Ошибка")
