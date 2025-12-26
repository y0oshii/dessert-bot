import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart

# TOKEN хранится в config.py (не добавляется в репозиторий)
from config import TOKEN
from recipes import recipes

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_start_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text="🍫 Шоколадное", callback_data="category_шоколадное")],
        [InlineKeyboardButton(text="🍪 Печенье", callback_data="category_печенье")],
        [InlineKeyboardButton(text="🍓 Фрукты", callback_data="category_фрукты")],
        [InlineKeyboardButton(text="☕ Напитки", callback_data="category_напитки")]
    ]
)

def get_recipes_menu(category):
    filtered = [r for r in recipes if category.lower() in [t.lower() for t in r["tags"]]]
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=r["name"], callback_data=f"recipe_{i}")] for i, r in enumerate(filtered)
        ]
    )
    keyboard.inline_keyboard.append(
        [InlineKeyboardButton(text="🔙 Назад к категориям", callback_data="back_to_categories")]
    )
    return keyboard, filtered

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("🍰 Привет! Выбери категорию десерта:", reply_markup=get_start_menu())

@dp.callback_query()
async def handle_callback(callback: CallbackQuery):
    data = callback.data

    if data.startswith("category_"):
        category = data.split("_")[1]
        keyboard, filtered = get_recipes_menu(category)
        await callback.message.edit_text(f"Выберите рецепт из категории {category}:", reply_markup=keyboard)

    elif data == "back_to_categories":
        await callback.message.edit_text("Выбери категорию десерта:", reply_markup=get_start_menu())

    elif data.startswith("recipe_"):
        index = int(data.split("_")[1])
        recipe = recipes[index]
        recipe_text = (
            f"🍫 <b>{recipe['name']}</b>\n"
            f"⏱ {recipe['time']}\n\n"
            "<b>Ингредиенты:</b>\n" +
            "\n".join(recipe["ingredients"]) +
            "\n\n<b>Как готовить:</b>\n" +
            "\n".join(f"{i+1}. {step}" for i, step in enumerate(recipe["steps"]))
        )
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="🔙 Назад к десертам", callback_data="back_to_categories")]
            ]
        )
        await callback.message.edit_text(recipe_text, parse_mode="HTML", reply_markup=keyboard)

async def main():
    import logging
    logging.basicConfig(level=logging.INFO)
    print("Бот запускается…")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())