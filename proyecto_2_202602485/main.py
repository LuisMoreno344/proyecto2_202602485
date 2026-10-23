from menu import leer_opcion_menu, mostrar_menu_principal, realizar_conversion


def main():
    historial = []  
    salir = False

    while not salir:
        mostrar_menu_principal()
        opcion = leer_opcion_menu("Seleccione una opción: ", 1, 4)

        if opcion == 1:
            realizar_conversion(historial)
        elif opcion == 2:
            print("\nEl historial se agregará en la siguiente parte.")
        elif opcion == 3:
            print("\nEl modo de práctica se agregará en la siguiente parte.")
        else:
            print("\nGracias por usar el conversor. ¡Hasta pronto!")
            salir = True


if __name__ == "__main__":
    main()