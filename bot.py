import logging
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Credentials
TELEGRAM_TOKEN = '8825783796:AAFMWxNHie6y4TlEZFqz8oOyCoP5eyyC7FE'
GEMINI_API_KEY = 'AQ.Ab8RN6LA3ejB2CoEmWda_z0Ih2SGX9UcM2coRFivo35d5ikKGg'

# Initialize Official Google GenAI Client
ai_client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your AI assistant powered by Gemini. Send me any message!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    try:
        # Generate response using official SDK
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_prompt
        )
        
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("No response received from AI.")
            
    except Exception as e:
        await update.message.reply_text(f"Gemini API Error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("AI Telegram Bot is starting...")
    app.run_polling()
