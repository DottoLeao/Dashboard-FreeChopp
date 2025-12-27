"""
🍺 Dashboard Free Chopp Bar
Dashboard interativo para gestão de reservas de chopp

Autor: Desenvolvido por Lorenzo Leão Dotto
Data: Dezembro 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import hashlib

# =============================================
# CONFIGURAÇÃO DE SEGURANÇA
# =============================================
# ALTERE ESTAS CREDENCIAIS PARA AS SUAS!
USUARIO_CORRETO = "igor"
SENHA_CORRETA = "12345678"

def verificar_senha(senha):
    """Verifica se a senha está correta"""
    return senha == SENHA_CORRETA

def verificar_usuario(usuario):
    """Verifica se o usuário está correto"""
    return usuario.lower() == USUARIO_CORRETO.lower()

def tela_login():
    """Exibe a tela de login estilizada"""
    st.markdown("""
        <style>
            .login-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 60px 40px;
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 25px;
                box-shadow: 0 15px 50px rgba(0,0,0,0.4);
                backdrop-filter: blur(15px);
                margin: 100px auto;
                max-width: 400px;
            }
            .login-title {
                font-size: 2rem;
                color: white;
                margin-bottom: 10px;
            }
            .login-subtitle {
                color: rgba(255,255,255,0.7);
                margin-bottom: 30px;
            }
            .login-icon {
                font-size: 4rem;
                margin-bottom: 20px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
            <div style="text-align: center; margin-top: 50px;">
                <div style="font-size: 5rem;">🍺</div>
                <h1 style="color: white; margin: 20px 0 10px 0;">Free Chopp Dashboard</h1>
                <p style="color: rgba(255,255,255,0.7); margin-bottom: 40px;">Faça login para acessar o dashboard</p>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                login_btn = st.form_submit_button("🔓 Entrar", use_container_width=True)
            
            if login_btn:
                if verificar_usuario(usuario) and verificar_senha(senha):
                    st.session_state['autenticado'] = True
                    st.session_state['usuario'] = usuario
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos!")
        
        st.markdown("""
            <div style="text-align: center; margin-top: 40px; color: rgba(255,255,255,0.5); font-size: 0.8rem;">
                🔒 Área protegida - Acesso restrito
            </div>
        """, unsafe_allow_html=True)
    
    return False

def verificar_autenticacao():
    """Verifica se o usuário está autenticado"""
    return st.session_state.get('autenticado', False)


# =============================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================
st.set_page_config(
    page_title="🍺 Free Chopp Dashboard",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================
# ESTILOS CSS PERSONALIZADOS
# =============================================
st.markdown("""
<style>
    /* Tema escuro moderno */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Cards de métricas - CORRIGIDO PARA NOVA VERSÃO STREAMLIT */
    div[data-testid="stMetric"],
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.08) 100%) !important;
        border: 1px solid rgba(255,255,255,0.25) !important;
        border-radius: 15px !important;
        padding: 18px 14px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
        backdrop-filter: blur(10px) !important;
        height: 120px !important;
        min-height: 120px !important;
        max-height: 120px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: center !important;
    }
    
    /* FORÇAR TODOS OS TEXTOS BRANCOS NOS CARDS */
    div[data-testid="stMetric"] *,
    div[data-testid="metric-container"] * {
        color: #ffffff !important;
    }
    
    /* Valor principal do card */
    div[data-testid="stMetric"] [data-testid="stMetricValue"],
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1.6rem !important;
        font-weight: bold !important;
        color: #ffffff !important;
    }
    
    /* Label do card - FORÇAR COR BRANCA */
    div[data-testid="stMetric"] [data-testid="stMetricLabel"],
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] *,
    div[data-testid="stMetric"] label,
    div[data-testid="metric-container"] label {
        color: #ffffff !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        line-height: 1.4 !important;
        opacity: 1 !important;
    }
    
    /* Delta (variação) - Verde positivo */
    div[data-testid="stMetric"] [data-testid="stMetricDelta"],
    div[data-testid="stMetric"] [data-testid="stMetricDelta"] *,
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
        color: #4ade80 !important;
    }

    
    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* === FORÇAR TODAS AS FONTES BRANCAS === */
    .stApp, .stApp * {
        color: #ffffff !important;
    }
    
    /* Textos gerais */
    p, span, div, label, a, li, td, th {
        color: #ffffff !important;
    }
    
    /* Markdown */
    .stMarkdown, .stMarkdown * {
        color: #ffffff !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button,
    .stTabs [data-baseweb="tab-list"] button * {
        color: #ffffff !important;
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        color: #ffffff !important;
        border-bottom-color: #e94560 !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #0f3460 100%);
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, #e94560 0%, #0f3460 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(233, 69, 96, 0.4);
    }
    
    /* Selectbox e outros inputs - TEXTO BRANCO */
    .stSelectbox, .stSelectbox > div > div > div:first-child,
    .stMultiSelect, .stMultiSelect > div > div > div:first-child {
        color: #ffffff !important;
    }
    
    /* Date Input - campo principal com texto PRETO (fundo branco) */
    .stDateInput input,
    .stDateInput > div > div > input,
    .stDateInput [data-baseweb="input"] input,
    div[data-baseweb="input"] input {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
    }
    
    /* === CALENDÁRIO/DATEPICKER - FORÇAR TEXTO ESCURO === */
    /* Container do popup */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] *,
    div[data-baseweb="popover"] div,
    div[data-baseweb="popover"] span,
    div[data-baseweb="popover"] button,
    div[data-baseweb="popover"] p {
        color: #000000 !important;
    }
    
    /* Date picker específico */
    div[data-baseweb="datepicker"],
    div[data-baseweb="datepicker"] *,
    div[data-baseweb="datepicker"] div,
    div[data-baseweb="datepicker"] span,
    div[data-baseweb="datepicker"] button {
        color: #000000 !important;
    }
    
    /* Calendário */
    div[data-baseweb="calendar"],
    div[data-baseweb="calendar"] * {
        color: #000000 !important;
    }
    
    /* Dias do calendário */
    div[data-baseweb="calendar"] button,
    div[data-baseweb="calendar"] div[role="gridcell"],
    div[data-baseweb="calendar"] div[role="gridcell"] * {
        color: #000000 !important;
    }
    
    /* Dia selecionado - texto branco no fundo rosa */
    div[data-baseweb="calendar"] button[aria-selected="true"],
    div[data-baseweb="calendar"] div[data-highlighted="true"],
    div[data-baseweb="calendar"] div[aria-selected="true"] {
        color: #ffffff !important;
        background-color: #e94560 !important;
    }
    
    /* Cabeçalho do calendário (mês/ano) */
    div[data-baseweb="calendar"] div[role="presentation"],
    div[data-baseweb="calendar"] select,
    div[data-baseweb="calendar"] option {
        color: #000000 !important;
    }
    
    /* Setas de navegação */
    div[data-baseweb="calendar"] button[aria-label],
    div[data-baseweb="calendar"] svg {
        color: #000000 !important;
        fill: #000000 !important;
    }
    
    /* Dropdown do calendário (mês/ano) */
    ul[role="listbox"],
    ul[role="listbox"] li,
    ul[role="listbox"] * {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    
    /* Menu dropdown genérico */
    div[data-baseweb="menu"],
    div[data-baseweb="menu"] * {
        color: #000000 !important;
    }
    
    
    /* Expander */
    .streamlit-expanderHeader,
    .streamlit-expanderHeader * {
        color: #ffffff !important;
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    
    /* Tabelas */
    .stDataFrame, .stDataFrame *,
    .dataframe, .dataframe * {
        color: #ffffff !important;
        background-color: rgba(255,255,255,0.05) !important;
    }
    
    /* Cabeçalhos de tabela */
    .stDataFrame th, .dataframe th {
        color: #ffffff !important;
        background-color: rgba(255,255,255,0.15) !important;
    }
    
    /* Linhas de tabela */
    .stDataFrame td, .dataframe td {
        color: #ffffff !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.5);
        padding: 20px;
        font-size: 12px;
    }
    
    /* === LOADING SPINNER CUSTOMIZADO === */
    .stSpinner > div {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        background: linear-gradient(135deg, rgba(233, 69, 96, 0.1) 0%, rgba(15, 52, 96, 0.2) 100%) !important;
        border: 1px solid rgba(233, 69, 96, 0.3) !important;
        border-radius: 20px !important;
        padding: 40px 60px !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.4) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stSpinner > div > div {
        border-color: #e94560 transparent transparent transparent !important;
        width: 50px !important;
        height: 50px !important;
        border-width: 4px !important;
    }
    
    .stSpinner > div > span,
    .stSpinner > div > div + div {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        margin-top: 15px !important;
    }
    
    /* Loading text estilizado */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 60px;
        background: linear-gradient(135deg, rgba(233, 69, 96, 0.15) 0%, rgba(15, 52, 96, 0.25) 100%);
        border-radius: 25px;
        border: 1px solid rgba(233, 69, 96, 0.3);
        box-shadow: 0 15px 50px rgba(0,0,0,0.4);
        backdrop-filter: blur(15px);
        margin: 50px auto;
        max-width: 400px;
    }
    
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(255,255,255,0.2);
        border-top: 4px solid #e94560;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    .loading-text {
        color: #ffffff;
        font-size: 1.2rem;
        font-weight: 500;
        margin-top: 20px;
        text-align: center;
    }
    
    .loading-subtext {
        color: rgba(255,255,255,0.7);
        font-size: 0.9rem;
        margin-top: 8px;
        text-align: center;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading-beer {
        font-size: 3rem;
        animation: pulse 1.5s ease-in-out infinite;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# =============================================
# CORES DAS MARCAS
# =============================================
CORES_MARCAS = {
    'Heineken': '#008200',
    'Amstel': '#E4002B', 
    'Schin': '#0033A0'
}

CORES_STATUS_PGTO = {
    'Pago': '#00C853',
    'Parcial': '#FFD600',
    'Não Pago': '#FF1744',
    'OK': '#00C853',
    'P': '#FFD600',
    'N': '#FF1744'
}

CORES_STATUS_LOGISTICA = {
    'Entregue': '#00C853',
    'Pendente': '#FFD600'
}

# =============================================
# FUNÇÕES DE CARREGAMENTO DE DADOS
# =============================================
# URL do Google Sheets (exportado como CSV)
GOOGLE_SHEETS_ID = "1sFcVmvPgGPzaw5k2YgMblihg2tlzYrzfyP0chTWs1qk"
GOOGLE_SHEETS_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEETS_ID}/export?format=csv"

# Alternar entre Google Sheets e Excel local
USAR_GOOGLE_SHEETS = True  # Mude para False para usar Excel local

@st.cache_data(ttl=60)  # Cache por 1 minuto para refletir atualizações do Sheets
def carregar_dados():
    """Carrega dados do Google Sheets ou Excel local"""
    
    try:
        if USAR_GOOGLE_SHEETS:
            # Carregar do Google Sheets
            df = pd.read_csv(GOOGLE_SHEETS_URL, sep=',')
            
            # Renomear colunas do Sheets para padrão
            df = df.rename(columns={
                'DATA': 'Data_Evento',
                '30': 'Qtd_30L',
                '50': 'Qtd_50L',
                'PGTO': 'Status_Pagamento',
                'ENTREGUE': 'Status_Logistico_Raw',
                'RECOLHIDO': 'Status_Recolha_Raw',
                'DATA DE RECOLHA': 'Data_Recolha',
                'OBS:': 'Observacoes'
            })
        else:
            # Carregar do Excel local (fallback)
            caminho_arquivo = os.path.join(os.path.dirname(__file__), "Reservas_Free_Chopp_Formatado.xlsx")
            df = pd.read_excel(caminho_arquivo, sheet_name="Reservas")
            
            # Renomear colunas do Excel para padrão
            df = df.rename(columns={
                'DATA': 'Data_Evento',
                30: 'Qtd_30L',
                50: 'Qtd_50L',
                'PGTO': 'Status_Pagamento',
                'ENTREGUE': 'Status_Logistico_Raw',
                'RECOLHIDO': 'Status_Recolha_Raw',
                'DATA DE RECOLHA': 'Data_Recolha',
                'OBS:': 'Observacoes'
            })
        
        # Verificar se há dados
        if df.empty:
            return None, "Planilha vazia. Adicione dados na planilha Google Sheets."
        
        # Limpar dados - remover linhas vazias
        df = df[df['CLIENTE'].notna()]
        df = df[~df['CLIENTE'].astype(str).str.contains('Total', na=False)]
        
        # Converter colunas numéricas
        df['Qtd_30L'] = pd.to_numeric(df['Qtd_30L'], errors='coerce').fillna(0)
        df['Qtd_50L'] = pd.to_numeric(df['Qtd_50L'], errors='coerce').fillna(0)
        df['Total_Litros'] = df['Qtd_30L'] * 30 + df['Qtd_50L'] * 50
        
        # Converter VALOR (remove R$, pontos e converte vírgula para ponto)
        def limpar_valor(x):
            if pd.isna(x):
                return 0
            x_str = str(x).replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
            try:
                return float(x_str)
            except:
                return 0
        
        df['VALOR'] = df['VALOR'].apply(limpar_valor)
        
        # Converter datas
        df['Data_Evento'] = pd.to_datetime(df['Data_Evento'], format='%d/%m/%Y', errors='coerce')
        df['Data_Recolha'] = pd.to_datetime(df['Data_Recolha'], format='%d/%m/%Y', errors='coerce')
        
        # Padronizar status de pagamento (aceita vários formatos)
        status_pgto_map = {
            'OK': 'Pago', 'Pago': 'Pago', 'pago': 'Pago',
            'P': 'Parcial', 'Parcial': 'Parcial', 'parcial': 'Parcial',
            'N': 'Não Pago', 'Não Pago': 'Não Pago', 'nao pago': 'Não Pago', 'Nao Pago': 'Não Pago'
        }
        df['Status_Pagamento_Label'] = df['Status_Pagamento'].map(status_pgto_map).fillna(df['Status_Pagamento'])
        
        # Padronizar status logístico (TRUE/FALSE ou texto)
        df['Status_Logistico'] = df['Status_Logistico_Raw'].apply(
            lambda x: 'Entregue' if str(x).upper() in ['TRUE', '1', 'ENTREGUE', 'SIM', 'YES'] else 'Pendente'
        )
        
        # Padronizar status recolha (TRUE/FALSE ou texto)
        df['Status_Recolha'] = df['Status_Recolha_Raw'].apply(
            lambda x: 'Recolhido' if str(x).upper() in ['TRUE', '1', 'RECOLHIDO', 'SIM', 'YES'] else 'Pendente'
        )
        
        return df, None
        
    except Exception as e:
        return None, f"Erro ao carregar dados: {str(e)}"

# =============================================
# FUNÇÕES DE CÁLCULO DE KPIs
# =============================================
def calcular_kpis(df):
    """Calcula todos os KPIs do dashboard"""
    kpis = {}
    
    # Financeiro
    kpis['faturamento_total'] = df['VALOR'].sum()
    kpis['faturamento_recebido'] = df[df['Status_Pagamento_Label'] == 'Pago']['VALOR'].sum()
    kpis['faturamento_pendente'] = kpis['faturamento_total'] - kpis['faturamento_recebido']
    kpis['faturamento_parcial'] = df[df['Status_Pagamento_Label'] == 'Parcial']['VALOR'].sum()
    
    # Operacional
    kpis['total_reservas'] = len(df)
    kpis['ticket_medio'] = kpis['faturamento_total'] / kpis['total_reservas'] if kpis['total_reservas'] > 0 else 0
    kpis['total_litros'] = df['Total_Litros'].sum()
    kpis['total_barris_30l'] = df['Qtd_30L'].sum()
    kpis['total_barris_50l'] = df['Qtd_50L'].sum()
    kpis['total_barris'] = kpis['total_barris_30l'] + kpis['total_barris_50l']
    
    # Taxas
    kpis['taxa_pagamento'] = (df['Status_Pagamento_Label'] == 'Pago').sum() / kpis['total_reservas'] * 100 if kpis['total_reservas'] > 0 else 0
    kpis['taxa_entrega'] = (df['Status_Logistico'] == 'Entregue').sum() / kpis['total_reservas'] * 100 if kpis['total_reservas'] > 0 else 0
    kpis['taxa_recolha'] = (df['Status_Recolha'] == 'Recolhido').sum() / kpis['total_reservas'] * 100 if kpis['total_reservas'] > 0 else 0
    
    # Clientes
    kpis['clientes_unicos'] = df['CLIENTE'].nunique()
    kpis['valor_medio_cliente'] = kpis['faturamento_total'] / kpis['clientes_unicos'] if kpis['clientes_unicos'] > 0 else 0
    
    # Avançados
    kpis['preco_por_litro'] = kpis['faturamento_total'] / kpis['total_litros'] if kpis['total_litros'] > 0 else 0
    kpis['barris_pendentes'] = len(df[(df['Status_Recolha'] == 'Pendente') & (df['Status_Logistico'] == 'Entregue')])
    kpis['pagamentos_atrasados'] = df[(df['Status_Logistico'] == 'Entregue') & (df['Status_Pagamento_Label'] != 'Pago')]['VALOR'].sum()
    
    return kpis

# =============================================
# COMPONENTES DE VISUALIZAÇÃO
# =============================================
def criar_grafico_faturamento_marca(df):
    """Gráfico de barras - Faturamento por Marca"""
    dados = df.groupby('MARCA')['VALOR'].sum().reset_index()
    dados = dados.sort_values('VALOR', ascending=True)
    
    fig = px.bar(
        dados, 
        x='VALOR', 
        y='MARCA',
        orientation='h',
        color='MARCA',
        color_discrete_map=CORES_MARCAS,
        text='VALOR'
    )
    
    fig.update_traces(
        texttemplate='R$ %{text:,.0f}',
        textposition='inside',  # Dentro da barra
        textfont=dict(color='white', size=12, family='Arial Black'),
        insidetextanchor='end'  # Alinhado à direita dentro da barra
    )
    
    fig.update_layout(
        title=dict(text='💰 Faturamento por Marca', font=dict(color='white', size=16)),
        xaxis_title='Faturamento (R$)',
        yaxis_title='',
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300,
        margin=dict(l=10, r=30, t=50, b=30),
        xaxis=dict(tickfont=dict(color='white'), title=dict(font=dict(color='white'))),
        yaxis=dict(tickfont=dict(color='white'))
    )
    
    return fig


def criar_grafico_status_pagamento(df):
    """Gráfico de pizza - Status de Pagamento"""
    dados = df['Status_Pagamento_Label'].value_counts().reset_index()
    dados.columns = ['Status', 'Quantidade']
    
    cores = [CORES_STATUS_PGTO.get(s, '#888888') for s in dados['Status']]
    
    fig = px.pie(
        dados,
        values='Quantidade',
        names='Status',
        color='Status',
        color_discrete_map=CORES_STATUS_PGTO,
        hole=0.4
    )
    
    fig.update_traces(
        textinfo='percent+label',
        textfont_size=12
    )
    
    fig.update_layout(
        title=dict(text='📊 Status de Pagamento', font=dict(color='white', size=16)),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300,
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, font=dict(color='white'))
    )
    
    return fig

def criar_grafico_litros_marca(df):
    """Gráfico de barras - Litros por Marca"""
    dados = df.groupby('MARCA')['Total_Litros'].sum().reset_index()
    dados = dados.sort_values('Total_Litros', ascending=True)
    
    fig = px.bar(
        dados,
        x='Total_Litros',
        y='MARCA',
        orientation='h',
        color='MARCA',
        color_discrete_map=CORES_MARCAS,
        text='Total_Litros'
    )
    
    fig.update_traces(
        texttemplate='%{text:,.0f}L',
        textposition='inside',
        textfont=dict(color='white', size=12, family='Arial Black'),
        insidetextanchor='end'
    )
    
    fig.update_layout(
        title=dict(text='🍺 Litros por Marca', font=dict(color='white', size=16)),
        xaxis_title='Litros',
        yaxis_title='',
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300,
        margin=dict(l=10, r=30, t=50, b=30),
        xaxis=dict(tickfont=dict(color='white'), title=dict(font=dict(color='white'))),
        yaxis=dict(tickfont=dict(color='white'))
    )
    
    return fig

def criar_grafico_tendencia(df):
    """Gráfico de linha - Faturamento ao longo do tempo"""
    df_temp = df.copy()
    df_temp['Data_Evento'] = pd.to_datetime(df_temp['Data_Evento'])
    dados = df_temp.groupby(df_temp['Data_Evento'].dt.date)['VALOR'].sum().reset_index()
    dados.columns = ['Data', 'Faturamento']
    
    fig = px.area(
        dados,
        x='Data',
        y='Faturamento',
        markers=True
    )
    
    fig.update_traces(
        fill='tozeroy',
        line=dict(color='#e94560', width=3),
        fillcolor='rgba(233, 69, 96, 0.3)'
    )
    
    fig.update_layout(
        title=dict(text='📈 Faturamento por Data', font=dict(color='white', size=16)),
        xaxis_title='Data',
        yaxis_title='Faturamento (R$)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=350,
        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white'), title=dict(font=dict(color='white'))),
        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='white'), title=dict(font=dict(color='white')))
    )
    
    return fig

def criar_grafico_barris(df):
    """Gráfico de barras - Comparação 30L vs 50L"""
    total_30 = df['Qtd_30L'].sum()
    total_50 = df['Qtd_50L'].sum()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=['30 Litros', '50 Litros'],
        y=[total_30, total_50],
        marker_color=['#4CAF50', '#2196F3'],
        text=[f'{int(total_30)} barris', f'{int(total_50)} barris'],
        textposition='outside',
        textfont=dict(color='white', size=12)
    ))
    
    fig.update_layout(
        title=dict(text='🛢️ Barris por Tamanho', font=dict(color='white', size=16)),
        xaxis_title='',
        yaxis_title='Quantidade',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=300,
        showlegend=False,
        xaxis=dict(tickfont=dict(color='white')),
        yaxis=dict(tickfont=dict(color='white'), title=dict(font=dict(color='white')))
    )
    
    return fig

def criar_tabela_pendentes(df):
    """Tabela de reservas com pagamento pendente"""
    pendentes = df[df['Status_Pagamento_Label'] != 'Pago'][
        ['CLIENTE', 'Data_Evento', 'MARCA', 'VALOR', 'Status_Pagamento_Label', 'Status_Logistico']
    ].copy()
    
    pendentes['Data_Evento'] = pendentes['Data_Evento'].dt.strftime('%d/%m/%Y')
    pendentes['VALOR'] = pendentes['VALOR'].apply(lambda x: f'R$ {x:,.2f}')
    
    pendentes.columns = ['Cliente', 'Data', 'Marca', 'Valor', 'Pagamento', 'Entrega']
    
    return pendentes

def criar_tabela_recolha(df):
    """Tabela de barris pendentes de recolha"""
    pendentes = df[(df['Status_Recolha'] == 'Pendente') & (df['Status_Logistico'] == 'Entregue')][
        ['CLIENTE', 'Data_Evento', 'Data_Recolha', 'MARCA', 'Qtd_30L', 'Qtd_50L', 'LOCAL']
    ].copy()
    
    pendentes['Data_Evento'] = pendentes['Data_Evento'].dt.strftime('%d/%m/%Y')
    pendentes['Data_Recolha'] = pendentes['Data_Recolha'].dt.strftime('%d/%m/%Y')
    pendentes['Total_Barris'] = pendentes['Qtd_30L'] + pendentes['Qtd_50L']
    
    pendentes = pendentes[['CLIENTE', 'Data_Recolha', 'MARCA', 'Total_Barris', 'LOCAL']]
    pendentes.columns = ['Cliente', 'Data Recolha', 'Marca', 'Barris', 'Local']
    
    return pendentes

# =============================================
# DASHBOARD PRINCIPAL
# =============================================
def main():
    # Placeholder para loading em tela cheia
    loading_container = st.empty()
    
    # Mostrar loading enquanto carrega
    with loading_container.container():
        st.markdown("""
            <style>
                .fullscreen-loading {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100vw;
                    height: 100vh;
                    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    z-index: 9999;
                }
                .fullscreen-loading .beer-icon {
                    font-size: 4rem;
                    animation: bounce 1s ease-in-out infinite;
                }
                .fullscreen-loading .spinner {
                    width: 60px;
                    height: 60px;
                    border: 4px solid rgba(255,255,255,0.2);
                    border-top: 4px solid #e94560;
                    border-radius: 50%;
                    animation: spin 0.8s linear infinite;
                    margin: 20px 0;
                }
                .fullscreen-loading .text {
                    color: white;
                    font-size: 1.3rem;
                    font-weight: 500;
                }
                .fullscreen-loading .subtext {
                    color: rgba(255,255,255,0.7);
                    font-size: 0.9rem;
                    margin-top: 8px;
                }
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                @keyframes bounce {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-10px); }
                }
            </style>
            <div class="fullscreen-loading">
                <div class="beer-icon">🍺</div>
                <div class="spinner"></div>
                <div class="text">Carregando dados...</div>
                <div class="subtext">Preparando seu dashboard de chopp</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Carregar dados (com cache de 5 minutos)
    df, erro = carregar_dados()
    
    # Limpar loading
    loading_container.empty()

    
    if erro:
        st.error(f"❌ {erro}")
        st.info("📁 Certifique-se de que o arquivo 'Reservas_Free_Chopp_Formatado.xlsx' está na mesma pasta do dashboard.")
        return
    
    if df is None or df.empty:
        st.warning("⚠️ Nenhum dado encontrado no arquivo.")
        return
    
    # =============================================
    # HEADER (após carregar dados)
    # =============================================
    col_header1, col_header2 = st.columns([3, 1])
    
    with col_header1:
        st.markdown("# 🍺 Free Chopp Dashboard")
        st.markdown("*Gestão completa de reservas de chopp*")
    
    with col_header2:
        if st.button("🔄 Atualizar Dados", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("---")
    
    # =============================================
    # SIDEBAR - FILTROS
    # =============================================
    with st.sidebar:
        # Info do usuário logado
        st.markdown(f"### 👤 Olá, {st.session_state.get('usuario', 'Usuário')}!")
        if st.button("🚪 Sair", use_container_width=True):
            st.session_state['autenticado'] = False
            st.session_state['usuario'] = None
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.markdown("## 🔍 Filtros")
        
        # Filtro de data
        st.markdown("### 📅 Período")
        data_min = df['Data_Evento'].min().date()
        data_max = df['Data_Evento'].max().date()
        
        datas = st.date_input(
            "Selecione o período",
            value=(data_min, data_max),
            min_value=data_min,
            max_value=data_max
        )
        
        if len(datas) == 2:
            df = df[(df['Data_Evento'].dt.date >= datas[0]) & (df['Data_Evento'].dt.date <= datas[1])]
        
        st.markdown("---")
        
        # Filtro de marca
        st.markdown("### 🍺 Marca")
        marcas = st.multiselect(
            "Selecione as marcas",
            options=df['MARCA'].unique().tolist(),
            default=df['MARCA'].unique().tolist()
        )
        df = df[df['MARCA'].isin(marcas)]
        
        st.markdown("---")
        
        # Filtro de status pagamento
        st.markdown("### 💳 Status Pagamento")
        status_pgto = st.multiselect(
            "Selecione os status",
            options=df['Status_Pagamento_Label'].unique().tolist(),
            default=df['Status_Pagamento_Label'].unique().tolist()
        )
        df = df[df['Status_Pagamento_Label'].isin(status_pgto)]
        
        st.markdown("---")
        
        # Info
        st.markdown("### ℹ️ Informações")
        st.markdown(f"**Registros:** {len(df)}")
        st.markdown(f"**Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    # Verificar se há dados após filtros
    if df.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
        return
    
    # Calcular KPIs
    kpis = calcular_kpis(df)
    
    # =============================================
    # LINHA 1 - CARDS DE KPIs PRINCIPAIS
    # =============================================
    st.markdown("## 📊 Indicadores Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Faturamento Total",
            value=f"R$ {kpis['faturamento_total']:,.2f}"
        )
    
    with col2:
        st.metric(
            label="✅ Faturamento Recebido",
            value=f"R$ {kpis['faturamento_recebido']:,.2f}",
            delta=f"{kpis['taxa_pagamento']:.1f}% pago"
        )
    
    with col3:
        st.metric(
            label="📋 Total de Reservas",
            value=f"{kpis['total_reservas']}"
        )
    
    with col4:
        st.metric(
            label="🎯 Ticket Médio",
            value=f"R$ {kpis['ticket_medio']:,.2f}"
        )
    
    st.markdown("")
    
    # Segunda linha de KPIs
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric(
            label="🍺 Total de Litros",
            value=f"{kpis['total_litros']:,.0f} L"
        )
    
    with col6:
        st.metric(
            label="🛢️ Total de Barris",
            value=f"{int(kpis['total_barris'])}",
            delta=f"{int(kpis['total_barris_30l'])} de 30L | {int(kpis['total_barris_50l'])} de 50L"
        )
    
    with col7:
        st.metric(
            label="👥 Clientes Únicos",
            value=f"{kpis['clientes_unicos']}"
        )
    
    with col8:
        st.metric(
            label="💵 Preço/Litro",
            value=f"R$ {kpis['preco_por_litro']:,.2f}"
        )
    
    st.markdown("---")
    
    # =============================================
    # LINHA 2 - GRÁFICOS ANALÍTICOS
    # =============================================
    st.markdown("## 📈 Análises")
    
    col_graf1, col_graf2, col_graf3 = st.columns(3)
    
    with col_graf1:
        st.plotly_chart(criar_grafico_faturamento_marca(df), use_container_width=True)
    
    with col_graf2:
        st.plotly_chart(criar_grafico_status_pagamento(df), use_container_width=True)
    
    with col_graf3:
        st.plotly_chart(criar_grafico_litros_marca(df), use_container_width=True)
    
    st.markdown("")
    
    # =============================================
    # LINHA 3 - TENDÊNCIA E DETALHES
    # =============================================
    col_tend, col_barris = st.columns([2, 1])
    
    with col_tend:
        st.plotly_chart(criar_grafico_tendencia(df), use_container_width=True)
    
    with col_barris:
        st.plotly_chart(criar_grafico_barris(df), use_container_width=True)
    
    st.markdown("---")
    
    # =============================================
    # ALERTAS OPERACIONAIS
    # =============================================
    st.markdown("## ⚠️ Alertas Operacionais")
    
    col_alert1, col_alert2, col_alert3 = st.columns(3)
    
    with col_alert1:
        cor = "🔴" if kpis['faturamento_pendente'] > 5000 else "🟡" if kpis['faturamento_pendente'] > 1000 else "🟢"
        st.metric(
            label=f"{cor} Faturamento Pendente",
            value=f"R$ {kpis['faturamento_pendente']:,.2f}"
        )
    
    with col_alert2:
        cor = "🔴" if kpis['barris_pendentes'] > 10 else "🟡" if kpis['barris_pendentes'] > 5 else "🟢"
        st.metric(
            label=f"{cor} Barris para Recolher",
            value=f"{kpis['barris_pendentes']} reservas"
        )
    
    with col_alert3:
        taxa_inadimplencia = 100 - kpis['taxa_pagamento']
        cor = "🔴" if taxa_inadimplencia > 30 else "🟡" if taxa_inadimplencia > 15 else "🟢"
        st.metric(
            label=f"{cor} Taxa Inadimplência",
            value=f"{taxa_inadimplencia:.1f}%"
        )
    
    st.markdown("---")
    
    # =============================================
    # TABELAS DETALHADAS
    # =============================================
    st.markdown("## 📋 Detalhes")
    
    tab1, tab2, tab3 = st.tabs(["💳 Pagamentos Pendentes", "🛢️ Recolhas Pendentes", "📊 Todos os Dados"])
    
    with tab1:
        st.markdown("### Reservas com Pagamento Pendente")
        tabela_pendentes = criar_tabela_pendentes(df)
        if not tabela_pendentes.empty:
            st.dataframe(tabela_pendentes, use_container_width=True, hide_index=True)
        else:
            st.success("✅ Todas as reservas estão pagas!")
    
    with tab2:
        st.markdown("### Barris Pendentes de Recolha")
        tabela_recolha = criar_tabela_recolha(df)
        if not tabela_recolha.empty:
            st.dataframe(tabela_recolha, use_container_width=True, hide_index=True)
        else:
            st.success("✅ Todos os barris foram recolhidos!")
    
    with tab3:
        st.markdown("### Base Completa")
        df_display = df[['CLIENTE', 'Data_Evento', 'MARCA', 'Qtd_30L', 'Qtd_50L', 'Total_Litros', 'VALOR', 'Status_Pagamento_Label', 'Status_Logistico', 'Status_Recolha']].copy()
        df_display['Data_Evento'] = df_display['Data_Evento'].dt.strftime('%d/%m/%Y')
        df_display.columns = ['Cliente', 'Data', 'Marca', '30L', '50L', 'Litros', 'Valor', 'Pagamento', 'Entrega', 'Recolha']
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # =============================================
    # FOOTER
    # =============================================
    st.markdown("---")
    st.markdown(
        """
        <div class="footer">
            🍺 Free Chopp Dashboard | Desenvolvido com Streamlit + Python | Dezembro 2025 | Lorenzo Dotto
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    # Verificar se está autenticado
    if not verificar_autenticacao():
        tela_login()
    else:
        main()
