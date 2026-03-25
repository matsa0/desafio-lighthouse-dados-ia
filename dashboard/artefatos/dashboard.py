# ----------- #
# Import Libs #
# ----------- #
import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.metrics import mean_absolute_error
import json
from pathlib import Path

# ------------------ #
# Page configuration #
# ------------------ #
st.set_page_config(
    layout="wide",
    page_title="Dashboard LH Nauticals",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ----------------------------- #
# Data extraction from datasets 
# ----------------------------- #
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent.parent

@st.cache_data
def load_daily_sales_data():
    df = pd.read_csv(BASE_DIR / "vendas_diarias.csv")
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df

@st.cache_data
def load_revenue_dow_data():
    return pd.read_csv(ROOT_DIR / "questao_06_calendario/artefatos/media_receita_dias_semana.csv")

@st.cache_data
def load_loss_products_data():
    return pd.read_csv(ROOT_DIR / "questao_04_dados_publicos/artefatos/produtos_com_prejuizo.csv")

@st.cache_data
def load_pred_data():
    df = pd.read_csv(ROOT_DIR / "questao_07_previsao_demanda/artefatos/real_x_previsao.csv")
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    return df.rename(columns={"qtd": "Real", "prediction": "Previsto"})

@st.cache_data
def load_clients_data():
    df = pd.read_csv(ROOT_DIR / "questao_05_analise_clientes/artefatos/ranking_ticket_medio.csv")
    
    with open(ROOT_DIR / "datasets/clientes_crm.json") as f:
        crm = pd.DataFrame(json.load(f))
    
    df = df.merge(crm.rename({"code": "id_client"}, axis=1), on="id_client")
    
    return df.rename(columns={
        "annual_revenue": "Faturamento",
        "frequency": "Frequência",
        "mean_ticket": "Ticket médio",
        "diversity": "Diversidade",
        "full_name": "Nome"
    })

@st.cache_data
def load_products_data():
    df = pd.read_csv(ROOT_DIR / "questao_05_analise_clientes/artefatos/produtos_vendidos.csv")
    df["sale_date"] = pd.to_datetime(df["sale_date"], format="mixed")
    return df.rename(columns={"name": "Produto"})

@st.cache_data
def load_cos_similarity_data():
    df = pd.read_csv(ROOT_DIR / "questao_08_sistema_recomendacao/artefatos/sim_cosseno_produto_alvo.csv", index_col=0)
    df.columns = df.columns.astype(int)
    return df  

# ------------------- #
# Auxiliary functions #
# ------------------- #
def apply_default_layout(fig):
    """Configure margins on the app"""
    fig.update_layout(margin=dict(l=20, r=20, t=40, b=20))
    return fig

# ---------------- # 
# Dashboard header #
# ---------------- # 
st.title("📊 Dashboard Financeiro - LH Nauticals")
st.markdown("Visão executiva de faturamento, perdas financeiras, projeções de demanda e perfil de clientela (2023–2024).")
st.markdown("---")

# ================ #
# Section 1: SALES #
# ================ #
st.markdown("### 📈 Desempenho de Vendas")

daily_sales_df = load_daily_sales_data()
df_dow = load_revenue_dow_data()

# space control with columns
revenue_col, quantity_col = st.columns(2)

with revenue_col:
    metric_option = st.radio(
        "Selecionar Métrica de Evolução:",
        ["Faturamento (R$)", "Quantidade"],
        horizontal=True
    )

with quantity_col:
    min_date = daily_sales_df["sale_date"].min().date()
    max_date = daily_sales_df["sale_date"].max().date()
    
    start_date, end_date = st.slider(
        "Selecione o Período:",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="DD/MM/YYYY"
    )

# date filter for slider
mask = (daily_sales_df["sale_date"].dt.date >= start_date) & (daily_sales_df["sale_date"].dt.date <= end_date)
filtered_sales_df = daily_sales_df.loc[mask]

metric_map = {"Faturamento (R$)": "total", "Quantidade": "qtd"}
selected_metric = metric_map[metric_option]

# columns for sales plots
sales_lineplot_col, sales_barplot_col = st.columns([2, 1])

with sales_lineplot_col:
    fig_sales = px.line(
        filtered_sales_df,
        x="sale_date",
        y=selected_metric,
        title=f"Evolução Temporal: {metric_option}",
        labels={"sale_date": "Data", selected_metric: metric_option}
    )
    st.plotly_chart(apply_default_layout(fig_sales), use_container_width=True)

with sales_barplot_col:
    fig_dow = px.bar(
        df_dow,
        x="day_of_week_name",
        y="average_daily_revenue",
        title="Média de Receita por Dia",
        labels={"day_of_week_name": "Dia da Semana", "average_daily_revenue": "Receita Média (R$)"}
    )
    st.plotly_chart(apply_default_layout(fig_dow), use_container_width=True)

st.markdown("---")

# ================= #
# Section 2: LOSSES #
# ================= #
st.markdown("### 💸 Análise de Prejuízo")

df_loss = load_loss_products_data()
total_revenue = df_loss["total_revenue"].sum()
total_loss = df_loss["total_loss"].sum()
avg_loss_pct = (total_loss / total_revenue) * 100

# Loss KPIs
loss_kpi1, loss_kpi2, loss_kpi3 = st.columns(3)
loss_kpi1.metric("💰 Receita Total (Amostra)", f"R$ {total_revenue:,.2f}", help="Soma total da receita feita com todos os produtos em prejuízo.")
loss_kpi2.metric("🔻 Prejuízo Total", f"R$ {total_loss:,.2f}", help="Soma de todo o prejuízo obtido na venda dos produtos.")
loss_kpi3.metric("📉 Percentual de Perda", f"{avg_loss_pct:.2f}%", help="Média do percentual de perda total.")

# columns for losses plots
loss_option_col, loss_plot_col = st.columns([1, 3])

with loss_option_col:
    st.markdown("<br>", unsafe_allow_html=True)
    loss_metric_option = st.radio(
        "Critério de Ordenação (Top 10):",
        ["Prejuízo Total Absoluto", "Percentual de Prejuízo (%)"]
    )
    loss_metric_map = {
        "Prejuízo Total Absoluto": "total_loss",
        "Percentual de Prejuízo (%)": "total_loss_pct"
    }
    selected_loss_metric = loss_metric_map[loss_metric_option]

with loss_plot_col:
    top_loss = df_loss.sort_values(selected_loss_metric, ascending=False).head(10)
    fig_loss = px.bar(
        top_loss.sort_values(selected_loss_metric),
        x=selected_loss_metric,
        y="product_name",
        orientation="h",
        title=f"Top 10 Produtos - {loss_metric_option}",
        text=selected_loss_metric,
        labels={"product_name": "Produto", selected_loss_metric: "Valor"}
    )
    fig_loss.update_traces(texttemplate="%{text:.2f}", textposition="auto")
    st.plotly_chart(apply_default_layout(fig_loss), use_container_width=True)

st.markdown("---")

# ========================== #
# Section 3: DEMAND FORECAST #
# ========================== #
st.markdown("### 📊 Previsão vs Realizado")

df_pred = load_pred_data()
mae = mean_absolute_error(df_pred["Real"], df_pred["Previsto"])

col_prev_kpi, col_prev_chart = st.columns([1, 4])

with col_prev_kpi:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.metric(label="Erro Médio Absoluto (MAE)", value=f"{mae:.2f}", help="Média da diferença absoluta entre os valores previstos e os reais.")

with col_prev_chart:
    fig_pred = px.line(
        df_pred,
        x="sale_date",
        y=["Real", "Previsto"],
        title="Volume: Real x Previsão (Jan/2024)",
        labels={"sale_date": "Data", "value": "Quantidade", "variable": "Legenda"}
    )
    st.plotly_chart(apply_default_layout(fig_pred), use_container_width=True)

st.markdown("---")

# ======================================== #
# Section 4: ELITE CLIENTS AND CONSUMPTION #
# ======================================== #
st.markdown("### 👥 Análise de Clientes e Consumo")

df_clients = load_clients_data()

crm_scatterplot_col, top10_crm_barplot_col = st.columns(2)

with crm_scatterplot_col:
    fig_scatter = px.scatter(
        df_clients,
        x="Frequência",
        y="Ticket médio",
        size="Faturamento",
        color="Diversidade",
        hover_data=["Nome"],
        title="Perfil dos Clientes de Elite",
        labels={"Frequência": "Frequência de Compra", "Ticket médio": "Ticket Médio (R$)"}
    )
    st.plotly_chart(apply_default_layout(fig_scatter), use_container_width=True)

with top10_crm_barplot_col:
    top_clients = df_clients.sort_values("Ticket médio", ascending=False).head(10)
    fig_top_cli = px.bar(
        top_clients.sort_values("Ticket médio"), 
        x="Ticket médio",
        y="Nome",
        orientation="h",
        title="Top 10 Clientes (Por Ticket Médio)",
        labels={"Nome": "Cliente", "Ticket médio": "Ticket Médio (R$)"}
    )
    st.plotly_chart(apply_default_layout(fig_top_cli), use_container_width=True)

df_products = load_products_data()
df_cosine_similarity = load_cos_similarity_data()

top10_products_barplot_col, similarity_heatmap_col = st.columns(2)

df_dict_names = df_products[["id_product", "Produto"]].drop_duplicates()

with top10_products_barplot_col:
    top_products = df_products["Produto"].value_counts().head(10).reset_index()
    top_products.columns = ["Produto", "Quantidade"]
    fig_top_prod = px.bar(
        top_products.sort_values("Quantidade"),
        x="Quantidade",
        y="Produto",
        orientation="h",
        title="Top 10 Produtos Mais Consumidos",
        text="Quantidade"
    )
    fig_top_prod.update_traces(textposition="auto")
    st.plotly_chart(apply_default_layout(fig_top_prod), use_container_width=True)
    
    
with similarity_heatmap_col:
    # filter products ids
    valid_ids = df_cosine_similarity.columns.tolist()
    available_products = df_dict_names[df_dict_names["id_product"].isin(valid_ids)]

    sorted_options = sorted(available_products["Produto"].tolist())
    target_product = "GPS Garmin Vortex Maré Drift" 
    
    # find target product position
    try:
        index = sorted_options.index(target_product)
    except ValueError:
        index = 0 
        
    selected_prod_name = st.selectbox(
        "🔍 Selecione um Produto para ver Similares (Heatmap):", 
        options=sorted_options,
        index=index
    )
    
    if selected_prod_name:
        target_id = available_products.loc[available_products["Produto"] == selected_prod_name, "id_product"].iloc[0]
        
        reference_product = (
            df_cosine_similarity.loc[target_id]
            .drop(target_id) # removes own product from the recomendation
            .sort_values(ascending=False)
        )
        
        top10_ranking = (
            reference_product
            .reset_index()
            .rename(columns={"index": "id_product", target_id: "cos_similarity"})
            .head(10)
        )
        
        # recovers name of products
        top10_ranking = top10_ranking.merge(
            df_dict_names, 
            on="id_product", 
            how="left"
        )
        
        # plot heatmap
        fig_sim = px.bar(
            top10_ranking.sort_values("cos_similarity"), 
            x="cos_similarity",
            y="Produto",
            orientation="h",
            color="cos_similarity", 
            color_continuous_scale="Blues", 
            title=f"Top 10 Similares a '{selected_prod_name}'",
            labels={"Produto": "Produto Recomendado", "cos_similarity": "Similaridade"}
        )
        fig_sim.update_traces(texttemplate="%{x:.3f}", textposition="auto")
        fig_sim.update_layout(coloraxis_showscale=False) 
        st.plotly_chart(apply_default_layout(fig_sim), use_container_width=True)
        
st.markdown("---")
        
        
st.markdown("#### 📅 Evolução de Consumo por Categoria")

min_date_cat = df_products["sale_date"].min().date()
max_date_cat = df_products["sale_date"].max().date()

start_date_cat, end_date_cat = st.slider(
    "Filtre o Período Histórico (Categorias):",
    min_value=min_date_cat,
    max_value=max_date_cat,
    value=(min_date_cat, max_date_cat),
    format="DD/MM/YYYY",
    key="slider_cat_tempo_full"
)

mask_cat = (df_products["sale_date"].dt.date >= start_date_cat) & (df_products["sale_date"].dt.date <= end_date_cat)
df_filtered_products = df_products.loc[mask_cat]

category_qtd_df = (
    df_filtered_products
    .groupby([df_filtered_products["sale_date"].dt.date, "actual_category"])["qtd"]
    .sum()
    .reset_index()
)
category_qtd_df.rename(columns={"sale_date": "Data"}, inplace=True)

fig_cat_time = px.line(
    category_qtd_df,
    x="Data",
    y="qtd",
    color="actual_category",
    labels={
        "Data": "Data da Venda",
        "qtd": "Volume Comprado",
        "actual_category": "Categoria"
    }
)

fig_cat_time.update_layout(height=500, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_cat_time, use_container_width=True)   