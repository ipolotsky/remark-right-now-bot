import logging
from logging.handlers import RotatingFileHandler

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import MessageHandler, Application, ConversationHandler, CommandHandler, filters, ContextTypes

import settings
from handlers.error_handler import error_handler
from messages import *

BUTTON_DEARS_LIST = "List of dears"
BUTTON_HELP = "Help"

WAITING_FOR_REMARK, TYPING_REPLY, TYPING_CHOICE = range(3)

keyboard = [
    [str(BUTTON_DEARS_LIST), str(BUTTON_HELP)]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Start the conversation and ask user for input."""
    1/0
    await update.message.reply_text(
        WELCOME_MESSAGE,
        reply_markup=markup,
    )
    await update.message.reply_text(
        LETS_TRY_MESSAGE,
        reply_markup=markup,
    )

    return None


def process_remark(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text(
        "Select a person:",
        reply_markup=markup
    )
    return WAITING_FOR_REMARK


def set_logger():
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    my_handler = RotatingFileHandler('app.log', maxBytes=50 * 1024 * 1024, backupCount=2)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)

    app_log.addHandler(my_handler)


def main() -> None:
    set_logger()

    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.BOT_TOKEN).build()

    # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_REMARK: [
                # MessageHandler(
                #     filters.Regex("^(Age|Favourite colour|Number of siblings)$"), regular_choice
                # ),
                # MessageHandler(filters.Regex("^Something else...$"), custom_choice),
            ],
            # FRIENDS_LIST: [
            #     MessageHandler(
            #         filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice
            #     )
            # ],
            # ADD_NEW_FRIEND: [
            #     MessageHandler(
            #         filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
            #         received_information,
            #     )
            # ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), process_remark)],
    )

    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)

    # Run the bot until the user presses Ctrl-C
    logging.getLogger('root').info("Bot started (polling)")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
