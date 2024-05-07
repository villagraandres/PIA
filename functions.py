import requests
import requests.utils
from Repositorio import Repositorio
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


def consultar_api():
    submmenu="""Seleecione de que quiere obtener los datos:
        1. Repositorio Publico
        2. Usuario
        3. Regresar"""
    print(submmenu)
    op=int(input("Opcion: "))
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
        resultados=response.json()['items'] #lista de diccionarios que contendra información de cada repositorio para las stats
        lista_datos = []
        print("Repositorios que coinciden con el nombre:")
        for i,n in enumerate(resultados):
            print(f"id: {i+1} Nombre: {n['name']} Autor: {n['owner']['login']} ")
            if len(n['topics'])!=0:
                print(f"Temas: {', '.join(n['topics'])}\n")
            else:
                print("El autor no proporciono temas\n")

        
        op=int(input("Seleccione el numero de repositorio del que quiero obtener las estadisticas: "))

        repositorio=Repositorio(n['owner']['login'],n['name'])
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

    


def buscar_usuario():
    pass



if __name__=="__main__":
    #pruebas

    #repo=Repositorio("villagraandres","petTrack1")
    #repo.detalles()
    pass