import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
@st.cache_data
def load_data(data_path):
    try:
        data = pd.read_csv(data_path)
    except:
        data = pd.read_csv("https://raw.githubusercontent.com/alwolmer/streamlit_projeto/refs/heads/main/time_df.csv")
    return data

data_path = "time_df.csv"
df = load_data(data_path)

# Sidebar options
st.sidebar.header("Opções de Visualização")
view_options = [
    "Comparação de Métrica entre Grupos",
    "Evolução Individual do Usuário",
    "Scatterplot entre Duas Variáveis",
    "Comparação de Boxplots por Quartil",
]
selected_view = st.sidebar.radio("Selecione a visualização desejada", view_options)

metrics = df.columns[3:]
metric_names_map = {
    'assiduity': 'Assiduidade',
    'sleep_duration': 'Duração do Sono',
    'sleep_quality': 'Qualidade do Sono',
    'hydration': 'Hidratação',
    'activity': 'Atividade',
    'stress': 'Estresse',
    'wellbeing': 'Bem-Estar'
}

# Show metric selector only for specific views
if selected_view in ["Comparação de Métrica entre Grupos", "Evolução Individual do Usuário"]:
    selected_metric = st.sidebar.selectbox("Selecione a métrica para visualização", metrics)

# Main Title
st.title("Análise Interativa dos Dados")

# Evolution of Metrics across Time for Both Groups
if selected_view == "Comparação de Métrica entre Grupos":
    st.header("Evolução das Métricas ao Longo do Tempo por Grupo")
    groups = df['group'].unique()
    selected_groups = st.sidebar.multiselect("Selecione os grupos", options=groups, default=groups)
    if len(selected_groups) > 0:
        filtered_data = df[df['group'].isin(selected_groups)]
        fig = go.Figure()
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        for i, group in enumerate(selected_groups):
            group_data = filtered_data[filtered_data['group'] == group]
            avg_metric = group_data.groupby('week')[selected_metric].mean()
            fig.add_trace(go.Scatter(
                x=avg_metric.index, y=avg_metric.values, mode='lines+markers', name=group, line=dict(color=colors[i % len(colors)])
            ))
        fig.update_layout(
            title=f"Evolução de {metric_names_map[selected_metric]} ao Longo do Tempo por Grupo",
            xaxis_title="Semana",
            yaxis_title=metric_names_map[selected_metric],
            legend_title="Grupo",
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font=dict(color='white')
        )
        st.plotly_chart(fig)

    # Basic Metric Comparisons for Both Groups (First and Last Week)
    st.header("Comparação Básica das Métricas entre os Grupos - Primeira e Última Semana")
    first_week = df['week'].min()
    last_week = df['week'].max()

    # Histogram for First Week
    st.subheader("Distribuição da Métrica na Primeira Semana")
    first_week_data = df[df['week'] == first_week]
    fig = px.histogram(
        first_week_data, x=selected_metric, color='group', barmode='overlay', marginal='violin',
        title=f"Distribuição de {metric_names_map[selected_metric]} na Primeira Semana por Grupo",
        labels={selected_metric: metric_names_map[selected_metric], "group": "Grupo", "user_id": "ID do Usuário", "week": "Semana", "assiduity": "Assiduidade", "sleep_duration": "Duração do Sono", "sleep_quality": "Qualidade do Sono", "hydration": "Hidratação", "activity": "Atividade", "stress": "Estresse", "wellbeing": "Bem-Estar"},
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white')
    )
    st.plotly_chart(fig)

    # Histogram for Last Week
    st.subheader("Distribuição da Métrica na Última Semana")
    last_week_data = df[df['week'] == last_week]
    fig = px.histogram(
        last_week_data, x=selected_metric, color='group', barmode='overlay', marginal='violin',
        title=f"Distribuição de {metric_names_map[selected_metric]} na Última Semana por Grupo",
        labels={selected_metric: selected_metric, "group": "Grupo", "user_id": "ID do Usuário", "week": "Semana", "assiduidade": "Assiduidade", "sleep_duration": "Duração do Sono", "sleep_quality": "Qualidade do Sono", "hydration": "Hidratação", "activity": "Atividade", "stress": "Estresse", "wellbeing": "Bem-Estar"},
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white')
    )
    st.plotly_chart(fig)

    # Boxplot for Last Week
    st.subheader("Boxplot da Métrica na Última Semana por Grupo")
    fig = px.box(
        last_week_data, x='group', y=selected_metric,
        title=f"Boxplot de {metric_names_map[selected_metric]} na Última Semana por Grupo",
        labels={"group": "Grupo", selected_metric: selected_metric},
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white')
    )
    st.plotly_chart(fig)

# Evolution of Metrics across Time for a Given User
elif selected_view == "Evolução Individual do Usuário":
    st.header("Evolução das Métricas ao Longo do Tempo para um Usuário")
    selected_group = st.selectbox("Selecione o Grupo", df['group'].unique())
    filtered_users = df[df['group'] == selected_group]['user_id'].unique()
    selected_user = st.selectbox("Selecione o ID do Usuário", filtered_users)
    user_data = df[df['user_id'] == selected_user]
    fig = px.line(
        user_data, x='week', y=selected_metric, markers=True,
        title=f"Evolução de {metric_names_map[selected_metric]} ao Longo do Tempo para o Usuário {selected_user}",
        labels={"week": "Semana", selected_metric: metric_names_map[selected_metric], "user_id": "ID do Usuário"},
        color_discrete_sequence=['#17becf']
    )
    fig.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white')
    )
    st.plotly_chart(fig)

# Scatterplot Comparison between Two Variables
elif selected_view == "Scatterplot entre Duas Variáveis":
    st.header("Scatterplot entre Duas Variáveis")
    variable_x = st.selectbox("Selecione a primeira variável (eixo X)", metrics, key='var_x')
    variable_y = st.selectbox("Selecione a segunda variável (eixo Y)", metrics, key='var_y')
    selected_week = st.slider("Selecione a Semana", int(df['week'].min()), int(df['week'].max()))
    week_data = df[df['week'] == selected_week]
    fig = px.scatter(
        week_data, x=variable_x, y=variable_y, color='group',
        title=f"Scatterplot de {variable_x} vs {variable_y} na Semana {selected_week}",
        labels={variable_x: variable_x, variable_y: variable_y, "group": "Grupo"},
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white')
    )
    st.plotly_chart(fig)

# Boxplot Comparison by Quartiles
elif selected_view == "Comparação de Boxplots por Quartil":
    st.header("Comparação de Boxplots de uma Variável por Quartil de Outra Variável")
    metric_to_boxplot = st.selectbox("Selecione a métrica para o boxplot", [metric for metric in metrics if metric != 'assiduity'], key='boxplot_metric')
    metric_for_quartiles = st.selectbox("Selecione a métrica para determinar os quartis", [metric for metric in metrics if metric != 'assiduity'], key='quartile_metric')
    last_week_data = df[df['week'] == df['week'].max()]
    quartiles = pd.qcut(last_week_data[metric_for_quartiles], q=4, labels=["1º Quartil", "2º Quartil", "3º Quartil", "4º Quartil"])
    last_week_data['Quartil'] = pd.qcut(last_week_data[metric_for_quartiles].rank(method='first'), q=4, labels=["1º Quartil", "2º Quartil", "3º Quartil", "4º Quartil"])
    fig = px.box(
    last_week_data.sort_values(by='Quartil'), x='Quartil', y=metric_to_boxplot,
        title=f"Boxplot de {metric_to_boxplot} por Quartil de {metric_for_quartiles} (Última Semana)",
        labels={"Quartil": "Quartil de " + metric_for_quartiles, metric_to_boxplot: metric_to_boxplot},
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color='white')
    )
    st.plotly_chart(fig)



# Run the Streamlit app with: streamlit run script_name.py
