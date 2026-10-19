# Papelaria da Bella

Site de achados do Mercado Livre (pintura, scrapbook, adesivos, cadernos, garrafinhas e canetas),
com link de afiliado, lojas bem avaliadas e menor preço. Gerado por `gerar_site.py`.

## Passo a passo
1. Crie um repositório NOVO no GitHub (ex.: `papelaria-da-bella`, público).
2. Envie os arquivos desta pasta (menos o `atualizar.bat`, que tem suas chaves).
3. Settings > Pages > Deploy from a branch > main > /docs.
4. Abra o `atualizar.bat` no Bloco de Notas e preencha ML_CLIENT_ID, ML_CLIENT_SECRET,
   ML_MATT_TOOL e ML_MATT_WORD (as mesmas chaves e a mesma etiqueta do outro site servem).
5. Duplo clique no `atualizar.bat`. Ele cria a pasta `docs`.
6. No GitHub, abra a pasta `docs`, Add file > Upload files, envie `index.html` e `dados.json`
   (e `.nojekyll`, se aparecer) e clique em Commit changes.
7. O site fica em https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/
8. Repita os passos 5 e 6 uma vez por dia.

Categorias, marcas e preços mínimos ficam em `config.json`. Em "Scrapbook" e "Adesivos" as listas de
marcas estão vazias de propósito (aceita qualquer marca; o filtro é a reputação da loja).
