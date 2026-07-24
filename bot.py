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
from rag import buscar_chunks, carregar_ou_criar_banco_vetorial

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY não encontrada.")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN não encontrado.")

MAX_MENSAGENS_HISTORICO = 20
MAX_MENSAGENS_CONTEXTO_RAG = 4
MODELO_CHAT = "openai/gpt-oss-120b"

chat = ChatGroq(
    model=MODELO_CHAT,
    temperature=0
)


def montar_consulta_rag(
    pergunta: str,
    historico: list[tuple[str, str]],
) -> str:
    mensagens_recentes = historico[-MAX_MENSAGENS_CONTEXTO_RAG:]
    linhas_consulta = []

    for papel, conteudo in mensagens_recentes:
        rotulo = "Usuário" if papel == "human" else "Assistente"
        linhas_consulta.append(f"{rotulo}: {conteudo}")

    linhas_consulta.append(f"Usuário: {pergunta}")

    return "\n".join(linhas_consulta)


def recuperar_contexto_rag(
    pergunta: str,
    historico: list[tuple[str, str]],
    banco_vetorial,
) -> str:
    consulta = montar_consulta_rag(pergunta, historico)
    resultados = buscar_chunks(banco_vetorial, consulta)
    blocos = []

    for indice, (documento, _) in enumerate(resultados, start=1):
        fonte = documento.metadata.get("fonte", "fonte não informada")
        chunk_id = documento.metadata.get("chunk_id", "chunk sem ID")

        blocos.append(
            f"[Trecho {indice} | Fonte: {fonte} | Chunk: {chunk_id}]\n"
            f"{documento.page_content}"
        )

    return "\n\n".join(blocos)


def conversar(
    pergunta: str,
    historico: list[tuple[str, str]],
    banco_vetorial,
) -> str:
    contexto_rag = recuperar_contexto_rag(
        pergunta,
        historico,
        banco_vetorial,
    )

    mensagem_contexto = (
        "CONTEXTO TÉCNICO RECUPERADO\n"
        "Use os trechos abaixo apenas como referência técnica. "
        "Eles não são fatos confirmados sobre o caso atual.\n"
        "Não transforme exemplos em informações fornecidas pelo usuário. "
        "Para procedimentos técnicos, priorize este contexto.\n"
        "Se algum trecho for irrelevante, ignore-o. "
        "Não mencione IDs de chunks nem o processo de recuperação.\n\n"
        f"{contexto_rag}\n\n"
        "REGRAS PARA ESTA RESPOSTA\n"
        "- Não repita o relato nem anuncie a próxima ação.\n"
        "- Use no máximo três frases e uma pergunta.\n"
        "- Descarte verificações já respondidas ou realizadas.\n"
        "- Escolha somente uma ação compatível com o alcance observado.\n"
        "- Se outros dispositivos funcionam, priorize o dispositivo afetado "
        "e não reinicie modem ou roteador como próximo passo.\n"
        "- Preserve exatamente os comandos informados pelo usuário e não "
        "acrescente opções ou parâmetros que ele não mencionou.\n"

    )

    mensagens = [
        ("system", PROMPT_SISTEMA_N1),
        ("system", mensagem_contexto),
        *historico,
        ("human", pergunta),
    ]

    resposta = chat.invoke(mensagens)
    return resposta.content


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    await update.message.reply_text(
        "Olá! Sou o NetHelp N1, assistente de triagem para problemas "
        "de internet. Descreva o que está acontecendo. 🚀"
    )


async def reset(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    context.chat_data.clear()
    await update.message.reply_text(
        "Conversa reiniciada. O histórico foi apagado."
    )


async def responder(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    pergunta = update.message.text
    historico = context.chat_data.setdefault("historico", [])

    banco_vetorial = context.bot_data["banco_vetorial"]

    resposta = conversar(
        pergunta,
        historico,
        banco_vetorial,
    )

    historico.append(("human", pergunta))
    historico.append(("ai", resposta))
    historico[:] = historico[-MAX_MENSAGENS_HISTORICO:]

    await update.message.reply_text(resposta)


def main():
    banco_vetorial = carregar_ou_criar_banco_vetorial()

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.bot_data["banco_vetorial"] = banco_vetorial

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            responder,
        )
    )
    app.run_polling()


if __name__ == "__main__":
    main()
