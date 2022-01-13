#verificar_ausentes_duplicados.py

import pandas as pd
import carregar_rotulos as cr

debug = True

#dados para atributos
df_habilitados = pd.read_excel("SQL/sql 1.xlsx", index_col='cnpj')
df_receita_bruta = pd.read_excel("SQL/sql 2.xlsx", index_col='cnpj')
df_arrecadacao = pd.read_excel("SQL/sql 3.xlsx", index_col='cnpj')
df_dasn = pd.read_excel("SQL/sql 4.xlsx", index_col='cnpj')
df_qtde_empregados = pd.read_excel("SQL/sql 5.xlsx", index_col='cnpj')
df_gps_gfip_dctf = pd.read_excel("SQL/sql 6.xlsx", index_col='cnpj')
df_mov_fin = pd.read_excel("SQL/sql 7.xlsx", index_col='cnpj')
df_nfe_clientes = pd.read_excel("SQL/sql 8.xlsx", index_col='cnpj')
df_cnae = pd.read_excel('SQL/sql 9.xlsx', index_col='cnpj')
#dados para rotulos
df_dis_perdimento = pd.read_excel("SQL/sql 10.xlsx", dtype={'cnpj': str})
df_fichas_radar = pd.read_excel("SQL/sql 11 novo.xlsx")

df_habilitados = cr.remove_duplicados_por_index(df_habilitados, debug, "df_habilitados")
df_receita_bruta = cr.remove_duplicados_por_index(df_receita_bruta, debug, "receita")
df_arrecadacao = cr.remove_duplicados_por_index(df_arrecadacao, debug, "df_arrecadacao")
df_dasn = cr.remove_duplicados_por_index(df_dasn, debug, "df_dasn")
df_qtde_empregados = cr.remove_duplicados_por_index(df_qtde_empregados, debug, "df_qtde_empregados")
df_gps_gfip_dctf = cr.remove_duplicados_por_index(df_gps_gfip_dctf, debug, "df_gps_gfip_dctf")
df_mov_fin = cr.remove_duplicados_por_index(df_mov_fin, debug, "df_mov_fin")
df_nfe_clientes = cr.remove_duplicados_por_index(df_nfe_clientes, debug, "df_nfe_clientes")
df_cnae = cr.remove_duplicados_por_index(df_cnae, debug, "df_cnae")

print("Verificando valores ausentes em df_habilitados: {}".format("Há ausentes." if df_habilitados.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_receita_bruta: {}".format("Há ausentes." if df_receita_bruta.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_arrecadacao: {}".format("Há ausentes." if df_arrecadacao.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_dasn: {}".format("Há ausentes." if df_dasn.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_qtde_empregados: {}".format("Há ausentes." if df_qtde_empregados.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_gps_gfip_dctf: {}".format("Há ausentes." if df_gps_gfip_dctf.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_mov_fin: {}".format("Há ausentes." if df_mov_fin.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_nfe_clientes: {}".format("Há ausentes." if df_nfe_clientes.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_cnae: {}".format("Há ausentes." if df_cnae.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_dis_perdimento: {}".format("Há ausentes." if df_dis_perdimento.isna().values.any() else "Não há ausentes."))
print("Verificando valores ausentes em df_fichas_radar: {}".format("Há ausentes." if df_fichas_radar.isna().values.any() else "Não há ausentes."))