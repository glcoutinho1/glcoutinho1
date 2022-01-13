#carregar_rotulos.py

import pandas as pd

def carregar_rotulos_fraude():
    #tratamento do dataset de DIs em perdimento
    df_dis_perdimento = pd.read_excel("SQL/sql 10.xlsx", dtype={'cnpj': str})
    df_dis_perdimento.drop(df_dis_perdimento[df_dis_perdimento['cnpj'].map(len) == 11].index, inplace=True)
    se_cnpj_di_perdimento = df_dis_perdimento.groupby(df_dis_perdimento['cnpj'].str[:8])['nr_di'].count()
    
    #tratamento do dataset de Fichas do Radar - novo
    df_fichas_radar = pd.read_excel("SQL/sql 11 novo.xlsx")
    filtro = df_fichas_radar['tipo_ocorrencia'].isin(
        ['Clas.Inc.Ncm,Ex Merc.Identif.C/Impl.Adm-Li Nao Automatica',
         'Clas.Inc.Ncm,Ex Merc Nao Identif.C/Impl.Trib-Aliq <,Anti-Duming',
         'Clas.Inc.Ncm,Ex Merc Nao Identif.C/Impl.Adm-Li Nao Automatic',
         'Fraude Qto A Preco,Peso,Medida,Classif.E Qualidade Exportacao',
         'Merc. Nao Manifestada,Mesmo Declarada No Despacho'
         ])
    df_fichas_radar = df_fichas_radar[~filtro]
    se_cnpj_com_fdi_ocorrencia_grave = df_fichas_radar['cnpj'].drop_duplicates()
    
    #Juntando os conjuntos de CNPJ envolvidos em fraudes relacionadas com interposicao
    lista_cnpjs_interpostos = pd.concat(
        [pd.to_numeric(se_cnpj_di_perdimento.index.to_series()),
         se_cnpj_com_fdi_ocorrencia_grave])
    lista_cnpjs_interpostos.drop_duplicates(inplace=True)
    
    df_rotulos = pd.DataFrame(data={'Fraude?' : 1}, index=lista_cnpjs_interpostos)
    
    return df_rotulos

#Os CNPJs que retornaram no SQL significa que operaram pelo menos 1 vez no período
#2018 a 2021
def carregar_rotulos_vai_operar(so_impo):
    df_qtd_importacoes = pd.read_excel("SQL/operar/sql 9.xlsx", index_col='cnpj')

    if (so_impo):
       return pd.DataFrame(data={'Operou?' : 1}, index=df_qtd_importacoes.index)
    
    df_qtd_exportacoes = pd.read_excel("SQL/operar/sql 10.xlsx", index_col='cnpj')
    df_ret = pd.merge(df_qtd_importacoes, df_qtd_exportacoes, left_index=True, right_index=True, how='outer')

    return pd.DataFrame(data={'Operou?' : 1}, index=df_ret.index)

def remove_duplicados_por_index(df, debug, nome):  
    df_ret = pd.DataFrame(df)
    antes = df_ret.index.size;
    df_ret['index'] = df_ret.index
    df_ret = df_ret.drop_duplicates(subset='index')
    df_ret.drop(columns='index', inplace=True)
    depois = df_ret.index.size
    
    if (debug):
        if (antes != depois):
            print("DF: {} possui {} linhas com {} duplicadas.".format(nome, antes, antes - depois))
        else:
            print("DF: {} possui {} linhas sem duplicadas.".format(nome, antes))
        
    return df_ret