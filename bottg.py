import os
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from duckduckgo_search import DDGS

# 1. ТОКЕН: Встав сюди свій API Token від @BotFather

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

# Налаштування логів (Настройка логов для консоли PyCharm)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_image_url(query):
    """Пошук картинки (Поиск картинки в DuckDuckGo)"""
    try:
        with DDGS() as ddgs:
            # Перетворюємо результат у список (Превращаем в список)
            results = list(ddgs.images(query, max_results=10))
            if results:
                # Вибираємо рандомне фото (Выбираем рандомное фото)
                return random.choice(results)['image']
    except Exception as e:
        print(f"Error in search: {e}")
    return None


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробка повідомлень з '!' (Обработка команд с '!')"""
    message_text = update.message.text

    # Перевіряємо, чи починається текст з '!'
    if message_text and message_text.startswith('!'):
        query = message_text[1:].strip()

        if not query:
            return

        print(f"User requested: {query}")

        # Отримуємо URL картинки
        image_url = get_image_url(query)

        if image_url:
            try:
                # Відправляємо фото в Telegram
                await update.message.reply_photo(
                    photo=image_url,
                    caption=f"Result for: {query}"
                )
            except Exception as e:
                print(f"Send Error: {e}")
                await update.message.reply_text("Found it, but couldn't send the file. Try another word.")
        else:
            await update.message.reply_text(f"No images found for '{query}'.")


if __name__ == '__main__':
    # Створюємо додаток (Создаем приложение)
    app = ApplicationBuilder().token(TOKEN).build()

    # Додаємо обробник тексту (Добавляем обработчик текста)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))

    print("MFBOXBOT IS LIVE! Press Ctrl+C to stop.")
    app.run_polling()