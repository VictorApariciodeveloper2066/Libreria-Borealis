import random

def seleccionar_ganador(boletos_pagados):
    """
    Selecciona un ganador aleatorio de los boletos pagados
    """
    if not boletos_pagados:
        return None
    return random.choice(boletos_pagados)
