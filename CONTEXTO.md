# Contexto do projeto (para continuar em uma nova conversa)

Cole este arquivo e o zip na nova conversa. Responda sempre em português do Brasil.

## Quem é a usuária e o objetivo
- Michelle (Brasil). Já tem no ar o site "Curadoria do Daniel" (som, transmissão, notebooks; tema escuro),
  no GitHub Pages do usuário `achadosbortone`, publicado a partir da pasta /docs do repositório.
- Agora quer um SEGUNDO site, em OUTRO repositório: "Papelaria da Bella", para a filha Isabella (17 anos).
  Gostos: pintura, material de scrapbook, adesivos, garrafinhas. NÃO gosta de rosa: tema verde e bege pastel.
- Objetivo: renda por comissão de afiliado do Mercado Livre, atualização diária, só produtos de qualidade
  de lojas bem avaliadas, ordenados por (1) qualidade/marca, (2) reputação da loja, (3) menor preço.

## Como o projeto funciona
- `gerar_site.py` + `template.html` + `config.json` geram `docs/index.html` e `docs/dados.json` (cache).
- Roda no PC Windows da usuária com duplo clique em `atualizar.bat` (tem as chaves; nunca subir ao GitHub).
  Ela tem Python (comando `py`). Depois ela envia `docs/index.html` e `docs/dados.json` ao GitHub pelo site
  (Add file > Upload files, dentro da pasta docs, e clica em Commit changes).
- GitHub Actions NÃO funciona: o Mercado Livre devolve 403 para IPs do GitHub. Não criar workflow.
- Chaves do app (client_credentials): ML_CLIENT_ID e ML_CLIENT_SECRET, as mesmas do outro site servem.
- Afiliado: ML_MATT_TOOL=22937192 e ML_MATT_WORD=especial (já confirmados no link dela). O script anexa
  `?matt_tool=...&matt_word=...` ao link do anúncio. Compra pelo próprio link não gera comissão.

## O que a API do Mercado Livre permite para este app
- BLOQUEADO (403): /sites/MLB/search, /items multiget, /reviews, /sites/MLB/categories.
- FUNCIONA: /products/search, /products/{id}, /products/{id}/items (ofertas com preço, seller_id,
  official_store_id, original_price, deal_ids, shipping), /users/{seller_id} (reputação).
- 429 tratado com repetição e espera. Produtos de catálogo antigos devolvem 404 em /items (sem anúncios).

## Regras de qualidade
- Marca: listas `marcas_premium` (qualidade 3) e `marcas_confiaveis` (2) por categoria em config.json.
  Categoria com as duas listas vazias não filtra por marca (usada em Scrapbook e Adesivos).
- Loja: oficial (3) > MercadoLíder Platinum (2) > Gold (1) > reputação verde `5_green` com 100+ vendas (0.5,
  selo "Boa reputação"; ativada por "verde" em niveis_aceitos). Nível 4_light_green é recusado de propósito.
- Ordem: chave_ordem = (-qualidade, -nível da loja, preço).

## Layout (já resolvido)
- Cards todos do mesmo tamanho: grade com minmax(190px), 2 colunas no celular, moldura de foto 4:3 fixa
  (img absoluta com object-fit:contain), título em 2 linhas, etiquetas com altura fixa.

## Lições de operação (Windows)
- Navegador renomeia downloads repetidos para "(1)": apagar os arquivos antigos antes de substituir.
- atualizar.bat deve ficar ASCII/ANSI com quebras CRLF.
- Se o GitHub não atualiza: arquivos foram para a pasta errada (precisa ser /docs) ou faltou "Commit changes".
- Pages demora 1 a 2 minutos; testar em aba anônima / Ctrl+F5.

## Estado da Papelaria da Bella
- Pasta pronta com 6 categorias: Pintura e arte, Scrapbook e papéis, Adesivos e washi tape,
  Garrafinhas e copos, Cadernos/planners/agendas, Canetas e lettering. Prévia visual conferida (tema verde-bege).
- Ainda NÃO testado com dados reais do Mercado Livre (o ambiente da IA não alcança a API).
- Próximos passos: criar o repositório novo, rodar atualizar.bat, enviar docs, ler o log de descartes por
  categoria e ajustar marcas/buscas/preço mínimo em config.json; opcional: categoria de estojos e mochilas.
