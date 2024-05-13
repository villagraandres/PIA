from datetime import datetime,timedelta
import requests
import functions

class Repositorio:
    
    def __init__(self,nombre,owner) -> None:
        self.nombre=nombre
        self.owner=owner
        self.mediana=""
        self.promedio=""
        self.info={}
        

    def __str__(self) -> str:
        return f"{self.owner} {self.nombre}"

    def detalles(self):
        #promedio de issues cerradas/abiertas en 30 dias o issues en un maximo
        self._calcularMedianayPromedio()
        print(f"La mediana de las ultimas 30 commits en fechas: {self.mediana}")
        print(f"El promedio de tiempo entre cada commit es: {self.promedio}")
    
    
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
            indexes  = [str(timedelta(t)) for t in hiatus_t_asc]
            t_entre_comm = dict(zip(indexes,hiatus_t_asc))
            functions.crear_grafica_barras(t_entre_comm,"","Mayor tiempo entre commits","green")
            print("Se creo exitosamente la gráfica de tiempos")
            
            
            
            
            

        else:
            pass

   