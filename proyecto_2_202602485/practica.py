import random

from conversiones import convertir_desde_decimal, convertir_numero
from validaciones import validar_numero

NOMBRES_BASES = ["Binario", "Octal", "Decimal", "Hexadecimal"]

VALOR_MINIMO_PRACTICA = 0
VALOR_MAXIMO_PRACTICA = 255




def crear_puntuacion():
    """Crea una puntuación nueva, con todo en cero."""
    return {"aciertos": 0, "respondidos": 0}


def reiniciar_puntuacion(puntuacion):
    """Pone la puntuación en cero."""
    puntuacion["aciertos"] = 0
    puntuacion["respondidos"] = 0


def calcular_porcentaje_aciertos(puntuacion):
    """Devuelve el porcentaje de aciertos (0.0 si aún no hay respuestas)."""
    if puntuacion["respondidos"] == 0:
        return 0.0
    return puntuacion["aciertos"] * 100 / puntuacion["respondidos"]


def formatear_puntuacion(puntuacion):
    """Devuelve las tres líneas de texto de la puntuación, listas para imprimir."""
    porcentaje = round(calcular_porcentaje_aciertos(puntuacion), 1)
    return [
        f"Aciertos: {puntuacion['aciertos']}",
        f"Ejercicios respondidos: {puntuacion['respondidos']}",
        f"Porcentaje de aciertos: {porcentaje}%",
    ]




def generar_ejercicio():
    """Genera un ejercicio aleatorio de conversión entre dos bases distintas.

    El valor equivale a un decimal entre 0 y 255.
    Devuelve un diccionario con: numero, base_origen, base_destino y
    respuesta_esperada.
    """
    valor_decimal = random.randint(VALOR_MINIMO_PRACTICA, VALOR_MAXIMO_PRACTICA)
    base_origen = random.choice(NOMBRES_BASES)

  
    bases_posibles_destino = []
    for nombre_base in NOMBRES_BASES:
        if nombre_base != base_origen:
            bases_posibles_destino.append(nombre_base)
    base_destino = random.choice(bases_posibles_destino)

   
    if base_origen == "Decimal":
        numero_origen = str(valor_decimal)
    else:
        numero_origen, _ = convertir_desde_decimal(valor_decimal, base_origen)

   
    respuesta_esperada, _ = convertir_numero(numero_origen, base_origen, base_destino)

    return {
        "numero": numero_origen,
        "base_origen": base_origen,
        "base_destino": base_destino,
        "respuesta_esperada": respuesta_esperada,
    }


def describir_ejercicio(ejercicio):
    """Devuelve el enunciado del ejercicio."""
    return (
        f"Convierta {ejercicio['numero']} de {ejercicio['base_origen']} "
        f"a {ejercicio['base_destino']}."
    )




def quitar_ceros_izquierda(texto):
    """Quita los ceros a la izquierda, dejando al menos un dígito ("000" -> "0")."""
    posicion = 0
    while posicion < len(texto) - 1 and texto[posicion] == "0":
        posicion = posicion + 1
    return texto[posicion:]


def respuesta_es_correcta(ejercicio, texto_respuesta):
    """Compara la respuesta con la esperada, sin distinguir mayúsculas
    (hexadecimal) ni ceros a la izquierda."""
    respuesta = quitar_ceros_izquierda(texto_respuesta.upper())
    esperada = quitar_ceros_izquierda(ejercicio["respuesta_esperada"].upper())
    return respuesta == esperada


def evaluar_respuesta(ejercicio, texto_respuesta, puntuacion):
    """Valida la respuesta, la compara con la esperada y actualiza la puntuación.

    Devuelve una tupla (fue_procesada, es_correcta, mensaje_error):
      - Formato inválido: (False, False, mensaje) y la puntuación NO cambia.
      - Formato válido:   (True, es_correcta, "") y se cuenta como respondido.
    """
    es_valida, mensaje_error = validar_numero(texto_respuesta, ejercicio["base_destino"])
    if not es_valida:
        return False, False, mensaje_error

    es_correcta = respuesta_es_correcta(ejercicio, texto_respuesta)

    puntuacion["respondidos"] = puntuacion["respondidos"] + 1
    if es_correcta:
        puntuacion["aciertos"] = puntuacion["aciertos"] + 1

    return True, es_correcta, ""


if __name__ == "__main__":
    
    from conversiones import convertir_a_decimal
    from validaciones import validar_numero as validar_para_prueba

   
    for _ in range(1000):
        ejercicio = generar_ejercicio()
        assert ejercicio["base_origen"] != ejercicio["base_destino"]

        es_valido, _mensaje = validar_para_prueba(ejercicio["numero"], ejercicio["base_origen"])
        assert es_valido

        if ejercicio["base_origen"] == "Decimal":
            valor = int(ejercicio["numero"])
        else:
            valor, _pasos = convertir_a_decimal(ejercicio["numero"], ejercicio["base_origen"])
        assert 0 <= valor <= 255

    print("Ejemplo de ejercicio generado:")
    print(describir_ejercicio(generar_ejercicio()))
    print()

    
    puntuacion = crear_puntuacion()
    assert calcular_porcentaje_aciertos(puntuacion) == 0.0

    ejercicio_1 = {"numero": "1A", "base_origen": "Hexadecimal",
                   "base_destino": "Binario", "respuesta_esperada": "11010"}
    ejercicio_2 = {"numero": "11010", "base_origen": "Binario",
                   "base_destino": "Hexadecimal", "respuesta_esperada": "1A"}

    
    assert evaluar_respuesta(ejercicio_1, "11010", puntuacion) == (True, True, "")
    assert puntuacion == {"aciertos": 1, "respondidos": 1}

   
    assert evaluar_respuesta(ejercicio_1, "11011", puntuacion) == (True, False, "")
    assert puntuacion == {"aciertos": 1, "respondidos": 2}

    
    procesada, correcta, mensaje = evaluar_respuesta(ejercicio_1, "12", puntuacion)
    assert procesada is False and correcta is False and mensaje != ""
    assert puntuacion == {"aciertos": 1, "respondidos": 2}


    assert evaluar_respuesta(ejercicio_2, "1a", puntuacion) == (True, True, "")
    assert evaluar_respuesta(ejercicio_2, "01A", puntuacion) == (True, True, "")

    for linea in formatear_puntuacion(puntuacion):
        print(linea)
    assert puntuacion == {"aciertos": 3, "respondidos": 4}
    assert calcular_porcentaje_aciertos(puntuacion) == 75.0


    reiniciar_puntuacion(puntuacion)
    assert puntuacion == {"aciertos": 0, "respondidos": 0}

    print("\nTodas las pruebas pasaron.")