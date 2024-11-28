import csv
import requests
import tkinter as tk
from tkinter import filedialog
import os
from math import radians, cos, sin, sqrt, atan2
import heapq
import time
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

GOOGLE_MAPS_API_KEY = "SUA_API_GOOGLE"

def abrir_arquivo():
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return caminho_arquivo

def carregar_dados_areas_verdes(caminho_arquivo, colunas_interessantes=[3, 10, 11], estado='São Paulo'):
    dados_areas = []
    with open(caminho_arquivo, newline='', encoding='latin-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            if len(row) > max(colunas_interessantes):
                nome_area = row[colunas_interessantes[0]].strip()
                uf_registro = row[colunas_interessantes[1]].strip()
                municipio = row[colunas_interessantes[2]].strip()
                if uf_registro == estado:  # Filtrar apenas as áreas no estado de São Paulo
                    dados_areas.append((nome_area, uf_registro, municipio))
    return dados_areas

def buscar_coordenadas_google(nome_area, dados_areas):
    correspondencias = [
        (nome, uf, municipio) for nome, uf, municipio in dados_areas if nome_area.lower() in nome.lower()
    ]
    if not correspondencias:
        print(f"Nenhuma correspondência encontrada para '{nome_area}' no estado de São Paulo.")
        return None, None

    if len(correspondencias) > 1:
        print(f"Várias correspondências encontradas para '{nome_area}':")
        for i, (nome, _, municipio) in enumerate(correspondencias, start=1):
            print(f"{i}. {nome} - {municipio}")
        escolha = input("Selecione o número correspondente à área desejada: ")
        try:
            index = int(escolha) - 1
            nome_corrigido, uf, municipio = correspondencias[index]
        except (ValueError, IndexError):
            print("Escolha inválida.")
            return None, None
    else:
        nome_corrigido, uf, municipio = correspondencias[0]

    endereco_busca = f"{nome_corrigido}, {municipio}, {uf}, Brazil"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': endereco_busca,
        'region': 'br',
        'components': 'country:BR|administrative_area:São Paulo|locality:' + municipio,
        'key': GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            resultado = data['results'][0]
            location = resultado['geometry']['location']
            endereco_formatado = resultado['formatted_address']
            print(f"Coordenadas encontradas para '{nome_area}': {endereco_formatado}")
            print(f"Latitude: {location['lat']}, Longitude: {location['lng']}")  # Coordenadas no log
            return location['lat'], location['lng']
        else:
            print(f"Coordenadas não encontradas para: {endereco_busca}")
            return None, None
    else:
        print(f"Erro ao acessar a API do Google Maps (status code: {response.status_code}).")
        return None, None


def calcular_distancia_geodesica(lat1, lng1, lat2, lng2):
    R = 6371.0  # Raio médio da Terra em quilômetros
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def calcular_rota_google(lat_inicio, lng_inicio, lat_destino, lng_destino):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        'origin': f"{lat_inicio},{lng_inicio}",
        'destination': f"{lat_destino},{lng_destino}",
        'key': GOOGLE_MAPS_API_KEY,
        'mode': 'driving'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['routes']:
            legs = data['routes'][0]['legs'][0]
            distancia_api_km = legs['distance']['value'] / 1000
            caminho = []
            for step in legs['steps']:
                location = step['end_location']
                caminho.append((location['lat'], location['lng']))
            return distancia_api_km, caminho
        else:
            print("Nenhuma rota encontrada entre os pontos.")
            return None, []
    else:
        print("Erro ao acessar a API do Google Maps.")
        return None, []

def a_star(grafo, inicio, fim):
    fila_prioridade = []
    heapq.heappush(fila_prioridade, (0, inicio))
    custos = {inicio: 0}
    caminhos = {inicio: None}

    while fila_prioridade:
        custo_atual, atual = heapq.heappop(fila_prioridade)

        if atual == fim:
            caminho = []
            while atual:
                caminho.append(atual)
                atual = caminhos[atual]
            caminho.reverse()
            return custo_atual, caminho

        for vizinho, distancia in grafo.get(atual, []):
            novo_custo = custos[atual] + distancia
            if vizinho not in custos or novo_custo < custos[vizinho]:
                custos[vizinho] = novo_custo
                heapq.heappush(fila_prioridade, (novo_custo, vizinho))
                caminhos[vizinho] = atual

    return float('inf'), []

def desenhar_mapa(lat_inicio, lng_inicio, lat_destino, lng_destino):
    # Configuração do mapa com foco no estado de São Paulo
    mapa = Basemap(
        projection='merc',
        llcrnrlat=-25.4,  # Latitude mínima
        urcrnrlat=-19.5,  # Latitude máxima
        llcrnrlon=-53.2,  # Longitude mínima
        urcrnrlon=-44.0,  # Longitude máxima
        resolution='i'
    )
    mapa.drawcountries()
    mapa.drawstates()
    mapa.drawcoastlines()

    # Converter coordenadas geográficas para projeção
    x_inicio, y_inicio = mapa(lng_inicio, lat_inicio)
    x_destino, y_destino = mapa(lng_destino, lat_destino)

    # Marcando os pontos e a linha da rota
    mapa.plot([x_inicio, x_destino], [y_inicio, y_destino], marker='D', markersize=5, linewidth=2, color='blue')

    # Adicionando os pontos de início e destino
    plt.text(x_inicio, y_inicio, 'Início', color='blue', fontsize=12, ha='right')
    plt.text(x_destino, y_destino, 'Destino', color='blue', fontsize=12, ha='right')

    return mapa

def salvar_imagem(mapa):
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_arquivo = os.path.join(diretorio_atual, "mapa_rota.png")

    plt.savefig(caminho_arquivo)

def main():
    caminho_arquivo = abrir_arquivo()
    if not caminho_arquivo:
        print("Nenhum arquivo selecionado.")
        return

    dados_areas = carregar_dados_areas_verdes(caminho_arquivo)
    if not dados_areas:
        print("Não foram encontradas áreas verdes válidas no arquivo.")
        return

    nome_inicio = input("Informe o nome da área verde de início: ")
    nome_destino = input("Informe o nome da área verde de destino: ")

    lat_inicio, lng_inicio = buscar_coordenadas_google(nome_inicio, dados_areas)
    if not (lat_inicio and lng_inicio):
        print("Não foi possível encontrar coordenadas para a área de início.")
        return

    lat_destino, lng_destino = buscar_coordenadas_google(nome_destino, dados_areas)
    if not (lat_destino and lng_destino):
        print("Não foi possível encontrar coordenadas para a área de destino.")
        return

    # Cronômetro para cálculo da rota usando API do Google Maps
    inicio_tempo_google = time.perf_counter()
    distancia_api_km, caminho_google = calcular_rota_google(lat_inicio, lng_inicio, lat_destino, lng_destino)
    fim_tempo_google = time.perf_counter()
    tempo_google = fim_tempo_google - inicio_tempo_google

    if distancia_api_km is not None:
        print(f"Distância calculada pela API do Google: {distancia_api_km:.2f} km")
        print(f"Tempo para cálculo da rota (Google): {tempo_google:.6f} segundos")
    else:
        print("Não foi possível calcular a rota entre os pontos usando a API do Google.")
        return

    # Cronômetro para cálculo da rota usando A*
    inicio_tempo_a_star = time.perf_counter()
    grafo = {  # Grafo simplificado para A*
        (lat_inicio, lng_inicio): [((lat_destino, lng_destino), calcular_distancia_geodesica(lat_inicio, lng_inicio, lat_destino, lng_destino))],
        (lat_destino, lng_destino): []
    }
    custo_a_star, caminho_a_star = a_star(grafo, (lat_inicio, lng_inicio), (lat_destino, lng_destino))
    fim_tempo_a_star = time.perf_counter()
    tempo_a_star = fim_tempo_a_star - inicio_tempo_a_star

    if custo_a_star != float('inf'):
        print(f"Distância calculada pelo A*: {custo_a_star:.2f} km")
        print(f"Tempo para cálculo da rota (A*): {tempo_a_star:.6f} segundos")
    else:
        print("Não foi possível calcular a rota entre os pontos usando o A*.")

    # Cronômetro para geração do mapa
    inicio_tempo_mapa = time.perf_counter()
    mapa = desenhar_mapa(lat_inicio, lng_inicio, lat_destino, lng_destino)
    fim_tempo_mapa = time.perf_counter()
    tempo_mapa = fim_tempo_mapa - inicio_tempo_mapa

    print(f"Tempo para geração do mapa: {tempo_mapa:.6f} segundos")

    salvar_imagem(mapa)

if __name__ == "__main__":
    main()
