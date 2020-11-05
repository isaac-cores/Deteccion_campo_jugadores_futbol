# -*- coding: utf-8 -*-
"""
@author: isaac
"""
import segmentar_campo_futbol as SegmentarCampoFutbol
import detectar_elementos as DetectarElementos
from skimage  import io
import matplotlib.pyplot as plt
from PIL import Image

def mostrar_im_ventanas(lista_im):
    for im in lista_im:
        plt.imshow(im)
        plt.show()

def mostrar_im_ventanas_gray(lista_im):
    for im in lista_im:
        plt.imshow(im, cmap=plt.cm.gray)
        plt.show()
        
def leer_imagenes(nombre_imagenes):
    
    resultado = []
    for nombre in nombre_imagenes:
        im = io.imread("images/"+str(nombre)+".jpg")
        list.append(resultado, im)
        
    return resultado


nombre_imagenes = [2, 6, 10, 14, 16, 19, 23, 33, 81, 90, 99, 100, 102, 174, 178, 182, 187]

lista_imagenes = leer_imagenes(nombre_imagenes)

imagen_umbralizada_binarizada = SegmentarCampoFutbol.umbralizar_binarizar(lista_imagenes)

componente_conexa_mayor = SegmentarCampoFutbol.componente_conexa_mas_grande(imagen_umbralizada_binarizada)

imagen_filtrada_rectas = SegmentarCampoFutbol.filtrar_con_rectas(lista_imagenes, componente_conexa_mayor)

im_jugadores = DetectarElementos.detectar_jugadores(componente_conexa_mayor, imagen_filtrada_rectas)

mostrar_im_ventanas(im_jugadores)