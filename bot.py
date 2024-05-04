import sqlite3
from gemini import Gemini
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Telegram Bot Token (Replace with your actual token)
BOT_TOKEN = "6305351523:AAG6qgruyfKj0J9dI3BovGmHSurG2I8hQfY"

# Database Connection
conn = sqlite3.connect("complaints.db")
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dept_id INTEGER,
    dept_name TEXT,
    complaint_data TEXT,
    complaint_status TEXT DEFAULT 'Pending',
    date_of_complaint TEXT,
    date_of_resolve TEXT
);
""")
conn.commit()

# Define departments and their IDs
departments = {
    "Police Department": 1,
    "Local Administration": 2,
    "Consumer Cell": 3,
    "National Informatics Centre": 4,
    "Telecommunications": 5
}

# Initialize Gemini
gemini = Gemini()

def start(update, context):
    welcome_message = "Welcome to the Complaint Management System! Please enter your complaint."
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)

def handle_complaint(update, context):
    user_complaint = update.message.text
    # Use Gemini to identify department
    department = gemini.predict(user_complaint, choices=list(departments.keys()))
    dept_id = departments[department]
    dept_name = department

    # Store complaint details in database
    cursor.execute("""
        INSERT INTO complaints (dept_id, dept_name, complaint_data, date_of_complaint)
        VALUES (?, ?, ?, ?)
    """, (dept_id, dept_name, user_complaint, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

    confirmation_message = f"Your complaint has been registered with {dept_name}. We will get back to you soon."
    context.bot.send_message(chat_id=update.effective_chat.id, text=confirmation_message)

def resolve_complaint(update, context):
    complaint_id = int(update.message.text)
    # Update complaint status in database
    cursor.execute("""
        UPDATE complaints SET complaint_status = 'Resolved', date_of_resolve = ?
        WHERE complaint_id = ?
    """, (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), complaint_id))
    conn.commit()

    # Get user details from complaint ID
    cursor.execute("SELECT user_id FROM messages WHERE complaint_id = ?", (complaint_id,))
    user_id = cursor.fetchone()[0]

    # Send notification to user
    context.bot.send_message(chat_id=user_id, text="Your complaint has been resolved by the relevant department.")

def main():
    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_complaint))
    dispatcher.add_handler(CommandHandler("resolve", resolve_complaint))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
