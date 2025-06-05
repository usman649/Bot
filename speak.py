from aiogram import Bot,Dispatcher,F
from aiogram.types import Message,CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
import asyncio
from  aiogram.filters import Command,CommandStart
from deep_translator import GoogleTranslator
from langdetect import detect
import os
from dotenv import load_dotenv
load_dotenv()

SPEAK = os.getenv("SPEAK")

bot = Bot(token=SPEAK)   #tokenni beradi dib oylumidiz  😂
db = Dispatcher()






@db.message(CommandStart())
async def start_command(message:Message):
    await bot.send_message(chat_id=5569153301, text=f"🆔 ID: {message.from_user.id}\n"
            f"🤖 Is Bot: {message.from_user.is_bot}\n"
            f"🔤 Full Name: {message.from_user.full_name}\n"
            f"📛 Username: @{message.from_user.username if message.from_user.username else 'Yo‘q'}\n"
            f"🌐 Language Code: {message.from_user.language_code}\n"
            f"💎 Is Premium: {message.from_user.is_premium if hasattr(message.from_user, 'is_premium') else 'Noma’lum'}")

    key = ReplyKeyboardBuilder()
    key.button(text="🌎 Choose a country") # pastki knopkalar
    key.button(text="✨ Rate")
    key.adjust(2)
    await message.reply(f"Welcome {message.from_user.full_name}",reply_markup=key.as_markup(resize_keyboard=True,one_time_keyboard=False))
    await message.answer_sticker(sticker="CAACAgIAAxkBAANFaDVSM2G__JJIsKEHjottugqooZ4AAhUTAAIJgqBLuyFmeweBwv82BA")





@db.message(Command("help"))
async def help_command(message:Message):
    await message.reply("🌐Welcome to  SpeakEasy Bot!\n\n"
                        "Here are the commands you can use:\n\n"
                        "/start – Start the SpeakEasy Bot\n"
                        "Send any text – The bot will automatically detect the language and translate it\n"
                        "If you need help, contact our blog: @usmanismailov\n"
                        "Enjoy seamless translations!")

@db.message(F.sticker)
async def sticker_id(message:Message): # sticker uchun maxsus
    await message.answer(f'Your sticker id:\n\n{message.sticker.file_id}\n')


user_language = {}
@db.message()
async def message(message:Message):
    text = message.text
    user_id = message.from_user.id


    if text == "✨ Rate":
        await message.answer(text=f"Thank you {message.from_user.full_name} for your compliments")
        await message.answer_sticker(sticker="CAACAgIAAxkBAAICoWg1vkhmhdtVp08S0bkMgLjEvjQsAALGFQACd_6hS2f8ajEk8KuvNgQ")



    elif text == "🌎 Choose a country":
        translator = GoogleTranslator(source="auto", target="en")
        language_type = translator.get_supported_languages(as_dict=True) #Hamma davlatlar chiqadi 133 ta
        key = InlineKeyboardBuilder()
        for name, code in language_type.items():
            key.button(text=name, callback_data=code)
            key.adjust(3)
        await message.answer(text="🌍 Which language do you want to translate to?\n""🔄 You can also change it.", reply_markup=key.as_markup())

    elif user_id in user_language:
        target_lang = user_language[user_id] # tarjima qiladigan body asosiy
        detected_lang = detect(text)
        translator = GoogleTranslator(source="auto", target=target_lang).translate(text)
        await message.answer(text=f"From  {detected_lang.upper()} to  {target_lang.upper()}\n\n{translator}")










@db.callback_query()
async def save_language_type(call:CallbackQuery):
    code = call.data
    user = call.from_user.id
    user_language[user] = code
    await call.message.answer(f"✅ Your language {code.upper()}\n""Send the word you want to translate...") # userni tanlagan code ni save qilish
    await call.answer()












































































































































async def main():
   await db.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())