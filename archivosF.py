import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
import functions
from PIL import Image

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
        estadisticas()
        plt.show()

    


def historial():

    print("Los registros guardados son:")
    if not os.path.exists("registros/historial"):
        os.makedirs("registros/historial")
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
                df = pd.read_json(f'registros/{archivos[op-1]}', orient='records', lines=True)
                df['created_at'] = df['created_at'].astype("str")
                df['pushed_at'] = df['pushed_at'].astype("str")
                df['updated_at'] = df['created_at'].astype("str")
                data = list(df.to_dict(orient='index').items())
                data_list = [data[i][1] for i in range(len(data))]

                for i,n in enumerate(data_list):
                
                    str = f'"name":{n["name"]}' + f'"owner":{n["owner"]}' + f'"topics":{n["topics"]}'
                    print(f"Repositorio #{i+1}--- " + str + "\n")


                while True: 
                    op4 = input("Quieres consultar alguno de los repositorios? Y/N: ")
                    if op4 == "y" or op4 == "Y":
                        try:
                            op5 = int(input("Cual repositorio? (numero de repositorio): "))

                        except:
                            print("Dato invalido, no entero")


                        while True: 
                            if op5<len(data_list) and op5>=0:
                                usuario = data_list[op5-1]["owner"]
                                nombre = data_list[op5-1]["name"]
                                functions.busqueda_especifica(usuario,nombre,1)
                                break

                            else: 
                                print("opcion invalida")

                    elif op4 == "n" or op4 == "N":
                        break


                    else:
                        print("Opcion invalida")

                break


            else:
                print("Opcion invalida")
                continue
    else:
        print("No hay registros guardados")


def estadisticas():
    if not os.path.exists("registros/estadisticas_re"):
        os.makedirs("registros/estadisticas_re")
    archivos=os.listdir("registros/estadisticas_re")

    print("Los repositorios consultados son:")
    if len(archivos)>0:
        for i,n in enumerate(archivos):
            print(f"Id:{i+1} {n}")
        
        

        while True:
            try:
                op=int(input("Selecciona el id del archivo que desees consultar: "))
                if op-1<len(archivos) and op>0:
                    break
                
            except ValueError:
                print("Dato invalido")
        
        with open(f"registros/estadisticas_re/{archivos[op-1]}") as f:
            contenido=f.read()
            print(contenido)
        n=archivos[op-1]
        n=n[:len(n)-4]

        print("Se mostraran las graficas generadas del repositorio")


        r=f"graficas/estadisticas/{n}"
        for grafica in os.listdir(r):
            a=os.path.join(r,grafica)
            img=Image.open(a)
            img.show()        
        return
    
    else:
        print("No hay archivos")
        return
  

if __name__ =="__main__":
    busqueda_archivo()