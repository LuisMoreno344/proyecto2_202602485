SIMBOLOS_DIGITOS = "0123456789ABCDEF"


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


if __name__ == "__main__":
    # Pruebas rápidas: se ejecutan solo con "python conversiones.py"
    # (decimal, binario, octal, hexadecimal) con resultados calculados a mano
    casos = [
        (0, "0", "0", "0"),
        (1, "1", "1", "1"),
        (10, "1010", "12", "A"),
        (26, "11010", "32", "1A"),
        (100, "1100100", "144", "64"),
        (255, "11111111", "377", "FF"),
        (4095, "111111111111", "7777", "FFF"),
    ]

    for decimal, binario, octal, hexadecimal in casos:
        assert decimal_a_binario(decimal)[0] == binario, f"Falló binario de {decimal}"
        assert decimal_a_octal(decimal)[0] == octal, f"Falló octal de {decimal}"
        assert decimal_a_hexadecimal(decimal)[0] == hexadecimal, f"Falló hexadecimal de {decimal}"

    # Número grande: 2 elevado a la 100
    assert decimal_a_binario(2 ** 100)[0] == "1" + "0" * 100
    assert decimal_a_octal(2 ** 100)[0] == "2" + "0" * 33
    assert decimal_a_hexadecimal(2 ** 100)[0] == "1" + "0" * 25

    print("Todas las pruebas pasaron.\n")

    resultado, pasos = decimal_a_binario(26)
    print("Procedimiento de 26 a binario:")
    for linea in pasos:
        print(linea)