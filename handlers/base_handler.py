from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove


router = Router()


@router.message(Command("start"))
async def start(message: Message):
    """
    Приветственное сообщение и краткая справка по командам
    """
    await message.answer(
        "Тебя приветствует Аполлон!\n"
        "Я создан для того, чтобы упростить структурирование всей полезной информации в рамках обучения!\n"
        "Что я умею?\n"
        "/help - полный список команд;\n"
        "/load - загрузить в себя ресурс;\n"
        "/find - выполнить поиск;\n"
        "/cancel - отменить текущую операцию.\n"
        "По всем вопросам, связанным со мной, обращайтесь к моему создателю, @zhikhkirill.\n"
    )


@router.message(Command("help"))
async def help(message: Message):
    """
    Справка по командам
    """
    await message.answer(
        "Список команд:\n"
        "/help - список команд;\n"
        "/load - загружать в себя ресурс;\n"
        "/find - выполнять поиск;\n"
        "/cancel - отменить текущую операцию.\n"
    )


@router.message(Command("cancel"))
@router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    В любой момент времени пользователь может отменить текущее действие
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Отменено",
        reply_markup=ReplyKeyboardRemove(),
    )
