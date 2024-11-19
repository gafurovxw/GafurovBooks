import os
from telebot import TeleBot, types

# Telegram bot tokeni
BOT_TOKEN = '7887034197:AAF2oQh9IRKXYZKyG5XVLqBVqzzzUTCVISc'
bot = TeleBot(BOT_TOKEN)

# Fayllar katalogi
BOOKS_DIR = 'books'
ADMIN_ID = 'YOUR_ADMIN_ID'

# Kitoblar ro'yxatini olish
def get_books():
    return [book for book in os.listdir(BOOKS_DIR) if book.endswith('.pdf')]

# Boshlang'ich xabar
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📚 Kitoblarni ko'rish"))
    if str(message.chat.id) == ADMIN_ID:
        markup.add(types.KeyboardButton("➕ Yangi kitob qo'shish"))
    bot.send_message(
        message.chat.id,
        "Salom! 'Gafurov ☕︎ Books' botiga xush kelibsiz!\n\n"
        "Kitoblarni ko‘rish uchun menyudan foydalaning.",
        reply_markup=markup,
    )

# Kitoblarni ko'rish
@bot.message_handler(func=lambda message: message.text == "📚 Kitoblarni ko'rish")
def show_books(message):
    books = get_books()
    if books:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for book in books:
            markup.add(types.KeyboardButton(book))
        bot.send_message(message.chat.id, "Quyidagi kitoblardan birini tanlang:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Hozircha kitoblar mavjud emas.")

# Kitoblarni yuklash va reklama xabari
@bot.message_handler(func=lambda message: message.text in get_books())
def send_book(message):
    book_path = os.path.join(BOOKS_DIR, message.text)
    with open(book_path, 'rb') as book:
        bot.send_document(message.chat.id, book)

    # Qo‘shimcha xabar
    bot.send_message(
        message.chat.id,
        (
            "📖 Kitob muvaffaqiyatli yuklandi!\n\n"
            "😊 Xursandmisiz? Ushbu loyihani qo‘llab-quvvatlashni istasangiz, quyidagi havolalarga tashrif buyuring va obuna bo‘ling:\n\n"
            "📢 **Bizning loyihalarimiz:**\n"
            "- [IodaSoft Telegram kanali](https://t.me/IodaSoft)\n"
            "- [IodaSoft Windows uchun](https://t.me/IodaSoft_Windows)\n"
            "- [IodaSoft MacOS uchun](https://t.me/IodaSoft_MacOS)\n\n"
            "📧 **Murojaat uchun:** jasurbekgafurov.dev@gmail.com (24/7 xizmat)\n\n"
            "Sizning qo‘llab-quvvatlashingiz biz uchun juda muhim! 😊"
        ),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )

# Admin: Yangi kitob qo'shish
@bot.message_handler(func=lambda message: str(message.chat.id) == ADMIN_ID and message.text == "➕ Yangi kitob qo'shish")
def add_book_prompt(message):
    bot.send_message(message.chat.id, "Yangi kitobni yuklash uchun faylni jo'nating:")

# Admin: Faylni qabul qilish va saqlash
@bot.message_handler(content_types=['document'])
def handle_document(message):
    if str(message.chat.id) == ADMIN_ID:
        file_id = message.document.file_id
        file_name = message.document.file_name
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Faylni saqlash
        with open(os.path.join(BOOKS_DIR, file_name), 'wb') as f:
            f.write(downloaded_file)

        bot.send_message(message.chat.id, f"✅ {file_name} muvaffaqiyatli yuklandi!")
    else:
        bot.send_message(message.chat.id, "Sizda fayl yuklash huquqi yo'q.")

# Botni ishga tushirish
bot.polling()