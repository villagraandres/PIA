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
        1. Consultar datos
        2. Buscar datos con la API de github
    """
    print(menu_string)
    op=int(input("Opcion: "))      
    return op


"""
#Dado un diccionario crea una gráfica de barras, supone valores númericos en los valores, y ordena los datos 
#En orden ascendente
"""
def crear_grafica_barras(dic,lable_y,title,color,tipo): 
    

    ord_dic={}
    for k,v in dic.items():
        if k is not  None:
            ord_dic[k]=v

    ord_dic = dict(sorted(ord_dic.items(), key=lambda item: item[1]))

    rgba_color = colors.to_rgba(color)
    n = len(ord_dic)
    fig, ax = plt.subplots(figsize=(15,6))
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
         
         if not os.path.exists("graficas/estadisticas"):
            os.makedirs("graficas/estadisticas")
        
         file_name = f"graph{random.randint(1,2147483648)}.png"
         ruta=os.path.join("graficas/estadisticas",file_name)
         if not os.path.exists(ruta):
            fig.savefig(ruta)       

        
    
    
        

    # plt.show()
    

def consultar_api():
    submmenu="""Seleecione de que quiere obtener los datos:
        1. Repositorio Publico
        2. Usuario
        3. Regresar"""
    print(submmenu)
    op=int(input("Opcion: "))
    try:
        match op:
            case 1:
                buscar_repo()
                return
            case 2:
                buscar_usuario()
                return
            case 3:
                return
            case _:
                print("Opcion invalida")    
            
    except:
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
        
        #Obtenemos la moda de los lenguajes usados en los repositorios
        lenguajes_count = {lang:lenguajes.count(lang) for lang in set(lenguajes)} 
        # moda = max(lenguajes_count.values())
        # lenguajes_moda = [lang for lang,count in lenguajes_count if count == moda] 
        # print("Los lenguajes más usados fueron: " + ", ".join(lenguajes_moda) + f"\nCon una moda de {moda}")
        crear_grafica_barras(lenguajes_count,"Frecuencia","Frecuencia de lenguajes de programación","blue","lenguajes")
        print("Se ha creado la grafica de lenguaje de la busqueda")

        while True:
            
            op2=input("Deseas guardar el registro de los repositorios en un archivo txt? Y/N:  ")
            if op2=="Y" or op2=="y":

                print("Creando archivo ...")

                if not os.path.exists("registros"):
                    os.makedirs("registros")
                
                fecha=datetime.now()
                nombre_archivo = fecha.strftime("%d-%m-%Y_%H-%M-%S")
                with open(f"registros/datos_repo_{nombre_archivo}","w") as f:
                    for n in detalles_repos:
                        f.write(f"id: {n['id']} , nombre: {n['name']}, visitas: {n['watchers_count']} ")
                        f.write("\n")
                
                print("Archivo creado con exito")

                break
            elif op2=="N" or op2=="n":
                break
            else:
                print("Dato invalido")

        
        

        while True:
            op = int(input("Seleccione el numero de repositorio del que quiero obtener las estadisticas: "))
            
            if op<1 or op>len(resultados):
                print("Opcion invalida")
                continue
            break

        repo=resultados[op-1]
        repositorio = Repositorio(repo['name'],repo['owner']['login'])
        print(repositorio)
        repositorio.detalles()


    
    else:
        pass


def busqueda_especifica():
    nombre,usuario="",""
    print("Introduzca back! para regresar")
    while nombre=="" or usuario=="":
        nombre=input("Introduzca el nombre del repositorio: ")
        if nombre=="back!":
            stack.pop()()     
        usuario=input("Introduzca el nombre del usuario que posee el repositorio: ")
    stack.append(busqueda_especifica)
    url = f"https://api.github.com/repos/{usuario}/{nombre}"
    response=requests.get(url)
    if response.status_code!=200:
        print("El repo no se encontro")
    else:
        print("ok!")

    
def excel_print():
    pass

def buscar_usuario():
    pass



if __name__=="__main__":
    #pruebas

    #repo=Repositorio("villagraandres","petTrack1")
    #repo.detalles()
    busqueda_coincidencias()
    pass