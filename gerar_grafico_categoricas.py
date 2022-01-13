#gerar_grafico_categoricas.py

import matplotlib.pyplot as plt
import seaborn as sb

def gerar_grafico_variavel_categorica(df_fim, coluna_dados, coluna_rotulos, labely, labelx, titulo_grafico, exibir_contagem):
    fig, ax = plt.subplots(constrained_layout=True, figsize=(6,4))
    sb.countplot(data=df_fim, x=coluna_dados, hue=coluna_rotulos)
    ax.set_ylabel(labely)
    ax.set_xlabel(labelx)
    fig.suptitle(titulo_grafico, fontsize=18)
    if (exibir_contagem):
        for p in ax.patches:
            ax.annotate('{:.0f}'.format(p.get_height()), (p.get_x(), p.get_height()+50))
    return fig, ax
    