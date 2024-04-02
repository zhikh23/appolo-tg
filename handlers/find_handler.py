import time
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from handlers.states import States


router = Router()


ANS_FIND__BY_ID = "По ID"
ANS_FIND__BY_NAME = "По названию"
ANS_FIND__BY_TAGS = "По тегам"

ANS_YES = "Да"
ANS_NO = "Нет"


by_id_btn = KeyboardButton(text=ANS_FIND__BY_ID)
by_name_btn = KeyboardButton(text=ANS_FIND__BY_NAME)
by_tags_btn = KeyboardButton(text=ANS_FIND__BY_TAGS)
yes_btn = KeyboardButton(text=ANS_YES)
no_btn = KeyboardButton(text=ANS_NO)


@router.message(Command("find"))
async def find__start(message: Message, state: FSMContext):
    await message.answer(
        "Готов найти ресурс любым возможным способом!\n",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [by_id_btn],
            [by_name_btn],
            [by_tags_btn],
        ])
    )
    await state.set_state(States.find__start)


# ID ==========================================================================
@router.message(States.find__start, F.text == ANS_FIND__BY_ID)
async def find__by_id(message: Message, state: FSMContext):
    await message.answer(
        "Введите id ресурса:\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(States.find__enter_id)


@router.message(States.find__enter_id)
async def find__enter_id(message: Message, state: FSMContext):
    assert message.text
    if not message.text.isdigit():
        return await message.reply(
            "К сожалению, это не похоже на ID ресурса :(\n"
            "Попробуйте ещё раз или используйте команду /cancel"
        )
    res_id = int(message.text)
    await state.update_data({"find__id": res_id})
    await find__process(message, state)
# =============================================================================


# NAME ========================================================================
@router.message(States.find__start, F.text == ANS_FIND__BY_NAME)
async def find__by_name(message: Message, state: FSMContext):
    await message.answer(
        "Введите название ресурса или его часть:\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(States.find__enter_name)


@router.message(States.find__enter_name)
async def find__enter_name(message: Message, state: FSMContext):
    assert message.text
    res_name = message.text
    await state.update_data({"find__name": res_name})
    await find__process(message, state)
# =============================================================================


# TAGS ========================================================================
@router.message(States.find__start, F.text == ANS_FIND__BY_TAGS)
async def find__by_tags(message: Message, state: FSMContext):
    await message.answer(
        "Введите #теги через пробел:\n",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(States.find__enter_tags)


@router.message(States.find__enter_tags)
async def find__enter_tags(message: Message, state: FSMContext):
    assert message.text
    tags = message.text.split()
    for tag in tags:
        if not tag.startswith("#"):
            return await message.reply(
                f"\"{tag}\" не похоже на тег :( Попробуйте ещё раз"
            )
    res_tags = list(map(lambda s: s.removeprefix("#"), tags))
    await state.update_data({"find__tags": res_tags})
    await find__process(message, state)
# =============================================================================


async def find__process(message: Message, state: FSMContext):
    data = await state.get_data()
    res_id: int = data.get("find__id", None)
    res_name: str = data.get("find__name", None)
    res_tags: list[str] = data.get("find__tags", [])

    reply_text = "Выполняю поиск по:\n"
    if res_id:
        reply_text += f"ID: {res_id}\n"
    if res_name:
        reply_text += f"Имени: {res_name}\n"
    if res_tags:
        res_tags_text = ", ".join(res_tags) + "\n"
        reply_text += f"Тегам: {res_tags_text}"

    await message.reply(
        reply_text,
        reply_markup=ReplyKeyboardRemove(),
    )

    time.sleep(1)

    await message.reply("*Делаю вид, что что-то нашёл*")
    await state.clear()


@router.message(States.find__start)
async def find__unknown(message: Message, state: FSMContext):
    await message.answer(
        "Я не понимаю Вас :( Попробуйте ещё раз",
    )
