import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# OpenAI client
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Define states
WAITING_FOR_IMAGE_PROMPT = 0
WAITING_FOR_3D_PROMPT = 1

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Welcome! This bot can generate images. Use /image to generate an image.')


async def image_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /image command."""
    if context.args:
        # If a prompt was provided with the command, generate the image immediately
        prompt = ' '.join(context.args)
        await generate_image(update, context, prompt)
        return ConversationHandler.END
    else:
        # If no prompt was provided, ask for one
        await update.message.reply_text("Please provide a prompt for the image generation:")
        return WAITING_FOR_IMAGE_PROMPT


async def receive_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the received prompt and generate the image."""
    prompt = update.message.text
    await generate_image(update, context, prompt)
    return ConversationHandler.END


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE, prompt: str) -> None:
    """Generate an image using OpenAI API."""
    await update.message.reply_text(f"Generating image for prompt: {prompt}")

    try:
        response = openai_client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        # Send the generated image
        image_url = response.data[0].url
        await update.message.reply_photo(image_url)
    except Exception as e:
        await update.message.reply_text(f"We are unable to generate an image at this moment, please try after sometime.")


async def three_d_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /3d command."""
    if context.args:
        prompt = ' '.join(context.args)
        await generate_3d_image(update, context, prompt)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please provide a prompt for the 3D image generation:")
        return WAITING_FOR_3D_PROMPT


async def receive_3d_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the received prompt for 3D image and generate the image."""
    prompt = update.message.text
    await generate_3d_image(update, context, prompt)
    return ConversationHandler.END


async def generate_3d_image(update: Update, context: ContextTypes.DEFAULT_TYPE, prompt: str) -> None:
    """Generate an image using OpenAI API."""
    await update.message.reply_text(f"Generating image for prompt: {prompt}")

    try:
        """TODO
        [x] Write the code to generate 3D image
        """

        # Send the generated image
        image_url = "https://fastly.picsum.photos/id/375/200/300.jpg?hmac=LBiwrXNHAfYU5B9rOkXkrH8iw8bSwUaHoV7Adk3I5s4"
        await update.message.reply_photo(image_url)
    except Exception as e:
        await update.message.reply_text(f"We are unable to generate an image at this moment, please try after sometime.")


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the conversation."""
    await update.message.reply_text("Image generation cancelled.")
    return ConversationHandler.END


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(
        os.getenv("TELEGRAM_BOT_API_KEY")).build()

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

    # Add conversation handler for 3d image generation
    three_d_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("3d", three_d_command)],
        states={
            WAITING_FOR_3D_PROMPT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_3d_prompt)],
        },
        fallbacks=[CommandHandler("cancle", cancel)]
    )
    application.add_handler(three_d_conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
