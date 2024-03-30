import time
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from handlers.states import States


router = Router()


ANS_FIND__BY_ID   = "По ID"
ANS_FIND__BY_NAME = "По названию"
ANS_FIND__BY_TAGS = "По тегам"


by_id_btn   = KeyboardButton(text=ANS_FIND__BY_ID)
by_name_btn = KeyboardButton(text=ANS_FIND__BY_NAME)
by_tags_btn = KeyboardButton(text=ANS_FIND__BY_TAGS)



@router.message(Command("find"))
async def find__start(message: Message, state: FSMContext):
    await state.set_state(States.find)
    await message.answer(
        "Готов найти ресурс любым возможным способом!\n",
        reply_markup=ReplyKeyboardMarkup(keyboard=[
            [ by_id_btn ],
            [ by_name_btn ],
            [ by_tags_btn ],
        ])
    )



@router.message(States.find, F.text == ANS_FIND__BY_ID)
async def find__by_id(message: Message, state: FSMContext):
    await state.set_state(States.find__wait_id)
    await message.answer(
        "Введите id ресурса:\n",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(States.find__wait_id)
async def find__enter_id(message: Message, state: FSMContext):
    assert message.text
    if not message.text.isdigit():
        return await message.reply(
            "К сожалению, это не похоже на ID ресурса :(\n"
            "Попробуйте ещё раз или используйте команду /cancel"
        )
    
    await state.set_state(default_state)
    res_id = int(message.text)
    await message.answer(
        f"Выполняю поиск по id={res_id}...",
        reply_markup=ReplyKeyboardRemove()
    )
    time.sleep(1)
    await message.reply("*Делаю вид, что что-то нашёл*")



@router.message(States.find, F.text == ANS_FIND__BY_NAME)
async def find__by_name(message: Message, state: FSMContext):
    await state.set_state(States.find__wait_name)
    await message.answer(
        "Введите название ресурса или его часть:\n",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(States.find__wait_name)
async def find__enter_name(message: Message, state: FSMContext):
    assert message.text
    await state.set_state(default_state)
    res_name = message.text
    await message.answer(
        f"Выполняю поиск по имени \'{res_name}\'...",
        reply_markup=ReplyKeyboardRemove(),
    )
    time.sleep(1)
    await message.answer("*Делаю вид, что что-то нашёл*")



@router.message(States.find, F.text == ANS_FIND__BY_TAGS)
async def find__by_tags(message: Message, state: FSMContext):
    await state.set_state(States.find__wait_tags)
    await message.answer(
        "Введите #теги через пробел:\n",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(States.find__wait_tags)
async def find__enter_tags(message: Message, state: FSMContext):
    assert message.text
    res_tags = message.text.split()
    for tag in res_tags:
        if not tag.startswith("#"):
            return await message.reply(
                f"\"{tag}\" не похоже на тег :( Попробуйте ещё раз"
            )
    await state.set_state(default_state)
    await message.reply(
        f"Выполняю поиск по тегам: " + \
        ", ".join([f"{tag}" for tag in res_tags]),
        reply_markup=ReplyKeyboardRemove(),
    )
    time.sleep(1)
    await message.reply("*Делаю вид, что что-то нашёл*")



@router.message(States.find)
async def find__unknown(message: Message, state: FSMContext):
    await message.answer(
        "Я не понимаю Вас :( Попробуйте ещё раз",
    )
