import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import requests

# Replace with your bot's token and admin chat ID
TELEGRAM_TOKEN = '7297716941:AAER55IjILZD-pMS-gr-A7aV8AWZEqczNbg'
ADMIN_CHAT_ID = 5424529390  # Replace with your Telegram User ID (admin)

# Dummy database for storing added Twitter accounts
added_twitter_accounts = {}

# Setup logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Start command, sets up the bot with buttons
def start(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("Add Funds", callback_data='add_funds'),
            InlineKeyboardButton("Check Twitter Account", callback_data='check_twitter')
        ],
        [InlineKeyboardButton("Contact Support", callback_data='contact_support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Choose an option:', reply_markup=reply_markup)

# Callback for button presses
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()  # Acknowledge the button press

    if query.data == 'add_funds':
        query.edit_message_text(text="Send the amount you want to add to your funds (e.g., 100).")
    elif query.data == 'check_twitter':
        query.edit_message_text(text="Send the Twitter handle you want to check (e.g., @elonmusk).")
    elif query.data == 'contact_support':
        query.edit_message_text(text="Please contact support at support@example.com or type your message.")

# Add funds command
def add_funds(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    try:
        amount = float(update.message.text.split()[1])
        if amount <= 0:
            update.message.reply_text("Amount must be greater than zero.")
            return
        if user_id not in user_funds:
            user_funds[user_id] = 0
        user_funds[user_id] += amount
        update.message.reply_text(f"You've added ${amount}. Your new balance is ${user_funds[user_id]}.")
    except (IndexError, ValueError):
        update.message.reply_text("Please provide a valid amount. Example: /addfunds 100")

# Check Twitter account availability
def check_twitter(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("Please provide a Twitter handle to check. Example: /checktwitter @elonmusk")
        return

    handle = context.args[0]
    # Here, you would use the Twitter API to check if the account exists.
    # For now, we'll mock the response.
    if handle == "@elonmusk":
        update.message.reply_text(f"The Twitter account {handle} exists!")
    else:
        update.message.reply_text(f"The Twitter account {handle} does not exist.")

# Command to allow the admin to add Twitter accounts
def add_twitter(update: Update, context: CallbackContext):
    # Check if the user is the admin
    if update.message.from_user.id != ADMIN_CHAT_ID:
        update.message.reply_text("You are not authorized to perform this action.")
        return
    
    if len(context.args) == 0:
        update.message.reply_text("Please provide a Twitter handle to add. Example: /addtwitter @newhandle")
        return
    
    twitter_handle = context.args[0]
    
    # Check if the account already exists
    if twitter_handle in added_twitter_accounts:
        update.message.reply_text(f"The Twitter account {twitter_handle} is already added.")
        return
    
    # Add the Twitter handle to the dictionary
    added_twitter_accounts[twitter_handle] = True
    update.message.reply_text(f"Successfully added the Twitter account {twitter_handle}.")

# Main function to set up the bot and commands
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Command Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("addfunds", add_funds))
    dp.add_handler(CommandHandler("checktwitter", check_twitter))
    dp.add_handler(CommandHandler("addtwitter", add_twitter))  # Admin command to add Twitter account

    # Button Callback Handler
    dp.add_handler(CallbackQueryHandler(button))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
