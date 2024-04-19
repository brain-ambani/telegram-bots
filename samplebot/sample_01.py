import os
from typing import Final

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from datetime import datetime

TOKEN: Final = os.getenv('API_SECRET')

BOT_USERNAME: Final = '@simple_chappie_bot'


# Command Handlers

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! I am a simple bot!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am here to help, share your query!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command')

# Response Handlers

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    
    if 'bye' in processed:
        return 'Goodbye!'
    
    if 'thanks' in processed:
        return 'You are welcome!'
    
    if 'how are you' in processed:
        return 'I am fine, thank you!'
    
    if 'what is your name' in processed:
        return 'I am Simple Chappie!'
    
    if 'who are you' in processed:
        return 'I am a simple bot!'
    
    if 'what can you do' in processed:
        return 'I can help you with your queries!'
    
    if 'what is the time' in processed:
        return f'The current time is {datetime.now()}'
    
    return 'I am sorry, I did not understand that!'

# Message Handlers

async def handle_message(update: Update, context: ContextTypes):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    
    print('Bot:', response)
    await update.message.reply_text(response)


async def error_handler(update: Update, context: ContextTypes):
    print(f'Update {Update} caused error: {context.error}')


# Main Function
if(__name__ == '__main__'):
    print('Starting the bot...')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    #Messages
    app.add_handler(MessageHandler(filters.Text, handle_message))

    #Errors
    app.add_error_handler(error_handler)

    # pools the bot
    print('Polling...')

    app.run_polling(poll_interval=3)