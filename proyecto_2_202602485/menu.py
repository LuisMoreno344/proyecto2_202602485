from conversiones import BASES_NUMERICAS, convertir_numero
from historial import (
    agregar_registro,
    eliminar_registro,
    formatear_historial,
    historial_esta_vacio,
    vaciar_historial,
)
from practica import (
    describir_ejercicio,
    evaluar_respuesta,
    formatear_puntuacion,
    generar_ejercicio,
    reiniciar_puntuacion,
)
from validaciones import LONGITUD_MAXIMA, validar_numero, validar_opcion_menu

ANCHO_LINEA = 60
NOMBRES_BASES = list(BASES_NUMERICAS)  # Binario, Octal, Decimal, Hexadecimal



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
            return int(texto)  # permitido: opción de menú ya validada
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




def eliminar_registro_seleccionado(historial):
    """Pide el número de un registro, lo valida y lo elimina."""
    total_registros = len(historial)
    numero_registro = leer_opcion_menu(
        f"Número de registro a eliminar (1 a {total_registros}, 0 para cancelar): ",
        0,
        total_registros,
    )
    if numero_registro == 0:
        print("\nNo se eliminó ningún registro.")
        return

    eliminar_registro(historial, numero_registro)
    print(f"\nRegistro {numero_registro} eliminado.")


def consultar_historial(historial):
    """Muestra el historial y permite eliminar un registro, vaciarlo o volver."""
    volver = False
    while not volver:
        imprimir_encabezado("HISTORIAL DE CONVERSIONES")

        if historial_esta_vacio(historial):
            print("\nEl historial está vacío.")
            pausar()
            return

        print()
        for linea in formatear_historial(historial):
            print(linea)

        print()
        print("1. Eliminar un registro")
        print("2. Vaciar historial")
        print("3. Volver al menú principal")
        opcion = leer_opcion_menu("Seleccione una opción: ", 1, 3)

        if opcion == 1:
            eliminar_registro_seleccionado(historial)
        elif opcion == 2:
            vaciar_historial(historial)
            print("\nHistorial vaciado.")
        else:
            volver = True




def resolver_ejercicio(puntuacion):
    """Genera un ejercicio, pide la respuesta (hasta que tenga formato válido)
    y actualiza la puntuación. Las entradas inválidas no cuentan."""
    ejercicio = generar_ejercicio()

    imprimir_encabezado("EJERCICIO DE PRÁCTICA")
    print(describir_ejercicio(ejercicio))
    print()
    print("Ingrese únicamente el número de la respuesta.")
    print("Escriba 'volver' para cancelar el ejercicio (no se cuenta).")

    while True:
        texto_respuesta = input("Su respuesta: ")

        if texto_respuesta.strip().lower() == "volver":
            return

        fue_procesada, es_correcta, mensaje_error = evaluar_respuesta(
            ejercicio, texto_respuesta, puntuacion
        )
        if fue_procesada:
            break

        print(mensaje_error)
        print("Intente de nuevo.")

    print()
    if es_correcta:
        print("¡Respuesta correcta!")
    else:
        print(f"Respuesta incorrecta. La respuesta esperada es: {ejercicio['respuesta_esperada']}")

    print()
    for linea in formatear_puntuacion(puntuacion):
        print(linea)
    pausar()


def modo_practica(puntuacion):
    """Menú del modo de práctica. La puntuación se conserva mientras el
    programa esté abierto, hasta que el usuario la reinicie."""
    volver = False
    while not volver:
        imprimir_encabezado("MODO DE PRÁCTICA")
        print()
        for linea in formatear_puntuacion(puntuacion):
            print(linea)

        print()
        print("1. Resolver un nuevo ejercicio")
        print("2. Reiniciar puntuación")
        print("3. Volver al menú principal")
        opcion = leer_opcion_menu("Seleccione una opción: ", 1, 3)

        if opcion == 1:
            resolver_ejercicio(puntuacion)
        elif opcion == 2:
            reiniciar_puntuacion(puntuacion)
            print("\nPuntuación reiniciada.")
        else:
            volver = True