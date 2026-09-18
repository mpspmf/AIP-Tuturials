export interface GuideFigure {
  id: number;
  src: string;
  width: number;
  height: number;
  caption: string;
}

export type GuideBlock =
  | { id: string; kind: 'paragraph'; text: string; figureIds?: number[] }
  | { id: string; kind: 'heading'; text: string }
  | { id: string; kind: 'step'; number: number; text: string; figureIds?: number[] }
  | { id: string; kind: 'table'; headers: string[]; rows: string[][] }
  | { id: string; kind: 'callout'; title: string; text: string; figureIds?: number[] }
  | { id: string; kind: 'example'; title: string; text: string };

export interface GuideChapter {
  id: string;
  title: string;
  shortTitle: string;
  intro: string;
  blocks: GuideBlock[];
  figures: GuideFigure[];
}

export const chapters: GuideChapter[] = [
  {
    "id": "01",
    "title": "Como utilizar este guia",
    "shortTitle": "Como utilizar",
    "intro": "Este guia acompanha a formação sobre comunicação e colaboração na AIP. Permite repetir os procedimentos, refazer passos das demonstrações e resolver dúvidas no trabalho diário.",
    "blocks": [
      {
        "id": "01-heading-01",
        "kind": "heading",
        "text": "Aplicações necessárias"
      },
      {
        "id": "01-paragraph-02",
        "kind": "paragraph",
        "text": "Conta profissional Microsoft 365, Microsoft Teams para computador, novo Outlook para Windows e Word e Excel para computador. O envio em série do capítulo 10 requer também o Outlook clássico para Windows instalado e configurado."
      },
      {
        "id": "01-heading-03",
        "kind": "heading",
        "text": "Microsoft Teams"
      },
      {
        "id": "01-paragraph-04",
        "kind": "paragraph",
        "text": "Use o Microsoft Teams para conversar, consultar equipas e canais, agendar reuniões e acompanhar tarefas no Planner."
      },
      {
        "id": "01-heading-05",
        "kind": "heading",
        "text": "Novo Outlook"
      },
      {
        "id": "01-paragraph-06",
        "kind": "paragraph",
        "text": "Use o novo Outlook para trabalhar com o email. Permite também consultar o calendário e agendar reuniões de forma semelhante ao Microsoft Teams."
      },
      {
        "id": "01-heading-07",
        "kind": "heading",
        "text": "Word Excel e Outlook clássico"
      },
      {
        "id": "01-paragraph-08",
        "kind": "paragraph",
        "text": "Use o Excel para organizar os destinatários e os campos de personalização. Use o Word para preparar o modelo e substituir os campos pelos valores da lista. Para enviar os emails em série a partir do Word, utilize o Outlook clássico para Windows, conforme o capítulo 10. O novo Outlook não permite este envio direto."
      }
    ],
    "figures": []
  },
  {
    "id": "02",
    "title": "Escolher a ferramenta dentro do Teams",
    "shortTitle": "Escolher a ferramenta",
    "intro": "Comece pelo tipo de informação que precisa de partilhar. O Teams concentra a colaboração, mas cada área da aplicação tem uma função própria.",
    "blocks": [
      {
        "id": "02-table-01",
        "kind": "table",
        "headers": [
          "Necessidade",
          "Onde trabalhar",
          "Exemplo"
        ],
        "rows": [
          [
            "Esclarecer uma questão breve",
            "Chat do Teams",
            "Confirmar quem revê o programa"
          ],
          [
            "Manter informação para a área",
            "Canal do Teams",
            "Publicar o planeamento de um encontro"
          ],
          [
            "Registar uma ação e um prazo",
            "Planner no Teams",
            "Validar o programa até 9 de outubro"
          ],
          [
            "Agendar e consultar disponibilidade",
            "Calendário do Teams",
            "Marcar a reunião de preparação"
          ]
        ]
      },
      {
        "id": "02-heading-02",
        "kind": "heading",
        "text": "Organização por área operacional"
      },
      {
        "id": "02-paragraph-03",
        "kind": "paragraph",
        "text": "Propõe-se a utilização de uma equipa para cada Área Operacional ou Direção, com os canais necessários configurados pelo diretor ou administrador."
      },
      {
        "id": "02-heading-04",
        "kind": "heading",
        "text": "Manter o contexto"
      },
      {
        "id": "02-paragraph-05",
        "kind": "paragraph",
        "text": "Se uma conversa originar uma decisão relevante para uma Área Operacional, considere partilhar a conclusão dessa conversa no canal adequado da respetiva equipa."
      }
    ],
    "figures": []
  },
  {
    "id": "03",
    "title": "Conversar no Teams",
    "shortTitle": "Conversar no Teams",
    "intro": "Use o chat para esclarecer uma questão curta ou coordenar uma ação com pessoas concretas.",
    "blocks": [
      {
        "id": "03-step-01",
        "kind": "step",
        "number": 1,
        "text": "Abra o Chat através da barra de opções vertical situada à esquerda. No topo do menu, selecione “Nova mensagem” ou “Novo chat”. Na vista combinada, a opção também pode aparecer na seta junto a “Nova mensagem”.",
        "figureIds": [
          1
        ]
      },
      {
        "id": "03-step-02",
        "kind": "step",
        "number": 2,
        "text": "No campo “Para”, procure o destinatário e confirme o endereço da sua conta. Neste passo pode selecionar vários destinatários, criando uma conversa de grupo onde todos os intervenientes podem ler e escrever mensagens.",
        "figureIds": [
          2
        ]
      },
      {
        "id": "03-step-03",
        "kind": "step",
        "number": 3,
        "text": "Escreva o texto na caixa da mensagem. Se precisar de uma nova linha, use o atalho Shift + Enter. Use os ícones junto à caixa de mensagem para abrir a barra de formatação, alterar o estilo do texto, anexar documentos ou enviar a mensagem.",
        "figureIds": [
          3
        ]
      },
      {
        "id": "03-step-04",
        "kind": "step",
        "number": 4,
        "text": "Utilize o botão “Enviar”, situado no canto inferior direito. Na caixa de composição expandida, também pode usar Ctrl + Enter."
      },
      {
        "id": "03-step-05",
        "kind": "step",
        "number": 5,
        "text": "Confirme que a mensagem aparece na conversa, conforme o exemplo.",
        "figureIds": [
          4
        ]
      }
    ],
    "figures": [
      {
        "id": 1,
        "src": "/images/figure-01.png",
        "width": 1919,
        "height": 1028,
        "caption": "Menu Nova mensagem no Chat do Teams para iniciar uma conversa."
      },
      {
        "id": 2,
        "src": "/images/figure-02.png",
        "width": 1919,
        "height": 1030,
        "caption": "Campo Para para procurar e selecionar os destinatários da conversa."
      },
      {
        "id": 3,
        "src": "/images/figure-03.png",
        "width": 1917,
        "height": 1030,
        "caption": "Caixa de mensagem e ícones para formatação, anexos e envio."
      },
      {
        "id": 4,
        "src": "/images/figure-04.png",
        "width": 1919,
        "height": 1029,
        "caption": "Mensagem enviada e apresentada no histórico da conversa."
      }
    ]
  },
  {
    "id": "04",
    "title": "Normas de utilização do chat e dos canais",
    "shortTitle": "Normas de utilização",
    "intro": "Estas regras propostas tornam a comunicação assíncrona através do Microsoft Teams mais clara e reduzem interrupções e equívocos. As orientações seguintes aplicam-se tanto a conversas de chat como a canais de equipas.",
    "blocks": [
      {
        "id": "04-heading-01",
        "kind": "heading",
        "text": "Contexto na primeira mensagem"
      },
      {
        "id": "04-paragraph-02",
        "kind": "paragraph",
        "text": "Evite enviar apenas mensagens introdutórias como “Olá” ou “Bom dia” e esperar pela resposta para explicar o assunto."
      },
      {
        "id": "04-paragraph-03",
        "kind": "paragraph",
        "text": "Deve agrupar o contexto, pedido, prazo (se aplicável) e outros elementos necessários numa mensagem concisa. Se mudar de tema, assinale a mudança de forma clara."
      },
      {
        "id": "04-heading-04",
        "kind": "heading",
        "text": "Resposta e urgência"
      },
      {
        "id": "04-paragraph-05",
        "kind": "paragraph",
        "text": "A presença Disponível ou uma confirmação de leitura não garante resposta imediata. Para uma comunicação urgente, use o meio urgente acordado internamente, como o WhatsApp, e deixe depois o contexto por escrito se necessário."
      },
      {
        "id": "04-heading-06",
        "kind": "heading",
        "text": "Conversa de grupo"
      },
      {
        "id": "04-paragraph-07",
        "kind": "paragraph",
        "text": "Inclua apenas as pessoas necessárias e dê um nome claro ao grupo."
      },
      {
        "id": "04-heading-08",
        "kind": "heading",
        "text": "Ficheiros e ligações"
      },
      {
        "id": "04-paragraph-09",
        "kind": "paragraph",
        "text": "Confirme as permissões dos ficheiros partilhados: copiar uma ligação não concede necessariamente acesso. Evite criar versões diferentes do mesmo documento em vários anexos. Os ficheiros partilhados no Teams ficam guardados no OneDrive ou no SharePoint, onde pode consultar o histórico de versões, de acordo com a configuração da organização."
      },
      {
        "id": "04-heading-10",
        "kind": "heading",
        "text": "Notificações e menções"
      },
      {
        "id": "04-paragraph-11",
        "kind": "paragraph",
        "text": "Nas definições do Teams, procure Notificações e atividade. Ajuste os alertas dos assuntos que acompanha. Nas mensagens, use uma menção à pessoa quando precisa da sua intervenção. Reserve as menções a todo o grupo, como @everyone quando disponível, para assuntos que exigem a atenção de todos.",
        "figureIds": [
          5,
          6
        ]
      },
      {
        "id": "04-heading-12",
        "kind": "heading",
        "text": "Fechar o pedido"
      },
      {
        "id": "04-paragraph-13",
        "kind": "paragraph",
        "text": "Uma resposta como “Revisto, corrigi os nomes na versão partilhada” confirma o trabalho realizado. Uma reação pode acusar receção, mas não substitui a decisão."
      }
    ],
    "figures": [
      {
        "id": 5,
        "src": "/images/figure-05.png",
        "width": 1656,
        "height": 815,
        "caption": "Página Notificações e atividade nas definições do Teams."
      },
      {
        "id": 6,
        "src": "/images/figure-06.png",
        "width": 1656,
        "height": 815,
        "caption": "Controlos de notificações de chats, canais e menções."
      }
    ]
  },
  {
    "id": "05",
    "title": "Criar e organizar a equipa e os canais",
    "shortTitle": "Criar equipa e canais",
    "intro": "A equipa reúne as pessoas de uma Área Operacional. Os canais separam os assuntos, como Eventos e Reuniões, Geral, Avisos, etc. Antes de criar um canal, confirme se já existe um adequado.",
    "blocks": [
      {
        "id": "05-step-01",
        "kind": "step",
        "number": 1,
        "text": "Abra Chat. Selecione “Nova equipa”.",
        "figureIds": [
          7
        ]
      },
      {
        "id": "05-step-02",
        "kind": "step",
        "number": 2,
        "text": "Preencha os campos Nome da equipa e Descrição consoante a área a que se destina. Em Tipo de equipa, recomenda-se manter a opção Privada: a adesão de novos membros depende da aprovação de um proprietário. Neste passo, pode também definir o primeiro canal da equipa.",
        "figureIds": [
          8
        ]
      },
      {
        "id": "05-step-03",
        "kind": "step",
        "number": 3,
        "text": "Para aceder ao menu de opções da equipa, utilize o botão “…” junto ao nome da equipa. Selecione “Gerir equipa” para consultar as opções e métricas disponíveis para a sua função.",
        "figureIds": [
          9
        ]
      },
      {
        "id": "05-step-04",
        "kind": "step",
        "number": 4,
        "text": "Para adicionar um canal a uma equipa, selecione “Adicionar canal” no menu de opções da equipa ou em Gerir equipa > Canais.",
        "figureIds": [
          10
        ]
      },
      {
        "id": "05-step-05",
        "kind": "step",
        "number": 5,
        "text": "Indique o nome e a descrição do novo canal. Selecione o tipo de canal de acordo com o acesso necessário: Padrão, para todos os membros da equipa; Privado, para membros específicos da equipa; ou Partilhado, para pessoas selecionadas dentro ou fora da equipa. A colaboração externa em canais partilhados depende das políticas da organização.",
        "figureIds": [
          11
        ]
      },
      {
        "id": "05-step-06",
        "kind": "step",
        "number": 6,
        "text": "A opção Esquema permite alterar a apresentação das conversas. Tópicos aproxima a conversa do canal de um chat de grupo, com respostas organizadas por tópico. Publicações apresenta mensagens com título e corpo de texto, seguidas das respetivas respostas.",
        "figureIds": [
          12
        ]
      },
      {
        "id": "05-step-07",
        "kind": "step",
        "number": 7,
        "text": "Conclua a criação do canal e confirme que este aparece por baixo da equipa correta."
      }
    ],
    "figures": [
      {
        "id": 7,
        "src": "/images/figure-07.png",
        "width": 1919,
        "height": 1031,
        "caption": "Opção Nova equipa no menu do Chat do Teams."
      },
      {
        "id": 8,
        "src": "/images/figure-08.png",
        "width": 1919,
        "height": 1028,
        "caption": "Formulário de criação de equipa com nome, descrição, privacidade e primeiro canal."
      },
      {
        "id": 9,
        "src": "/images/figure-09.png",
        "width": 1919,
        "height": 1031,
        "caption": "Opção Gerir equipa no menu junto ao nome da equipa."
      },
      {
        "id": 10,
        "src": "/images/figure-10.png",
        "width": 1919,
        "height": 1030,
        "caption": "Opção Adicionar canal no menu da equipa e na lista de canais."
      },
      {
        "id": 11,
        "src": "/images/figure-11.png",
        "width": 1919,
        "height": 1029,
        "caption": "Formulário de criação de canal com nome, descrição, tipo e esquema."
      },
      {
        "id": 12,
        "src": "/images/figure-12.png",
        "width": 1656,
        "height": 815,
        "caption": "Exemplo de canal padrão com o esquema Publicações selecionado."
      }
    ]
  },
  {
    "id": "06",
    "title": "Utilizar canais de equipas",
    "shortTitle": "Utilizar canais",
    "intro": "Os canais organizam conversas por assunto. O esquema escolhido determina a apresentação das mensagens: Publicações organiza o conteúdo em publicações e respostas; Tópicos apresenta uma conversa contínua com respostas em tópicos.",
    "blocks": [
      {
        "id": "06-step-01",
        "kind": "step",
        "number": 1,
        "text": "No menu à esquerda, navegue até Equipas e canais. Selecione a equipa e o canal que pretende utilizar. As figuras 13 e 14 mostram, respetivamente, os esquemas Publicações e Tópicos.",
        "figureIds": [
          13,
          14
        ]
      },
      {
        "id": "06-step-02",
        "kind": "step",
        "number": 2,
        "text": "No esquema Publicações, selecione “Publicar no canal” para escrever uma mensagem. Introduza um título e o corpo da mensagem, utilizando a barra de formatação para alterar o estilo do texto e anexar ficheiros. Selecione o botão “Publicação” para publicar. Na caixa de composição expandida, pode usar Ctrl + Enter.\nNo esquema Tópicos, escreva e envie a mensagem seguindo o procedimento do capítulo 03 Conversar no Teams.",
        "figureIds": [
          15
        ]
      },
      {
        "id": "06-step-03",
        "kind": "step",
        "number": 3,
        "text": "No esquema Publicações, os utilizadores com acesso ao canal podem selecionar a publicação a que pretendem responder e utilizar a respetiva caixa de texto.",
        "figureIds": [
          16
        ]
      },
      {
        "id": "06-step-04",
        "kind": "step",
        "number": 4,
        "text": "No esquema Tópicos, pode responder a uma mensagem numa conversa associada a essa mensagem. Coloque o ponteiro do rato sobre a mensagem para mostrar o menu de contexto e selecione “Responder no tópico”.",
        "figureIds": [
          17
        ]
      },
      {
        "id": "06-step-05",
        "kind": "step",
        "number": 5,
        "text": "As respostas a um tópico aparecem num painel à direita dedicado a esse tópico, evitando acumular respostas na conversa principal do canal.",
        "figureIds": [
          18
        ]
      }
    ],
    "figures": [
      {
        "id": 13,
        "src": "/images/figure-13.png",
        "width": 1916,
        "height": 1027,
        "caption": "Canal com o esquema Publicações e o botão Publicar no canal."
      },
      {
        "id": 14,
        "src": "/images/figure-14.png",
        "width": 1917,
        "height": 1029,
        "caption": "Canal com o esquema Tópicos e a caixa de mensagem na parte inferior."
      },
      {
        "id": 15,
        "src": "/images/figure-15.png",
        "width": 1918,
        "height": 1031,
        "caption": "Composição de uma publicação com título, corpo de texto e botão Publicação."
      },
      {
        "id": 16,
        "src": "/images/figure-16.png",
        "width": 1919,
        "height": 1024,
        "caption": "Publicações do canal e caixa de resposta a uma publicação."
      },
      {
        "id": 17,
        "src": "/images/figure-17.png",
        "width": 1918,
        "height": 1026,
        "caption": "Opção Responder no tópico no menu de contexto de uma mensagem."
      },
      {
        "id": 18,
        "src": "/images/figure-18.png",
        "width": 1919,
        "height": 1027,
        "caption": "Painel lateral com as respostas ao tópico selecionado."
      }
    ]
  },
  {
    "id": "07",
    "title": "Agendar no Calendário do Teams",
    "shortTitle": "Calendário do Teams",
    "intro": "O Calendário do Teams permite agendar reuniões e eventos, funcionando de forma semelhante ao calendário do Outlook. Para a mesma conta profissional, as reuniões agendadas no Teams também aparecem no calendário do Outlook e vice-versa.",
    "blocks": [
      {
        "id": "07-step-01",
        "kind": "step",
        "number": 1,
        "text": "Na barra lateral esquerda do Teams, abra Calendário. Escolha a vista Semana ou Mês, navegue até à data pretendida e selecione Novo no canto superior direito.",
        "figureIds": [
          19
        ]
      },
      {
        "id": "07-step-02",
        "kind": "step",
        "number": 2,
        "text": "Introduza o título e, se for uma reunião, os participantes. No campo seguinte, confirme a data e defina as horas de início e fim do evento ou selecione “Todo o dia”. Pode também definir a periodicidade, se se tratar de um evento recorrente.",
        "figureIds": [
          20,
          21
        ]
      },
      {
        "id": "07-step-03",
        "kind": "step",
        "number": 3,
        "text": "Na área de data e hora, utilize o “Planeador” para verificar a disponibilidade dos participantes adicionados.",
        "figureIds": [
          22
        ]
      },
      {
        "id": "07-step-04",
        "kind": "step",
        "number": 4,
        "text": "Termine a configuração do evento, ativando Reunião do Teams se houver participação online. Adicione uma descrição e os pontos da ordem de trabalhos, se necessário. Para um compromisso sem convidados, selecione “Guardar”; numa reunião com participantes, selecione “Enviar” para lhes enviar o convite."
      }
    ],
    "figures": [
      {
        "id": 19,
        "src": "/images/figure-19.png",
        "width": 1656,
        "height": 815,
        "caption": "Vista mensal do Calendário do Teams e botão Novo."
      },
      {
        "id": 20,
        "src": "/images/figure-20.png",
        "width": 1919,
        "height": 1023,
        "caption": "Formulário de evento com campos para título, participantes, data e hora."
      },
      {
        "id": 21,
        "src": "/images/figure-21.png",
        "width": 1656,
        "height": 815,
        "caption": "Definição das horas de início e fim e do fuso horário do evento."
      },
      {
        "id": 22,
        "src": "/images/figure-22.png",
        "width": 1916,
        "height": 1023,
        "caption": "Planeador de disponibilidade dos participantes no formulário de evento."
      }
    ]
  },
  {
    "id": "08",
    "title": "Adicionar um calendário do canal",
    "shortTitle": "Calendário do canal",
    "intro": "O calendário do canal mostra as reuniões associadas a esse canal. É diferente do calendário pessoal e não reúne automaticamente todos os eventos da equipa.",
    "blocks": [
      {
        "id": "08-step-01",
        "kind": "step",
        "number": 1,
        "text": "No menu lateral, navegue até à equipa e ao canal padrão. Na barra do topo, escolha “Adicionar um separador” e, se surgir esse passo, Aplicações. Procure Calendário do canal.",
        "figureIds": [
          23,
          24
        ]
      },
      {
        "id": "08-step-02",
        "kind": "step",
        "number": 2,
        "text": "Selecione a aplicação, dê um nome ao separador e escolha Guardar.",
        "figureIds": [
          25
        ]
      },
      {
        "id": "08-step-03",
        "kind": "step",
        "number": 3,
        "text": "Para criar um evento, selecione “Adicionar novo evento” na barra do calendário do canal. Se esta opção estiver no menu junto a “Reunir agora”, abra esse menu. Os passos seguintes são semelhantes aos do capítulo 07 Agendar no Calendário do Teams. Confirme o canal no formulário. Para enviar um convite individual, adicione explicitamente os participantes; a reunião não aparece automaticamente no calendário pessoal de todos os membros da equipa.",
        "figureIds": [
          26,
          27
        ]
      }
    ],
    "figures": [
      {
        "id": 23,
        "src": "/images/figure-23.png",
        "width": 1918,
        "height": 1026,
        "caption": "Menu Adicionar um separador na barra superior do canal."
      },
      {
        "id": 24,
        "src": "/images/figure-24.png",
        "width": 1919,
        "height": 1020,
        "caption": "Pesquisa da aplicação Calendário do canal."
      },
      {
        "id": 25,
        "src": "/images/figure-25.png",
        "width": 1656,
        "height": 815,
        "caption": "Definição do nome do separador Calendário do canal."
      },
      {
        "id": 26,
        "src": "/images/figure-26.png",
        "width": 1656,
        "height": 815,
        "caption": "Calendário do canal sem reuniões e opção Adicionar novo evento."
      },
      {
        "id": 27,
        "src": "/images/figure-27.png",
        "width": 1656,
        "height": 815,
        "caption": "Formulário de reunião com o canal identificado e os campos do convite."
      }
    ]
  },
  {
    "id": "09",
    "title": "Planner no Teams",
    "shortTitle": "Planner no Teams",
    "intro": "Um plano do Planner reúne tarefas e pode ser disponibilizado num separador de um canal do Teams. Cada tarefa pode ter responsáveis, datas de início e conclusão e um estado de progresso. Também existem planos pessoais, sem associação a um canal.",
    "blocks": [
      {
        "id": "09-step-01",
        "kind": "step",
        "number": 1,
        "text": "Para adicionar um plano a um canal de uma equipa, selecione Chat na barra lateral esquerda e navegue até ao canal escolhido. Na barra do topo, escolha “Adicionar um separador” e, se surgir esse passo, Aplicações. Procure “Planner” e adicione a aplicação ao canal.",
        "figureIds": [
          28
        ]
      },
      {
        "id": "09-step-02",
        "kind": "step",
        "number": 2,
        "text": "Selecione Criar um novo plano, escolha o tipo de plano e o modelo e clique em “Criar plano básico”. Atribua um nome quando for solicitado e confirme a criação.",
        "figureIds": [
          29
        ]
      },
      {
        "id": "09-step-03",
        "kind": "step",
        "number": 3,
        "text": "Aceda ao plano pelo separador na barra do topo do canal. Pode alterar a visualização das tarefas através de Grelha, Quadro, Calendário ou Gráficos, consoante as opções disponíveis no plano. Na vista Quadro, use “Agrupar por”, no canto superior direito, para escolher como organizar as tarefas.",
        "figureIds": [
          30
        ]
      },
      {
        "id": "09-step-04",
        "kind": "step",
        "number": 4,
        "text": "Em Agrupar por > Grupo, use “Adicione um novo grupo” ou “Mais opções” para adicionar ou remover grupos. Arraste o nome de um grupo para reordenar as colunas e arraste um cartão para mudar a tarefa de grupo. Esta mudança não altera o campo Estado (Progresso noutras versões), mesmo que o grupo se chame “Tarefas em Curso”.",
        "figureIds": [
          31
        ]
      },
      {
        "id": "09-step-05",
        "kind": "step",
        "number": 5,
        "text": "Para adicionar uma tarefa, selecione “Adicionar tarefa” na coluna pretendida. Introduza um nome, defina a data de conclusão e atribua a tarefa ao colaborador ou aos colaboradores responsáveis. Selecione “Adicionar tarefa” para concluir.",
        "figureIds": [
          32,
          33
        ]
      },
      {
        "id": "09-step-06",
        "kind": "step",
        "number": 6,
        "text": "Para editar ou acrescentar elementos a uma tarefa, selecione-a e altere os campos necessários. Pode adicionar itens à lista de verificação, útil para tarefas com vários critérios ou subtarefas. Pode também adicionar notas e, quando disponível, utilizar a conversa da tarefa. Atualize o campo Estado para registar se a tarefa não foi iniciada, está em curso ou está concluída.",
        "figureIds": [
          34
        ]
      },
      {
        "id": "09-heading-07",
        "kind": "heading",
        "text": "Consultar as tarefas pessoais"
      },
      {
        "id": "09-paragraph-08",
        "kind": "paragraph",
        "text": "Para além disso, cada colaborador tem acesso ao seu Planner individual, onde pode consultar as tarefas que lhe estão atribuídas e criar os seus próprios planos pessoais."
      },
      {
        "id": "09-step-09",
        "kind": "step",
        "number": 1,
        "text": "No Teams, abra Aplicações ou as reticências da barra lateral e procure Planner. Abra a aplicação. Pode afixá-la à barra lateral para voltar a ela rapidamente.",
        "figureIds": [
          35
        ]
      },
      {
        "id": "09-step-10",
        "kind": "step",
        "number": 2,
        "text": "No menu lateral, selecione “As minhas tarefas” para consultar as tarefas que lhe estão atribuídas. Na vista Quadro, escolha Agrupar por > Estado para as ver nas colunas “Não iniciada”, “Em curso” e “Concluído”, conforme o exemplo.",
        "figureIds": [
          36
        ]
      }
    ],
    "figures": [
      {
        "id": 28,
        "src": "/images/figure-28.png",
        "width": 1919,
        "height": 1001,
        "caption": "Separador Planner no canal com a opção de criar um novo plano."
      },
      {
        "id": 29,
        "src": "/images/figure-29.png",
        "width": 1919,
        "height": 1024,
        "caption": "Escolha do tipo de plano e de um modelo, com o botão Criar plano básico."
      },
      {
        "id": 30,
        "src": "/images/figure-30.png",
        "width": 1919,
        "height": 1025,
        "caption": "Plano aberto no separador do canal, com as vistas e o menu Agrupar por."
      },
      {
        "id": 31,
        "src": "/images/figure-31.png",
        "width": 1919,
        "height": 1021,
        "caption": "Quadro do Planner com grupos de tarefas e o menu de opções de um grupo."
      },
      {
        "id": 32,
        "src": "/images/figure-32.png",
        "width": 1916,
        "height": 1031,
        "caption": "Botões Adicionar tarefa nas colunas do quadro."
      },
      {
        "id": 33,
        "src": "/images/figure-33.png",
        "width": 1917,
        "height": 1023,
        "caption": "Criação de uma tarefa com nome, data de conclusão e responsável."
      },
      {
        "id": 34,
        "src": "/images/figure-34.png",
        "width": 1914,
        "height": 1017,
        "caption": "Detalhes da tarefa com estado, datas, lista de verificação, notas e conversa."
      },
      {
        "id": 35,
        "src": "/images/figure-35.png",
        "width": 1656,
        "height": 815,
        "caption": "Acesso à aplicação Planner pelo menu da barra lateral do Teams."
      },
      {
        "id": 36,
        "src": "/images/figure-36.png",
        "width": 1918,
        "height": 1026,
        "caption": "Vista As minhas tarefas com o quadro organizado por estado."
      }
    ]
  },
  {
    "id": "10",
    "title": "Envio de emails em série personalizados",
    "shortTitle": "Emails em série",
    "intro": "Para enviar emails personalizados em série, utilize Excel, Word e Outlook clássico para Windows. O Word entrega as mensagens ao Outlook através da integração MAPI, que o novo Outlook não suporta. Neste capítulo, o envio é feito pelo Outlook clássico.",
    "blocks": [
      {
        "id": "10-heading-01",
        "kind": "heading",
        "text": "Preparar o Outlook clássico"
      },
      {
        "id": "10-paragraph-02",
        "kind": "paragraph",
        "text": "Abra o Outlook clássico e confirme que a conta remetente está configurada, ligada e pronta a enviar. Mantenha a aplicação aberta durante o envio em série. Ter apenas a conta configurada no novo Outlook não é suficiente."
      },
      {
        "id": "10-paragraph-03",
        "kind": "paragraph",
        "text": "Use o Excel para preparar uma lista com os destinatários e os campos a utilizar no email. Coloque os nomes dos campos na primeira linha da folha e um destinatário em cada linha seguinte, conforme o exemplo. Os endereços example.com são fictícios e destinam-se apenas à demonstração.",
        "figureIds": [
          37
        ]
      },
      {
        "id": "10-table-example",
        "kind": "table",
        "headers": [
          "Email",
          "Nome",
          "Empresa",
          "Saudacao"
        ],
        "rows": [
          [
            "ana.silva@example.com",
            "Ana Silva",
            "Empresa A",
            "Cara"
          ],
          [
            "rui.costa@example.com",
            "Rui Costa",
            "Empresa B",
            "Caro"
          ],
          [
            "joana.martins@example.com",
            "Joana Martins",
            "Empresa C",
            "Cara"
          ]
        ]
      },
      {
        "id": "10-paragraph-04",
        "kind": "paragraph",
        "text": "Use o Word para preparar o modelo do email. Depois, introduza os campos de impressão em série, que serão substituídos pelos valores da lista de destinatários."
      },
      {
        "id": "10-example-invite",
        "kind": "example",
        "title": "Exemplo corrigido do modelo no Word",
        "text": "«Saudacao» «Nome»,\n\nConvidamos a «Empresa» a participar no evento x.\n\nCom os melhores cumprimentos,\nEquipa organizadora"
      },
      {
        "id": "10-step-05",
        "kind": "step",
        "number": 1,
        "text": "No Word, abra Correspondências, Correio ou Mailings, consoante o idioma da aplicação. Escolha Iniciar Impressão em Série > Mensagens de Correio Eletrónico e prepare o corpo da mensagem."
      },
      {
        "id": "10-step-06",
        "kind": "step",
        "number": 2,
        "text": "Escolha Selecionar Destinatários > Utilizar uma Lista Existente. Selecione o ficheiro Excel que contém a lista de destinatários.",
        "figureIds": [
          38
        ]
      },
      {
        "id": "10-step-07",
        "kind": "step",
        "number": 3,
        "text": "Se surgir a escolha da tabela ou folha, selecione a que contém a lista de destinatários, por exemplo Destinatarios$. Confirme que a opção “A primeira linha de dados inclui os cabeçalhos das colunas” está selecionada.",
        "figureIds": [
          39
        ]
      },
      {
        "id": "10-step-08",
        "kind": "step",
        "number": 4,
        "text": "Abra Editar Lista de Destinatários e confirme os registos selecionados. Para introduzir um campo personalizável, coloque o cursor na posição pretendida, selecione Inserir Campo de Impressão em Série e escolha o campo. Também pode usar Ctrl + F9 para criar as chavetas de um campo, escrever MERGEFIELD seguido do nome do campo, por exemplo { MERGEFIELD Nome }, e premir F9 para o atualizar. As chavetas têm de ser criadas pelo atalho, não escritas manualmente."
      },
      {
        "id": "10-step-09",
        "kind": "step",
        "number": 5,
        "text": "Em Pré-Visualizar Resultados, pode percorrer os destinatários e confirmar a correta aplicação dos campos personalizáveis."
      },
      {
        "id": "10-step-10",
        "kind": "step",
        "number": 6,
        "text": "Selecione Concluir e Intercalar > Enviar Mensagens de Correio Eletrónico. Em “Para”, escolha o campo Email; preencha o assunto e escolha o formato HTML. Selecione os registos a enviar. Ao confirmar com OK, o Word inicia o envio através do Outlook clássico, sem criar rascunhos para revisão individual.",
        "figureIds": [
          40
        ]
      },
      {
        "id": "10-step-11",
        "kind": "step",
        "number": 7,
        "text": "No Outlook clássico, verifique a Caixa de Saída e Itens Enviados. Confirme a receção do teste, o remetente e a personalização. Depois, volte a ligar o Word à lista final pelo passo 2 e repita a pré-visualização e o envio."
      },
      {
        "id": "10-heading-12",
        "kind": "heading",
        "text": "Definir o remetente no Outlook clássico"
      },
      {
        "id": "10-paragraph-13",
        "kind": "paragraph",
        "text": "No Outlook clássico, abra Ficheiro > Definições de Conta > Definições de Conta. No separador Email, selecione a conta remetente e escolha “Predefinir”. Em Ficheiro > Opções > Correio > Enviar mensagens, ative “Utilizar sempre a conta predefinida ao compor novas mensagens”. Confirme o endereço efetivamente utilizado com o teste antes de enviar o lote."
      },
      {
        "id": "10-paragraph-14",
        "kind": "paragraph",
        "text": "A janela de impressão em série do Word não tem um campo “De”. Alterar o remetente numa mensagem avulsa ou a conta principal do novo Outlook não define o remetente deste envio em série."
      },
      {
        "id": "10-paragraph-15",
        "kind": "paragraph",
        "text": "Para enviar a partir de uma caixa partilhada, como geral@... ou suporte@..., é necessária a permissão “Enviar como” ou “Enviar em nome de”. A caixa aparecer na lista de pastas não garante que esteja disponível como conta remetente para a impressão em série. Peça à equipa de informática que valide a configuração no Outlook clássico e confirme-a num teste. Não é necessário iniciar sessão diretamente na caixa partilhada com uma palavra-passe própria."
      }
    ],
    "figures": [
      {
        "id": 37,
        "src": "/images/figure-37.png",
        "width": 554,
        "height": 229,
        "caption": "Lista de exemplo no Excel com os campos Email, Nome, Empresa e Saudacao."
      },
      {
        "id": 38,
        "src": "/images/figure-38.png",
        "width": 1918,
        "height": 1023,
        "caption": "Seleção de uma lista de destinatários existente no separador de impressão em série do Word."
      },
      {
        "id": 39,
        "src": "/images/figure-39.png",
        "width": 585,
        "height": 257,
        "caption": "Escolha da folha Destinatarios$ e confirmação dos cabeçalhos das colunas."
      },
      {
        "id": 40,
        "src": "/images/figure-40.png",
        "width": 1918,
        "height": 1027,
        "caption": "Janela de impressão em série do Word com o campo Email, o assunto, o formato e os registos a enviar através do Outlook clássico."
      }
    ]
  }
];
