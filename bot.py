import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = '8825783796:AAFMWxNHie6y4TlEZFqz8oOyCoP5eyyC7FE'
GEMINI_API_KEY = 'AQ.Ab8RN6K5PJMb0w7-o3BesgwyTVKXMLRLgXaYAM-V-ckGvk-siw'

GEMINI_URL = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={GEMINI_API_KEY}'

session = requests.Session()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your AI assistant powered by Gemini. Send me any message!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    payload = {"contents": [{"parts": [{"text": user_prompt}]}]}
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = session.post(GEMINI_URL, headers=headers, json=payload, timeout=30)
        data = response.json()
        
        if response.status_code == 200:
            bot_reply = data['candidates'][0]['content']['parts'][0]['text']
            await update.message.reply_text(bot_reply)
        else:
            error_msg = data.get('error', {}).get('message', 'API Error')
            await update.message.reply_text(f"Gemini API Error: {error_msg}")
    except Exception as e:
        await update.message.reply_text(f"Network error communicating with AI: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).connect_timeout(60.0).read_timeout(60.0).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("AI Telegram Bot is starting...")
    app.run_polling()
