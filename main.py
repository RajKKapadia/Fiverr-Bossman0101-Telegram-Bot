import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from bot_states import WAITING_FOR_IMAGE_PROMPT
from image_generation import image_command, receive_prompt
import config


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Welcome! This bot can generate images. Use /image to generate an image.')


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text("Image generation cancelled.")
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(config.TELEGRAM_BOT_API_KEY).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))

    # Add conversation handler for image generation
    image_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("image", image_command)],
        states={
            WAITING_FOR_IMAGE_PROMPT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_prompt)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    application.add_handler(image_conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
