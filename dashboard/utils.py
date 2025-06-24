import pandas as pd
import plotly.graph_objects as go
from dash import html
import dash_bootstrap_components as dbc
from .config import CINZA_NEUTRO, ALTURA_GRAFICO # Importar as novas constantes

def criar_figura_vazia(texto_titulo="Sem dados para os filtros selecionados", altura=ALTURA_GRAFICO): # Refatorar nome da função e parâmetros
    """Cria uma figura Plotly vazia com uma mensagem central."""
    fig = go.Figure()
    fig.update_layout(
        height=altura, # Usar novo parâmetro
        annotations=[dict(
            text=texto_titulo, # Usar novo parâmetro
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16, color=CINZA_NEUTRO) # Usar nova constante
        )]
    )
    # O template 'rossmann_template' cuidará do resto do estilo
    return fig

def criar_icone_informacao(id_icone, texto_tooltip): # Refatorar nome da função e parâmetros
    """Cria um ícone de informação com uma tooltip associada."""
    return html.Span([
        html.I(id=id_icone, className="fas fa-info-circle info-icon ms-2"),
        dbc.Tooltip(texto_tooltip, target=id_icone, placement='top')
    ], className="d-inline-block")

def filtrar_dataframe_para_3d(df_original, data_inicio, data_fim, feriado_estadual, feriado_escolar): # Refatorar nome da função e parâmetros
    """Filtra o DataFrame para a página 3D, aplicando apenas filtros de data e feriado."""
    if not data_inicio or not data_fim: # Usar novos parâmetros
        return pd.DataFrame()

    data_inicio_dt = pd.to_datetime(data_inicio) # Usar novo parâmetro
    data_fim_dt = pd.to_datetime(data_fim) # Usar novo parâmetro

    if data_inicio_dt > data_fim_dt: # Usar novos parâmetros
        return pd.DataFrame()

    # Aplica o filtro de data
    mascara_data = (df_original['Date'] >= data_inicio_dt) & (df_original['Date'] <= data_fim_dt) # Usar novos parâmetros
    df_filtrado = df_original[mascara_data].copy() # Refatorar nome da variável

    # Aplica filtros de feriado
    if feriado_estadual != 'all': # Usar novo parâmetro
        df_filtrado = df_filtrado[df_filtrado['StateHoliday'] == feriado_estadual] # Usar novo parâmetro

    if feriado_escolar != 'all': # Usar novo parâmetro
        df_filtrado = df_filtrado[df_filtrado['SchoolHoliday'] == int(feriado_escolar)] # Usar novo parâmetro

    return df_filtrado # Retornar novo nome de variável

def filtrar_dataframe(df_original, data_inicio, data_fim, tipos_loja, lojas_especificas, feriado_estadual, feriado_escolar): # Refatorar nome da função e parâmetros
    """Filtra o DataFrame principal com base nos inputs do usuário (LÓGICA CENTRALIZADA)."""

    # Validação de datas
    if not data_inicio or not data_fim: # Usar novos parâmetros
        return pd.DataFrame()

    data_inicio_dt = pd.to_datetime(data_inicio) # Usar novo parâmetro
    data_fim_dt = pd.to_datetime(data_fim) # Usar novo parâmetro

    if data_inicio_dt > data_fim_dt: # Usar novos parâmetros
        return pd.DataFrame()

    # Aplica o filtro de data que é comum a todos
    mascara_data = (df_original['Date'] >= data_inicio_dt) & (df_original['Date'] <= data_fim_dt) # Usar novos parâmetros
    df_filtrado = df_original[mascara_data].copy() # Refatorar nome da variável

    # Aplica filtros de tipo de loja e loja específica de forma cumulativa
    if tipos_loja:
        df_filtrado = df_filtrado[df_filtrado['StoreType'].isin(tipos_loja)].copy()
    if lojas_especificas:
        df_filtrado = df_filtrado[df_filtrado['Store'].isin(lojas_especificas)].copy()

    # Aplica filtros de feriado
    if feriado_estadual != 'all': # Usar novo parâmetro
        df_filtrado = df_filtrado[df_filtrado['StateHoliday'] == feriado_estadual] # Usar novo parâmetro

    if feriado_escolar != 'all': # Usar novo parâmetro
        df_filtrado = df_filtrado[df_filtrado['SchoolHoliday'] == int(feriado_escolar)] # Usar novo parâmetro

    return df_filtrado # Retornar novo nome de variável