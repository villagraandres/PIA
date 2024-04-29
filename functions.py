import requests
import requests.utils
from datetime import datetime

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
            #anadir al stack
        case 2:
            buscar_usuario()
            #anadir al stack
        case _:
            print("Opcion invalida")
            consultar_api()



def detalles_repo(owner,nombre):
     url = f"https://api.github.com/repos/{owner}/{nombre}/commits"
     response=requests.get(url)
     fechas_commits=[]
     if response.status_code==200:
         resultados=response.json()
         for n in resultados:
             #mediana de las ultimas 30 commits en fechas
             fecha = datetime.strptime(n['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
             fechas_commits.append(fecha)

         fechas_commits=fechas_commits[::-1]
         l=len(fechas_commits)
         if l%2!=0:
             mediana=fechas_commits[l//2]
         else:
             timestamp1 = fechas_commits[l // 2 - 1].timestamp()
             timestamp2 = fechas_commits[l // 2].timestamp()
             print(timestamp1)
             mediana = datetime.fromtimestamp((timestamp1 + timestamp2) / 2)
  
         print("mediana es",mediana)
         
   

def buscar_repo():
    nombre_repo=input("Introduzca el nombre del repositorio: ")

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


        detalles_repo(n['owner']['login'],n['name'])

        

    else:
        pass


def buscar_usuario():
    pass



if __name__=="__main__":
    #pruebas

    detalles_repo("villagraandres","petTrack1")