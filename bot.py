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

from prompts import PROMPT_SISTEMA_N1

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY não encontrada.")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não encontrado.")

MAX_MENSAGENS_HISTORICO = 20

chat = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def conversar(pergunta: str, historico: list[tuple[str, str]]) -> str:
    mensagens = [
        ("system", PROMPT_SISTEMA_N1),
        *historico,
        ("human", pergunta)
    ]
    resposta = chat.invoke(mensagens)
    return resposta.content

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Sou o NetHelp N1, assistente de triagem para problemas "
        "de internet. Descreva o que está acontecendo. 🚀"
    )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data.clear()
    await update.message.reply_text("Conversa reiniciada. O histórico foi apagado.")


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pergunta = update.message.text
    historico = context.chat_data.setdefault("historico", [])

    resposta = conversar(pergunta, historico)

    historico.append(("human", pergunta))
    historico.append(("ai", resposta))
    historico[:] = historico[-MAX_MENSAGENS_HISTORICO:]

    await update.message.reply_text(resposta)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    main()
