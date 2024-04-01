import time
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

import constants
from handlers.states import States
from repository import Repository
from utils.validators import validate_url


router = Router()
repo = Repository()

ANS_LOAD__URL = "Ссылку на ресурс"
ANS_LOAD__FILE = "Файл"

btn_url = KeyboardButton(text=ANS_LOAD__URL)
btn_file = KeyboardButton(text=ANS_LOAD__FILE)


@router.message(Command("load"))
async def load__start(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Загрузить ресурс в систему «Аполлон»\n"
        "_В любой момент введите команду /cancel для отмены_\n",
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardRemove(),
    )
    return await __load__prompt_type(message, state)


async def __load__prompt_type(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Что Вы собираетесь загрузить?\n",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [ btn_url ],
            [ btn_file ],
        ])
    )
    return await state.set_state(States.load__enter_type)


@router.message(States.load__enter_type)
async def load__enter_type(message: Message, state: FSMContext) -> None:
    assert message.text
    if message.text == ANS_LOAD__URL:
        await state.update_data({ "load__type": "url" })
        return await __load__prompt_url(message, state)
    if message.text == ANS_LOAD__FILE:
        await state.update_data({ "load__type": "file" })
        return await __load__prompt_file(message, state)
    await message.reply(
        "К сожалению, я не понимаю Вас :(\n"
        "Попробуйте ещё раз\n"
    )


async def __load__prompt_url(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Введите URL ресурса:\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    return await state.set_state(States.load__enter_url)


@router.message(States.load__enter_url)
async def load__enter_url(message: Message, state: FSMContext) -> None:
    assert message.text
    if not validate_url(message.text):
        await message.reply(
            "К сожалению, это не похоже на URL ресурса :(\n"
            "Попробуйте ещё раз:\n",
            reply_markup=ReplyKeyboardRemove(),
        )
        return
    await state.update_data({ "load__url": message.text })
    return await __load__prompt_name(message, state)


async def __load__prompt_file(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Отправьте ровно один файл\n"
        "Если файлов несколько, используйте архивирование (.zip)\n",
        reply_markup=ReplyKeyboardRemove()
    )
    return await state.set_state(States.load__enter_file)


@router.message(States.load__enter_file)
async def load__enter_file(message: Message, state: FSMContext) -> None:
    if not message.document:
        await message.answer(
            "К сожалению, это не файл :(\n"
            "Попробуйте ещё раз\n",
            reply_markup=ReplyKeyboardRemove(),
        )
        return
    assert message.document.file_name
    await repo.tgbot.download(message.document, "./resources/"+message.document.file_name)
    await state.update_data({ "load__filename": message.document.file_name })
    await message.reply(
        "Файл успешно загружен!\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    return await __load__prompt_name(message, state)


async def load__wait_url(message: Message, state: FSMContext):
    await message.answer(
        "Введите url ресурса:\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(States.load__enter_url)


async def __load__prompt_name(message: Message, state: FSMContext):
    await message.answer(
        "Введите уникальное имя ресурса:\n\n"
        "_Название должно отражать содержимое ресурса и отличать его от "
        "других_\n"
        "_Хороший пример: ИУ Линал РК 1 Теория_\n"
        "_Плохой пример: ~РК1~_\n",
        parse_mode="MarkdownV2",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(States.load__enter_name)


@router.message(States.load__enter_name)
async def load__enter_name(message: Message, state: FSMContext):
    assert message.text
    res_name = message.text
    if len(res_name) < constants.MIN_RESOURCE_NAME_LENGTH:
        return await message.reply(
            "Мне кажется, или имя слишком короткое?\n"
            "Попробуйте ещё раз\n",
            reply_markup=ReplyKeyboardRemove(),
        )
    await state.update_data({"load__name": res_name})
    await load__wait_description(message, state)


async def load__wait_description(message: Message, state: FSMContext):
    await message.answer(
        "Хорошо, а теперь опишите ресурс или пропустите командой /continue\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(States.load__enter_description)


@router.message(Command("continue"), States.load__enter_description)
async def load__skip_description(message: Message, state: FSMContext):
    await __load__prompt_tags(message, state)


@router.message(States.load__enter_description)
async def load__enter_description(message: Message, state: FSMContext):
    assert message.text
    res_desc = message.text
    await state.update_data({"load__description": res_desc})
    await __load__prompt_tags(message, state)


async def __load__prompt_tags(message: Message, state: FSMContext):
    await message.answer(
        "Последнее: введите #теги черех пробел, по которым другие студенты "
        "могли бы найти ресурс:\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(States.load__enter_tags)


@router.message(States.load__enter_tags)
async def load__enter_tags(message: Message, state: FSMContext):
    assert message.text
    res_tags = message.text.split()
    for tag in res_tags:
        if not tag.startswith("#"):
            return await message.reply(
                f"\"{tag}\" не похоже на тег :( Попробуйте ещё раз\n"
            )
    await state.update_data({"load__tags": res_tags})
    await __load__process(message, state)

async def __load__process(message: Message, state: FSMContext):
    data = await state.get_data()

    msg = "Подтвердить загрузку?\n"

    if data["load__type"] == "url":
        url = data["load__url"]
        msg += f"URL: {url}\n"
    elif data["load__type"] == "file":
        filename = data["load__filename"]
        msg += f"Файл: {filename}\n"
    name = data["load__name"]
    description = data["load__description"]
    tags = data.get("load__tags", "")

    msg += f"Название: {name}\nОписание: {description}\nТеги: {tags}\n"

    await message.answer(msg)
    await state.clear()
