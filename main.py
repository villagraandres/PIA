import functions

if __name__ == "__main__":
    while True:
        op = functions.menu()
        f = 0
    
        match op:
            case 1:
                functions.consultar_datos()
                pass
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