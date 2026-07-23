import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)


DIRETORIO_PROJETO = Path(__file__).resolve().parent
CAMINHO_CONHECIMENTO = (
    DIRETORIO_PROJETO
    / "knowledge"
    / "nethelp-n1-base-conhecimento.md"
)

CAMINHO_INDICE = (
    DIRETORIO_PROJETO
    / "vectorstore"
    / "nethelp-n1-granite-97m-v2.json"
)

CABECALHOS_PARA_DIVISAO = [
    ("#", "titulo"),
    ("##", "secao"),
    ("###", "subsecao"),
]

TAMANHO_CHUNK = 2000
SOBREPOSICAO_CHUNK = 200

MODELO_EMBEDDING = (
    "ibm-granite/granite-embedding-97m-multilingual-r2"
)
PROVEDOR_EMBEDDING = "hf-inference"
QUANTIDADE_PADRAO_RESULTADOS = 3


def separar_front_matter(texto):
    linhas = texto.splitlines()

    if not linhas or linhas[0].strip() != "---":
        return {}, texto

    fim_front_matter = None

    for indice, linha in enumerate(linhas[1:], start=1):
        if linha.strip() == "---":
            fim_front_matter = indice
            break

    if fim_front_matter is None:
        raise ValueError(
            "O front matter foi iniciado, mas não foi finalizado."
        )

    metadados = {}

    for linha in linhas[1:fim_front_matter]:
        chave, separador, valor = linha.partition(":")

        if separador:
            metadados[chave.strip()] = valor.strip()

    conteudo = "\n".join(
        linhas[fim_front_matter + 1:]
    ).lstrip()

    return metadados, conteudo


def carregar_secoes():
    if not CAMINHO_CONHECIMENTO.exists():
        raise FileNotFoundError(
            f"Base de conhecimento não encontrada: "
            f"{CAMINHO_CONHECIMENTO}"
        )

    texto_original = CAMINHO_CONHECIMENTO.read_text(
        encoding="utf-8"
    )

    metadados_documento, texto = separar_front_matter(
        texto_original
    )

    divisor_markdown = MarkdownHeaderTextSplitter(
        headers_to_split_on=CABECALHOS_PARA_DIVISAO,
        strip_headers=False,
    )

    secoes = divisor_markdown.split_text(texto)

    fonte = CAMINHO_CONHECIMENTO.relative_to(
        DIRETORIO_PROJETO
    ).as_posix()

    for secao in secoes:
        for chave, valor in metadados_documento.items():
            secao.metadata.setdefault(chave, valor)

        secao.metadata["fonte"] = fonte

    return secoes


def enriquecer_chunks(chunks):
    chunks_enriquecidos = []

    for chunk in chunks:
        rotulos = []

        nome_secao = chunk.metadata.get("secao")
        nome_subsecao = chunk.metadata.get("subsecao")

        if nome_secao:
            rotulos.append(f"Seção: {nome_secao}")

        if nome_subsecao:
            rotulos.append(f"Subseção: {nome_subsecao}")

        prefixo = "\n".join(rotulos)
        conteudo = chunk.page_content

        if prefixo:
            conteudo = f"{prefixo}\n\n{conteudo}"

        chunks_enriquecidos.append(
            Document(
                page_content=conteudo,
                metadata=chunk.metadata.copy(),
            )
        )

    return chunks_enriquecidos


def criar_chunks(secoes):
    divisor_recursivo = RecursiveCharacterTextSplitter(
        chunk_size=TAMANHO_CHUNK,
        chunk_overlap=SOBREPOSICAO_CHUNK,
        length_function=len,
    )

    chunks_divididos = divisor_recursivo.split_documents(secoes)
    chunks = enriquecer_chunks(chunks_divididos)

    if secoes:
        document_id = secoes[0].metadata.get(
            "document_id",
            CAMINHO_CONHECIMENTO.stem,
        )
    else:
        document_id = CAMINHO_CONHECIMENTO.stem

    for indice, chunk in enumerate(chunks, start=1):
        chunk.metadata["chunk_id"] = (
            f"{document_id}-{indice:03d}"
        )

    return chunks


def criar_embeddings():
    load_dotenv()

    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    if not token:
        raise RuntimeError(
            "HUGGINGFACEHUB_API_TOKEN não encontrado."
        )

    return HuggingFaceEndpointEmbeddings(
        model=MODELO_EMBEDDING,
        task="feature-extraction",
        provider=PROVEDOR_EMBEDDING,
        huggingfacehub_api_token=token,
    )


def criar_banco_vetorial(chunks):
    if not chunks:
        raise ValueError(
            "Não é possível criar o banco vetorial sem chunks."
        )

    embeddings = criar_embeddings()

    banco_vetorial = InMemoryVectorStore(
        embedding=embeddings
    )

    ids = [
        chunk.metadata["chunk_id"]
        for chunk in chunks
    ]

    banco_vetorial.add_documents(
        documents=chunks,
        ids=ids,
    )

    return banco_vetorial


def salvar_banco_vetorial(banco_vetorial):
    banco_vetorial.dump(str(CAMINHO_INDICE))

    return CAMINHO_INDICE


def carregar_banco_vetorial():
    if not CAMINHO_INDICE.exists():
        raise FileNotFoundError(
            f"Índice vetorial não encontrado: "
            f"{CAMINHO_INDICE}"
        )

    embeddings = criar_embeddings()

    return InMemoryVectorStore.load(
        str(CAMINHO_INDICE),
        embedding=embeddings,
    )


def buscar_chunks(
    banco_vetorial,
    pergunta,
    quantidade=QUANTIDADE_PADRAO_RESULTADOS,
):
    pergunta = pergunta.strip()

    if not pergunta:
        raise ValueError(
            "A pergunta de busca não pode estar vazia."
        )

    if quantidade < 1:
        raise ValueError(
            "A quantidade de resultados deve ser maior que zero."
        )

    return banco_vetorial.similarity_search_with_score(
        pergunta,
        k=quantidade,
    )


def exibir_diagnostico(secoes, chunks, limite=5):
    print(f"ARQUIVO: {CAMINHO_CONHECIMENTO.name}")
    print(f"SECOES: {len(secoes)}")
    print(f"CHUNKS: {len(chunks)}")

    if not chunks:
        print("Nenhum chunk foi produzido.")
        return

    tamanhos = [
        len(chunk.page_content)
        for chunk in chunks
    ]

    print(f"MENOR_CHUNK: {min(tamanhos)}")
    print(f"MAIOR_CHUNK: {max(tamanhos)}")
    print(
        f"MEDIA_CARACTERES: "
        f"{sum(tamanhos) / len(tamanhos):.1f}"
    )

    for indice, chunk in enumerate(
        chunks[:limite],
        start=1,
    ):
        amostra = chunk.page_content[:200].replace(
            "\n",
            " ",
        )

        print()
        print(f"CHUNK {indice}")
        print(f"METADADOS: {chunk.metadata}")
        print(f"CARACTERES: {len(chunk.page_content)}")
        print(f"CONTEUDO: {amostra}")


if __name__ == "__main__":
    secoes_carregadas = carregar_secoes()
    chunks_criados = criar_chunks(secoes_carregadas)

    exibir_diagnostico(
        secoes_carregadas,
        chunks_criados,
    )
