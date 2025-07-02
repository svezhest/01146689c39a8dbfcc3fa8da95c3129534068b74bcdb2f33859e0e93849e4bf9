from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from keyboards.default import get_menu_keyboard
from loader import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"🤖 Привет, {hbold(message.from_user.full_name)}! \n\n🤝 Я - Степай Ипотечный! Я бот, который поможет тебе отслеживать настроения инвесторов для акций, торгующихся на Московской бирже!\n\n❕ Обрати внимание, что выдача бота не является инвестиционной рекомендацией.\nМы не претендуем на точность оценки или полноту покрытия.", reply_markup=(await get_menu_keyboard()))

@dp.message(Command("help"))
async def command_help_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f'ℹ️ Список доступных команд ℹ️\n\n/start - Запустить бота\n/help - Вывести список доступных команд\n/analyze - Проанализировать каналы\n/get - Список компаний', reply_markup=(await get_menu_keyboard()))

@dp.message(Command("get"))
async def command_get_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(f"📋 Список компаний, по которым нам удалось проанализировать настроения за сегодняшний день: (фича в разработке)", reply_markup=(await get_menu_keyboard()))

@dp.message(Command("analyze"))
async def command_analyze_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'✍️ Введите ссылки на каналы, которые хотите проанализировать (каналы должны быть публичными):')
    