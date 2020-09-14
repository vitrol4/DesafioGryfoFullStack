# Desafio Gryfo FullStack

Desafio para testar a capacidade de projetar uma arquitetura simples de cliente (web) - servidor (python) para processamento de imagens.

Nesse desafio o objetivo é entregar uma página web que tenha opções de processamento de imagem e upload de uma imagem para o endpoint da API.
Essa API fará o processamento no servidor (pode ser mesma máquina) e devolverá para o browser (pode ser como download estático, NÃO precisa ser assíncrono na mesma página)

Além do input de upload de imagem, o form da página devera ter pelo menos os seguintes checkboxes:
- Flip Horizontal
- Flip Vertical
- Inverter cores (negativo)
- Borrar imagem
- Detecção de arestas (por exemplo, filtro canny)
- Desenhar contornos

Nenhum desses processamentos precisa ser parametrizados, podem ser fixos.
Mas todos devem poder ser ligados em qualquer ordem.

Requisitos
- API deve ser feita com python utilizando o Flask
- o processamento de imagem deve ser feito com OpenCV (python cv2)

Dicas
- estruturar a comunicação utilizando exemplos do próprio Flask
- depois preencher as funções mockadas de processamento de imagem com o exemplos da documentação/stack overflow da opencv em python
