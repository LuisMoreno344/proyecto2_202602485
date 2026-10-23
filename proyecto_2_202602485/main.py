from menu import (
    consultar_historial,
    leer_opcion_menu,
    modo_practica,
    mostrar_menu_principal,
    realizar_conversion,
)
from practica import crear_puntuacion


def main():
    historial = []  
    puntuacion = crear_puntuacion() 
    salir = False

    while not salir:
        mostrar_menu_principal()
        opcion = leer_opcion_menu("Seleccione una opción: ", 1, 4)

        if opcion == 1:
            realizar_conversion(historial)
        elif opcion == 2:
            consultar_historial(historial)
        elif opcion == 3:
            modo_practica(puntuacion)
        else:
            print("\nGracias por usar el conversor. ¡Hasta pronto!")
            salir = True


if __name__ == "__main__":
    main()