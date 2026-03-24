from question import BIG_QUIZ_POOL


# В коде измени выбор количества вопросов на 10:
# sample_size = min(len(all_questions), 10)
sample_size = 10 # Бот выберет 10 случайных из списка
import asyncio
import random
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- SOZLAMALAR (TOKENNI KIRITING) ---
TOKEN = '8741088390:AAGxE-9NQjxYQbDRsvfeDnKgy7xpuwS7m_A'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- SAVOLLAR BAZASI (O'zbek tilida) ---
BIG_QUIZ_POOL = {
    "1-4 sinflar (Boshlang'ich)": [
        {"q": "Olmaning rangi qanday? (Red/Blue)", "a": "red"},
        {"q": "Mushukning nechta oyog'i bor?", "a": "4"},
        {"q": "Ingliz tilida 'Salom' nima bo'ladi?", "a": "hello"},
        {"q": "I ___ a student. (am/is/are)", "a": "am"},
        {"q": "Quyoshning rangi qanday? (Yellow/Green)", "a": "yellow"},
        # Shu kabi yana 15-100 ta savol qo'shishingiz mumkin
    ],
    "5-9 sinflar (O'rta)": [
        {"q": "'Go' fe'lining o'tgan zamon shakli (Past Simple)?", "a": "went"},
        {"q": "Samolyot boshqaradigan odam kim?", "a": "pilot"},
        {"q": "Ingliz tilida 'Sayohat' nima bo'ladi?", "a": "travel"},
        {"q": "She ___ (work/works) every day.", "a": "works"},
        {"q": "London qaysi davlatning poytaxti?", "a": "uk"},
    ],
    "10-11 sinflar va Kattalar": [
        {"q": "If I ___ (be) you, I would go.", "a": "were"},
        {"q": "Kompaniya rahbari inglizcha qisqartmasi?", "a": "ceo"},
        {"q": "'Mas'uliyat' so'zining inglizcha tarjimasi?", "a": "responsibility"},
        {"q": "'Piece of cake' iborasi nima degani? (Oson/Qiyin)", "a": "oson"},
        {"q": "By the time he came, the film ___ (finish).", "a": "had finished"},
    ]
}

user_sessions = {}


@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for level in BIG_QUIZ_POOL.keys():
        builder.button(text=level)
    await message.answer("Assalomu alaykum! Ingliz tili testi darajasini tanlang:",
                         reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(F.text.in_(BIG_QUIZ_POOL.keys()))
async def start_quiz(message: types.Message):
    level = message.text
    all_questions = BIG_QUIZ_POOL[level]
    sample_size = min(len(all_questions), 15)
    selected_questions = random.sample(all_questions, sample_size)

    user_sessions[message.from_user.id] = {"questions": selected_questions, "current_idx": 0}

    q = selected_questions[0]['q']
    await message.answer(f"Boshladik! 1/{sample_size}-savol:\n\n{q}",
                         reply_markup=types.ReplyKeyboardRemove())


@dp.message()
async def check_answer(message: types.Message):
    uid = message.from_user.id
    if uid not in user_sessions:
        return

    session = user_sessions[uid]
    current_q = session["questions"][session["current_idx"]]
    user_answer = message.text.lower().strip()
    correct_answer = current_q["a"].lower()

    if user_answer == correct_answer:
        await message.answer("To'g'ri topdingiz, balli! ✅")
        session["current_idx"] += 1

        if session["current_idx"] < len(session["questions"]):
            next_q = session["questions"][session["current_idx"]]["q"]
            await message.answer(f"{session['current_idx'] + 1}-savol:\n\n{next_q}")
        else:
            await message.answer("Tabriklaymiz! Siz barcha savollarga javob berdingiz! 🏆")
            del user_sessions[uid]
            # Menyuni qaytarish
            builder = ReplyKeyboardBuilder()
            for level in BIG_QUIZ_POOL.keys():
                builder.button(text=level)
            await message.answer("Yana urinib ko'rasizmi?", reply_markup=builder.as_markup(resize_keyboard=True))
    else:
        await message.answer("Voy, xato! Yana bir bor urinib ko'ring) ❌")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
