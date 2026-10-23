def agregar_registro(historial, numero_ingresado, nombre_base_origen, nombre_base_destino, resultado):
    """Agrega una conversión válida al final del historial."""
    registro = {
        "entrada": numero_ingresado,
        "origen": nombre_base_origen,
        "destino": nombre_base_destino,
        "resultado": resultado,
    }
    historial.append(registro)


def historial_esta_vacio(historial):
    """Devuelve True si no hay registros."""
    return len(historial) == 0


def eliminar_registro(historial, numero_registro):
    """Elimina el registro con ese número (empezando en 1) y lo devuelve.

    numero_registro debe estar ya validado: entre 1 y len(historial).
    """
    return historial.pop(numero_registro - 1)


def vaciar_historial(historial):
    """Elimina todos los registros."""
    historial.clear()


def formatear_historial(historial):
    """Devuelve una lista de líneas de texto con los registros numerados
    y el total, lista para imprimir. Usar solo si el historial no está vacío.
    """
    lineas = []
    numero_registro = 1

    for registro in historial:
        lineas.append(f"Registro {numero_registro}")
        lineas.append(f"  Entrada: {registro['entrada']}")
        lineas.append(f"  Origen: {registro['origen']}")
        lineas.append(f"  Destino: {registro['destino']}")
        lineas.append(f"  Resultado: {registro['resultado']}")
        lineas.append("")
        numero_registro = numero_registro + 1

    lineas.append(f"Total de registros: {len(historial)}")
    return lineas


if __name__ == "__main__":
    # Pruebas rápidas: se ejecutan solo con "python historial.py"
    historial = []
    assert historial_esta_vacio(historial)

    agregar_registro(historial, "1A", "Hexadecimal", "Binario", "11010")
    agregar_registro(historial, "10", "Decimal", "Binario", "1010")
    agregar_registro(historial, "377", "Octal", "Decimal", "255")
    assert len(historial) == 3
    assert not historial_esta_vacio(historial)

    for linea in formatear_historial(historial):
        print(linea)

    # Eliminar el registro 2: el registro 3 pasa a ser el 2
    eliminado = eliminar_registro(historial, 2)
    assert eliminado["entrada"] == "10"
    assert len(historial) == 2
    assert historial[1]["entrada"] == "377"

    vaciar_historial(historial)
    assert historial_esta_vacio(historial)
    assert len(historial) == 0

    print("\nTodas las pruebas pasaron.")