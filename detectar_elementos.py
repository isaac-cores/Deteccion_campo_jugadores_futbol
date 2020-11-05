# -*- coding: utf-8 -*-
"""
@author: isaac
"""
import numpy as np
from skimage import measure
import cv2


# =============================================================================
# ------------------------------ Jugadores ------------------------------------
# =============================================================================
"""
Función principal para detectar jugadores
Detecta los jugadores del campo y dibuja un rectangulo sobre ellos.
"""
def detectar_jugadores(lista_imagenes_binarias, lista_imagen_rgb):
        
    resultado = []
    
    for i in np.arange(0, len(lista_imagenes_binarias)):
        im_rgb = lista_imagen_rgb[i]
        im_rgb_copy = np.copy(im_rgb)
        imagen_binaria = lista_imagenes_binarias[i]
        # Invertimos los colores de la imagen. Blanco <-> negro
        imagen_binaria_inversa = np.invert(imagen_binaria)
    
        # Obtenemos las componentes conexas de la imagen utilizando
        # vecindad 8.
        componentes_conexas = measure.label(imagen_binaria_inversa, 8)
        # Obtenemos el  array con las propiedades de las regiones.
        propiedades_componentes_conexas = measure.regionprops(componentes_conexas)
        
        propiedades_componentes_conexas_sin_grandes_componentes = filtrar_jugadores(propiedades_componentes_conexas)
        for componente in propiedades_componentes_conexas_sin_grandes_componentes:
            (min_fil, min_col, max_fil, max_col) = componente.bbox
            x = min_fil
            y = min_col
            x2 = max_fil
            y2 = max_col
            cv2.rectangle(im_rgb_copy, (y, x), (y2, x2), (0, 0, 255), 3)
            
        list.append(resultado, im_rgb_copy)
            
    return resultado

"""
Calcula la proporción anchura/altura del bbox
"""
def proporcion_anchura_altura(min_fil, min_col, max_fil, max_col):
    return (max_col-min_col+1)/(max_fil-min_fil+1)
"""
Descarta las componentes que no son jugadores.
"""
def filtrar_jugadores(propiedades_componentes_conexas):
    limite_superior = 3942
    limite_inferior = 400

    # anchura = (max_col-min_col+1)
    # altura = (max_fil-min_fil+1)
    propiedades_componentes_conexas_salida = []
    
    for componente in propiedades_componentes_conexas:
        if (componente.area <= limite_superior) & (componente.area >= limite_inferior) & ((proporcion_anchura_altura(*componente.bbox) <= 1)) & ((proporcion_anchura_altura(*componente.bbox) >= 0.3)):
            propiedades_componentes_conexas_salida.append(componente)
            
    return propiedades_componentes_conexas_salida
