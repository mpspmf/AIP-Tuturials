# Guia de comunicação e colaboração na AIP

Guia de consulta em português europeu para repetir demonstrações e esclarecer dúvidas sobre comunicação e colaboração na AIP. Inclui os 10 capítulos: utilizar este guia; escolher ferramentas no Teams; conversar no Teams; normas para chats e canais; criar equipas e canais; utilizar canais; agendar no Calendário do Teams; adicionar um calendário de canal; utilizar o Planner; e enviar emails personalizados em série.

As figuras avançam automaticamente de 8 em 8 segundos. A reprodução suspende-se ao pausar, ao passar o ponteiro sobre o carrossel, ao focar os controlos ou ao abrir a visualização ampliada. É possível navegar manualmente; a preferência do sistema por movimento reduzido desativa o avanço automático.

No computador, o índice e as instruções deslocam-se de forma independente, enquanto o título do capítulo e o visualizador permanecem fixos. Em tablets e telemóveis, a página desloca-se normalmente. Clicar num passo ilustrado seleciona a primeira figura associada e pausa o avanço automático; as etiquetas «Figura» selecionam diretamente cada imagem.

O site é local e não requer backend. Não descarrega ficheiros nem configura uma implantação. Os exemplos apresentados são fictícios. Os documentos fonte `AIP_GUIA.docx`, `Lista_Demonstracao_AIP.xlsx` e `Modelo_Convite_AIP.docx` ficam na raiz do repositório.

## Estrutura

- `app/page.tsx` abre a aplicação em `components/guide/`.
- `data/guide.ts` contém o conteúdo tipado e curado; `public/images/` guarda as figuras locais.
- `scripts/extract-guide.py` extrai o conteúdo e as imagens das fontes; `scripts/validate-guide.py` verifica a fidelidade e integridade do conteúdo. Os dois scripts usam Python e `openpyxl`, procuram os documentos na raiz por predefinição e aceitam `--project-dir` para indicar outra localização.

## Desenvolvimento

Recomenda-se Node.js 24; o starter declara Node.js 22.13 ou superior. Na pasta `website/`:

```bash
npm ci
npm run dev
npm run build
npm run typecheck
npm run check:content
```
