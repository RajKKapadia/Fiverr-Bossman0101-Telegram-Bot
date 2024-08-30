from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot_states import WAITING_FOR_IMAGE_PROMPT
import config


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
        response = config.openai_client.images.generate(
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
