# busqueda
# import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from nltk.corpus import stopwords

import nltk
# from pandas import read_csv

from django.db.models import Q

from proyecto.models import RegistroPerfil, ProyectoDeGrado
from .models import *

def contenido(db_proyectos):
    contenido = [[m, f"{m.titulo} {m.resumen} {m.indice} {m.bibliografia}"] for m in db_proyectos]
    # print(contenido)
    return contenido


# Prueba, no implementa al sistema
def search(buscado):
    tesis_df = pd.read_csv("~/csv_json_files/proyectos_carrera_etn/proy_titulo_autor.csv")
    lista_nombres = [item for item in tesis_df['NOMBRE']]
    lista_titulos = [item for item in tesis_df['TITULO']]
    # agregando a las listas nombres y titulos de la base de datos
    lista_titulos_sistema = [m.titulo for m in ProyectosInscritos.objects.all()]
    lista_nombres_sistema = [m.autor for m in ProyectosInscritos.objects.all()]
    lista_titulos = lista_titulos + lista_titulos_sistema
    lista_nombres = lista_nombres + lista_nombres_sistema
    stop_words = set(stopwords.words('spanish')) 
    # agregando a las listas nombres y titulos de la base de datos perfiles
    lista_titulos_sistema = [m.titulo for m in RegistroPerfil.objects.all()]
    lista_nombres_sistema = [m.equipo for m in RegistroPerfil.objects.all()]
    lista_titulos = lista_titulos + lista_titulos_sistema
    lista_nombres = lista_nombres + lista_nombres_sistema
    stop_words = set(stopwords.words('spanish')) 
    # agregando a las listas nombres y titulos de la base de datos perfiles
    lista_titulos_sistema = [m.titulo for m in ProyectoDeGrado.objects.all()]
    lista_nombres_sistema = [m.equipo for m in ProyectoDeGrado.objects.all()]
    lista_titulos = lista_titulos + lista_titulos_sistema
    lista_nombres = lista_nombres + lista_nombres_sistema
    stop_words = set(stopwords.words('spanish')) 
    # search_terms = 'servicio de voz'
    search_terms = buscado
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    vectors = vectorizer.fit_transform([search_terms] + lista_titulos)
    cosine_similarities = linear_kernel(vectors[0:1], vectors).flatten()
    titulo_scores = [round(item.item()*100,1) for item in cosine_similarities[1:]]  # convert back to native Python dtypes
    score_titles = list(zip(titulo_scores, lista_titulos, lista_nombres))
    ordenado_score = sorted(score_titles, reverse=True, key=lambda x:
            x[0])[:20] 
    dicc_score = {}
    for score_titulo in ordenado_score:
        dicc_score[score_titulo[0]] = score_titulo[1]
    return dicc_score

# Prueba, no implementa al sistema
def searchShowAll(buscado):
    tesis_df = pd.read_csv("~/csv_json_files/proyectos_carrera_etn/proy_titulo_autor.csv")
    lista_nombres = [item for item in tesis_df['NOMBRE']]
    lista_titulos = [item for item in tesis_df['TITULO']]
    # agregando a las listas nombres y titulos de la base de datos
    lista_titulos_sistema = [m.titulo for m in ProyectosInscritos.objects.all()]
    lista_nombres_sistema = [m.autor for m in ProyectosInscritos.objects.all()]
    lista_titulos = lista_titulos + lista_titulos_sistema
    lista_nombres = lista_nombres + lista_nombres_sistema
    stop_words = set(stopwords.words('spanish')) 
    # agregando a las listas nombres y titulos de la base de datos perfiles
    lista_titulos_sistema = [m.titulo for m in RegistroPerfil.objects.all()]
    lista_nombres_sistema = [m.equipo for m in RegistroPerfil.objects.all()]
    lista_titulos = lista_titulos + lista_titulos_sistema
    lista_nombres = lista_nombres + lista_nombres_sistema
    stop_words = set(stopwords.words('spanish')) 
    # agregando a las listas nombres y titulos de la base de datos perfiles
    lista_titulos_sistema = [m.titulo for m in ProyectoDeGrado.objects.all()]
    lista_nombres_sistema = [m.equipo for m in ProyectoDeGrado.objects.all()]
    lista_titulos = lista_titulos + lista_titulos_sistema
    lista_nombres = lista_nombres + lista_nombres_sistema
    stop_words = set(stopwords.words('spanish')) 
    # search_terms = 'servicio de voz'
    search_terms = buscado
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    vectors = vectorizer.fit_transform([search_terms] + lista_titulos)
    cosine_similarities = linear_kernel(vectors[0:1], vectors).flatten()
    titulo_scores = [round(item.item()*100,1) for item in cosine_similarities[1:]]  # convert back to native Python dtypes
    score_titles = list(zip(titulo_scores, lista_titulos, lista_nombres))
    ordenado_score = sorted(score_titles, reverse=True, key=lambda x:
            x[0])[:20] 
    dicc_score = {}
    for score_titulo in ordenado_score:
        dicc_score[score_titulo[0]] = score_titulo[1]
    return dicc_score

def searchGeneralDb(buscado):
    """Algoritmo de busqueda profunda"""

    c1 = contenido(ProyectosInscritos.objects.all())
    c2 = contenido(ProyectosExcel.objects.all())

    nombres1 = [m[0] for m in c1]
    contenidos1 = [m[1]for m in c1]

    nombres2 = [m[0] for m in c2]
    contenidos2 = [m[1]for m in c2]

    nombres = nombres1 + nombres2
    contenidos = contenidos1 + contenidos2

    stop_words = set(stopwords.words('spanish')) 
    search_terms = buscado
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    vectors = vectorizer.fit_transform([search_terms] + contenidos)
    cosine_similarities = linear_kernel(vectors[0:1], vectors).flatten()
    contenido_scores = [round(item.item()*100,1) for item in cosine_similarities[1:]]  # convert back to native Python dtypes
    score_titles = list(zip(contenido_scores, nombres))
    ordenado_score = sorted(score_titles, reverse=True, key=lambda x: x[0])[:20] 
    return ordenado_score

def searchByData(buscado):
    query_proyectos = ProyectosInscritos.objects.filter(
        Q(autor__icontains=buscado) |
        Q(mencion__icontains=buscado) |
        Q(titulo__icontains=buscado) |
        Q(tutor__icontains=buscado) |
        Q(docente__icontains=buscado) |
        Q(fecha_concluida__icontains=buscado)
       ).distinct()
    return query_proyectos

def searchByDataExcel(buscado):
    query_proyectos = ProyectosExcel.objects.filter(
        Q(autor__icontains=buscado) |
        Q(mencion__icontains=buscado) |
        Q(titulo__icontains=buscado) |
        Q(tutor__icontains=buscado) |
        Q(docente__icontains=buscado) |
        Q(fecha_concluida__icontains=buscado)
       ).distinct()
    return query_proyectos

# def searchProyectosInscritosCsv():
    # proyectos_df = pd.read_csv("~/csv_json_files/proyectos_carrera_etn/proyectos_inscripcion.csv")
    # proyectos_html = proyectos_df.to_html(classes='table sortable')
    # return proyectos_html
