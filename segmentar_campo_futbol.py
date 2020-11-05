# -*- coding: utf-8 -*-
"""
@author: isaac
"""
import numpy as np
from skimage import color
from skimage import measure

"""
 Función que aplica 2 umbralizaciones por color en el espacio HSV y a continuación
 aplica una binarización.
 Entrada: lista de strings con los nombres de las imágenes RGB.
 Salida: lista con las imágenes umbralizadas en binario.
"""
def umbralizar_binarizar(lista_imagen):
    
    resultado = []
    
    # El umbral se realiza sobre el matiz en el espacio HSV.
    # Utilizamos los mismos umbrales para todas las imágenes y nos han dado
    # buenos resultados. Si los resultados no fueran buenos, se hubiera
    # implementado algún algoritmo para el cáclulo dinámico del umbral.
    
    # Umbral inferior del matiz
    umb_inf_matiz = 0.17
    # Umbral superior del matiz
    umbral_sup_matiz = 0.30
    
    for im_rgb in lista_imagen:
        
        # Convertimos la imagen RGB a HSV (matiz-saturación-valor)
        im_hsv = color.rgb2hsv(im_rgb)
        
        # Umbralizamos y binarizamos la imagen:
        # Los píxeles que respetan el umbral se ponen a True.
        # y los que no a False.
        im_umb_bin = np.bitwise_and(im_hsv[:,:,0] > umb_inf_matiz, im_hsv[:,:,0] < umbral_sup_matiz)
        
        # En im_umb_bin.astype(int) se cambia la imagen de Boolean a int.
        # True  -> 1 (blanco)
        # False -> 0 (negro).
        list.append(resultado, im_umb_bin.astype(int))
   
    return resultado


"""
 Función que devuelve la componentes conexa con más píxeles.
 Entrada: lista de imágenes binarias.
 Salida: lista de imágenes binarias con las componentes conexas más grandes.
"""     
def componente_conexa_mas_grande(lista_imagenes_binarias):
    
    resultado = []
    componente_mas_masa = None
    
    for i in lista_imagenes_binarias:
        
        # Obtenemos las componentes conexas de la imagen utilizando
        # vecindad 8.
        componentes_conexas = measure.label(i, 8)
        
        # Obtenemos el  array con las propeidades de las regiones.
        propiedades_componentes_conexas = measure.regionprops(componentes_conexas)
        
        # a) Metemos en un array las areas de las componentes
        # conexas.
        # b) Calculamos la más grande con la función numpy.amax.
        # c) Miramos a que componente corresponde esa área.
        # d) Finalmente guardamos la componente en la variable resultado.
        
        area_componentes = []
        
        # a)
        for componente in propiedades_componentes_conexas:
            area_componentes.append(componente.area)
          
        # b)
        max_masa = np.amax(area_componentes)
        
        # c)
        for componente in propiedades_componentes_conexas:
            if componente.area == max_masa:
                componente_mas_masa = componente
        # d)        
        list.append(resultado, (componentes_conexas == componente_mas_masa.label).astype(int))
        
    return resultado

"""
 Función auxiliar que calcula la imagen del punto "x" en la recta que pasa por 
 los puntos ("x1", "y1") y ("x2", "y2").
 Entrada: coordenadas del punto 1 ("x1", "y1"), del punto 2 ("x2", "y2") y 
 coordenada "x" de la imagen a calcular.
 Salida: imagen de "x".
 Postcondición: como estamos trabajando sobre matrices de píxeles, la imagen
 será un int.
"""
def imagen_en_la_recta(x1, y1, x2, y2, x):
    # Pendiente de la recta.
    m = (y2 - y1)/(x2 - x1) 
    
    # Devolvemos la parte entera de la imagen
    return int(m*x - m*x1 + y1)

"""
 Recorremos la imagen desde el principio hasta "limite_columnas" hasta
 encontrar el primer píxel blanco.
 Entrada: imagen binaria que representa en campo de fútbol y el número
 de columna que limita la búsqueda.
 Salida: coordenadas del primer píxel blanco de la zona izquierda de la
 imagen.
"""
def calcular_punto_izquierda(imagen_binaria, limite_columnas):
    
    # Número de filas de la imagen.
    numero_filas = imagen_binaria.shape[0]
    
    # Recorremos la imagen desde el principio hasta "limite_columnas" hasta
    # encontrar el primer píxel blanco.
    for j in np.arange(0, limite_columnas):
        for i in np.arange(0, numero_filas):
            if imagen_binaria[i, j] == 1:
                return (i, j)

"""
 Recorremos la zona central de la imagen hasta encontrar el primer píxel
 blanco.
 Entrada: imagen binaria que representa en campo de fútbol y el número
 de columna que limita el intervalo de búsqueda.
 Salida: coordenadas del primer píxel blanco de la zona central.
"""
def calcular_punto_centro(imagen_binaria, limite_columnas):
    
    for i in np.arange(0, imagen_binaria.shape[0]):
        for j in np.arange(limite_columnas, (imagen_binaria.shape[1]-limite_columnas)):
            if imagen_binaria[i][j] == 1:
                return (i, j)
"""
 Recorremos la imagen desde el final hasta "n - limite_columnas" hasta 
 encontrar el primer píxel blanco.
 Entrada: imagen binaria que representa en campo de fútbol y el número
 de columna que limita el intervalo de búsqueda.
 Salida: coordenadas del primer píxel blanco de la zona derecha de la imagen.
"""
def calcular_punto_derecha(imagen_binaria, limite_columnas):
    
    # 3) Recorremos la primera columna hasta obtener el primer píxel blanco.
    numero_filas = imagen_binaria.shape[0]
    numero_columnas = imagen_binaria.shape[1]
    
    aux = np.arange(numero_columnas - limite_columnas, numero_columnas)
    recorrer = np.flip(aux, 0)
    
    for j in recorrer:
        for i in np.arange(0, numero_filas):
            if imagen_binaria[i, j] == 1:
                return (i, j)


"""
 Obtenemos los puntos de la 2 rectas que pasan por los bordes del campo
 de fútbol.
 Entrada: imagen binaria que representa en campo de fútbol
 Salida: lista con los puntos de las rectas. ¿?
"""
def obtener_puntos_recta(imagen_binaria):
    
    """
     Buscamos los 3 primeros píxeles blancos de las zonas izquierda, central y
     derecha de la imagen.
     La zona de la izquierda es la primera veinteava parte de la imagen.
     La zona de la derecha es la última veinteava parte de la imagen.
     La zona central es el resto de veinteavas.
    """
    veinteava = int(imagen_binaria.shape[1]/20)   
    (y_izq, x_izq) = calcular_punto_izquierda(imagen_binaria, veinteava)
    (y_cen, x_cen) = calcular_punto_centro(imagen_binaria, veinteava)
    (y_der, x_der) = calcular_punto_derecha(imagen_binaria, veinteava)
    
    puntos_rectas = [(x_izq, y_izq)]
    
    # Calculamos los puntos de la recta que pasa por el punto de la izquierda 
    # y el central.
    for x in np.arange(x_izq+1, x_cen):
        y = imagen_en_la_recta(x_izq, y_izq, x_cen, y_cen, x)
        list.append(puntos_rectas, (x, y))
    
    # Calculamos los puntos de la recta que pasa por el punto central y el de 
    # la derecha
    for x in np.arange(x_cen, x_der):
        y = imagen_en_la_recta(x_cen, y_cen, x_der, y_der, x)
        list.append(puntos_rectas, (x, y))
    
    list.append(puntos_rectas, (x_der, y_der))
    return (puntos_rectas, min([y_izq, y_cen, y_der]))

"""
 Pone en negro los píxeles que están arriba de los puntos "puntos_recta".
""" 
def filtro(imagen_rgb_entrada, puntos_recta, fila_punto_mas_alto):    
    
    # np.copy nos permite copiar una matriz para no modificarla.
    imagen_rgb = np.copy(imagen_rgb_entrada)
    
    # Ponemos a negro los píxeles por encima del punto más alto
    submatriz_superior = np.zeros((fila_punto_mas_alto, imagen_rgb.shape[1], 3))
    
    # *************************************************************************
    # Recorremos la imagen por COLUMNAS
    # Pintamos la recta de violeta
    for j in np.arange(0, imagen_rgb.shape[1]):
        for i in np.arange(fila_punto_mas_alto,imagen_rgb.shape[0]):
            # Si es un píxel de la recta saltamos a la siguiente iteración.
            if ((j, i) in puntos_recta):
                break
            else:
                imagen_rgb[i][j][0] = 0
                imagen_rgb[i][j][1] = 0
                imagen_rgb[i][j][2] = 0  
                
            
    submatriz_inferior = imagen_rgb[np.ix_(np.arange(fila_punto_mas_alto,imagen_rgb.shape[0]), np.arange(0, imagen_rgb.shape[1]))]
    
    # concatenar 2 matrices. Una encima de otra.
    return np.concatenate((submatriz_superior.astype(np.uint8), submatriz_inferior), axis=0)

def filtrar_con_rectas(lista_imagen_rgb, lista_imagenes_binarias):
    
    resultado = []
    
    for i in np.arange(0, len(lista_imagenes_binarias)):
        imagen_rgb = lista_imagen_rgb[i]
        imagen_binaria = lista_imagenes_binarias[i]
        
        # Calculamos los puntos de las 2 rectas que pasan por los bordes del
        # campo de fútbol.
        puntos_recta, fila_punto_mas_alto = obtener_puntos_recta(imagen_binaria)
        list.append(resultado, filtro(imagen_rgb, puntos_recta, fila_punto_mas_alto))
        
    return resultado