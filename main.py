import functions
import archivosF

if __name__ == "__main__":
    while True:
        
        op = functions.menu()
        try:
           op= int(op)
        except ValueError:
            print("Opcion invalida")
            continue
        f = 0
        print(op)
        match op:
            
            case 1:
                archivosF.busqueda_archivo()
                break     
                
            case 2:
                functions.consultar_api()
            case 3:
                print("salineod")
                break
            case _:
                print("adasd")
            
        if f != 0:
            print("\nSaliendo...")
            break