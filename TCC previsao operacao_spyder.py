#arquivo principal

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import math
from pandas_profiling import ProfileReport
from sklearn.model_selection import train_test_split

import carregar_rotulos as cr
import gerar_grafico_categoricas as ggc

import treinarArvoreDecisao as tad
import treinarNB as tnb
import treinarRL as trl

import discretizador as discret

from yellowbrick.target import ClassBalance

debug = False
gerarGraficos = False
gerarRelatorio = False
treinar = True
cn = ['Não Fraude', 'Fraude']

#carrega dados para atributos
df_habilitados = pd.read_excel("SQL/sql 1.xlsx", index_col='cnpj')
df_receita_bruta = pd.read_excel("SQL/sql 2.xlsx", index_col='cnpj')
df_arrecadacao = pd.read_excel("SQL/sql 3.xlsx", index_col='cnpj')
df_dasn = pd.read_excel("SQL/sql 4.xlsx", index_col='cnpj')
df_qtde_empregados = pd.read_excel("SQL/sql 5.xlsx", index_col='cnpj')
df_gps_gfip_dctf = pd.read_excel("SQL/sql 6.xlsx", index_col='cnpj')
df_mov_fin = pd.read_excel("SQL/sql 7.xlsx", index_col='cnpj')
df_nfe_clientes = pd.read_excel("SQL/sql 8.xlsx", index_col='cnpj')
df_cnae = pd.read_excel('SQL/sql 9.xlsx', index_col='cnpj')

#remove cnpjs duplicados
df_habilitados = cr.remove_duplicados_por_index(df_habilitados, debug, "df_habilitados")
df_receita_bruta = cr.remove_duplicados_por_index(df_receita_bruta, debug, "receita")
df_arrecadacao = cr.remove_duplicados_por_index(df_arrecadacao, debug, "df_arrecadacao")
df_dasn = cr.remove_duplicados_por_index(df_dasn, debug, "df_dasn")
df_qtde_empregados = cr.remove_duplicados_por_index(df_qtde_empregados, debug, "df_qtde_empregados")
df_gps_gfip_dctf = cr.remove_duplicados_por_index(df_gps_gfip_dctf, debug, "df_gps_gfip_dctf")
df_mov_fin = cr.remove_duplicados_por_index(df_mov_fin, debug, "df_mov_fin")
df_nfe_clientes = cr.remove_duplicados_por_index(df_nfe_clientes, debug, "df_nfe_clientes")
df_cnae = cr.remove_duplicados_por_index(df_cnae, debug, "df_cnae")

#cria coluna com total de clientes
df_nfe_clientes['total_clientes'] = df_nfe_clientes['qtde_pj'] + df_nfe_clientes['qtde_pf']

#carregar dados dos rotulos
df_rotulos = cr.carregar_rotulos_fraude()

#junta os dataframes num dataframe único
df_fim = pd.merge(df_habilitados, df_receita_bruta, left_index=True, right_index=True, how='left')
df_fim = pd.merge(df_fim, df_arrecadacao, left_index=True, right_index=True, how='left')
df_fim = pd.merge(df_fim, df_dasn, left_index=True, right_index=True, how='left')
df_fim = pd.merge(df_fim, df_qtde_empregados, left_index=True, right_index=True, how='left')
df_fim = pd.merge(df_fim, df_mov_fin, left_index=True, right_index=True, how='left')
df_fim = pd.merge(df_fim, df_nfe_clientes, left_index=True, right_index=True, how='left')
df_fim = pd.merge(df_fim, df_cnae, left_index=True, right_index=True, how='left')
df_fim = pd.merge(df_fim, df_gps_gfip_dctf, left_index=True, right_index=True, how='left')
df_fim = pd.merge(df_fim, df_rotulos, left_index=True, right_index=True, how='left')

#limpeza de colunas que nao seram utilizadas
df_fim.drop(columns=
            ['nome_empresa',
             'ano_regis_rad',
             'dt_dia_regis_rad',
             'cd_sit_ficha_hab',
             'cd_sit_hab',
             'qtde_pj', 'qtde_pf'], inplace=True)

print(df_fim.info())

#contabiliza os ausentes
print(df_fim.isna().sum())

#preenche os valores inexistentes com 0
df_fim = df_fim.fillna(0)

#gera relatorio com estatisticas de cada coluna
if (gerarRelatorio):
    profile = ProfileReport(df_fim, title='Profiling TCC PUCMinas',html={'style':{'full_width':True}})
    profile.to_file(output_file="tcc_df_report.html")

#remover outlier de max_vinc_empregaticio
df_fim.drop(index=CCCCCCCC, inplace=True) #CNPJ omitido

#ordena os valores da coluna de rotulos para melhorar a visualizacao na hora de plotar
df_fim.sort_values(by='Fraude?', ascending=True, inplace=True)

#analise e exploracao das variaveis quantitativas
vars_quantitativas = ['receita_bruta', 'dasn_debito_declarado', 
                      'arrecadacao', 'mov_fin', 'max_vinc_empregaticio',
                      'total_clientes', 'gfip_debito','gps_inss', 'dctf_debito']

if (gerarGraficos):
    g = sb.pairplot(data=df_fim, vars=vars_quantitativas, hue='Fraude?', diag_kind=None, palette="tab10")
    g.fig.suptitle("Variáveis Contínuas (Sem Log)") 
    plt.savefig('figs/pp_continuas_sem_log.png')

    plt.rcParams.update({'font.size': 14, 'font.weight' : 'bold'})

    fig, ax = plt.subplots(constrained_layout=True, figsize=(18,10)) 
    sb.heatmap(df_fim[vars_quantitativas].corr(), annot=True) 
    fig.suptitle("Correlação Variáveis Quantitativas (Sem LOG)", fontsize = 18, fontweight='bold')
    fig.savefig('figs/heatmap_quant_no_log.png')

#aplica log nas colunas quantitativas tendo em vista a assimetria dos dados
df_fim_log = pd.DataFrame(df_fim, copy=True)
for var in vars_quantitativas:
    df_fim_log[var] = df_fim_log[var].apply(np.log10).replace([np.inf, -np.inf], np.nan).fillna(0)

if (gerarGraficos):
    g = sb.pairplot(data=df_fim_log, vars=vars_quantitativas, hue='Fraude?', diag_kind='hist', palette="tab10")
    g.fig.suptitle("Variáveis Contínuas (com Log)")
    plt.savefig('figs/pp_continuas_com_log.png')

    fig, ax = plt.subplots(constrained_layout=True, figsize=(18,10)) 
    sb.heatmap(df_fim_log[vars_quantitativas].corr(), annot=True) 
    fig.suptitle("Correlação Variáveis Quantitativas (LOG)", fontsize = 18, fontweight='bold') 
    fig.savefig('figs/heatmap_quant_log.png')


#analise e exploracao das variaveis qualitativas
vars_qualitativas = ['cd_submodalidade', 'cd_ua_jurisdicao_aduana', 'cnae']

if (gerarGraficos):
    for coluna in vars_qualitativas:
        fig, ax = ggc.gerar_grafico_variavel_categorica(df_fim, coluna, 'Fraude?', "Quantidade", coluna, coluna, False)
        fig.savefig('figs/' + coluna + '.png')

print('Quantidade de unidades aduaneiras distintas: {}'.format(len(df_fim['cd_ua_jurisdicao_aduana'].value_counts())))
print(df_fim['cnae'].value_counts())

df_fim.insert(2, column='rf_jur_aduana', value=(df_fim['cd_ua_jurisdicao_aduana'] / 100000).apply(math.trunc))
df_fim_log.insert(2, column='rf_jur_aduana', value=(df_fim_log['cd_ua_jurisdicao_aduana'] / 100000).apply(math.trunc))

if (gerarGraficos):
    #gerar novamente o grafico de jurisdicao, mas agora pela RF
    fig, ax = ggc.gerar_grafico_variavel_categorica(df_fim, 'rf_jur_aduana', None, "Quantidade", "Região Fiscal", "Região Fiscal", True)
    fig.savefig('figs/rf_jur_aduana.png')

print('Quantidade de CNAEs distintos: {}'.format(len(df_fim['cnae'].value_counts())))
print('Quant. de CNAE com ocorrência de fraude: {}'.format(len(df_fim[df_fim['Fraude?'] == 1]['cnae'].value_counts())))
print(df_fim['cnae'].value_counts())
print(df_fim[df_fim['Fraude?'] == 1]['cnae'].value_counts())

df_fim.drop(columns=['cd_ua_jurisdicao_aduana'], inplace=True)
df_fim_log.drop(columns=['cd_ua_jurisdicao_aduana'], inplace=True)

#padroniza as habilitacoes expressas (403, 404, 405 e 415) = 1
#ajusta as demais para 2, 3 e 4 de acordo com a intensidade de exigencias para obter a habilitacao
df_fim['cd_submodalidade'].replace({403:1, 404:1, 405:1, 415:1, 413:2, 407:3, 416:4}, inplace=True)
df_fim_log['cd_submodalidade'].replace({403:1, 404:1, 405:1, 415:1, 413:2, 407:3, 416:4}, inplace=True)

#gerar dataset discretizado
df_fim_discretizado = pd.DataFrame(df_fim, copy=True)
for var_quant in vars_quantitativas:
    if (var_quant in ['receita_bruta', 'arrecadacao', 'mov_fin', 'gfip_debito', 'gps_inss', 'dctf_debito']):
        df_fim_discretizado[var_quant] = df_fim_discretizado[var_quant].apply(discret.discretizar_variavel_10M)
    elif (var_quant in ['dasn_debito_declarado']):
        df_fim_discretizado[var_quant] = df_fim_discretizado[var_quant].apply(discret.discretizar_variavel_1M)
    elif (var_quant in ['max_vinc_empregaticio', 'total_clientes']):
        df_fim_discretizado[var_quant] = df_fim_discretizado[var_quant].apply(discret.discretizar_variavel_100k)
    
if (gerarGraficos):
    g = sb.pairplot(data=df_fim_log, vars=vars_quantitativas, hue='Fraude?', diag_kind='hist', palette="tab10")
    g.fig.suptitle("Variáveis Contínuas (Discretizadas)")
    plt.savefig('figs/pp_continuas_discretizadas.png')
    
#verificar ocorrencias de fraude em cada valor
for v in vars_quantitativas:
    print(df_fim_discretizado[[v, 'Fraude?']].value_counts())
    
if (treinar):
    #separa os atributos e as classes (dados brutos)
    X = df_fim.iloc[:,0:(df_fim.shape[1] - 1)] 
    y = df_fim.iloc[:,df_fim.shape[1] - 1]
    
    #plota grafico de balanceamento das cargas
    if (gerarGraficos):
        visualizer = ClassBalance(labels=cn)
        visualizer.fit(y)
        visualizer.show()
    
    #base transformada em LOG
    X2 = df_fim_log.iloc[:,0:(df_fim_log.shape[1] - 1)] 
    y2 = df_fim_log.iloc[:,df_fim_log.shape[1] - 1]
    
    #discretizado
    X3 = df_fim_discretizado.iloc[:,0:(df_fim_discretizado.shape[1] - 1)] 
    y3 = df_fim_discretizado.iloc[:,df_fim_discretizado.shape[1] - 1]
    
    #gera os conjuntos de treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.3, stratify=y) 
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y2, random_state=0, test_size=0.3, stratify=y2) 
    X_train3, X_test3, y_train3, y_test3 = train_test_split(X3, y3, random_state=0, test_size=0.3, stratify=y3) 
    
    print('\nTreinando Conjunto com Dados Brutos---------\n')
    y_prev1 = tad.treinarArvore(X_train, y_train, X_test, y_test, cn, "Dados Brutos - AD")
    print('\nTreinando Conjunto com Dados Transformado LOG---------\n')
    y_prev2 = tad.treinarArvore(X_train2, y_train2, X_test2, y_test2, cn, "Dados LOG - AD")
    print('\nTreinando Conjunto com Dados Transformados Discretização---------\n')
    y_prev3 = tad.treinarArvore(X_train3, y_train3, X_test3, y_test3, cn, "Dados Discretizados - AD")
    
    print('\nTreinando Conjunto com Dados Brutos---------\n')
    y_prev4 = tnb.treinarGNB(X_train, y_train, X_test, y_test, cn, "Dados Brutos GNB")
    print('\nTreinando Conjunto com Dados Transformado LOG---------\n')
    y_prev5 = tnb.treinarGNB(X_train2, y_train2, X_test2, y_test2, cn, "Dados LOG GNB")
    
    print('\nTreinando Conjunto com Dados Brutos---------\n')
    y_prev9 = trl.treinarRL(X_train, y_train, X_test, y_test, cn, "Dados Brutos - RL")
    print('\nTreinando Conjunto com Dados Transformado LOG---------\n')
    y_prev10 = trl.treinarRL(X_train2, y_train2, X_test2, y_test2, cn, "Dados LOG - RL")
    print('\nTreinando Conjunto com Dados Transformados Discretização---------\n')
    y_prev11 = trl.treinarRL(X_train3, y_train3, X_test3, y_test3, cn, "Dados Discretizados - RL")
    
print("\n\n------FIM------\n\n")