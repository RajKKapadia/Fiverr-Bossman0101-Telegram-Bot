from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot_states import WAITING_FOR_ASK_PROMPT
import config


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the /ask command."""
    if context.args:
        prompt = ' '.join(context.args)
        await generate_text(update, context, prompt)
        return ConversationHandler.END
    else:
        await update.message.reply_text("Please ask your question:")
        return WAITING_FOR_ASK_PROMPT


async def receive_ask_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the received prompt for ask and generate the response."""
    prompt = update.message.text
    await generate_text(update, context, prompt)
    return ConversationHandler.END


async def generate_text(update: Update, context: ContextTypes.DEFAULT_TYPE, prompt: str) -> None:
    """Generate an answer using OpenAI API."""
    await update.message.reply_text(f"Generating response for prompt: {prompt}")

    try:
        response = config.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        # Send the generated text
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"We are unable to generate answer at this moment, please try after sometime.")
