from aiogram import Bot,Dispatcher,F
from aiogram.filters import CommandStart,Command
import asyncio
import yt_dlp
import wikipedia
wikipedia.set_lang("uz")
import os
from dotenv import load_dotenv
load_dotenv()

KINO_XIT = os.getenv("KINO_XIT")



from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, CallbackQuery,FSInputFile


bot = Bot(token=KINO_XIT)   #tokenni beradi dib oylumidiz  😂
db = Dispatcher()


@db.message(CommandStart())
async def start_command(message:Message):
    key = InlineKeyboardBuilder()
    key.button(text="Search movie 🎥",callback_data="search")
    key.button(text="New movies 🔥",callback_data="news")
    key.adjust(2)
    await message.answer_photo(photo="https://pfst.cf2.poecdn.net/base/image/c18f983105cf8e5be2a4bc931f3e45dac6d756099406de710b30aed1c2246e45?w=832&h=1216&pmaid=351803481"
                               ,caption=f"Hi  {message.from_user.full_name}  just send me that video url !\n\n"
                                        "You can also download videos from these social platforms:\n"
                                        "* You Tube\n"
                                        "* Facebook\n"
                                        "* Instagram\n"
                                        "* TikTok\n"
                                        "* Twitter/X\n"
                                        "* VK (VKontakte)\n"
                                        "* Snapchat\n"
                                        "* Likee\n"
                                        "* LinkedIn\n"
                                        "* Reddit\n"
                                        "* SoundCloud\n"
                                        "* Vimeo\n"
                                        "and more ......"




                               ,

                               reply_markup=key.as_markup())

@db.message(Command("help"))
async def help_command(message:Message):
    await message.reply("🎬 Welcome to Movie Bot!\n\n"
        "Here are the commands you can use:\n\n"
        "/start - Start the Movie Bot\n"
        "If you need any assistance,contact our blog @usmanismailov\n"  
        "Enjoy your movie time! 🍿")


file_path_global = None

@db.message()
async def search(message:Message):
    search_query = message.text.strip()


    if search_query.startswith("https://"):
        upload =  await message.answer('⏳ _Uploading_...',parse_mode="Markdown")
        await asyncio.sleep(3)
        await upload.delete()

        with yt_dlp.YoutubeDL() as yash:
            info = yash.extract_info(search_query, download=True)
            file_path = yash.prepare_filename(info)

            key = InlineKeyboardBuilder()
            key.button(text="🎵 Music", callback_data="music")
            global file_path_global
            file_path_global = file_path


            video = FSInputFile(file_path)
            await message.answer_video(video=video, caption=f"🎬 {info['title']}",reply_markup=key.as_markup())




    else:
        url = f"http://uzbeklar.biz/index.php?do=search&subaction=search&story={search_query}"



        key = InlineKeyboardBuilder()
        key.button(text="Watch now 🎬",url=url)
        key.adjust(1)
        await message.answer_animation("https://substack-post-media.s3.amazonaws.com/public/images/29cfcf2c-63fe-4e08-9bc1-b80086f1532e_498x280.gif",reply_markup=key.as_markup())

        wik = wikipedia.summary(search_query)
        await message.answer(text=f"About this movie 🔎\n\n{wik}")




@db.callback_query(F.data == "music")
async def music_button(call:CallbackQuery):
    global file_path_global
    await call.answer("")
    music = FSInputFile(file_path_global)
    await call.message.answer_audio(audio=music)











@db.callback_query(F.data == "search")
async def search_button(call:CallbackQuery):
    await call.answer("")
    await call.message.answer(
        "🎬 *How to search a movie:*\n\n"
        "Just type the name of any movie you'd like to search.\n\n"
        "🔍 *Example:*\n\n"
        "_Avatar_\n"
        "_The Dark Knight_\n"
        "_Harry Potter and the Sorcerer's Stone_\n\n"
        "I'll find the movie details like title, poster, rating, plot, and maybe even the trailer for you! 🍿",
        parse_mode="Markdown"
    )




@db.callback_query(F.data == "news")
async def news_button(call:CallbackQuery):
    await call.answer("")
    search = await call.message.answer("🔎 _Searching_...",parse_mode="Markdown")
    await asyncio.sleep(3)
    await search.delete()





















async def main():
   await db.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())







