SIMBOLOS_DIGITOS = "0123456789ABCDEF"

BASES_NUMERICAS = {
    "Binario": 2,
    "Octal": 8,
    "Decimal": 10,
    "Hexadecimal": 16,
}


# ---------------------------------------------------------------
# Desde decimal: divisiones sucesivas
# ---------------------------------------------------------------

def convertir_decimal_a_base(numero_decimal, base):
    """Convierte un entero decimal a la base indicada (2, 8 o 16)
    mediante divisiones sucesivas.

    numero_decimal debe ser un entero ya validado.
    """
    pasos = []
    digitos_obtenidos = []  # residuos, en el orden en que se calculan

    # Caso especial: el cero no entra al ciclo de divisiones
    if numero_decimal == 0:
        pasos.append(f"0 / {base}: cociente = 0, residuo = 0, dígito = 0")
        pasos.append("Leer los residuos del último al primero: 0")
        return "0", pasos

    dividendo = numero_decimal
    while dividendo > 0:
        cociente = dividendo // base
        residuo = dividendo % base
        digito = SIMBOLOS_DIGITOS[residuo]

        pasos.append(
            f"{dividendo} / {base}: cociente = {cociente}, "
            f"residuo = {residuo}, dígito = {digito}"
        )

        digitos_obtenidos.append(digito)
        dividendo = cociente

    # Leer los residuos del último al primero
    resultado = ""
    posicion = len(digitos_obtenidos) - 1
    while posicion >= 0:
        resultado = resultado + digitos_obtenidos[posicion]
        posicion = posicion - 1

    pasos.append(f"Leer los residuos del último al primero: {resultado}")
    return resultado, pasos


def decimal_a_binario(numero_decimal):
    """Decimal a binario: divisiones sucesivas entre 2."""
    return convertir_decimal_a_base(numero_decimal, 2)


def decimal_a_octal(numero_decimal):
    """Decimal a octal: divisiones sucesivas entre 8."""
    return convertir_decimal_a_base(numero_decimal, 8)


def decimal_a_hexadecimal(numero_decimal):
    """Decimal a hexadecimal: divisiones sucesivas entre 16 (dígitos A-F)."""
    return convertir_decimal_a_base(numero_decimal, 16)



def convertir_base_a_decimal(texto_numero, base):
    """Convierte un número escrito en la base indicada (2, 8 o 16) a decimal
    mediante notación posicional.

    texto_numero debe ser una cadena ya validada para esa base.
    Devuelve (valor_decimal, pasos), donde valor_decimal es un entero.
    """
    pasos = []
    suma_aportes = 0
    potencia_actual = 1  # base elevada a la posición actual
    posicion = 0

    # Se recorre de derecha a izquierda: la posición 0 es el último dígito
    indice = len(texto_numero) - 1
    while indice >= 0:
        digito = texto_numero[indice].upper()
        valor_digito = SIMBOLOS_DIGITOS.index(digito)
        aporte = valor_digito * potencia_actual

        pasos.append(f"{digito} (valor {valor_digito}) x {base}^{posicion} = {aporte}")

        suma_aportes = suma_aportes + aporte
        potencia_actual = potencia_actual * base
        posicion = posicion + 1
        indice = indice - 1

    pasos.append(f"Suma de los aportes: {suma_aportes}")
    return suma_aportes, pasos


def binario_a_decimal(texto_binario):
    """Binario a decimal: notación posicional con base 2."""
    return convertir_base_a_decimal(texto_binario, 2)


def octal_a_decimal(texto_octal):
    """Octal a decimal: notación posicional con base 8."""
    return convertir_base_a_decimal(texto_octal, 8)


def hexadecimal_a_decimal(texto_hexadecimal):
    """Hexadecimal a decimal: notación posicional con base 16."""
    return convertir_base_a_decimal(texto_hexadecimal, 16)




def convertir_a_decimal(texto_numero, nombre_base_origen):
    """Elige la función de conversión hacia decimal según la base de origen."""
    if nombre_base_origen == "Binario":
        return binario_a_decimal(texto_numero)
    if nombre_base_origen == "Octal":
        return octal_a_decimal(texto_numero)
    return hexadecimal_a_decimal(texto_numero)


def convertir_desde_decimal(numero_decimal, nombre_base_destino):
    """Elige la función de conversión desde decimal según la base de destino."""
    if nombre_base_destino == "Binario":
        return decimal_a_binario(numero_decimal)
    if nombre_base_destino == "Octal":
        return decimal_a_octal(numero_decimal)
    return decimal_a_hexadecimal(numero_decimal)


def convertir_numero(texto_numero, nombre_base_origen, nombre_base_destino):
    """Convierte un número entre dos bases distintas.

    Si ninguna de las dos bases es decimal, se usa decimal como base intermedia.
    texto_numero debe estar validado para la base de origen, y las bases
    deben ser distintas.
    Devuelve (resultado, pasos) con los encabezados ETAPA incluidos.
    """
    pasos = []
    numero_etapa = 1

   
    if nombre_base_origen == "Decimal":
        numero_decimal = int(texto_numero)  # permitido: entrada decimal ya validada
    else:
        numero_decimal, pasos_hacia_decimal = convertir_a_decimal(texto_numero, nombre_base_origen)
        pasos.append(f"ETAPA {numero_etapa}: {nombre_base_origen.upper()} A DECIMAL")
        pasos.extend(pasos_hacia_decimal)
        numero_etapa = numero_etapa + 1

    
    if nombre_base_destino == "Decimal":
        resultado = str(numero_decimal)
    else:
        resultado, pasos_desde_decimal = convertir_desde_decimal(numero_decimal, nombre_base_destino)
        if len(pasos) > 0:
            pasos.append("")  # línea en blanco entre etapas
        pasos.append(f"ETAPA {numero_etapa}: DECIMAL A {nombre_base_destino.upper()}")
        pasos.extend(pasos_desde_decimal)

    pasos.append("")
    pasos.append(f"Resultado final en {nombre_base_destino}: {resultado}")
    return resultado, pasos


if __name__ == "__main__":
   
    casos = [
        {"Decimal": "0", "Binario": "0", "Octal": "0", "Hexadecimal": "0"},
        {"Decimal": "1", "Binario": "1", "Octal": "1", "Hexadecimal": "1"},
        {"Decimal": "10", "Binario": "1010", "Octal": "12", "Hexadecimal": "A"},
        {"Decimal": "26", "Binario": "11010", "Octal": "32", "Hexadecimal": "1A"},
        {"Decimal": "100", "Binario": "1100100", "Octal": "144", "Hexadecimal": "64"},
        {"Decimal": "255", "Binario": "11111111", "Octal": "377", "Hexadecimal": "FF"},
        {"Decimal": "4095", "Binario": "111111111111", "Octal": "7777", "Hexadecimal": "FFF"},
    ]
    nombres_bases = ["Binario", "Octal", "Decimal", "Hexadecimal"]

  
    for caso in casos:
        for origen in nombres_bases:
            for destino in nombres_bases:
                if origen != destino:
                    resultado, _ = convertir_numero(caso[origen], origen, destino)
                    assert resultado == caso[destino], (
                        f"Falló {origen} a {destino} con {caso[origen]}: "
                        f"obtuvo {resultado}, esperaba {caso[destino]}"
                    )

    
    assert convertir_numero("ff", "Hexadecimal", "Binario")[0] == "11111111"

    # Números grandes: 2 elevado a la 100
    assert convertir_numero("1" + "0" * 100, "Binario", "Hexadecimal")[0] == "1" + "0" * 25

    
    numero_grande = "9" * 128
    for destino in ["Binario", "Octal", "Hexadecimal"]:
        convertido, _ = convertir_numero(numero_grande, "Decimal", destino)
        de_vuelta, _ = convertir_numero(convertido, destino, "Decimal")
        assert de_vuelta == numero_grande, f"Falló la ida y vuelta con {destino}"

    print("Todas las pruebas pasaron.\n")

    resultado, pasos = convertir_numero("1A", "Hexadecimal", "Binario")
    for linea in pasos:
        print(linea)