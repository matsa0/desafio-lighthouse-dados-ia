# ✦ Questão 07 - Previsão de demanda 🔮   

Nesta questão, devemos realizar a previsão de demanda do mês de janeiro de 2024 para o produto **"Motor de Popa Yamaha Evo Dash 155HP"**. A previsão de demanda é muito útil para controle de estoque, pois ela pode te fornecer uma base confiável sobre o **controle de estoque de determinados produtos**. Isso evita que os compradores fiquem apenas no "achismo" do quanto será vendido, o que evita perda de lucro por conta de ausência ou estoque excedente.

## ⮞ Premissas Obrigatórias 

- O período de treino deve incluir dados até **31/12/2023**.
- O período de teste deve ser **todo o mês de Janeiro de 2024**.
- A previsão deve ser feita em **base diária**.
- Não é permitido utilizar dados **futuros no treino (data leakage)**.
- Considere apenas o produto: **"Motor de Popa Yamaha Evo Dash 155HP"**

Obs: Todo o baseline do modelo foi criado no arquivo [model.py](./artefatos/model.py). Ele segue uma estrutura de células similar a arquivos *.ipynb*.

### 🏷️ Construa um modelo baseline simples
- **Ele deve utilizar a média móvel dos últimos 7 dias de vendas (considerando apenas dados anteriores à data prevista).**

    O modelo baseline criado respeita as seguintes normas acima, sendo baseado em média móvel de 7 dias, no qual a previsão para cada dia é calculada como a **média das vendas dos 7 dias anteriores**, considerando apenas informações disponíveis até aquele momento.

    A previsão foi realizada de forma sequencial, de forma que cada novo dia previsto pelo modelo, o valor real observado fosse incorporado ao histórico, evitando *data leakage*.

### 🏷️ Quais são as previsões diárias de vendas para Janeiro de 2024?

As previsões diárias para o mês de Janeiro de 2024 do produto alvo são **baixas**, refletindo o comportamento da dimensão de tempo.

- Fazendo uma breve análise, até o dia 10 de janeiro, a previsão é **nenhuma venda do produto**, isso devido à baixa ocorrência de vendas no período anterior. A partir do dia 11, vendas podem começar a aparecer, tendo um cenário mais otimista a partir da metade do mês, pois um pico de vendas do produto pode ocorrer entre os dias 22 e 28 de janeiro, voltando a ser mais estável nos últimos 2 dias do mês.

### 🏷️ Validação: Compare as previsões com os valores reais do período de teste utilizando a métrica MAE — Mean Absolute Error

- **O baseline é adequado para esse produto?**
    O baseline **não é adequado** para esse produto.

    O Mean Absolute Error `MAE` obtido foi de **1.45**, o que parece bom à primeira vista, sugerindo que o modelo erra apenas cerca de 1.45 unidades produtos por dia. No entanto, ela é muito influeciada pelos dias que não tiveram vendas. 
    
    Ao observar os dias que tiveram vendas em janeiro e compararmos com a predição, é perceptível que o modelo não consegue capturar os dias que tiveram picos de demanda.

    | Data de venda | Quantidade  | Predição
    | :------------ | :---------: | :-------:
    | 2024-01-10    | 10          | 0 
    | 2024-01-21    | 11          | 0
    | 2024-01-22	| 6           | 2

    Isso ocorre porque a média móvel depende das vendas dos dias anteriores, que, nesse caso, apresentam predominantemente valores zero ou muito baixos.

### 🏷️ Interpretação

- **Como o baseline foi construído?**

    Primeiramente, foi necessário filtrar a base para considerar apenas o produto alvo: **"Motor de Popa Yamaha Evo Dash 155HP"**. Em seguida, dividir a base filtrada em conjuntos de treino e teste de acordo com as datas especificadas no enunciado. 

    O modelo baseline foi construído levando em consideração a média móvel de 7 dias, onde a previsão para cada dia corresponde à **média das quantidades vendidas nos 7 dias anteriores**.
    
    A previsão foi realizada de forma sequencial, ou seja, após cada previsão, o valor previsto é adicionado ao histórico de datas (**que começa com os últimos 7 dias de dezembro de 2023**). Isso garante que as próximas previsões utilizem apenas informações disponíveis até aquele momento.

- **Como evitou data leakage?**

    Para evitar o *data leakage*, bastou garantir na construção do modelo que para cada previsão, fossem considerados apenas dados anteriores à data prevista para base do cálculo da média móvel. Dessa forma, o modelo utiliza apenas o histórico conhecido até o momento da previsão, sem acesso aos valores dos dias seguintes.
    

- **Cite uma limitação do modelo proposto.**

    Uma limitação do modelo é que a média móvel suaviza a série temporal, dificultando a previsão correta de variações abruptas como foi demonstrado através dos picos de vendas. 
    
    Além disso, o valor resultante do erro médio absoluto (MAE) pode levar a interpretações equivocadas, pois a grande quantidade de dias sem registro/sem vendas reduz abruptamente o erro médio, o que mascara a qualidade do modelo em prever a quantidade de vendas real.