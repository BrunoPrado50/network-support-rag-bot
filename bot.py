import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY não encontrada.")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não encontrado.")

chat = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def conversar(pergunta: str) -> str:
    resposta = chat.invoke([
        ("system", "Você é um assistente."),
        ("human", pergunta)
    ])
    return resposta.content

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot online 🚀")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = conversar(update.message.text)
    await update.message.reply_text(resposta)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    main()
