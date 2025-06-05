import asyncio
import json
import os
import aiohttp
from aiogram.filters import CommandStart,Command
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder,InlineKeyboardButton
from aiogram.utils.media_group import MediaGroupBuilder
import requests
from dotenv import load_dotenv
load_dotenv()
import os

QURAN = os.getenv("QURAN")


bot= Bot(token=QURAN) #tokenni beradi dib oylumidiz  😂
db = Dispatcher()


SURAH_PER_PAGE = 10
TOTAL_SURAHS = 114

SURAH_LIST = [
    "Al-Fatiha (The Opener)", "Al-Baqarah (The Cow)", "Al-Imran (Family of Imran)",
    "An-Nisa (The Women)", "Al-Ma'idah (The Table Spread)", "Al-Anam (The Cattle)",
    "Al-A'raf (The Heights)", "Al-Anfal (The Spoils of War)", "At-Taubah (The Repentance)",
    "Yunus (Jonah)", "Hud (Hud)", "Yusuf (Joseph)", "Ar-Ra'd (Thunder)", "Ibrahim (Abraham)",
    "Al-Hijr (The Stoneland)", "An-Nahl (The Bee)", "Al-Isra (The Night Journey)",
    "Al-Kahf (The Cave)", "Maryam (Mary)", "Ta-Ha (Ta-Ha)", "Al-Anbiya (The Prophets)",
    "Al-Hajj (The Pilgrimage)", "Al-Mu'minun (The Believers)", "An-Nur (The Light)",
    "Al-Furqan (The Criterion)", "Ash-Shu'ara (The Poets)", "An-Naml (The Ants)",
    "Al-Qasas (The Story)", "Al-Ankabut (Spider)", "Ar-Rum (The Romans)", "Luqman (Luqman)",
    "As-Sajdah (Prostration)", "Al-Ahzab (The Confederates)", "Saba (Sheba)", "Fatir (The Originator)",
    "Ya-Sin (Ya Sin)", "As-Saffat (Those Who Set the Ranks)", "Sad (The letter Saad)",
    "Az-Zumar (The Troops)", "Ghafir (The Forgiver)", "Fussilat (Explained in Detail)",
    "Ash-Shura (The Consultation)", "Az-Zukhruf (The Ornaments of Gold)", "Ad-Dukhan (The Smoke)",
    "Al-Jathiyah (The Crouching)", "Al-Ahqaf (The Wind Curved Sandhill)", "Muhammad (Muhammad)",
    "Al-Fath (The Victory)", "Al-Hujurat (The Private Chambers)", "Qaf (Qaf)",
    "Adh-Dhariyat (The Scatterers)", "At-Tur (The Mountain)", "An-Najm (The Star)",
    "Al-Qamar (The Moon)", "Ar-Rahman (The Beneficent)", "Al-Waqi'ah (The Inevitable)",
    "Al-Hadid (The Iron)", "Al-Mujadila (The Pleading Women)", "Al-Hashr (The Exile)",
    "Al-Mumtahanah (She That is to be Examined)", "As-Saff (The Ranks)", "Al-Jumu'ah (Congregation Prayer)",
    "Al-Munafiqun (The Hypocrites)", "At-Taghabun (Mutual Disposession)", "At-Talaq (The Divorce)",
    "At-Tahrim (The Prohibition)", "Al-Mulk (The Sovereignty)", "Al-Qalam (The Pen)",
    "Al-Haqqah (The Reality)", "Al-Ma'arij (The Ascending Stairways)", "Nuh (Noah)",
    "Al-Jinn (The Jinn)", "Al-Muzzammil (The Enshrouded One)", "Al-Muddaththir (The Cloaked One)",
    "Al-Qiyamah (The Resurrection)", "Al-Insan (The Man)", "Al-Mursalat (The Emissaries)",
    "An-Naba (The Tidings)", "An-Nazi'at (Those who drag forth)", "Abasa (He Frowned)",
    "At-Takwir (The Overthrowing)", "Al-Infitar (The Cleaving)", "Al-Mutaffifin (The Defrauding)",
    "Al-Inshiqaq (The Sundering)", "Al-Buruj (The Mansions of the Stars)", "At-Tariq (The Nightcommer)",
    "Al-Ala (The Most High)", "Al-Ghashiyah (The Overwhelming)", "Al-Fajr (The Dawn)",
    "Al-Balad (The City)", "Ash-Shams (The Sun)", "Al-Lail (The Night)",
    "Ad-Duha (The Morning Brightness)", "Ash-Sharh (The Expansion)", "At-Tin (The Fig)",
    "Al-Alaq (The Blood Clot)", "Al-Qadr (The Power)", "Al-Bayyina (The Evidence)",
    "Az-Zalzalah (The Earthquake)", "Al-Adiyat (The Courser)", "Al-Qari'ah (The Calamity)",
    "At-Takathur (Vying for increase)", "Al-Asr (The Declining Day)", "Al-Humazah (The Slanderer)",
    "Al-Fil (The Elephant)", "Quraysh (Quraish)", "Al-Ma'un (The Small Kindness)",
    "Al-Kawthar (The Abundance)", "Al-Kafirun (The Disbelievers)", "An-Nasr (The Divine Support)",
    "Al-Masad (The Palm Fiber)", "Al-Ikhlas (The Sincerity)", "Al-Falaq (The Daybreak)",
    "An-Nas (The Mankind)"
]

def get_surah_text(page: int = 1):
    start = (page - 1) * SURAH_PER_PAGE
    end = min(start + SURAH_PER_PAGE, TOTAL_SURAHS)
    text = ""
    for i in range(start, end):
        text += f"{i+1}. {SURAH_LIST[i]}\n"
    return text.strip()


def get_surah_keyboard(page: int = 1):
    key = InlineKeyboardBuilder()
    start = (page - 1) * SURAH_PER_PAGE
    end = min(start + SURAH_PER_PAGE, TOTAL_SURAHS)

    for i in range(start, end):
        surah_number = i + 1
        key.button(text=f"{surah_number}", callback_data=str(surah_number))

    key.adjust(5)
    nav_buttons = []

    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"page_{page - 1}"))
    nav_buttons.append(InlineKeyboardButton(text="❌", callback_data="delete"))
    if end < TOTAL_SURAHS:
        nav_buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"page_{page + 1}"))

    key.row(*nav_buttons)
    return key.as_markup()







@db.message(CommandStart())
async def start_command(message:Message):
    key = ReplyKeyboardBuilder()
    key.button(text="🕌 Reciter")
    key.button(text="📖 Surah")
    key.adjust(2)
    await message.answer(text=f"*_Assalamu Alaikum_* {message.from_user.full_name} ",reply_markup=key.as_markup(resize_keyboard=True,input_field_placeholder="Write order"),parse_mode="MarkdownV2")

@db.message(Command("help"))
async def help_command(message:Message):
    await message.reply(text="🕌 Quran Life Bot\n\n"
                             "This bot allows you to listen to beautiful Quran recitations and explore Surahs with ease.\n"
                            "✅ To get started, simply type or click:\n\n"
                            "/start - Start Quran Life Bot\n\n"
                            "You will then be able to:\n"
                            "📖 Choose a Surah\n"
                            "🎧 Select a Qari (reciter)\n"
                            "🕋 Listen to Quranic recitations anytime\n\n"
                            "Contact the admin @usmanismailov")

@db.message(Command("qibla"))
async def qibla_command(message:Message):
    await message.reply_location(latitude=21.4225,longitude=39.8262)









reciter_id_save = {}
@db.message()
async def basic_message(message:Message):
    text = message.text
    if text == "🕌 Reciter":
        key = InlineKeyboardBuilder()
        for i in range(1,6):
            key.button(text=f"{i}",callback_data=f"recister_{i}")

        key.adjust(5)
        key.row(
                InlineKeyboardButton(text="◀️", callback_data="left"),
                        InlineKeyboardButton(text="❌", callback_data="delete"),
                        InlineKeyboardButton(text="▶️", callback_data="right"),
            )

        await message.answer(text="1. Mishary Rashid Al Afasy\n""2. Abu Bakr Al Shatri\n""3. Nasser Al Qatami\n""4. Yasser Al Dosari\n""5. Hani Ar Rifai", reply_markup=key.as_markup())

    if text == "📖 Surah":
        page = 1
        text_content = get_surah_text(page)
        keyboard = get_surah_keyboard(page)

        await message.answer(text=text_content,  reply_markup=keyboard)




@db.callback_query(F.data.startswith("page_"))
async def paginate_surah(call: CallbackQuery):
    page = int(call.data.split("_")[1])

    text_content = get_surah_text(page)
    keyboard = get_surah_keyboard(page)

    await call.message.edit_text(
        text=text_content,
        reply_markup=keyboard
    )

    await call.answer()


@db.callback_query(F.data == "delete")
async def delete_message(call:CallbackQuery):
    await call.message.delete()
    await call.answer()


qori_list = {
   "1": "Mishary Rashid Al Afasy",
   "2": "Abu Bakr Al Shatri",
   "3": "Nasser Al Qatami",
   "4": "Yasser Al Dosari",
   "5": "Hani Ar Rifai"
}

@db.callback_query()
async def audio_api_call(call:CallbackQuery):
    await call.answer()
    surah_id = call.data
    user = call.message.from_user.id

    if surah_id.startswith("recister_"):
        reciter_id = int(surah_id.split("_")[1])
        reciter_id_save[user] = reciter_id
        for n,q in qori_list.items():
            if str(reciter_id) == n:
                await call.message.answer(f"✅ Your reciter {q}\n""📖 Choose Surah ")



    if user not in reciter_id_save:
        await call.message.answer(text="Choose recister")


    reciter_id_number = reciter_id_save[user]






    audio_url = f"https://github.com/The-Quran-Project/Quran-Audio-Chapters/raw/refs/heads/main/Data/{reciter_id_number}/{surah_id}.mp3"
    file_name = f"{surah_id}_reciter{reciter_id_number}.mp3"




    async with aiohttp.ClientSession() as session:
        async with session.get(audio_url) as response:
            if response.status == 200:
                content = await response.read()
                with open(file_name, "wb") as f:
                    f.write(content)

                with open(file_name, "rb") as a:
                    input = FSInputFile(file_name)
                    await call.message.answer_audio(audio=input)


                os.remove(file_name)
























































































async def main():
   await db.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())








