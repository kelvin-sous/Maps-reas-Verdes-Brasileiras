# 🚀 Cálculo de Rotas entre Áreas Verdes com Algoritmo A* e API Google Maps

Este projeto permite calcular rotas entre áreas verdes no estado de São Paulo utilizando duas abordagens: 
1. Algoritmo **A*** para caminhos curtos baseados em distância geodésica.  
2. API Google Maps para obter rotas detalhadas e calculadas de forma dinâmica.

O sistema também gera mapas visuais das rotas calculadas.

---

## 📝 Funcionalidades

- **Busca de Áreas Verdes**: Carrega dados de áreas verdes a partir de arquivos CSV.
- **Coordenadas Geográficas**: Obtém latitude e longitude usando a API Google Maps.
- **Cálculo de Rotas**:
  - Via **API Google Maps** (direções detalhadas e otimizadas).
  - Via **Algoritmo A*** (calculando distâncias geodésicas).
- **Comparação de Performance**: Mede o tempo de execução entre os dois métodos.
- **Visualização de Rotas**: Gera um mapa com as rotas marcadas.

---

## 📂 Estrutura do Projeto

```plaintext
.
├── main.py                # Código principal
├── mapa_rota.png          # Mapa gerado pelo programa (após execução)
├── README.md              # Este arquivo
```

## ⚙️ Pré-requisitos

Antes de executar o projeto, certifique-se de ter os seguintes itens instalados:

### 🛠️ Python

- **Python 3.8 ou superior**  

### 🛠️ Bibliotecas Necessárias

Instale as dependências com o seguinte comando:

```bash
pip install requests matplotlib basemap tkinter
```

## 🚀 Como Executar
Clone este repositório:

```bash
git clone https://github.com/seuusuario/seu-repositorio.git
cd seu-repositorio
```

Execute o script:

```bash
python main.py
```

Siga as instruções no terminal para:

Selecionar o arquivo CSV contendo os dados das áreas verdes.
Informar os nomes das áreas de início e destino.

## 🗂️ Exemplo de Entrada

O programa utiliza um arquivo CSV com as seguintes colunas relevantes:

| Nome da Área       | Estado       | Município    |
|--------------------|--------------|--------------|
| Parque Ibirapuera  | São Paulo    | São Paulo    |
| Parque das Águas   | São Paulo    | Sorocaba     |

**Nota**: Você pode ajustar as colunas no código para atender ao seu formato de arquivo CSV.

---

## 🌟 Resultados

- **Log de Rotas**: O terminal exibirá:
  - Distância calculada pelos dois métodos.
  - Tempo de processamento.
- **Mapa Gerado**: Um arquivo `mapa_rota.png` será criado na pasta do projeto.

---

## 📊 Comparação de Métodos

| Método         | Distância Calculada | Tempo de Execução |
|----------------|---------------------|-------------------|
| API Google Maps| 15.2 km            | 0.1234 s          |
| Algoritmo A*   | 15.8 km            | 0.0089 s          |

---

## 🔑 Chave da API Google Maps

Certifique-se de substituir a variável `GOOGLE_MAPS_API_KEY` no código com sua chave válida.

---

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal.
- **Tkinter**: Para a interface de seleção de arquivos.
- **Matplotlib + Basemap**: Para visualização do mapa.
- **Google Maps API**: Para busca de coordenadas e rotas.

---

## 📜 Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais informações.

---

## 🧑‍💻 Autor

**Kelvin Lima | Elson Gois | Paulo Roberto**  
[GitHub](https://github.com/kelvin-sous)
