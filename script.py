# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 17:26:08 2024

@author: rodri
"""

#%%
# To make maps
import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.lines import Line2D

# To add text and a border to the map
from PIL import Image, ImageOps, ImageColor, ImageFont, ImageDraw 

#%%
# Define city/cities
places = ["São Paulo, Brazil"]

# Get data for places
G = ox.graph_from_place(places, network_type="all", simplify=True)

#%%

u = []
v = []
key = []
data = []
for uu, vv, kkey, ddata in G.edges(keys=True, data=True):
    u.append(uu)
    v.append(vv)
    key.append(kkey)
    data.append(ddata) 
#%%

# List to store colors
roadColors = []

# The length is in meters
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
    
#%%
# List to store linewidths
roadWidths = []

for item in data:
    if "footway" in item["highway"]:
        linewidth = 1

    else:
        linewidth = 2.5
        
    roadWidths.append(linewidth)

#%%
# Center of map
latitude = -23.550520
longitude = -46.633308

# Bbox sides
north = latitude + 0.035
south = latitude - 0.035
east = longitude + 0.05
west = longitude - 0.05

# Make Map
fig, ax = ox.plot_graph(G, node_size=0, bbox=(north, south, east, west), 
                        figsize=(40, 40), dpi=300, bgcolor="#061529",
                        save=False, edge_color=roadColors,
                        edge_linewidth=roadWidths, edge_alpha=1)


# Text and marker size
markersize = 16
fontsize = 16

# Add legend
legend_elements = [Line2D([0], [0], marker='s', color="#061529", label='Length < 100 m',
                          markerfacecolor="#d40a47", markersize=markersize),
                  
                   Line2D([0], [0], marker='s', color="#061529", label='Length between 100-200 m',
                          markerfacecolor="#e78119", markersize=markersize),
                  
                   Line2D([0], [0], marker='s', color="#061529", label='Length between 200-400 m',
                          markerfacecolor="#30bab0", markersize=markersize),
                  
                   Line2D([0], [0], marker='s', color="#061529", label='Length between 400-800 m',
                          markerfacecolor="#bbbbbb", markersize=markersize),
                  
                   Line2D([0], [0], marker='s', color="#061529", label='Length > 800 m',
                          markerfacecolor="w", markersize=markersize)]    
                      
l = ax.legend(handles=legend_elements, bbox_to_anchor=(0.0, 0.0), frameon=True, ncol=1,
              facecolor='#061529', framealpha=0.9,
              loc='lower left', fontsize=fontsize, prop={'family':"Georgia", 'size':fontsize})  
  
# Legend font color
for text in l.get_texts():
    text.set_color("w")
    
# Save figure
output_image_path = "C:/Users/rodri/Documents/testes/mapa/Sao_Paulo.png"
fig.savefig(output_image_path, dpi=300, bbox_inches='tight', format="png", facecolor=fig.get_facecolor(), transparent=True)


#%% t

# Get color
def _color(color, mode):
    color = ImageColor.getcolor(color, mode)
    return color

# Expand image
def expand(image, fill='#e0474c', bottom=50, left=None, right=None, top=None):
    """
    Expands image
    
    Parameters
    ----------
    
    image: The image to expand.
    bottom, left, right, top: Border width, in pixels.
    param fill: Pixel fill value (a color value).  Default is 0 (black).
    
    return: An image.
    """
    
    
    if left == None:
        left = 0
    if right == None:
        right = 0
    if top == None:
        top = 0
        
    width = left + image.size[0] + right
    height = top + image.size[1] + bottom
    out = Image.new(image.mode, (width, height), _color(fill, image.mode))
    out.paste(image, (left, top))
    return out

# Add border
def add_border(input_image, output_image, fill='#e0474c', bottom=50, left=None, right=None, top=None):
    """ Adds border to image and saves it.
    Parameters
    ----------
    
        
    input_image: str,
        String object for the image you want to load. This is the name of the file you want to read.
    
    output_image: str,
        String object for the output image name. This is the name of the file you want to export.
    
    fill: str,
        Hex code for border color. Default is set to reddish. 
        
    bottom, left, right, top: int,
        Integer object specifying the border with in pixels.
    
    """
    
    
    if left == None:
        left = 0
    if right == None:
        right = 0
    if top == None:
        top = 0
        
    img = Image.open(input_image)
    bimg = expand(img, bottom=bottom, left=left, right=right, top=top, fill=fill)
    bimg.save(output_image)
    
#%%

# Input image 
in_img = "Sao_Paulo.png"

# Output Image
add_border(in_img, output_image='Sao_Paulo.png', fill = '#e0474c', bottom = 800)

#%%

# Open Image
img = Image.open("Sao_Paulo.png")
draw = ImageDraw.Draw(img)

# Get font from working directory. Visit https://www.wfonts.com/search?kwd=pmingliu to download fonts
font = ImageFont.truetype("PMINGLIU.ttf", 650)

# Add font: position, text, color, font
draw.text((1650,8500),"SÃO PAULO, BRASIL", (255,255,255), font=font)

# Save image
img.save('Sao_Paulo.png')
