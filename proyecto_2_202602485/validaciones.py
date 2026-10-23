LONGITUD_MAXIMA = 128

DIGITOS_DECIMALES = "0123456789"

DIGITOS_POR_BASE = {
    "Binario": "01",
    "Octal": "01234567",
    "Decimal": "0123456789",
    "Hexadecimal": "0123456789ABCDEFabcdef",
}

DESCRIPCION_DIGITOS_POR_BASE = {
    "Binario": "0 y 1",
    "Octal": "del 0 al 7",
    "Decimal": "del 0 al 9",
    "Hexadecimal": "del 0 al 9 y de la A a la F (mayúsculas o minúsculas)",
}


def contiene_solo_digitos_decimales(texto):
    """Devuelve True si el texto no está vacío y todos sus caracteres son 0-9."""
    if texto == "":
        return False
    for caracter in texto:
        if caracter not in DIGITOS_DECIMALES:
            return False
    return True


def validar_opcion_menu(texto, opcion_minima, opcion_maxima):
    """Valida que el texto sea un número entero dentro del rango del menú."""
    if texto == "":
        return False, "Error: no ingresó ninguna opción."

    if not contiene_solo_digitos_decimales(texto):
        return False, "Error: la opción debe ser un número entero."

    opcion = int(texto)  
    if opcion < opcion_minima or opcion > opcion_maxima:
        return False, f"Error: la opción debe estar entre {opcion_minima} y {opcion_maxima}."

    return True, ""


def validar_numero(texto, nombre_base):
    """Valida un número escrito en la base indicada.

    Reglas: entero no negativo, hasta 128 dígitos, sin espacios, signos,
    fracciones ni prefijos de base, y solo con los dígitos de esa base.
    """
    digitos_validos = DIGITOS_POR_BASE[nombre_base]

    if texto == "":
        return False, "Error: la entrada está vacía."

    if " " in texto:
        return False, "Error: no se permiten espacios."

    if "-" in texto or "+" in texto:
        return False, "Error: no se permiten signos; solo enteros no negativos."

    if "." in texto or "," in texto:
        return False, "Error: no se permiten números fraccionarios."

   
    if len(texto) > 1 and texto[0] == "0" and texto[1] in "boxBOX" and texto[1] not in digitos_validos:
        return False, "Error: no se permiten prefijos de base (0b, 0o, 0x)."

    if len(texto) > LONGITUD_MAXIMA:
        return False, f"Error: el número excede el máximo de {LONGITUD_MAXIMA} dígitos."

    for caracter in texto:
        if caracter not in digitos_validos:
            descripcion = DESCRIPCION_DIGITOS_POR_BASE[nombre_base]
            return False, f"Error: el carácter '{caracter}' no es válido en {nombre_base}. Dígitos permitidos: {descripcion}."

    return True, ""


def validar_bases_distintas(nombre_base_origen, nombre_base_destino):
    """Valida que la base de origen y la de destino no sean la misma."""
    if nombre_base_origen == nombre_base_destino:
        return False, "Error: la base de origen y la de destino no pueden ser la misma."
    return True, ""


if __name__ == "__main__":
    
    pruebas = [
        ("1010", "Binario"),
        ("0", "Binario"),
        ("", "Binario"),
        ("102", "Binario"),
        ("0b101", "Binario"),
        ("1 0", "Binario"),
        ("8", "Octal"),
        ("-5", "Decimal"),
        ("3.5", "Decimal"),
        ("1A", "Hexadecimal"),
        ("1a", "Hexadecimal"),
        ("0x1A", "Hexadecimal"),
        ("1G", "Hexadecimal"),
        ("9" * 128, "Decimal"),
        ("9" * 129, "Decimal"),
    ]
    for texto_prueba, base_prueba in pruebas:
        es_valido, mensaje = validar_numero(texto_prueba, base_prueba)
        texto_corto = texto_prueba if len(texto_prueba) <= 12 else texto_prueba[:12] + "..."
        print(f"{base_prueba:12} | {texto_corto:16} | {es_valido} {mensaje}")

    print(validar_opcion_menu("3", 1, 4))
    print(validar_opcion_menu("abc", 1, 4))
    print(validar_opcion_menu("9", 1, 4))
    print(validar_bases_distintas("Octal", "Octal"))