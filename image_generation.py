import asyncio

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot_states import WAITING_FOR_IMAGE_PROMPT
import config
from utils import call_meshy_api


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
        task = asyncio.create_task(call_meshy_api(prompt=prompt))
        url, video_url, _, status = await asyncio.wait_for(task, timeout=config.WAIT_TIME)
        if status:
            await update.message.reply_photo(url[0])
            await update.message.reply_video(video_url[0])
        else:
            await update.message.reply_text(f"We are unable to generate an image at this moment, please try after sometime.")
    except asyncio.TimeoutError:
        await update.message.reply_text("Image generation is taking longer than expected. Please try again later.")
    except Exception as e:
        await update.message.reply_text(f"We are unable to generate an image at this moment, please try after sometime.")
