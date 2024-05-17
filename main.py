import functions
import archivosF

if __name__ == "__main__":
    while True:
        op = functions.menu()
        f = 0
    
        match op:
            case 1:
                archivosF.busqueda_archivo()
            case 2:
                functions.consultar_api()
            case 3:
                functions.borrar_todo()
            
            case 4:
                print("Saliendo...")
                break
            case _:
                print("Opción invalida")
            
        if f != 0:
            print("\nSaliendo...")
            break