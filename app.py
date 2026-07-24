import logging
import os
from contextlib import asynccontextmanager
from json import JSONDecodeError
from secrets import compare_digest

import uvicorn
from dotenv import load_dotenv
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from telegram import Update

from bot import criar_aplicacao_telegram


load_dotenv()

TELEGRAM_WEBHOOK_SECRET = os.getenv(
    "TELEGRAM_WEBHOOK_SECRET"
)
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

if not TELEGRAM_WEBHOOK_SECRET:
    raise RuntimeError(
        "TELEGRAM_WEBHOOK_SECRET não encontrado."
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)

aplicacao_telegram = criar_aplicacao_telegram(
    usar_updater=False
)


def obter_url_webhook() -> str | None:
    if not RENDER_EXTERNAL_URL:
        return None

    endereco_base = RENDER_EXTERNAL_URL.rstrip("/")

    return f"{endereco_base}/telegram"


async def receber_webhook(request: Request) -> Response:
    segredo_recebido = request.headers.get(
        "X-Telegram-Bot-Api-Secret-Token",
        "",
    )

    if not compare_digest(
        segredo_recebido,
        TELEGRAM_WEBHOOK_SECRET,
    ):
        return JSONResponse(
            {"erro": "Acesso negado."},
            status_code=403,
        )

    try:
        dados = await request.json()
    except (JSONDecodeError, UnicodeDecodeError):
        return JSONResponse(
            {"erro": "JSON inválido."},
            status_code=400,
        )

    if not isinstance(dados, dict):
        return JSONResponse(
            {"erro": "Atualização inválida."},
            status_code=400,
        )

    atualizacao = Update.de_json(
        dados,
        aplicacao_telegram.bot,
    )

    if atualizacao is None:
        return JSONResponse(
            {"erro": "Atualização inválida."},
            status_code=400,
        )

    await aplicacao_telegram.update_queue.put(
        atualizacao
    )

    return Response(status_code=200)


async def verificar_saude(
    _: Request,
) -> JSONResponse:
    return JSONResponse(
        {
            "status": "ok",
            "telegram": (
                "running"
                if aplicacao_telegram.running
                else "stopped"
            ),
        }
    )


@asynccontextmanager
async def lifespan(_: Starlette):
    async with aplicacao_telegram:
        url_webhook = obter_url_webhook()

        if url_webhook:
            await aplicacao_telegram.bot.set_webhook(
                url=url_webhook,
                secret_token=TELEGRAM_WEBHOOK_SECRET,
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=False,
            )

            logger.info(
                "Webhook configurado em %s",
                url_webhook,
            )
        else:
            logger.warning(
                "RENDER_EXTERNAL_URL ausente. "
                "O webhook não será registrado localmente."
            )

        await aplicacao_telegram.start()

        try:
            yield
        finally:
            await aplicacao_telegram.stop()


app = Starlette(
    routes=[
        Route(
            "/health",
            verificar_saude,
            methods=["GET"],
        ),
        Route(
            "/telegram",
            receber_webhook,
            methods=["POST"],
        ),
    ],
    lifespan=lifespan,
)


if __name__ == "__main__":
    porta = int(os.getenv("PORT", "8000"))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=porta,
    )