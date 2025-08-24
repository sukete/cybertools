#!/usr/bin/python3
# 
# My own miscelaeneus libraries
#
from pyfiglet import Figlet
import os

TEXTCOLOR={"normal":"\033[0;0m","red":"\033[0;31m","green":"\033[0;32m","blue":"\033[0;34m","black":"\033[0;30m","yellow":"\033[0;33m","white":"\033[0;37m","orange":"\33[38;5;208m"}
'''
this function is to do a formated print in a designated file
'''
def myprint (fichero,texto,mark,color="normal"):
    COL=""
    if color in TEXTCOLOR:
       COL=TEXTCOLOR[color]
    if mark=="":
        lista=mark
    else:
        lista="["+mark+"] "
    #fichero.write (COL+lista+texto+"\n")
    print(COL+lista+texto+TEXTCOLOR['normal'])

def messg (texto,mark,color="normal"):
    COL=""
    if color in TEXTCOLOR:
       COL=TEXTCOLOR[color]
    if mark=="":
        lista=mark
    else:
        lista="["+mark+"] "
    return COL+lista+texto+TEXTCOLOR['normal']
'''
this function prints an empty line
'''
def printlinea (fichero):
    fichero.write("\n")

'''
'''
def titulo (TITULO,DESC1,DESC2,color,bkcolor):
    os.system('clear')
    size = os.get_terminal_size()
    #texto = pyfiglet.figlet_format(TITULO,font='larry3d',width=size.columns)
    try:
        # Carga manual desde archivo .flf
        font_path = os.path.join(os.path.dirname(__file__), 'figlet-fonts', 'larry3d.flf')
        fig = Figlet(font=font_path, width=size.columns)
    except Exception:
        # Fallback si falla la fuente personalizada
        fig = Figlet(font='slant', width=size.columns)

    texto = fig.renderText(TITULO)

    print(messg(texto,'',color))
    print(messg(DESC1,'##',color))
    print(messg(DESC2,'##',color))

'''
La funcion do_nothing no hace nada
'''

def do_nothing():
    return 1


'''
Functions to validate input strings
'''

def check_int(string,maxv=0,minv=-1):
  result=False
  try:
      value=int(string)
  except:
      return result,0
  if (maxv > minv): 
        result=maxv>value
  elif minv==maxv:
        result=value>=minv
  return result,value      


'''
'''
def printfmt(values,fields,fmt,sep='|'):
    if fmt=='csv': 
        print(sep.join(fields))
        for item in values:
            print (sep.join(item))
    elif fmt=='json':
       resultado="["
       for item in values:
           resultado+="{"
           for i in range (len(fields)):
               resultado+=f"\'{fields[i]}\':\'{item[i]}\',"
           resultado=resultado[:-1]
           resultado+="},"   
       resultado=resultado[:-1]
       resultado+=']'
       print(resultado)
