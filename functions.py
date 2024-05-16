import requests
import requests.utils
from Repositorio import Repositorio
import os
import random
import pandas as pd
from matplotlib import colors
import matplotlib.pyplot as plt
from datetime import datetime


stack=[]


def menu():
    menu_string="""
    Bienvenido, seleccione la opcion deseada:
        1. Consultar datos almacenados
        2. Buscar datos con la API de github
        3.Salir
    """
    print(menu_string)
    op=input("Opcion: ")    
    return op


"""
#Dado un diccionario crea una gráfica de barras, supone valores númericos en los valores, y ordena los datos 
#En orden ascendente
"""
def crear_grafica_barras(dic,lable_y,title,color,tipo,path=None): 
    

    ord_dic={}
    for k,v in dic.items():
        if k is not  None:
            ord_dic[k]=v

    ord_dic = dict(sorted(ord_dic.items(), key=lambda item: item[1]))

    rgba_color = colors.to_rgba(color)
    n = len(ord_dic)
    if tipo=="lenguajes":       
        fig, ax = plt.subplots(figsize=(15,6))
    elif tipo=="estadisticas":
        fig, ax = plt.subplots(figsize=(20,4))

    bar_colors = [rgba_color[:3] + (i/n,)  for i in range(1,n+1)] #Usa el color dado y da un degradado para diferenciar
    ax.bar(ord_dic.keys(), ord_dic.values(), color=bar_colors)

    ax.set_ylabel(lable_y)
    ax.set_title(title)
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    
        
    #Crea una carpeta donde se almacenaran las imágenes
    if os.path.exists("graficas") and os.path.isdir("graficas"):
        pass
    else:
        os.makedirs("graficas")
        
    #Guarda la gráfica creada en png
    if tipo=="lenguajes":
        if not os.path.exists("graficas/lenguajes"):
            os.makedirs("graficas/lenguajes")
        
        file_name = f"graph{random.randint(1,2147483648)}.png"
        ruta=os.path.join("graficas/lenguajes",file_name)
        if not os.path.exists(ruta):
            fig.savefig(ruta)
    elif tipo=="estadisticas":
         f=datetime.now()
         tiempo = f.strftime("%d-%m-%Y_%I_%M%p")
         
         if not os.path.exists("graficas/estadisticas"):
            os.makedirs("graficas/estadisticas")
        
         file_name = f"grafica_tiempo_{tiempo}.png"
         ruta=os.path.join(path,file_name)
         if not os.path.exists(ruta):
            fig.savefig(ruta)       

        
    
    
        

    # plt.show()
    

def consultar_api():
    submmenu="""Seleecione de que quiere obtener los datos:
        1. Repositorio Publico
        2. Regresar"""
    print(submmenu)
    op=int(input("Opcion: "))
    try:
        match op:
            case 1:
                buscar_repo()
                return
            case 2:
                return
            case _:
                print("Opcion invalida")    
            
    except ValueError:
        print("Opción equivocada, ingrese números")
    
    stack.append(consultar_api)





def buscar_repo():
    #busqueda detallada
    submenu="""Metodo de busqueda:
    1. Ya conozco el nombre del reposiorio y usuario
    2. Quiero Buscar por coincidencias
    3. Regresar"""
    print(submenu)
    op=int(input("Opcion:"))
    stack.append(buscar_repo)

    match op:
        case 1:
            busqueda_especifica()
        case 2:
            busqueda_coincidencias()
        case 3:
            stack.pop()()
        case _:
            pass



def busqueda_coincidencias():
    print("Escriba back! para regresar")
    nombre_repo=input("Introduzca el nombre del repositorio: ")
    if nombre_repo=="back!":
        stack.pop()()
        return 
    stack.append(busqueda_coincidencias)

    url = f"https://api.github.com/search/repositories?q={nombre_repo}"
    response=requests.get(url)
    if response.status_code==200:
        resultados=response.json()['items']
        detalles_repos = []
        lenguajes = []
        print("Repositorios que coinciden con el nombre:")
        for i,n in enumerate(resultados):
            print(f"id: {i+1} Nombre: {n['name']} Autor: {n['owner']['login']} ")
            if len(n['topics'])!=0:
                print(f"Temas: {', '.join(n['topics'])}\n")
            else:
                print("El autor no proporciono temas\n")
                
            lenguajes.append( {"lang":n["language"]} )
            datos_int = ["id","name","created_at","updated_at","pushed_at","topics","watchers_count","open_issues","score","language"]
            repo = {dato:n[dato] for dato in datos_int}
            repo['owner']=n["owner"]["login"]     
            detalles_repos.append(repo)
            
            
        lenguajes = [repo["language"] for repo in detalles_repos]    

        lenguajes_count = {lang:lenguajes.count(lang) for lang in set(lenguajes)} 
  
        crear_grafica_barras(lenguajes_count,"Frecuencia",f"Frecuencia de lenguajes de programación de busqueda {nombre_repo}","blue","lenguajes")
        print("Se ha creado la grafica de lenguaje de la busqueda")

        while True:
            
            op2=input("Deseas guardar el registro de los repositorios en un archivo txt? Y/N:  ")
            if op2=="Y" or op2=="y":

                print("Creando archivo ...")

                if not os.path.exists("registros"):
                    os.makedirs("registros")
                if not os.path.exists("registros/historial"):
                    os.makedirs("registros/historial")
                
                fecha=datetime.now()
                nombre_archivo = fecha.strftime("%d-%m-%Y_%H-%M-%S")
                df = pd.DataFrame.from_dict(detalles_repos)
                df.to_json(f'registros/datos_repo_{nombre_archivo}.json', orient='records', lines=True)
               
                
                print("Archivo creado con exito")

                break
            elif op2=="N" or op2=="n":
                break
            else:
                print("Dato invalido")
                
        while True:
    
            op3=input("Deseas guardar el registro de los repositorios en un archivo excel? Y/N:  ")
            if op3=="Y" or op3=="y":

                print("Creando archivo ...")

                if not os.path.exists("excel"):
                    os.makedirs("excel")
                if not os.path.exists("excel/registros"):
                    os.makedirs("excel/registros")

                fecha=datetime.now()
                nombre_archivo = fecha.strftime("%d-%m-%Y_%H-%M-%S") + ".xlsx"
                ruta = os.path.join("excel/registros/", nombre_archivo)
                df = pd.DataFrame(detalles_repos)
                df.to_excel(ruta, index=False, sheet_name="Hoja1")
                
                
                print("Archivo creado con exito")

                break
            elif op3=="N" or op3=="n":
                break
            else:
                print("Dato invalido")


        
        

        while True:
            op = int(input("Seleccione el id del repositorio del que quiere obtener las estadisticas: "))
            
            if op<1 or op>len(resultados):
                print("Opcion invalida")
                continue
            break

        repo=resultados[op-1]
        repositorio = Repositorio(repo['name'],repo['owner']['login'])
        repositorio.detalles()


    
    else:
        pass


def busqueda_especifica(usuario,nombre):
    print("Introduzca back! para regresar")
    while nombre=="" or usuario=="":
        nombre=input("Introduzca el nombre del repositorio: ")
        if nombre=="back!":
            consultar_api()   
        usuario=input("Introduzca el nombre del usuario que posee el repositorio: ")
    url = f"https://api.github.com/repos/{usuario}/{nombre}"
    response=requests.get(url)
    if response.status_code!=200:
        print("El repo no se encontro")
    else:
        repo=Repositorio(nombre,usuario)
        repo.detalles()
        repo.excelEstadisticas()
        print("Se ha guardado el excel con estadisticas del repositorio")



def busqueda_archivo():

    f = 0
    print("Los registros guardados son:")
    archivos=os.listdir("registros")
    for i,n in enumerate(archivos):
        print(f"id: {i+1} Nombre: {n}")
    
    while True:
        if f == 1:
            break

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
                            busqueda_especifica(usuario,nombre)
                            break

                        else: 
                            print("opcion invalida")

                elif op4 == "n" or op4 == "N":
                    f = 1
                    break
                    

                else:
                    print("Opcion invalida")

            break

            #Siendo sincero, no me parece que sea correcto añadir mas opciones
            #ver si tiene internet

                
        else:
            print("Opcion invalida")
            continue

    



def excel_print():
    pass

def buscar_usuario():
    pass



if __name__=="__main__":
    #pruebas

    #repo=Repositorio("villagraandres","petTrack1")
    #repo.detalles()
    busqueda_especifica("","")
    pass