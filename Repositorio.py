from datetime import datetime,timedelta
import requests
import os
import pandas as pd
import matplotlib.pyplot as plt

class Repositorio:
    
    def __init__(self,nombre,owner) -> None:
        self.nombre=nombre
        self.owner=owner
        self.mediana=""
        self.promedio=""
        self.moda=""
        self.info={}
        self.ruta=""
        

    def __str__(self) -> str:
        return f"{self.owner} {self.nombre}"

    def detalles(self):
        self._calcularMedianayPromedio()
        self._calcularModa()
        self._generartxt()
        self._excelEstadisticas()
        print("********* Se han generado las graficas, un excel con estadisticas y un archivo txt ********* \n")
        print(" ")
        print(f"La moda en el lenguaje mas usado es: {self.moda} ")
        print(" ")
        print(f"La mediana de las ultimas 30 commits en fechas: {self.mediana} ")
        print(" ")
        print(f"El promedio de tiempo entre cada commit es: {self.promedio} ")   
        print(" ")

        
        
        #promedio de issues cerradas/abiertas en 30 dias o issues en un maximo

    
    
    def _calcularMedianayPromedio(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.nombre}/commits"
        response=requests.get(url)
        fechas_commits=[]
        if response.status_code==200:
            print("Se esta calculando la mediana y el promedio de los commits...")
            resultados=response.json()
            for i,n in enumerate(resultados):
                
                fecha = datetime.strptime(n['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
                fechas_commits.append(fecha)
                if i>29:
                    break
            
            #mediana de las ultimas 30 commits en fechas
            fechas_commits=fechas_commits[::-1]
            l=len(fechas_commits)
            if l%2!=0:
                self.mediana=fechas_commits[l//2]
                
            else:
                timestamp1 = fechas_commits[l // 2 - 1].timestamp()
                timestamp2 = fechas_commits[l // 2].timestamp()
                self.mediana = datetime.fromtimestamp((timestamp1 + timestamp2) / 2)
                
            #Promedio de tiempo en las últimas 30 commits formateado
            diff_tiempo = [abs(fechas_commits[i + 1] - fechas_commits[i]).total_seconds() for i in range(len(fechas_commits) - 1)]
            t_prom = sum(diff_tiempo)/len(diff_tiempo)
            self.promedio = str(timedelta(seconds=t_prom))
            hiatus_t_asc = sorted(diff_tiempo)[20:]
            indexes  = [str(timedelta(seconds=t)) for t in hiatus_t_asc]
            t_entre_comm = dict(zip(indexes,hiatus_t_asc))
            import functions
            f=datetime.now()
            tiempo = f.strftime("%d-%m-%Y_%I_%M%p")
            if not os.path.exists(f"graficas/estadisticas/{self.nombre}_{tiempo}"):
                os.makedirs(f"graficas/estadisticas/{self.nombre}_{tiempo}")

            self.ruta=f"graficas/estadisticas/{self.nombre}_{tiempo}"
            


            functions.crear_grafica_barras(t_entre_comm,"",f"Mayor tiempo entre commits en: {self.nombre}","green","estadisticas",self.ruta)
            print("Se creo exitosamente la gráfica de tiempos")

        else:
            pass
    def _excelEstadisticas(self):
        #excel con nombre, autor estrellas visitas issues commits fecha de creado rama principal contribuidores
        url = f"https://api.github.com/repos/{self.owner}/{self.nombre}"
        response=requests.get(url)
        if response.status_code==200:
            resultado=response.json()
            h={}
            h["id"]=resultado["id"]
            h["Nombre"]=resultado["name"]
            h["Autor"]=resultado["owner"]["login"]
            h["Mediana commits"]=self.mediana
            h["Promedio commits"]=self.promedio
            h["Rama default"]=resultado["default_branch"]
            h["Tamaño (Kb)"]=resultado["size"]
            h["Estrellas"]=resultado["stargazers_count"]
            h["Visitas"]=resultado["watchers_count"]
            h["Lenguaje principal"]=resultado["language"]
            h["Forks"]=resultado["forks_count"]

            url2=url+"/contributors"
            response2=requests.get(url2)
            if response2.status_code==200:
                resultado2=response2.json()
                cont=[]
                for n in resultado2:
                    cont.append(n["login"])
            else:
                cont="Los colaboradores son mas de 500"
            h["contribuidores"]=cont

            if not os.path.exists("excel"):
                os.makedirs("excel")
            if not os.path.exists("excel/repo"):
                os.makedirs("excel/repo")
            fecha=datetime.now()
            nombre_archivo = fecha.strftime("%d-%m-%Y_%H-%M-%S") + ".xlsx"
            ruta=os.path.join("excel/repo/",nombre_archivo)

            df=pd.DataFrame([h])
            df.to_excel(ruta,index=False)          


        else:
            pass


    
    def _calcularModa(self):
        url = f"https://api.github.com/repos/{self.owner}/{self.nombre}/languages"
        respuesta=requests.get(url)

        if respuesta.status_code==200:
            lenguajes=respuesta.json()
            total=sum(lenguajes.values())
            porcentajes={lang:(c/total)*100 for lang,c in lenguajes.items()}
            max_key = max(porcentajes.items(), key=lambda x: x[1])[0]
            self.moda=max_key


            if not os.path.exists("graficas"):
                os.makedirs("graficas")
            if not os.path.exists("graficas/estadisticas"):
                os.makedirs("graficas/estadisticas")

            #crear grafica de pastel  
            f=datetime.now()
            tiempo=f.strftime("%d-%m-%Y_%H")  
            nombre=f"graficaP_{self.nombre}_{tiempo}"
            plt.figure(figsize=(15,10))
            wedges, texts = plt.pie(porcentajes.values())
            plt.title("Porcentajes del lenguajes de programacion")
            plt.legend(wedges, porcentajes.keys(),
                title="Lenguajes",
                loc="center left",
                bbox_to_anchor=(1, 0, 0.5, 1))
            plt.savefig(f"{self.ruta}/{nombre}")
            plt.close()
            
        else:
            pass

    def _generartxt(self):
        
        
        if not os.path.exists("registros"):
            os.makedirs("registros")
        
        if not os.path.exists("registros/estadisticas_re"):
            os.makedirs("registros/estadisticas_re")

        f=datetime.now()
        nombre=f"{self.nombre}_"
        print(nombre)

        with open(f"registros/estadisticas_re/{nombre}{datetime.now().strftime("%d-%m-%Y_%I_%M%p")}.txt", "w") as f:
            f.write(f"Nombre: {self.nombre},")
            f.write("\n")
            f.write(f"Mediana de fecha de commits: {self.mediana}")
            f.write("\n")
            f.write(f"Promedio entre commits:{self.promedio}")
            f.write("\n")
            f.write(f"Moda de lenguajes de programacion: {self.moda}")

        
   