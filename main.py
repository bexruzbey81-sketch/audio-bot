import os
import telebot
from moviepy.editor import VideoFileClip

TOKEN = "8870511778:AAFN88au-z-bVrMwV65YPmkGYy7r7uf3pOU"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Menga biror video yuboring, men undan audiosini ajratib beraman.")

@bot.message_handler(content_types=['video', 'document'])
def handle_video(message):
    try:
        msg = bot.reply_to(message, "Video qabul qilindi. Audio ajratilmoqda, kuting...")
        
        file_info = bot.get_file(message.video.file_id if message.video else message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        video_path = "input_video.mp4"
        audio_path = "output_audio.mp3"
        
        with open(video_path, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path)
        clip.close()
        
        with open(audio_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, title="Extract_Audio.mp3")
            
        os.remove(video_path)
        os.remove(audio_path)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi. Video formatini tekshirib qayta yuboring.")

bot.infinity_polling()
