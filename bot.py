# Importing Required Libraries, Imported os Module For Security
import logging
import os
import random
import urllib.parse
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, MessageHandler, Updater


# Getting Bot Token From Secrets
BOT_TOKEN = os.environ.get('BOT_TOKEN')
LOG_CHANNEL = os.environ.get('LOG_CHANNEL')

# Creating Telegram Bot object
bot = telegram.Bot(token=BOT_TOKEN)


# Welcome message handler
def welcome(update: Update, context):
    # Inline keyboard with a single button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add me to your group", url=f"http://t.me/Postfinderbot?startgroup=true")]
    ])

    # Send welcome message with inline keyboard
    message = f"Hey *{update.effective_chat.first_name}*, welcome to *Post Finder bot*.\n\nYou can use this bot in your group to find your channel post link."
    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown', reply_markup=keyboard)
    logging.info(f"Welcome message sent to {update.effective_chat.first_name}")


# Document handler
def handle_docs_photo(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Sorry {update.effective_chat.first_name}, documents not supported at this time")
    logging.info(f"Message replied to {update.effective_chat.first_name}")


# Message handler to reply to all messages
def reply_to_message(update: Update, context):
    # Get the text of the message
    query_text = update.effective_message.text
    # Encode the text for use in a URL
    encoded_query = urllib.parse.quote_plus(query_text)

    # Create an inline keyboard with a single button
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Click me!", url=f"https://www.ellisamovies.com/?s={encoded_query}")]
    ])

    # Generate a random filename for the image
    filename = f"{update.effective_chat.id}_{update.effective_message.message_id}_{random.randint(1, 100000)}.jpg"

    # Send the image with a caption and inline keyboard
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open("image.jpg", "rb"),
        caption=f"𝐑𝐞𝐪𝐮𝐞𝐬𝐭 𝐛𝐲 - {update.effective_chat.first_name}\n\n𝐇𝐞𝐫𝐞' 𝐰𝐡𝐚𝐭 𝐈 𝐟𝐨𝐮𝐧𝐝 𝐟𝐨𝐫'{message.text}':",reply_markup=keyboard)
                       
    print(f"Message Replied To {message.chat.first_name}\n")
    
    # Log requests
    if message.text and ('#request' in message.text or '/request' in message.text):
        # Forward the message to the log channel
        bot.forward_message(chat_id=LOG_CHANNEL, from_chat_id=message.chat.id, message_id=message.message_id)
        # Reply to the user who sent the message
        bot.reply_to(message, 'Your request has been logged.')
        print(f"Request Logged From {message.chat.first_name}\n")


# Set up logging to a file
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot.log'
)


# Define a function to handle messages containing the #request or /request keyword
def log_request(update: Update, context):
    message = update.effective_message
    chat_id = LOG_CHANNEL # Replace with the ID of your log channel
    
    # Check if message contains the keyword
    if message.text and ('#request' in message.text or '/request' in message.text):
        # Forward the message to the log channel
        context.bot.forward_message(chat_id=chat_id, from_chat_id=message.chat_id, message_id=message.message_id)
        # Reply to the user who sent the message
        message.reply_text('Your request has been logged.')
    
# Set up the bot and its handles 
updater = Updater(BOT_TOKEN, use_context=True)



dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text & (Filters.command | Filters.regex('#request|/request')), log_request))
print("bot started And Waiting For New Messages\n")
  
# Waiting For New Messages
bot.infinity_polling()
