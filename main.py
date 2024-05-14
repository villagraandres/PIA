import functions

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
                t="""Selecciona la opcion que desees:
                    1. Ver registros de busqueda
                    2. Ver directorio de excel
                    3. Regresar"""
                print(t)
                while True:       
                    try:
                        op2=int(input())
                        if op2==1:
                            functions.busqueda_archivo()
                        elif op==2:
                            pass
                        else:
                            print("Opcion invalida")
                            break
                    except ValueError:
                        print("Valor no valido")
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