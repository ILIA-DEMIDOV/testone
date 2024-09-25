from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# Токен вашего бота
BOT_TOKEN = '7915298434:AAGif53T03tKt3nfvpHlCDBrTs-EkK_-p4U'  # Замените на свой токен

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Описание сервисов
details_rus = (
    '<b>Здесь вы найдете:</b>\n\n'
    '<b>Тесты/Билеты</b> - Здесь вы можете пройти тесты DMV и попрактиковаться на билетах, '
    'чтобы подготовиться к настоящему экзамену.\n\n'
    '<b>Знаки</b> - В этом разделе вы можете изучить дорожные знаки, '
    'вопросы по знакам обязательно будут в вашем экзамене.\n\n'
    '<b>ПДД</b> - Здесь вы найдете полное руководство по правилам дорожного движения, '
    'организованное по разделам и подразделам.\n\n'
    '<b>Экзамен</b> - В этом разделе вам предстоит ответить на 40 вопросов за 45 минут, '
    'что имитирует реальный тест DMV.'
)
details_eng = (
    '<b>Here you will find:</b>\n\n'
    '<b>Tests/Tickets</b> - Here you can take DMV tests and practice on tickets to prepare for the real exam.\n\n'
    '<b>Signs</b> - In this section, you can study traffic signs, as questions about signs will definitely be on your exam.\n\n'
    '<b>Traffic Rules</b> - Here you will find a complete guide to traffic rules, organized by sections and subsections.\n\n'
    '<b>Exam</b> - In this section, you will need to answer 40 questions in 45 minutes, simulating the real DMV test.'
)

# Кнопки для выбора языка
language_button_eng = InlineKeyboardButton(text='English 🇺🇸️', callback_data='lang_eng')
language_button_rus = InlineKeyboardButton(text='Russian 🇷🇺️', callback_data='lang_rus')

# Клавиатура для выбора языка
language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[language_button_eng], [language_button_rus]])

# Кнопки для выбора штата
state_buttons = [
    InlineKeyboardButton(text='California ☀️', callback_data='state_california'),
    InlineKeyboardButton(text='Washington 🌲', callback_data='state_washington'),
    InlineKeyboardButton(text='Florida 🌴', callback_data='state_florida'),
    InlineKeyboardButton(text='Chicago 🌆', callback_data='state_chicago')
]

# Клавиатура для выбора штата
state_keyboard = InlineKeyboardMarkup(inline_keyboard=[[button] for button in state_buttons])

# Клавиатура для тестов на русском
service_keyboard_rus = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Тесты / билеты', callback_data='test_1')],
    [InlineKeyboardButton(text='ПДД', callback_data='test_2')],
    [InlineKeyboardButton(text='Знаки', callback_data='test_3')],
    [InlineKeyboardButton(text='Экзамен', callback_data='test_4')]
])

# Клавиатура для тестов на английском
service_keyboard_eng = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Tests / Tickets', callback_data='test_1')],
    [InlineKeyboardButton(text='Traffic Rules', callback_data='test_2')],
    [InlineKeyboardButton(text='Signs', callback_data='test_3')],
    [InlineKeyboardButton(text='Exam', callback_data='test_4')]
])

# Переменная для хранения выбранного языка
lang_ = "Russian"


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text='.            Choose language:          .', reply_markup=language_keyboard)


# Хэндлер для обработки выбора языка
@dp.callback_query(lambda callback: callback.data.startswith('lang_'))
async def handle_language_selection(callback: types.CallbackQuery):
    global lang_
    lang_ = "English" if callback.data == 'lang_eng' else "Russian"
    await callback.answer()

    # Обновляем текст в зависимости от выбранного языка
    if lang_ == "Russian":
        await callback.message.edit_text(text='.            Выберите штат 🇷🇺️:          .',
                                         reply_markup=state_keyboard)
    else:
        await callback.message.edit_text(text='.            Choose state 🇺🇸️:          .',
                                         reply_markup=state_keyboard)


# Хэндлер для обработки выбора штата
@dp.callback_query(lambda callback: callback.data.startswith('state_'))
async def handle_state_selection(callback: types.CallbackQuery):
    await callback.answer()
    state_name = callback.data.split('_')[1].capitalize()  # Извлекаем название штата

    await send_state_details(callback, state_name)


async def send_state_details(callback, state_name):
    if lang_ == "Russian":
        await callback.message.edit_text(
            text=f'<b>Вы выбрали штат {state_name}!</b> {details_rus}',
            reply_markup=service_keyboard_rus,
            parse_mode='HTML'
        )
    else:
        await callback.message.edit_text(
            text=f'<b>You have chosen the state of {state_name}!</b> {details_eng}',
            reply_markup=service_keyboard_eng,
            parse_mode='HTML'
        )


# Хэндлер для обработки выбора сервиса
@dp.callback_query(lambda callback: callback.data.startswith('test_'))
async def handle_service_selection(callback: types.CallbackQuery):
    await callback.answer()
    service_name = callback.data.split('_')[1].capitalize()  # Извлекаем название сервиса

    if service_name == '1':  # Тесты / билеты
        if lang_ == "Russian":
            await callback.message.edit_text(
                text='<b>Тесты/Билеты</b> - Здесь вы можете пройти тесты DMV и попрактиковаться на билетах, чтобы подготовиться к настоящему экзамену.',
                reply_markup=None,
                parse_mode='HTML'
            )
        else:
            await callback.message.edit_text(
                text='<b>Tests/Tickets</b> - Here you can take DMV tests and practice on tickets to prepare for the real exam.',
                reply_markup=None,
                parse_mode='HTML'
            )
    else:
        await callback.message.edit_text(text=f'Вы выбрали сервис номер {service_name}.', reply_markup=None)


if __name__ == '__main__':
    dp.run_polling(bot)
