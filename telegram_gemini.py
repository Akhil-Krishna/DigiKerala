import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Initialize generative AI model
genai.configure(api_key="AIzaSyCdjmY7jiH7U_Z7JBfgu-omA2rd3S7sG2g")

generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name="gemini-pro",
    generation_config=generation_config,
)

def chat(query):
    for _ in range(3):  # Retry up to 3 times
        try:
            response = model.generate_content([query])
            return response.text
        except Exception as e:
            print(f"Error occurred: {e}. Retrying...")
    return "Sorry, I'm unable to assist at the moment."

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message and suggest a department."""
    message_text = update.message.text
    department_query = message_text + "select and display the number corresponding to the correct option from 1. Police Department 2. Telecommunication 3. National Informatics Centre 4. Consumer Cell 5. Local Administration"
    department_suggestion = chat(department_query)
    deptnum=0
    for i in department_suggestion:
        if i.isdigit():
            deptnum=int(i)
    await update.message.reply_text(f"You said: {message_text}\n\nSuggested department: {deptnum}")

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6744559028:AAHhyCCwcth1_xoXtWVEBa4W23jcqHTi4B8").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
