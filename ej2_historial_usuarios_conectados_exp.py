# -*- coding: utf-8 -*-
# Se importa Popen que permite ejecutar comandos de Linux en Python
# Se importa PIPE para manejar la salidas estandar
from subprocess import Popen, PIPE

# Se importa para desplegar mensajes en la salida estandar de errores.
import sys
#import os

# Se importa argparse para interpretar parametros
import argparse
parser = argparse.ArgumentParser()

# Funcion para normalizar el resultado del script bash
def normalizarlista(lista_conexiones_ej1):
    listaTemp = []
    for i in range(0, len(lista_conexiones_ej1)):
        listaTemp.append(lista_conexiones_ej1[i].split())

    return listaTemp

# Funcion para imprimir lista ordenada
def imprimo_lista(listaConOrdenadas, cabecera, pie):
    print("{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}\t\t{}".format(*cabecera))
    for i in range(0, len(listaConOrdenadas)):
        print("{}\t\t{}\t\t{}\t\t{} {} {}\t\t{} {}\t{}\t\t{}".format(*listaConOrdenadas[i]))
    print("\r")
    print("{} {} {} {} {} {} {} {} {} {} {} {} {}".format(*pie))

def imprimo_lista_filtrada(listaConOrdenadas, cabecera, pie):
    # Se usa el reverso del split, join para unir texto
    print("\t\t ".join(cabecera))
    for i in range(0, len(listaConOrdenadas)):
        print("\t\t ".join(listaConOrdenadas[i]))
    print("\r")
    print(" ".join(pie))
    print("\r")
    print("Cantidad de conexiones listadas para el usuario", args.usuario, len(listaConOrdenadas), ".")

def filtro(listaConOrdenadas,cabecera):
    # Saco el guion que es una bolsa...
    for i in range(0,len(listaConOrdenadas)):
        del listaConOrdenadas[i][7]

    noHayf=False

    if "u" in args.filtro:
        listaNueva = list(filter(lambda x: x[0], listaConOrdenadas))
        for listaConOrdenadas in listaNueva:
            del listaConOrdenadas[0]
        del cabecera[0]
    else:
        listaNueva = listaConOrdenadas
    if "f" in args.filtro:
        for i in range(0,len(cabecera)-1):
            if "Fecha" == cabecera[i]:
                for x in range (0, len(listaNueva)):
                    del listaNueva[x][i]
                    del listaNueva[x][i]
                    del listaNueva[x][i]
                del cabecera[i]
    else:
        noHayf=True
    if "t" in args.filtro:
        for i in range(0,len(cabecera)-1):
            if "Term" == cabecera[i]:
                for x in range (0, len(listaNueva)):
                    del listaNueva[x][i]
                del cabecera[i]
    if "h" in args.filtro:
        for i in range(0,len(cabecera)-1):
            if "Host" == cabecera[i]:
                for x in range (0, len(listaNueva)):
                        del listaNueva[x][i]
                del cabecera[i]
    if "c" in args.filtro:
        for i in range(0,len(cabecera)-1):
            if "H.Con" == cabecera[i]:
                for x in range (0, len(listaNueva)):
                    if noHayf:
                        del listaNueva[x][i+2]
                    else:
                        del listaNueva[x][i]
                del cabecera[i]
    if "n" in args.filtro:
        for i in range(0,len(cabecera)-1):
            if "H.Des" == cabecera[i]:
                for x in range (0, len(listaNueva)):
                    if noHayf:
                        del listaNueva[x][i+2]
                    else:
                        del listaNueva[x][i]
                del cabecera[i]
    if "d" in args.filtro:
        for i in range(0,len(cabecera)):
            if "T.Con" == cabecera[i]:
                for x in range (0, len(listaNueva)):
                    if noHayf:
                        del listaNueva[x][i+2]
                    else:
                        del listaNueva[x][i]
                del cabecera[i]


# Se definen los modificadores
parser.add_argument("-u", "--usuario", type=str, help="Usuario a desplegar sus conexiones.", action="store")

parser.add_argument("-r", "--redondeo", help="Despĺiega el tiempo total de conexiones.", action="store_true")

# Se ordena el resultado dependiendo del parametro
parser.add_argument("-o", "--orden", type=str, choices=["u", "t", "h", "d"], help="Ordena segun el criterio. {u} se ordenara por nombre. {t} se ordena por nombre de terminal. {h} se ordena por host. {d} se ordena por su duracion")

#
parser.add_argument("-i", "--inverso", help="Ordena por orden inverso.", action="store_true")

# [-f {u,t,h,f,c,n,d}]
parser.add_argument("-f", "--filtro", type=str, choices=["u", "t", "h", "f", "c", "n", "d"], nargs='+', help="Filtra por cualquiera de estos valores: {u} ")

# Validamos que no hayan errores
try:
    args = parser.parse_args()
except SystemExit as e:
    exit(25)

# Cargamos el script
ej1YParametros = ['/root/ej1_historial_usuarios_conectados.sh']

ej1YParametros.append("-u")
ej1YParametros.append(args.usuario)

# Enviamos los parametros
if args.redondeo:
    ej1YParametros.append("-r")

# Creamos el proceso
proceso = Popen(ej1YParametros, stdout=PIPE, stderr=PIPE)

# Causa la ejecucion del proceso y trae el resultado
salida= proceso.communicate()

# Validamos que el proceso no haya dado errores
if proceso.returncode > 0:
    print(salida[0].decode(), file=sys.stderr, end="")
    exit(proceso.returncode)

if salida[1].decode() != "":
    print(salida[1].decode(), file=sys.stderr, end="")
    exit(0)

# Se carga lista por cada linea obtenida
lista_conexiones_ej1 = salida[0].decode().split("\n")

# Se elimina la ultima linea vacia
lista_conexiones_ej1.pop(-1)

# Aca se puede comenzar a escribir las lineas correspondientes a cada funcion
hayQueOrdenar=False
if not (args.orden == None):
    hayQueOrdenar=True
# Hay que filtrar?
hayQueFiltrar=False
if not (args.filtro == None):
    hayQueFiltrar=True
# En caso de i se retorna el inverso
esReverso=False
if args.inverso:
    esReverso=True

# Si es necesario normalizar
if hayQueOrdenar:

    # Se normaliza el texto
    listaConOrdenadas = normalizarlista(lista_conexiones_ej1)

    cabecera = listaConOrdenadas[0]
    pie = listaConOrdenadas[int(len(listaConOrdenadas)) - 1]

    # Borro cebecera y pie. Tambien se borra el enter con el objetivo de normalizar y luego ordenar
    listaConOrdenadas.pop(0)
    listaConOrdenadas.pop(int(len(listaConOrdenadas)) - 1)
    listaConOrdenadas.pop(int(len(listaConOrdenadas)) - 1)

    # Ordeno segun lo solicitado
    if (args.orden == "u"):
        listaConOrdenadas = sorted(listaConOrdenadas, key=lambda x: x[0], reverse=esReverso)

    if (args.orden == "t"):
        listaConOrdenadas = sorted(listaConOrdenadas, key=lambda x: x[1], reverse=esReverso)

    if (args.orden == "h"):
        listaConOrdenadas = sorted(listaConOrdenadas, key=lambda x: x[2], reverse=esReverso)

    if (args.orden == "d"):
        listaConOrdenadas = sorted(listaConOrdenadas, key=lambda x: x[9], reverse=esReverso)

#    filtro(listaConOrdenadas)

    # Imprimo el resultado si no hay que filtrar
    if not hayQueFiltrar:
        imprimo_lista(listaConOrdenadas, cabecera, pie)

# Hay que filtrar?
if hayQueFiltrar:
    # Se normaliza el texto
    if not hayQueOrdenar:
        listaConOrdenadas = normalizarlista(lista_conexiones_ej1)

        cabecera = listaConOrdenadas[0]
        pie = listaConOrdenadas[int(len(listaConOrdenadas)) - 1]

        # Borro cebecera y pie. Tambien se borra el enter con el objetivo de normalizar y luego ordenar
        listaConOrdenadas.pop(0)
        listaConOrdenadas.pop(int(len(listaConOrdenadas)) - 1)
        listaConOrdenadas.pop(int(len(listaConOrdenadas)) - 1)

    if not len(args.filtro) >= 7:
        filtro(listaConOrdenadas,cabecera)
        imprimo_lista_filtrada(listaConOrdenadas, cabecera, pie)
    else:
        print("Al menos un campo debe estar visible, no pudiendose ocultar todos.")
        exit(20)




# En caso de que no existan otros modificadores
if not hayQueOrdenar and not hayQueFiltrar:
    for i in range(0, len(lista_conexiones_ej1)):
        print(lista_conexiones_ej1[i])
