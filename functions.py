import requests
import requests.utils


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
        2. Usuario"""
    print(submmenu)
    op=int(input("Opcion: "))
    match op:
        case 1:
            buscar_repo()
        case 2:
            buscar_usuario()
        case _:
            print("Opcion invalida")
            consultar_api()


def detalles_repo(owner,nombre):
     url = f"https://api.github.com/repos/{owner}/{repo}/commits"
     response=requests.get(url)
     if response.status_code==200:
         pass
   

def buscar_repo():
    nombre_repo=input("Introduzca el nombre del repositorio: ")

    url = f"https://api.github.com/search/repositories?q={nombre_repo}"
    response=requests.get(url)
    if response.status_code==200:
        resultados=response.json()['items']
        print("Repositorios que coinciden con el nombre:")
        for i,n in enumerate(resultados):
            print(f"id: {i+1} Nombre: {n['name']} Autor: {n['owner']['login']} ")
            if len(n['topics'])!=0:
                print(f"Temas: {', '.join(n['topics'])}\n")
            else:
                print("El autor no proporciono temas\n")

        
        op=int(input("Seleccione el numero de repositorio del que quiero obtener las estadisticas: "))

        detalles_repo(n['owner']['login'],n['name'])

    else:
        pass


def buscar_usuario():
    pass

