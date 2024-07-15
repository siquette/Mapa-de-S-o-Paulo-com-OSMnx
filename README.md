# README

# Mapa de São Paulo com OSMnx

Este repositório contém um script Python para a criação de um mapa estilizado da cidade de São Paulo utilizando OSMnx. O mapa exibe ruas com diferentes larguras e cores dependendo do comprimento das vias. Além disso, o script adiciona texto e borda ao mapa.

## Requisitos de Instalação

Para rodar este script, você precisará instalar os seguintes pacotes Python:

```bash
pip install osmnx
pip install networkx
pip install requests
pip install matplotlib
pip install Pillow
```

## Estrutura do Código

### Importando as Bibliotecas

O código começa importando os pacotes necessários para a criação e manipulação do mapa:

```python
import osmnx as ox
import networkx as nx
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines as Line2D
from PIL import Image, ImageOps, ImageColor, ImageFont, ImageDraw 
```

### Definindo a Cidade

A cidade de interesse é definida em uma lista e os dados são obtidos usando a biblioteca OSMnx:

```python
places = ["São Paulo, Brazil"]
G = ox.graph_from_place(places, network_type="all", simplify=True)
```

### Extraindo Dados das Arestas

Extraímos os dados das arestas do grafo para manipulação posterior:

```python
u = []
v = []
key = []
data = []
for uu, vv, kkey, ddata in G.edges(keys=True, data=True):
    u.append(uu)
    v.append(vv)
    key.append(kkey)
    data.append(ddata)
```

### Definindo Cores das Estradas

A cor das estradas é definida com base no comprimento das vias:

```python
roadColors = []
for item in data:
    if "length" in item.keys():
        if item["length"] <= 100:
            color = "#d40a47"
        elif item["length"] > 100 and item["length"] <= 200:
            color = "#e78119"
        elif item["length"] > 200 and item["length"] <= 400:
            color = "#30bab0"
        elif item["length"] > 400 and item["length"] <= 800:
            color = "#bbbbbb"
        else:
            color = "w"
    roadColors.append(color)
```

### Definindo Larguras das Estradas

A largura das estradas é definida com base no tipo de via:

```python
roadWidths = []
for item in data:
    if "footway" in item["highway"]:
        linewidth = 1
    else:
        linewidth = 2.5
    roadWidths.append(linewidth)
```

### Definindo Parâmetros do Mapa

Definimos os parâmetros de latitude, longitude e limites da caixa delimitadora (bounding box):

```python
latitude = -23.550520
longitude = -46.633308
north = latitude + 0.035
south = latitude - 0.035
east = longitude + 0.05
west = longitude - 0.05
```

### Criando o Mapa

Criamos o mapa usando OSMnx com as cores e larguras definidas anteriormente:

```python
fig, ax = ox.plot_graph(G, node_size=0, bbox=(north, south, east, west), 
                        figsize=(40, 40), dpi=300, bgcolor="#061529",
                        save=False, edge_color=roadColors,
                        edge_linewidth=roadWidths, edge_alpha=1)
```

### Adicionando Legenda

Adicionamos uma legenda ao mapa para indicar o significado das cores:

```python
markersize = 16
fontsize = 16
legend_elements = [
    Line2D([0], [0], marker='s', color="#061529", label='Length < 100 m',
           markerfacecolor="#d40a47", markersize=markersize),
    Line2D([0], [0], marker='s', color="#061529", label='Length between 100-200 m',
           markerfacecolor="#e78119", markersize=markersize),
    Line2D([0], [0], marker='s', color="#061529", label='Length between 200-400 m',
           markerfacecolor="#30bab0", markersize=markersize),
    Line2D([0], [0], marker='s', color="#061529", label='Length between 400-800 m',
           markerfacecolor="#bbbbbb", markersize=markersize),
    Line2D([0], [0], marker='s', color="#061529", label='Length > 800 m',
           markerfacecolor="w", markersize=markersize)
]
l = ax.legend(handles=legend_elements, bbox_to_anchor=(0.0, 0.0), frameon=True, ncol=1,
              facecolor='#061529', framealpha=0.9,
              loc='lower left', fontsize=fontsize, prop={'family':"Georgia", 'size':fontsize})
for text in l.get_texts():
    text.set_color("w")
```

### Salvando o Mapa

O mapa é salvo em um arquivo PNG:

```python
output_image_path = "Sao_Paulo.png"
fig.savefig(output_image_path, dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=True)
```

### Funções de Expansão e Borda

Funções para expandir a imagem e adicionar uma borda:

```python
def _color(color, mode):
    return ImageColor.getcolor(color, mode)

def expand(image, fill='#e0474c', bottom=50, left=None, right=None, top=None):
    if left is None:
        left = 0
    if right is None:
        right = 0
    if top is None:
        top = 0
    width = left + image.size[0] + right
    height = top + image.size[1] + bottom
    out = Image.new(image.mode, (width, height), _color(fill, image.mode))
    out.paste(image, (left, top))
    return out

def add_border(input_image, output_image, fill='#e0474c', bottom=50, left=None, right=None, top=None):
    if left is None:
        left = 0
    if right is None:
        right = 0
    if top is None:
        top = 0
    img = Image.open(input_image)
    bimg = expand(img, bottom=bottom, left=left, right=right, top=top, fill=fill)
    bimg.save(output_image)
```

### Adicionando Texto

Adicionamos texto à imagem do mapa:

```python
in_img = "Sao_Paulo.png"
add_border(in_img, output_image='Sao_Paulo.png', fill='#e0474c', bottom=800)
img = Image.open("Sao_Paulo.png")
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("PMINGLIU.ttf", 650)
draw.text((1650,8500), "SÃO PAULO, BRASIL", (255,255,255), font=font)
img.save('Sao_Paulo.png')
```

## Conclusão

Este script fornece um guia detalhado para a criação de um mapa estilizado da cidade de São Paulo utilizando OSMnx, com etapas para manipulação de cores, larguras, adição de legendas e personalização da imagem final.



Para quaisquer dúvidas ou sugestões, sinta-se à vontade para abrir uma issue ou enviar um pull request.

---

Espero que este guia ajude você a entender melhor o processo de criação e personalização de mapas usando OSMnx!
