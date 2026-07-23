---
document_id: nethelp-n1-base-conhecimento-v1
title: Base de Conhecimento RAG - NetHelp N1
version: 1.1
updated_at: 2026-07-23
language: pt-BR
scope: Triagem N1 de problemas de internet e rede em ambientes domésticos e pequenos escritórios
platforms: Windows 10 e Windows 11
---

# Base de Conhecimento RAG - NetHelp N1

## Objetivo e limites

Este documento fornece conhecimento técnico para um assistente de triagem N1 de problemas de internet e rede. Ele deve apoiar a identificação do escopo do incidente, a escolha de verificações simples e seguras, a interpretação de resultados e a preparação de um encaminhamento para suporte humano.

O conteúdo não autoriza o assistente a acessar dispositivos, roteadores, contas ou sistemas. O assistente deve orientar o usuário e interpretar somente informações fornecidas por ele. O diagnóstico deve distinguir:

- **Fato observado:** informação fornecida pelo usuário ou resultado de uma verificação.
- **Hipótese:** explicação compatível com os fatos, mas ainda não confirmada.
- **Causa confirmada:** causa demonstrada por uma verificação específica ou por intervenção técnica autorizada.

O escopo N1 inclui verificações reversíveis e de baixo risco. Ele não inclui alteração de firmware, edição do Registro do Windows, configuração administrativa de roteadores, redefinição de fábrica, desativação de firewall ou antivírus, coleta de senhas ou procedimentos ofensivos.

## Princípios da triagem

Antes de sugerir uma ação, determine o máximo possível com as informações já fornecidas. Não repita perguntas respondidas.

Ordem recomendada:

1. Descobrir se o problema afeta um dispositivo ou vários dispositivos.
2. Identificar se a conexão é Wi-Fi, cabo Ethernet ou ambas.
3. Classificar o sintoma: sem internet, lentidão, instabilidade ou falha em um serviço específico.
4. Verificar se o dispositivo permanece conectado à rede local.
5. Observar sinais físicos relevantes, como LEDs de link, Internet, PON ou LOS, sem presumir que os nomes são iguais em todos os equipamentos.
6. Orientar uma verificação ou ação por vez.
7. Interpretar o resultado antes de escolher a próxima etapa.
8. Encaminhar quando o limite do N1 for atingido, houver risco ou o usuário solicitar atendimento humano.

## Isolamento: um dispositivo ou toda a rede

Quando somente um dispositivo apresenta falha e outros dispositivos
conectados à mesma rede acessam a internet normalmente, o alcance do
problema provavelmente está limitado ao dispositivo afetado. Isso não
confirma a causa específica.

Próximos passos N1:

1. confirmar se o dispositivo permanece conectado à rede;
2. consultar IPv4, máscara, gateway e DNS com `ipconfig /all`;
3. testar o dispositivo em outra rede, como um hotspot, se disponível.

Não concluir falha de DHCP, DNS ou adaptador sem uma evidência específica.

Quando todos os dispositivos falham ao mesmo tempo, investigar modem,
roteador, LEDs e possível falha externa. Isso não confirma sozinho uma
indisponibilidade da operadora.

## Matriz inicial de interpretação

| Evidência observada | Interpretação possível | O que ainda não está provado | Próximo passo N1 |
|---|---|---|---|
| Um dispositivo falha e outros funcionam | Problema localizado no dispositivo ou na relação dele com a rede | Não prova defeito de hardware | Verificar tipo de conexão, IP, gateway e teste em outra rede |
| Todos os dispositivos falham | Problema compartilhado na rede, no modem, no roteador ou na operadora | Não prova indisponibilidade da operadora | Observar LEDs e reiniciar uma vez, se autorizado |
| Wi-Fi conectado, mas sem internet | O enlace Wi-Fi existe, mas a conectividade IP ou externa pode estar falhando | Não prova problema de DNS | Verificar IP, gateway e conectividade |
| IPv4 em 169.254.x.x | O dispositivo está usando endereço IPv4 link-local/APIPA | Não prova que o DHCP do roteador está desativado | Verificar gateway, DHCP e renovação de endereço |
| IP público responde, mas nome não resolve | Há indício de falha de resolução de nomes | Não identifica sozinho qual servidor ou configuração falhou | Usar `nslookup` e verificar DNS configurado |
| Gateway responde, mas destino externo não | A comunicação local com o roteador funciona | Não prova falha da operadora; ICMP pode ser filtrado | Comparar dispositivos e observar modem/roteador |
| Gateway não responde | Pode haver falha entre dispositivo e rede local | Não prova que o roteador está desligado | Conferir conexão, IP, cabo ou Wi-Fi |
| Um único site ou aplicativo falha | Pode ser falha do serviço, aplicativo, DNS específico, bloqueio ou configuração local | Não prova problema geral de internet | Testar outros serviços e outro dispositivo |

## Wi-Fi conectado, mas sem internet

### Sintomas

- O dispositivo exibe o nome da rede como conectado.
- O Windows pode mostrar “Sem internet”.
- Sites e aplicativos não carregam ou funcionam de forma intermitente.

### Verificações N1

1. Confirmar se outros dispositivos na mesma rede funcionam.
2. Confirmar se o problema ocorre somente no Wi-Fi ou também por cabo.
3. Verificar se o dispositivo permanece conectado ou se desconecta.
4. Consultar `ipconfig /all` no Windows e observar IPv4, máscara, gateway padrão, DHCP habilitado e servidores DNS.
5. Se houver gateway, testar a comunicação com ele usando `ping <gateway>`.
6. Se o dispositivo funcionar em um hotspot do celular, registrar que a conectividade básica do dispositivo funciona em outra rede. Isso reduz a probabilidade de uma falha geral do adaptador, mas não identifica sozinho a causa na rede doméstica.

### Ações seguras

- Desconectar e conectar novamente ao Wi-Fi.
- Esquecer a rede e reconectar somente se o usuário tiver acesso legítimo à senha. O bot nunca deve pedir que a senha seja enviada.
- Reiniciar o dispositivo uma vez.
- Reiniciar modem e roteador uma vez, com autorização e aviso de que outros usuários serão desconectados temporariamente.

### Interpretação

Conectar ao Wi-Fi confirma apenas a associação com o ponto de acesso. Não confirma endereço IP válido, gateway funcional, DNS funcional ou acesso à internet.

## Problemas de cabo Ethernet

### Sintomas

- O Windows mostra cabo desconectado.
- O LED da porta não acende.
- A conexão aparece ativa, mas sem internet.
- A conexão cai quando o cabo é movimentado.

### Verificações N1

1. Confirmar se o cabo está firmemente conectado nas duas extremidades.
2. Observar o LED de link da porta, quando existir.
3. Testar outro cabo conhecido como funcional.
4. Testar outra porta LAN autorizada no roteador ou switch.
5. Consultar `ipconfig /all` e verificar endereço, máscara e gateway.

### Interpretação

- Ausência de link em mais de um cabo e porta pode indicar problema na interface de rede, no equipamento ou na configuração, mas exige suporte técnico.
- Link ativo não garante acesso à internet.
- Um cabo danificado pode causar perda total, negociação instável ou redução de desempenho.

Não oriente o usuário a alterar configurações administrativas de switch, VLAN ou roteador durante a triagem N1.

## DHCP e endereço APIPA

### Função do DHCP

O DHCP fornece parâmetros de configuração aos clientes de uma rede, incluindo endereço IP e outras opções necessárias. A obtenção de um endereço por DHCP segue um modelo cliente-servidor. [F6]

### O que significa 169.254.x.x

No Windows, um adaptador configurado para obter endereço automaticamente pode atribuir a si mesmo um endereço no intervalo `169.254.0.0/16` quando uma configuração DHCP utilizável não está disponível. Esse mecanismo é conhecido como APIPA ou IPv4 link-local. [F1] [F7]

Um endereço link-local serve para comunicação limitada no mesmo enlace. Ele não é encaminhado normalmente por roteadores e não oferece, por si só, uma rota normal para a internet. [F1] [F7]

Encontrar `169.254.x.x` é uma evidência forte de que o dispositivo não obteve uma configuração IPv4 roteável. Isso **não confirma sozinho** que:

- o DHCP do roteador está desativado;
- o roteador está defeituoso;
- a placa de rede está defeituosa;
- a operadora está indisponível.

Também podem existir problemas de comunicação com o ponto de acesso, segmentação de rede, cliente DHCP, políticas de rede ou indisponibilidade temporária do servidor.

### Verificações N1

Solicitar o resultado de:

```text
ipconfig /all
```

Observar:

- DHCP habilitado;
- IPv4;
- máscara de sub-rede;
- gateway padrão;
- servidores DNS;
- adaptador relevante.

Se o IPv4 for `169.254.x.x`, a máscara for `255.255.0.0` e não houver gateway, registrar:

- fato: o dispositivo está usando endereço link-local/APIPA;
- hipótese: falha na obtenção de configuração IPv4 por DHCP;
- causa: não confirmada.

Uma ação N1 possível é:

```text
ipconfig /renew
```

O comando solicita renovação da configuração DHCP em adaptadores configurados automaticamente. [F2]

### Interpretação de resultados

- **Recebeu endereço privado e gateway após renovar:** a conectividade pode ter sido restaurada; a causa original permanece não confirmada.
- **Não foi possível contatar o servidor DHCP:** reforça a hipótese de falha no processo DHCP, mas ainda não mostra onde está a falha.
- **Funciona no hotspot e recebe endereço válido:** o dispositivo consegue obter configuração em outra rede; a investigação deve se concentrar na rede doméstica ou na relação entre ela e o dispositivo.
- **Outros dispositivos novos também recebem 169.254.x.x:** aumenta a suspeita de indisponibilidade do DHCP compartilhado.
- **Outros dispositivos funcionam:** eles podem possuir concessões anteriores; isso não elimina totalmente uma falha atual do DHCP.

### Encaminhamento

Encaminhe se a renovação falhar, uma reinicialização autorizada do equipamento não resolver ou for necessária alteração administrativa no DHCP. Não recomende IP estático aleatório, edição do Registro ou redefinição de fábrica.

## Falha de DNS

### Função do DNS

O DNS converte nomes, como `example.com`, em endereços usados na comunicação IP. Uma falha de resolução pode impedir o acesso por nome mesmo quando existe conectividade por endereço IP.

### Indícios

- Um endereço IP externo conhecido responde, mas um nome não é localizado.
- `nslookup example.com` apresenta tempo limite, ausência de resposta ou falha do servidor.
- Vários sites deixam de abrir por nome, mas a conectividade IP permanece disponível.

O comando `ping` pode testar um destino por IP ou nome. Se o teste por IP funciona e por nome falha, pode existir problema de resolução de nomes. Esse resultado é um indício, não uma confirmação completa, porque ICMP pode ser bloqueado e destinos podem responder de formas diferentes. [F3]

### Verificações N1

1. Confirmar se existe IPv4 válido e gateway.
2. Testar o gateway.
3. Comparar um teste por IP com um teste por nome.
4. Executar:

```text
nslookup example.com
```

O `nslookup` usa o servidor DNS padrão quando um segundo servidor não é especificado e fornece mensagens úteis para diagnóstico. [F4]

5. Se autorizado, comparar com um resolvedor conhecido:

```text
nslookup example.com 1.1.1.1
```

### Interpretação

- **Servidor padrão falha e servidor alternativo responde:** há indício de problema no caminho ou no serviço DNS padrão. A causa exata ainda pode estar no roteador, no provedor ou na configuração do dispositivo.
- **Ambos falham e não há acesso por IP:** o problema provavelmente não está restrito ao DNS.
- **Nome resolve, mas o site não abre:** investigar conectividade, aplicação, proxy, VPN ou o próprio serviço.

Uma ação simples possível no Windows é:

```text
ipconfig /flushdns
```

Esse comando limpa o cache do resolvedor DNS. Ele não corrige um servidor DNS indisponível nem uma falha de conectividade. [F2]

Alterar permanentemente o DNS deve ser uma ação autorizada e reversível. Não trate a troca de DNS como solução universal.

## Gateway, roteador, modem e operadora

### Gateway padrão

O gateway padrão normalmente representa o equipamento usado para alcançar outras redes. Seu endereço pode ser consultado com `ipconfig`.

Teste:

```text
ping <gateway>
```

### Interpretação

- **Gateway responde:** há comunicação IP local com o equipamento. Isso não garante acesso externo.
- **Gateway não responde:** pode haver problema local, mas alguns equipamentos filtram ICMP. Combine o resultado com IP, conexão e outros dispositivos.
- **Todos os dispositivos falham:** aumenta a probabilidade de problema compartilhado.

### LEDs

Os nomes e significados variam conforme fabricante e operadora. Exemplos comuns:

- **Power:** alimentação.
- **Internet/WAN:** estado da conexão externa, conforme o fabricante.
- **PON:** registro em redes ópticas, conforme a operadora.
- **LOS:** perda de sinal óptico; vermelho ou piscando pode exigir contato com a operadora.
- **LAN:** link por cabo.
- **Wi-Fi/WLAN:** rádio sem fio ativo.

Nunca afirme que uma luz confirma uma causa sem conhecer o modelo e a documentação. Registre exatamente o que o usuário observa.

### Reinicialização segura

Reiniciar modem e roteador pode restabelecer sessões e conexões. Antes:

- avisar que todos os usuários serão desconectados temporariamente;
- obter autorização;
- executar apenas uma vez;
- aguardar a inicialização completa;
- não pressionar o botão de reset.

Reset de fábrica apaga configurações e não pertence ao procedimento N1 padrão.

## Lentidão

### Informações necessárias

- Um ou todos os dispositivos.
- Wi-Fi, cabo ou ambos.
- Horários e frequência.
- Distância do roteador e obstáculos.
- Aplicativos ou serviços afetados.
- Uso simultâneo da rede.
- Plano contratado, se o usuário souber.

### Verificações N1

1. Comparar outro dispositivo no mesmo local.
2. Comparar Wi-Fi e cabo, quando possível.
3. Aproximar-se do roteador sem alterar configurações.
4. Verificar se downloads, backups ou atualizações estão consumindo banda.
5. Executar teste de velocidade em condição controlada, registrando horário, dispositivo, conexão e servidor do teste.
6. Usar `ping` para observar latência e perda, lembrando que ICMP pode receber tratamento diferente do tráfego de aplicações.

### Interpretação

- Lentidão somente no Wi-Fi e próxima a interferências pode estar relacionada ao ambiente sem fio.
- Lentidão em todos os dispositivos e também por cabo pode envolver roteador, modem, congestionamento ou provedor.
- Um único teste de velocidade não confirma descumprimento do plano.
- Alta latência distante geograficamente pode ser normal; compare destinos e horários.

## Conexão instável

Primeiro diferencie:

- o dispositivo desconecta do Wi-Fi;
- o Wi-Fi permanece conectado, mas a internet cai;
- somente um aplicativo perde conexão;
- todos os dispositivos caem simultaneamente.

Colete:

- horários aproximados;
- duração das quedas;
- dispositivos afetados;
- estado dos LEDs durante a falha;
- resultado por Wi-Fi e cabo;
- alterações recentes.

Se o Wi-Fi desconecta somente em um dispositivo, considere adaptador, driver, economia de energia, intensidade de sinal e compatibilidade como hipóteses. Não recomende desinstalação de driver sem preparação para recuperação.

Se todos os dispositivos perdem acesso e uma luz externa muda ao mesmo tempo, registre a correlação e encaminhe com esses dados. Correlação não é prova definitiva da causa.

## VPN, proxy, firewall e antivírus

Uma VPN ou proxy pode alterar a rota e a resolução de nomes. Pergunte se o usuário sabe que está usando algum desses recursos e se o problema começou após uma mudança.

Não peça credenciais e não recomende desativar firewall ou antivírus. Se uma proteção for hipótese relevante, encaminhe para análise autorizada. Como alternativa segura, pode-se:

- verificar se uma VPN reconhecida aparece como conectada;
- comparar o comportamento antes e depois de encerrar voluntariamente uma sessão VPN pessoal, se o usuário estiver autorizado;
- verificar as configurações de proxy sem alterar valores desconhecidos;
- testar outro serviço para definir o escopo.

Em equipamentos corporativos, não oriente mudanças sem autorização.

## Falha em um site ou aplicativo

Se outros sites funcionam:

1. confirmar se a falha ocorre em outro dispositivo;
2. registrar a mensagem de erro exata;
3. testar outro navegador somente para isolar aplicação;
4. verificar resolução DNS do domínio;
5. considerar indisponibilidade do serviço como hipótese, nunca como fato sem fonte confiável;
6. não abrir links enviados pelo usuário nem afirmar que acessou o serviço.

Falha em um serviço específico não deve ser tratada automaticamente como falha geral de internet.

## Referência de comandos do Windows

### Exibir configuração

```text
ipconfig /all
```

Mostra a configuração TCP/IP completa dos adaptadores, incluindo IPv4, máscara, gateway, DHCP e DNS. [F2]

### Renovar DHCP

```text
ipconfig /renew
```

Solicita renovação da configuração DHCP para adaptadores configurados automaticamente. Pode falhar se o servidor DHCP não estiver alcançável. [F2]

### Limpar cache DNS

```text
ipconfig /flushdns
```

Limpa o cache local do resolvedor DNS. Não altera o servidor configurado. [F2]

### Testar gateway

```text
ping 192.168.1.1
```

Substituir pelo gateway real informado por `ipconfig`. Uma resposta indica comunicação ICMP local; ausência de resposta não prova sozinha que o equipamento está desligado. [F3]

### Comparar IP e nome

```text
ping 1.1.1.1
ping example.com
```

Se o primeiro funciona e o segundo falha por não localizar o host, existe indício de resolução de nomes. Não conclua a causa sem `nslookup` e demais evidências. [F3]

### Consultar DNS

```text
nslookup example.com
```

Usa o servidor DNS padrão e mostra informações úteis sobre a consulta. [F4]

### Observar o caminho

```text
tracert /d 1.1.1.1
```

Mostra saltos observáveis até o destino. Asteriscos podem representar equipamentos que não respondem a ICMP e não provam necessariamente perda de conectividade. [F5]

### Regras para comandos

- Explicar o objetivo antes de pedir a execução.
- Pedir somente um comando ou ação por vez.
- Não solicitar saída contendo credenciais ou dados sensíveis.
- Interpretar somente o adaptador relevante.
- Não executar comandos destrutivos ou administrativos avançados.

## Encaminhamento para suporte humano

Encaminhe quando:

- o usuário solicitar atendimento humano;
- houver risco físico, elétrico ou de segurança;
- forem necessárias credenciais ou configuração administrativa;
- o problema persistir após as ações N1 permitidas;
- houver indício de falha da operadora ou do equipamento;
- o diagnóstico exigir captura de pacotes, logs avançados, firmware, driver ou acesso remoto;
- as evidências forem contraditórias.

Use este formato:

```text
Resumo para o suporte:
- Problema relatado:
- Dispositivos afetados:
- Tipo de conexão:
- Verificações realizadas:
- Resultados:
- Hipótese atual:
```

Regras:

- Usar “Não informado” para fatos que o usuário não forneceu.
- Usar “Não verificado” para verificações ou resultados que não ocorreram.
- Usar “Causa não confirmada” quando as verificações não demonstrarem a causa.
- Não inventar modelo do equipamento, operadora, IP, luzes ou ações.
- Não continuar fazendo perguntas depois do resumo.

## Casos de referência

### Caso A - APIPA em um notebook

Fatos:

- notebook conecta ao Wi-Fi, mas fica sem internet;
- celular e televisão funcionam;
- IPv4 `169.254.73.21`;
- máscara `255.255.0.0`;
- sem gateway;
- `ipconfig /renew` não contata servidor DHCP;
- hotspot funciona.

Interpretação:

- fato: endereço link-local/APIPA e ausência de gateway;
- hipótese: falha na obtenção de configuração DHCP na rede doméstica;
- causa: não confirmada;
- encaminhamento: necessário se renovação e uma reinicialização autorizada não resolverem.

### Caso B - Indício de DNS

Fatos:

- IP e gateway válidos;
- gateway responde;
- teste por IP externo funciona;
- nome não é localizado;
- `nslookup` no servidor padrão falha.

Interpretação:

- fato: conectividade IP observada e falha de consulta pelo servidor padrão;
- hipótese: falha de DNS padrão ou no caminho até ele;
- causa exata: não confirmada;
- próximo passo: comparar consulta autorizada e encaminhar se persistir.

### Caso C - Todos os dispositivos sem internet

Fatos:

- Wi-Fi e cabo afetados;
- vários dispositivos sem acesso;
- reinicialização única não resolveu;
- LED LOS vermelho, segundo relato do usuário.

Interpretação:

- fato: falha compartilhada e alteração observada no equipamento óptico;
- hipótese: perda de sinal ou falha externa;
- causa: depende do modelo e da confirmação da operadora;
- encaminhamento: operadora ou suporte responsável.

## Glossário

- **APIPA:** mecanismo de atribuição automática de endereço IPv4 link-local no Windows.
- **DHCP:** protocolo que entrega parâmetros de configuração de rede a clientes.
- **DNS:** sistema de resolução de nomes.
- **Gateway padrão:** destino usado para alcançar outras redes.
- **ICMP:** protocolo usado por ferramentas como `ping` e `tracert`.
- **IP link-local:** endereço válido somente no enlace local e não destinado a roteamento normal.
- **LAN:** rede local.
- **N1:** primeiro nível de atendimento e triagem.
- **Roteador:** equipamento que encaminha tráfego entre redes.
- **Switch:** equipamento que conecta dispositivos em uma rede local.

## Fontes

- **[F1] Microsoft Learn - Como usar o endereçamento TCP/IP automático sem um servidor DHCP.**
  https://learn.microsoft.com/pt-br/windows-server/troubleshoot/how-to-use-automatic-tcpip-addressing-without-a-dh

- **[F2] Microsoft Learn - ipconfig.**
  https://learn.microsoft.com/pt-br/windows-server/administration/windows-commands/ipconfig

- **[F3] Microsoft Learn - ping.**
  https://learn.microsoft.com/pt-br/windows-server/administration/windows-commands/ping

- **[F4] Microsoft Learn - nslookup.**
  https://learn.microsoft.com/pt-br/windows-server/administration/windows-commands/nslookup

- **[F5] Microsoft Learn - tracert.**
  https://learn.microsoft.com/pt-br/windows-server/administration/windows-commands/tracert

- **[F6] RFC 2131 - Dynamic Host Configuration Protocol.**
  https://www.rfc-editor.org/rfc/rfc2131.html

- **[F7] RFC 3927 - Dynamic Configuration of IPv4 Link-Local Addresses.**
  https://www.rfc-editor.org/rfc/rfc3927.html

- **[F8] Microsoft Support - Corrigir problemas de conexão Wi-Fi no Windows.**
  https://support.microsoft.com/pt-BR/Windows/Experience/Connectivity-Networking/fix-wi-fi-connection-issues-in-windows

## Controle de versão

- **Versão 1.0 - 2026-07-23:** primeira base de conhecimento do NetHelp N1, cobrindo triagem, Wi-Fi, Ethernet, DHCP/APIPA, DNS, gateway, modem, roteador, lentidão, instabilidade, segurança, comandos e encaminhamento.
