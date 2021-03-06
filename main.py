from matplotlib.axis import YAxis
import streamlit as st
import pandas as pd
import numpy as np
import csv
import plotly.graph_objects as go
import plotly.express as px

st.write('''# Análise dos Cursos de BSI - UAST
- Análise de Situação Unidade Curricular por Período''')
df = pd.read_csv('df_vinculo_disciplina_periodo.csv')
df_selection = df.query("PERIODO >= 2000.1 & CURSO == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO - UAST'")

df_curso = pd.read_csv('df_vinculo_curso_periodo.csv')
df_selection_curso = df_curso.query("CURSO == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO - UAST' |  CURSO == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO' | CURSO == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO - UEDT'") #& CURSO == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO - UAST'
#CURSO == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO - UAST' &  CURSO == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO' & CURSO == 'BACHARELADO EM SISTEMAS DE INFORMAÇÃO - UEDT'


#FILTRO
st.sidebar.title("Filtros")

lista_curso = df_selection_curso[str('CURSO')].unique().tolist()
with st.sidebar.expander(label='Cursos', expanded=True): 
    for i, todo_text in enumerate(lista_curso):
        periodo_filtro = st.checkbox(label=f"{todo_text}",key=i)

lista_disciplinas = df_selection[str('UNIDADE_CURRICULAR')].unique().tolist()
with st.sidebar.expander(label='Disciplinas', expanded=True): 
    for i, todo_text in enumerate(lista_disciplinas):
        periodo_filtro = st.checkbox(label=f"{todo_text}",key=i)

lista_periodo = df_selection_curso[str('PERIODO')].unique().tolist()
with st.sidebar.expander(label='Período', expanded=True): 
    for i, todo_text in enumerate(lista_periodo):
        periodo_filtro = st.checkbox(label=f"{todo_text}",key=i)

lista_situacao = df_selection_curso[str('SITUACAO')].unique().tolist()
with st.sidebar.expander(label='Situação', expanded=True): 
    for i, todo_text in enumerate(lista_situacao):
        periodo_filtro = st.checkbox(label=f"{todo_text}",key=i)

#Página inicial

df_situacao_tipo_unidade = df_selection.query('TIPO_UNIDADE_CURRICULAR == "ESTAGIO" | TIPO_UNIDADE_CURRICULAR == "TCC" | TIPO_UNIDADE_CURRICULAR == "MONOGRAFIA" | SITUACAO == "APROVADO" | SITUACAO == "REPROVADO" ')
df_situacao_tipo_unidade = pd.DataFrame(df_situacao_tipo_unidade.groupby(['SITUACAO','PERIODO']).count()['TIPO_UNIDADE_CURRICULAR']).reset_index()

df_aprovado= df_situacao_tipo_unidade.query('SITUACAO=="APROVADO"')
df_situacao_tipo_unidade["SITUACAO_APROVADO"] = df_aprovado["SITUACAO"]

df_reprovado= df_situacao_tipo_unidade.query('SITUACAO=="REPROVADO"')
df_situacao_tipo_unidade["SITUACAO_REPROVADO"] = df_reprovado["SITUACAO"]

df_cancelado = df_situacao_tipo_unidade.query('SITUACAO=="CANCELADO"')
df_situacao_tipo_unidade["SITUACAO_CANCELADO"] = df_cancelado["SITUACAO"]

df_dispensado = df_situacao_tipo_unidade.query('SITUACAO=="DISPENSADO"')
df_situacao_tipo_unidade["SITUACAO_DISPENSADO"] = df_dispensado["SITUACAO"]

qtd_aprovado = pd.DataFrame(df_situacao_tipo_unidade.groupby(['SITUACAO_APROVADO']).agg({'TIPO_UNIDADE_CURRICULAR' : np.sum}))
qtd_reprovado = pd.DataFrame(df_situacao_tipo_unidade.groupby(['SITUACAO_REPROVADO']).agg({'TIPO_UNIDADE_CURRICULAR' : np.sum}))
qtd_cancelado = pd.DataFrame(df_situacao_tipo_unidade.groupby(['SITUACAO_CANCELADO']).agg({'TIPO_UNIDADE_CURRICULAR' : np.sum}))
qtd_dispensado = pd.DataFrame(df_situacao_tipo_unidade.groupby(['SITUACAO_DISPENSADO']).agg({'TIPO_UNIDADE_CURRICULAR' : np.sum}))

st.write(
"Nº Aprovados: ", qtd_aprovado.iat[0,0], 
" \n  Nº Reprovados: ",qtd_reprovado.iat[0,0],
"")

# Grafico 1 - Situação Unidade Curricular por Período
st.write('- Análise de Situação dos estudantes aprovados e reprovados')
col1, col2 = st.columns(2)
df_unidade_situacao = pd.DataFrame(df_selection.groupby(['SITUACAO','PERIODO']).count()['UNIDADE_CURRICULAR']).reset_index()

df_aprovado1= df_unidade_situacao.query('SITUACAO=="REPROVADO"')
df_unidade_situacao["SITUACAO_APROVADO"] = df_aprovado1["SITUACAO"]

df_reprovado1= df_unidade_situacao.query('SITUACAO=="DISPENSADO"')
df_unidade_situacao["SITUACAO_REPROVADO"] = df_reprovado1["SITUACAO"]

chart_1 = px.bar( df_unidade_situacao, x = 'PERIODO', y = 'UNIDADE_CURRICULAR', color = 'SITUACAO', barmode = 'group',labels={
'PERIODO': ' Período',
'UNIDADE_CURRICULAR': ' Total de alunos',
'SITUACAO': ' Situação' 
}, color_discrete_map={
    "CANCELADO" : "#ffdc00",
    "DISPENSADO" : "#0303ff",
    "OUTRO" : "#5a5a5a"
})

chart_1.update_layout(xaxis_type='category', yaxis_title='Quantidade de estudantes')
chart_1.update_xaxes(categoryorder='category ascending', tickangle= 45, showline=True, showgrid=False)
chart_1.update_yaxes(showline=True, showgrid=False)
chart_1.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',   
})
col1.plotly_chart(chart_1, use_container_width = True)
#st.write(chart_1)

# Grafico 2 - Situação dos estudantes aprovados e reprovados

chart_3= px.bar( df_situacao_tipo_unidade, x = 'PERIODO', y = 'TIPO_UNIDADE_CURRICULAR', color = 'SITUACAO', barmode = 'group',labels={
'PERIODO' : ' Período ',
'TIPO_UNIDADE_CURRICULAR' : 'SITUAÇÃO EM ESTÁGIO/TCC/MONOGRAFIA',
'SITUACAO' : ' Situação ' 

}, color_discrete_map={
    "APROVADO" : "#5ac85a",
    "CANCELADO" : "#ffdc00",
    "DISPENSADO" : "#0303ff",
    "REPROVADO" : "#f0785a",
    "OUTRO" : "#5a5a5a"
})
chart_3.update_layout(xaxis_type='category', yaxis_title='Situação em estágio/TCC/Monografia')
chart_3.update_xaxes(categoryorder='category ascending', tickangle= 45, showline=True, showgrid=False)
chart_3.update_yaxes(showline=True, showgrid=False)
chart_3.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',})
col2.plotly_chart(chart_3, use_container_width = True)
#st.plotly_chart(chart_3)



# Gráfico de pizza 1
st.write('- Análise de Situação dos estudantes em gráfico de pizza')
col3, col4 = st.columns(2)
df_situacao_estudante = df_selection.query('SITUACAO_SIGA == "APROVADO" | SITUACAO_SIGA == "REPROVADO"')
df_situacao_estudante = pd.DataFrame(df_situacao_estudante.groupby(['SITUACAO','PERIODO']).count()['SITUACAO_SIGA']).reset_index()
df_falta = df_selection.query('SITUACAO_SIGA == "REPROVADO"')
qtd_falta = (df_falta['SITUACAO_SIGA'].count()).sum()
df_nota = df_selection.query('SITUACAO_SIGA == "APROVADO"')
qtd_nota = (df_nota["SITUACAO_SIGA"].count()).sum()
labels = ['APROVADO','REPROVADO']
color_pie = ['#32CD32', '#DC143C']
fig = go.Figure(data=[go.Pie(labels=labels, values=[qtd_nota, qtd_falta], hole=.3, marker_colors=color_pie)])
fig.update_layout(xaxis_type='category', yaxis_title='BACHARELADO EM SISTEMAS DE INFORMAÇÃO - UAST')
col3.plotly_chart(fig, use_container_width = True )

#Gráfico de pizza 2
df_cancelado = df_selection.query('SITUACAO_SIGA == "CANCELADO"')
qtd_cancelado = (df_cancelado['SITUACAO_SIGA'].count()).sum()
df_dispensado = df_selection.query('SITUACAO_SIGA == "DISPENSADO"')
qtd_dispensado = (df_dispensado["SITUACAO_SIGA"].count()).sum()
labels = ['CANCELADO','DISPENSADO']
color_pie = ['#df5a24', '#ffdc00']
fig2 = go.Figure(data=[go.Pie(labels=labels, values=[qtd_cancelado, qtd_dispensado], hole=.3, marker_colors=color_pie)])
fig2.update_layout(xaxis_type='category', yaxis_title='BACHARELADO EM SISTEMAS DE INFORMAÇÃO - UAST')
col4.plotly_chart(fig2, use_container_width = True )

#Disciplinas em Gráfico de Pizza
st.write('- Análise de disciplinas em Gráfico de Pizza')
df_unidade_s = pd.DataFrame(df_selection.groupby(['UNIDADE_CURRICULAR','PERIODO']).count()['SITUACAO_SIGA']).reset_index()
fig_PIE = px.pie(df_unidade_s, values='SITUACAO_SIGA', names='UNIDADE_CURRICULAR')
st.write(fig_PIE)

bar_3 = px.histogram(df_selection, x="SITUACAO", y="MEDIA", color="NOME_CAMPUS", barmode='group', text_auto=True, height=400)
bar_3.update_layout(xaxis_title='Situação do Estudante', yaxis_title='Quantidade de Vinculados')
bar_3.update_xaxes(showline=True, showgrid=False)
bar_3.update_yaxes(showline=True, showgrid=False)
st.write(bar_3)
#gráfico bar
df_situacao = df_selection_curso

bar = px.histogram(df_situacao, x='SITUACAO', y='QTD_VINC',
             color='CAMPUS', barmode='group', text_auto=True)
bar.update_layout(xaxis_title='Situação do Estudante', yaxis_title='Quantidade de Vinculados no Campus')
bar.update_xaxes(showline=True, showgrid=False)
bar.update_yaxes(showline=True, showgrid=False)
st.write(bar)

bar_2 = px.histogram(df_situacao, x='SITUACAO', y='QTD_VINC',
             color='CURSO', barmode='group', text_auto=True)
bar_2.update_layout(xaxis_title='Situação do Estudante', yaxis_title='Quantidade de Vinculados')
bar_2.update_xaxes(showline=True, showgrid=False)
bar_2.update_yaxes(showline=True, showgrid=False)
st.write(bar_2)

fig4 = px.treemap(df_situacao, path=[px.Constant("TODOS"), 'SITUACAO'],
                    values='QTD_VINC'
)
st.write(fig4)