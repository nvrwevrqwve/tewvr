import os
import telebot
from dotenv import load_dotenv
import time
import threading

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GATEWAY_CHANNEL_ID = int(os.getenv("GATEWAY_CHANNEL_ID"))
PRIVATE_CHANNELS = list(map(int, os.getenv("PRIVATE_CHANNELS").split(",")))

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def test_alive(message):
    print(f"📩 Got a message from {message.chat.id} — {message.text}")
    bot.reply_to(message, "✅ Bot is alive!")

@bot.chat_join_request_handler()
def handle_join_request(request):
    user = request.from_user
    chat_id = request.chat.id
    username = user.username or user.first_name or str(user.id)
    

    try:
        # 📌 GATEWAY CHANNEL (manual approval required)
        if chat_id == GATEWAY_CHANNEL_ID:
            # Do NOT auto-approve
            bot.send_message(user.id, "Message mo lang ako Boss, kapag nakapag-request ka na sa channel‼️\n📩 @SinCheats")
            print(f"🕓 @{username} requested to join GATEWAY (awaiting manual approval)")

        # 🔐 PRIVATE CHANNELS (auto-approval if in gateway)
        elif chat_id in PRIVATE_CHANNELS:
            try:
                member = bot.get_chat_member(GATEWAY_CHANNEL_ID, user.id)
            except Exception as e:
                print(f"❌ Error checking gateway membership for @{username}: {e}")
                member = None

            if member and member.status in ['member', 'administrator', 'creator']:
                bot.approve_chat_join_request(chat_id, user.id)
                bot.send_message(user.id, f"CHANNEL '{request.chat.title}' APPROVED✅!\nJABOL NA PARA PUMALDO🤤🔥!\n\nKAPAG HINDI MO NAKIKITA ANG CHANNEL, SEARCH MO LANG ITO '{request.chat.title}'")
                print(f"✅ Approved @{username} to {request.chat.title}")
            else:
                bot.decline_chat_join_request(chat_id, user.id)
                bot.send_message(user.id, "AVAIL KANA BOSS🔥\nWAG MO SUBUKAN😏\n\nBILI NA 📩 @SinCheats")
                print(f"❌ Denied @{username} from {request.chat.title} — not in gateway")

        else:
            bot.decline_chat_join_request(chat_id, user.id)
            bot.send_message(user.id, "AVAIL KANA BOSS🔥\nWAG MO SUBUKAN😏\n\nBILI NA 📩 @SinCheats")
            print(f"⚠️ Unknown join request from @{username} in chat {chat_id}")

    except Exception as e:
        print(f"⚠️ Error handling @{username}'s request: {e}")
        try:
            bot.send_message(user.id, "AVAIL KANA BOSS🔥\nWAG MO SUBUKAN😏\n\nBILI NA 📩 @SinCheats")
        except:
            pass



print("✅ Bot is running.")
bot.infinity_polling()
