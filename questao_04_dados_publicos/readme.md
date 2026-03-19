# ✦ Questão 04 - Trabalhando com dados públicos 🗂️🏦

## ⮞ Premissas Obrigatórias

- O custo em USD é unitário
- O custo em BRL deve ser calculado usando o **câmbio da data da venda**
- A taxa de câmbio deve ser considerada a **média da cotação de venda do dia (Banco Central)**
- A **receita total** do produto considera todas as vendas (inclusive as sem prejuízo)
- Ignore impostos e frete

### 🏷️ Cálculo e modelagem 

- **Custo total em BRL por transação**

    Para identificar corretamente o custo em R$ por transação, foi necessário utilizar a **API do Banco Central (Olinda)**, que fornece cotações oficiais de USD para BRL historicamente.

    > https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=\'USD\',dataCotacao=\'{date}\')

    O Endpoint utilizado, retorna todas as cotações do dólar no dia, referentes a data passada na **URL**. No arquivo [api_requests.py](./artefatos/api_requests.py) é possível visualizar o código utilizado para obter a **média das cotações** de venda do dólar no dia para cada data referente aos custos de importação.

- **Identifique transações com prejuízo**
- **Agregue os dados por id_produto, gerando:**
    - Receita total (BRL)
    - Prejuízo total (BRL)
    - Percentual de perda (prejuízo_total / receita_total)

Para as tarefas acima, no arquivo [query.py](./artefatos/query.py) foi construída uma query que possibilita a obtenção de todas essas informações.

### 🏷️ Análise visual

![Top 15 produtos com prejuízo](./artefatos/produtos_com_prejuizo.png)


### 🏷️ Análise objetiva 

Responda objetivamente:

#### Qual produto concentra o maior prejuízo absoluto?

De acordo com as análises realizadas, o produto com maior prejuízo é o **Motor Diesel Honda Aero 205HP** com `id 76`. Ele acumulou uma perda total de **R$ 2.104.588,39** representando **2.52%**. Esse valor representa a quantidade de lucro que a empresa deixou de acrrecar devido a vendas realizadas abaixo do custo de importação convertido na data da transação.

#### O produto com maior prejuízo absoluto também é o que possui a maior porcentagem de perda? (Sim ou Não) 

Não. O produto com maior porcentagem de perda é o de `id 86` **Motor Diesel Volvo Helix Evo Force 144HP** com **3.57%**.

### 🏷️ Interpretação

#### Qual data de câmbio você utilizou?
Para garantir que o cálculo seja preciso, utilizei a **cotação média de venda do dólar** referente à **data de importação mais recente anterior à data de venda**.

Como cada produto possui um histórico de custos de importação, apliquei a função `merge_asof` do **Pandas** (parâmetro `direction='backward'`). Isso permite um alinhamento temporal, ou seja, que seja identificado o custo vigente e a taxa de câmbio do Banco Central no momento em que o produto estava em estoque.

#### Como definiu o prejuízo?
Para definir o prejuízo, foi necessário comparar a receita bruta em **BRL** com o custo total convertido (`Preço USD * Taxa de câmbio média * Quantidade`). Mantenho apenas os resultados negativos, ou seja, **prejuízos**, foi possível identificar produtos que a empresa deixou de ganhar dinheiro devido à custos de importação.

#### Alguma suposição relevante? 
É importante observar que baixos percentuais de perdas, como **2.52% no caso do produto 76**, mascaram um problema de alto prejuízo devido ao alto volume de vendas. E isso ocorre para diversos outros produtos vendidos com porcentagens ainda maiores de prejuízo. É importante abrir essa "caixa preta" financeira, pois observa-se um rombo milionário quando soma-se o prejuízo que muitos produtos podem gerar.