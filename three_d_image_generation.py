from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot_states import WAITING_FOR_3D_PROMPT


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
