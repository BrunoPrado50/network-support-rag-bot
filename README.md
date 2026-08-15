# NetHelp N1

Protótipo funcional de um assistente de triagem N1 para problemas de conexão à internet e redes, integrado ao Telegram e apoiado por RAG.

## Objetivo

Orientar verificações iniciais simples e seguras, evitar ações incompatíveis com o problema relatado e preparar um resumo para encaminhamento ao suporte humano quando necessário.

## Funcionalidades

* Atendimento por meio do Telegram;
* triagem de problemas de Wi-Fi, cabo, DNS, DHCP, lentidão e instabilidade;
* orientação de uma verificação por vez;
* histórico recente da conversa;
* consulta semântica a uma base técnica própria;
* geração de resumo para suporte humano;
* comando para reiniciar a conversa;
* funcionamento por webhook em ambiente de deploy.

## Tecnologias

* Python
* LangChain
* Groq
* Hugging Face
* IBM Granite Embeddings
* Telegram Bot API
* Starlette e Uvicorn
* Render

## Demonstração

A aplicação está hospedada no plano gratuito do Render e pode entrar em modo de espera após um período sem uso. Para testar:

1. Acesse [Ativar demonstração](https://network-support-rag-bot.onrender.com/health).
2. Aguarde a página informar `"status": "ok"`.
3. Abra [Conversar com o NetHelp N1 no Telegram](https://t.me/NetHelpN1Bot).

## Como funciona

A mensagem recebida pelo Telegram é combinada ao contexto recente da conversa. O sistema consulta uma base de conhecimento por meio de busca semântica e utiliza uma LLM para produzir a próxima pergunta, orientação ou resumo de encaminhamento.

## Execução local

No PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python bot.py
```

Após criar o arquivo `.env`, preencha as variáveis indicadas em `.env.example`. Tokens e chaves privadas não devem ser enviados ao GitHub.

## Estado do projeto

O NetHelp N1 é um protótipo funcional em desenvolvimento. Ele não acessa dispositivos, roteadores ou sistemas de operadoras e não substitui o diagnóstico de um profissional.

Melhorias planejadas:

* estado estruturado da triagem;
* testes automatizados;
* aprimoramento da memória de conversação;
* ampliação dos cenários de avaliação.
