import json
import os

def calcular_rankings():
    """
    Calcula los rankings diarios y mensuales a partir del archivo de resultados.
    """
    try:
        with open('data/match-results.json', 'r', encoding='utf-8') as f:
            resultados = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'data/match-results.json'.")
        return

    # Asegura que la carpeta 'rankings' exista
    if not os.path.exists('rankings'):
        os.makedirs('rankings')
    
    # Inicializar el ranking mensual
    ranking_mensual_total = {}

    for mes, fechas in resultados.items():
        ranking_mensual_parcial = {}
        
        for fecha, partidos in fechas.items():
            ranking_diario = {}

            # Calcular puntos y estadísticas para la fecha actual
            for partido in partidos:
                equipoA = partido['equipoA']
                equipoB = partido['equipoB']
                puntuacionA = partido['puntuacionA']
                puntuacionB = partido['puntuacionB']
                
                # Definir puntos por partido
                puntos_ganador = 3
                puntos_perdedor = 1

                if puntuacionA > puntuacionB:
                    ganador = equipoA
                    perdedor = equipoB
                    puntos_ganador = 3
                    puntos_perdedor = 1
                elif puntuacionB > puntuacionA:
                    ganador = equipoB
                    perdedor = equipoA
                    puntos_ganador = 3
                    puntos_perdedor = 1
                else:
                    # En caso de empate, todos ganan 2 puntos
                    ganador = equipoA + equipoB
                    perdedor = []
                    puntos_ganador = 2
                    puntos_perdedor = 2
                
                # Actualizar estadísticas para los jugadores del equipo ganador
                for jugador in ganador:
                    if jugador not in ranking_diario:
                        ranking_diario[jugador] = {'pts': 0, 'gg': 0, 'gp': 0}
                    if jugador not in ranking_mensual_parcial:
                        ranking_mensual_parcial[jugador] = {'pts': 0, 'gg': 0, 'gp': 0}
                    if jugador not in ranking_mensual_total:
                        ranking_mensual_total[jugador] = {'pts': 0, 'gg': 0, 'gp': 0}

                    ranking_diario[jugador]['pts'] += puntos_ganador
                    ranking_diario[jugador]['gg'] += puntuacionA if jugador in equipoA else puntuacionB
                    ranking_diario[jugador]['gp'] += puntuacionB if jugador in equipoA else puntuacionA
                    
                    ranking_mensual_parcial[jugador]['pts'] += puntos_ganador
                    ranking_mensual_parcial[jugador]['gg'] += puntuacionA if jugador in equipoA else puntuacionB
                    ranking_mensual_parcial[jugador]['gp'] += puntuacionB if jugador in equipoA else puntuacionA
                    
                    ranking_mensual_total[jugador]['pts'] += puntos_ganador
                    ranking_mensual_total[jugador]['gg'] += puntuacionA if jugador in equipoA else puntuacionB
                    ranking_mensual_total[jugador]['gp'] += puntuacionB if jugador in equipoA else puntuacionA

                # Actualizar estadísticas para los jugadores del equipo perdedor
                for jugador in perdedor:
                    if jugador not in ranking_diario:
                        ranking_diario[jugador] = {'pts': 0, 'gg': 0, 'gp': 0}
                    if jugador not in ranking_mensual_parcial:
                        ranking_mensual_parcial[jugador] = {'pts': 0, 'gg': 0, 'gp': 0}
                    if jugador not in ranking_mensual_total:
                        ranking_mensual_total[jugador] = {'pts': 0, 'gg': 0, 'gp': 0}
                        
                    ranking_diario[jugador]['pts'] += puntos_perdedor
                    ranking_diario[jugador]['gg'] += puntuacionA if jugador in equipoA else puntuacionB
                    ranking_diario[jugador]['gp'] += puntuacionB if jugador in equipoA else puntuacionA

                    ranking_mensual_parcial[jugador]['pts'] += puntos_perdedor
                    ranking_mensual_parcial[jugador]['gg'] += puntuacionA if jugador in equipoA else puntuacionB
                    ranking_mensual_parcial[jugador]['gp'] += puntuacionB if jugador in equipoA else puntuacionA

                    ranking_mensual_total[jugador]['pts'] += puntos_perdedor
                    ranking_mensual_total[jugador]['gg'] += puntuacionA if jugador in equipoA else puntuacionB
                    ranking_mensual_total[jugador]['gp'] += puntuacionB if jugador in equipoA else puntuacionA

            # Ordenar el ranking diario y guardarlo en un archivo JSON
            ranking_diario_ordenado = sorted(
                [{'name': k, **v} for k, v in ranking_diario.items()],
                key=lambda x: x['pts'],
                reverse=True
            )
            
            nombre_archivo_diario = f"rankings/{mes}_{fecha.replace(' ', '_')}_ranking.json"
            with open(nombre_archivo_diario, 'w', encoding='utf-8') as f:
                json.dump(ranking_diario_ordenado, f, indent=4, ensure_ascii=False)

    # Ordenar el ranking mensual y guardarlo en un archivo JSON
    ranking_mensual_total_ordenado = sorted(
        [{'name': k, **v} for k, v in ranking_mensual_total.items()],
        key=lambda x: x['pts'],
        reverse=True
    )

    with open('rankings/ranking_mensual.json', 'w', encoding='utf-8') as f:
        json.dump(ranking_mensual_total_ordenado, f, indent=4, ensure_ascii=False)

    print("Rankings calculados y guardados con éxito.")

if __name__ == "__main__":
    calcular_rankings()