import csv
import requests
from rapidfuzz import process
import tkinter as tk
from tkinter import filedialog
from math import radians, cos, sin, sqrt, atan2

GOOGLE_MAPS_API_KEY = "SUA_API_GOOGLE"

def abrir_arquivo():
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    return caminho_arquivo

def carregar_nomes_areas_verdes(caminho_arquivo, coluna_nome=3):
    nomes_areas = []
    with open(caminho_arquivo, newline='', encoding='latin-1') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            if len(row) > coluna_nome:
                nomes_areas.append(row[coluna_nome].strip())
    return nomes_areas

def buscar_nome_similar_para_api(nome_usuario, nomes_areas):
    melhor_correspondencia = process.extractOne(nome_usuario, nomes_areas)
    if melhor_correspondencia and melhor_correspondencia[1] > 70:
        return melhor_correspondencia[0]
    return None

def buscar_coordenadas_google(nome_area, nomes_areas):
    nome_corrigido = buscar_nome_similar_para_api(nome_area, nomes_areas)
    if nome_corrigido:
        if nome_corrigido != nome_area:
            print(f"Você quis dizer: \"{nome_corrigido}\"?")
    else:
        print(f"Nome fornecido '{nome_area}' não possui correspondências próximas.")
        return None, None

    endereco_busca = f"{nome_corrigido}, São Paulo, SP, Brazil"
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': endereco_busca,
        'key': GOOGLE_MAPS_API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['results']:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            print(f"Coordenadas não encontradas para: {endereco_busca}")
            return None, None
    else:
        print("Erro ao acessar a API do Google Maps.")
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
        'mode': 'driving'  # Pode ser 'driving', 'bicycling', ou 'transit'
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['routes']:
            legs = data['routes'][0]['legs'][0]
            distancia_api_km = legs['distance']['value'] / 1000  # Distância em quilômetros
            
            # Distância geodésica
            distancia_geo_km = calcular_distancia_geodesica(lat_inicio, lng_inicio, lat_destino, lng_destino)

            print(f"Distância (API do Google): {distancia_api_km:.2f} km")
            print(f"Distância (Geodésica): {distancia_geo_km:.2f} km")

            print("\nRota Encontrada:")
            for step in legs['steps']:
                instrucoes = step['html_instructions']
                print(f"- {instrucoes}")

            return distancia_api_km
        else:
            print("Nenhuma rota encontrada entre os pontos.")
            return None
    else:
        print("Erro ao acessar a API do Google Maps.")
        return None

def main():
    caminho_arquivo = abrir_arquivo()
    if not caminho_arquivo:
        print("Nenhum arquivo selecionado.")
        return

    nomes_areas = carregar_nomes_areas_verdes(caminho_arquivo)
    if not nomes_areas:
        print("Não foram encontradas áreas verdes válidas no arquivo.")
        return

    nome_inicio = input("Informe o nome da área verde de início: ")
    nome_destino = input("Informe o nome da área verde de destino: ")

    lat_inicio, lng_inicio = buscar_coordenadas_google(nome_inicio, nomes_areas)
    lat_destino, lng_destino = buscar_coordenadas_google(nome_destino, nomes_areas)

    if lat_inicio and lng_inicio:
        print(f"Coordenadas de início: Latitude {lat_inicio}, Longitude {lng_inicio}")
    else:
        print("Não foi possível encontrar coordenadas para a área de início.")

    if lat_destino and lng_destino:
        print(f"Coordenadas de destino: Latitude {lat_destino}, Longitude {lng_destino}")
    else:
        print("Não foi possível encontrar coordenadas para a área de destino.")

    if lat_inicio and lng_inicio and lat_destino and lng_destino:
        calcular_rota_google(lat_inicio, lng_inicio, lat_destino, lng_destino)

if __name__ == "__main__":
    main()
