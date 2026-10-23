from conversiones import BASES_NUMERICAS, convertir_numero
from historial import agregar_registro
from validaciones import LONGITUD_MAXIMA, validar_numero, validar_opcion_menu

ANCHO_LINEA = 60
NOMBRES_BASES = list(BASES_NUMERICAS)  



def imprimir_encabezado(titulo):
    """Imprime un título entre dos líneas de signos '='."""
    print()
    print("=" * ANCHO_LINEA)
    print(titulo)
    print("=" * ANCHO_LINEA)


def pausar():
    """Espera a que el usuario presione Enter."""
    input("\nPresione Enter para continuar...")


def leer_opcion_menu(mensaje, opcion_minima, opcion_maxima):
    """Pide una opción hasta que sea válida y la devuelve como entero."""
    while True:
        texto = input(mensaje)
        es_valida, mensaje_error = validar_opcion_menu(texto, opcion_minima, opcion_maxima)
        if es_valida:
            return int(texto)  
        print(mensaje_error)




def mostrar_menu_principal():
    imprimir_encabezado("CONVERSOR DE SISTEMAS NUMÉRICOS")
    print("1. Realizar una conversión")
    print("2. Consultar el historial")
    print("3. Iniciar el modo de práctica")
    print("4. Salir")



def mostrar_opciones_bases(nombres_bases):
    """Muestra las bases numeradas desde 1 y la opción 0 para volver."""
    numero_opcion = 1
    for nombre_base in nombres_bases:
        print(f"{numero_opcion}. {nombre_base}")
        numero_opcion = numero_opcion + 1
    print("0. Volver al menú principal")


def seleccionar_base_origen():
    """Devuelve el nombre de la base de origen, o None si el usuario vuelve."""
    imprimir_encabezado("SELECCIONE LA BASE DE ORIGEN")
    mostrar_opciones_bases(NOMBRES_BASES)
    opcion = leer_opcion_menu("Seleccione una opción: ", 0, len(NOMBRES_BASES))
    if opcion == 0:
        return None
    return NOMBRES_BASES[opcion - 1]


def seleccionar_base_destino(nombre_base_origen):
    """Devuelve el nombre de la base de destino, o None si el usuario vuelve.

    La base de origen no aparece en el menú, así que no se puede elegir
    la misma base como origen y destino.
    """
    bases_destino = []
    for nombre_base in NOMBRES_BASES:
        if nombre_base != nombre_base_origen:
            bases_destino.append(nombre_base)

    imprimir_encabezado("SELECCIONE LA BASE DE DESTINO")
    mostrar_opciones_bases(bases_destino)
    opcion = leer_opcion_menu("Seleccione una opción: ", 0, len(bases_destino))
    if opcion == 0:
        return None
    return bases_destino[opcion - 1]




def pedir_numero(nombre_base_origen, nombre_base_destino):
    """Pide el número a convertir hasta que sea válido.

    Devuelve el texto ingresado, o None si el usuario escribe 'volver'.
    """
    imprimir_encabezado(f"CONVERSIÓN: {nombre_base_origen.upper()} A {nombre_base_destino.upper()}")
    print(f"Ingrese un entero no negativo de hasta {LONGITUD_MAXIMA} dígitos.")
    print("Escriba 'volver' para regresar al menú principal.")
    print()

    while True:
        texto_numero = input("Número a convertir: ")

        if texto_numero.strip().lower() == "volver":
            return None

        es_valido, mensaje_error = validar_numero(texto_numero, nombre_base_origen)
        if es_valido:
            return texto_numero

        print(mensaje_error)
        print("Intente de nuevo.")


def mostrar_resultado(texto_numero, nombre_base_origen, nombre_base_destino, resultado, pasos):
    """Muestra el resultado y el procedimiento paso a paso."""
    imprimir_encabezado("RESULTADO")
    print(f"Número ingresado: {texto_numero}")
    print(f"Base de origen: {nombre_base_origen}")
    print(f"Base de destino: {nombre_base_destino}")
    print(f"Resultado: {resultado}")

    imprimir_encabezado("PROCEDIMIENTO PASO A PASO")
    for linea in pasos:
        print(linea)


def realizar_conversion(historial):
    """Flujo completo de la opción 1. Solo las conversiones válidas se
    agregan al historial."""
    nombre_base_origen = seleccionar_base_origen()
    if nombre_base_origen is None:
        return

    nombre_base_destino = seleccionar_base_destino(nombre_base_origen)
    if nombre_base_destino is None:
        return

    texto_numero = pedir_numero(nombre_base_origen, nombre_base_destino)
    if texto_numero is None:
        return

    resultado, pasos = convertir_numero(texto_numero, nombre_base_origen, nombre_base_destino)
    mostrar_resultado(texto_numero, nombre_base_origen, nombre_base_destino, resultado, pasos)

    agregar_registro(historial, texto_numero, nombre_base_origen, nombre_base_destino, resultado)
    print("\nConversión agregada al historial.")
    pausar()