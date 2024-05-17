import functions
import archivosF
import urllib.request

if __name__ == "__main__":
    while True:
        op = functions.menu()
        f = 0
    
        match op:
            case 1:
                archivosF.busqueda_archivo()
            case 2:
                if functions.verificarC():
                    functions.consultar_api()
                else:
                    print("No tienes conexion o la api de github tiene fallas, redirigiendo...")
                    archivosF.busqueda_archivo()
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