from datetime import datetime
import requests
class Repositorio:
    
    def __init__(self,nombre,owner) -> None:
        self.nombre=nombre
        self.owner=owner
        self.mediana=""
        self.info={}
        


    def detalles(self):
     #promedio de issued cerrdas/abiertas en 30 dias o issues en un maximo
     self._calcularMediana()
     print(self.mediana)
    
    
    def _calcularMediana(self):
        url = f"https://api.github.com/repos/{self.nombre}/{self.owner}/commits"
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
                self.mediana=fechas_commits[l//2]
                
            else:
                timestamp1 = fechas_commits[l // 2 - 1].timestamp()
                timestamp2 = fechas_commits[l // 2].timestamp()
                self.mediana = datetime.fromtimestamp((timestamp1 + timestamp2) / 2)

        else:
            pass

   