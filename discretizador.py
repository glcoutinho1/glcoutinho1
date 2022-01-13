#discretizador.py

def discretizar_variavel_10M(x):
    if (x < 100000):
        return 1
    else:
        return 0
    
def discretizar_variavel_1M(x):
    if (x < 10000):
        return 1
    else:
        return 0
    
def discretizar_variavel_100k(x):
    if (x < 20):
        return 1
    else:
        return 0