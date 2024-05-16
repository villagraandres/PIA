import os

def busqueda_archivo():
    while True:
        t="""Escriba la opcion que desee
            1. Consultar historial de busqueda
            2. Consultar estadisticas y graficas de repositorios"""
        print(t)
        

        try:
            op=int(input("Opcion: "))
            if op in [1,2]:
                break
        except ValueError:
            print("Dato invalido")
            continue
        
    if op==1:
        historial()
    if op==2:
        pass

    


def historial():

    print("Los registros guardados son:")
    archivos=os.listdir("registros/historial")
    if len(archivos)>1:

        for i,n in enumerate(archivos):
            print(f"id: {i+1} Nombre: {n}")
        
        while True:
            try:
                op=int(input("Selecciona el id del archivo que quieres consultar: "))
            except ValueError:
                print("Dato invalido")
                continue


            if op-1<len(archivos) and op-1>=0:
                with open(f"registros/historial/{archivos[op-1]}") as archivo:
                    contenido=archivo.read()
                    print(contenido)

                   

                    #ver si tiene internet

                    
            else:
                print("Opcion invalida")
                continue
    else:
        print("No hay registros guardados")

