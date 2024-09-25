from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# Токен вашего бота
BOT_TOKEN = '7915298434:AAGif53T03tKt3nfvpHlCDBrTs-EkK_-p4U'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Кнопки для выбора языка
language_button_eng = InlineKeyboardButton(text='English 🇺🇸️', callback_data='lang_eng')
language_button_rus = InlineKeyboardButton(text='Russian 🇷🇺️', callback_data='lang_rus')
language_button_esp = InlineKeyboardButton(text='Spanish 🇪🇸', callback_data='lang_esp')

# Клавиатура для выбора языка
language_keyboard = InlineKeyboardMarkup(inline_keyboard=[[language_button_eng], [language_button_rus], [language_button_esp]])


# Кнопки для выбора штата
state_buttons = [
    InlineKeyboardButton(text='California', callback_data='state_california'),
    InlineKeyboardButton(text='Washington', callback_data='state_washington'),
    InlineKeyboardButton(text='Florida', callback_data='state_florida'),
    InlineKeyboardButton(text='New York', callback_data='state_new_york')
]
# Клавиатура для выбора штата
state_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button] for button in state_buttons])

# Кнопки для тестов после выбора штата California
service_buttons = [
    InlineKeyboardButton(text='Тест 1', callback_data='test_1'),
    InlineKeyboardButton(text='Тест 2', callback_data='test_2'),
    InlineKeyboardButton(text='Тест 3', callback_data='test_3'),
    InlineKeyboardButton(text='Тест 4', callback_data='test_4')
]
# Клавиатура для тестов
service_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button] for button in service_buttons])

# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='.            Choose language:          .', reply_markup=language_keyboard)


# Хэндлер для обработки выбора языка
@dp.callback_query()
async def handle_language_selection(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text='.            Choose state 🇺🇸️:          .', reply_markup=state_keyboard)

# Хэндлер для обработки выбора сервиса
@dp.callback_query()
async def handle_service_selection(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text='.            Choose service :          .', reply_markup=service_keyboard)


# Запускаем бота
if __name__ == '__main__':
    dp.run_polling(bot)
