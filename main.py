from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# Токен вашего бота
BOT_TOKEN = '7915298434:AAGif53T03tKt3nfvpHlCDBrTs-EkK_-p4U'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
#описание сервисов
details = (
    'Здесь вы найдете:\n\n'
    'Тесты/Билеты - Здесь вы можете пройти тесты DMV и попрактиковаться на билетах, '
    'чтобы подготовиться к настоящему экзамену.\n\n'
    'Знаки - В этом разделе вы можете изучить дорожные знаки, '
    'вопросы по знакам обязательно будут в вашем экзамене.\n\n'
    'ПДД - Здесь вы найдете полное руководство по правилам дорожного движения, '
    'организованное по разделам и подразделам.\n\n'
    'Экзамен - В этом разделе вам предстоит ответить на 40 вопросов за 45 минут, '
    'что имитирует реальный тест DMV.'
)

# Кнопки для выбора языка
language_button_eng = InlineKeyboardButton(text='English 🇺🇸️', callback_data='lang_eng')
language_button_rus = InlineKeyboardButton(text='Russian 🇷🇺️', callback_data='lang_rus')
language_button_esp = InlineKeyboardButton(text='Spanish 🇪🇸', callback_data='lang_esp')

# Клавиатура для выбора языка
language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[language_button_eng], [language_button_rus], [language_button_esp]])

# Кнопки для выбора штата
state_buttons = [
    InlineKeyboardButton(text='California ☀️', callback_data='state_california'),
    InlineKeyboardButton(text='Washington 🌲', callback_data='state_washington'),
    InlineKeyboardButton(text='Florida 🌴', callback_data='state_florida'),
    InlineKeyboardButton(text='New York 🗽', callback_data='state_new_york')  # Изменено на 'New York'
]

# Клавиатура для выбора штата
state_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button] for button in state_buttons])

# Кнопки для тестов после выбора штата
service_buttons = [
    InlineKeyboardButton(text='Тесты / билеты', callback_data='test_1'),
    InlineKeyboardButton(text='ПДД', callback_data='test_2'),
    InlineKeyboardButton(text='Знаки', callback_data='test_3'),
    InlineKeyboardButton(text='Экзамен', callback_data='test_4')
]
# Клавиатура для тестов
service_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button] for button in service_buttons])


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='.            Choose language:          .', reply_markup=language_keyboard)


# Хэндлер для обработки выбора языка
@dp.callback_query(lambda callback: callback.data.startswith('lang_'))
async def handle_language_selection(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text='.            Choose state 🇺🇸️:          .', reply_markup=state_keyboard)


# Хэндлер для обработки выбора штата
@dp.callback_query(lambda callback: callback.data.startswith('state_'))
async def handle_state_selection(callback: types.CallbackQuery):
    await callback.answer()
    state_name = callback.data.split('_')[1].replace("New-York", "New York").replace("-", " ").capitalize()  # Извлекаем название штата


    # Проверяем, выбран ли штат
    if state_name == 'California':
        await callback.message.edit_text(
            text=f'Вы выбрали штат California! {details}',
            reply_markup=service_keyboard
        )
    elif state_name == 'Washington':
        await callback.message.edit_text(
            text=f'Вы выбрали штат Washington! {details}',
            reply_markup=service_keyboard
        )
    elif state_name == 'Florida':
        await callback.message.edit_text(
            text=f'Вы выбрали штат Florida! {details}',
            reply_markup=service_keyboard
        )
    elif state_name == 'New York':  # Изменено на 'New York'
        await callback.message.edit_text(
            text=f'Вы выбрали штат New York! {details}',  # Изменено на 'New York'
            reply_markup=service_keyboard
        )

# Хэндлер для обработки выбора сервиса
@dp.callback_query(lambda callback: callback.data.startswith('test_'))
async def handle_service_selection(callback: types.CallbackQuery):
    await callback.answer()
    service_name = callback.data.split('_')[1].capitalize()  # Извлекаем название сервиса
    await callback.message.edit_text(text=f'Вы выбрали сервис номер {service_name}.', reply_markup=None)


# Запускаем бота
if __name__ == '__main__':
    dp.run_polling(bot)
