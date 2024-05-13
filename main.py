import functions

if __name__ == "__main__":
    while True:
        op = functions.menu()
        f = 0
    
        match op:
            case 1:
                # Add your code for option 1 here
                pass
            case 2:
                functions.consultar_api()
            case 3:
                # Add an option for the user to exit the program
                print("salineod")
                break
            case _:
                print("adasd")
            
        if f != 0:
            print("\nSaliendo...")
            break