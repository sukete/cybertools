#!/usr/bin/python3
from sukolib import *
from bruteforce import *
import argparse

parms={}
parser = argparse.ArgumentParser(description='Comando para realizar ataques de fuerza bruta utilizando distitos tipos de protocolo')  

parser.add_argument ("-f","--fmt", help="Formato de la salida del comando. (Console,json,csv)",default='console')
parser.add_argument ("-U","--user", help="Fichero con lista de usuarios para probar",default='users.txt')
parser.add_argument ("-u","--url", help="url de destino",default="http://127.0.0.1/DVWA/login.php")
parser.add_argument ("-P","--password", help="Fichero con lista de contraseñas a probar",default="passwords.txt")
parser.add_argument ("-p","--protocol", help="Protocolo a utilizar para el ataque. Utiliza 'locksmith -L' para listar los protocolos soportados",default="http")
parser.add_argument ("-m","--message", help="Mensaje de error en el login que indica que usuario/contraseña no son validos",default="Login failed")
parser.add_argument ("-i","--input", help="Define la estructura de los cambios del formulario de login",default="username:username,password:password,user_token:user_token,login:Login")
parser.add_argument ("-t","--threads", help="Permite ejecucion en 'n' hilos",default="0")
parser.add_argument ("-a","--agent", help="Permite incluir user agent en la cabecera de las peticiones http,como una lista de \'user agents\' separados por \':\'",default="None")
parser.add_argument ("-l","--target_list", help="permite definir una lista de destinos en un fichero",default="None")
parser.add_argument ("-s","--stop", action='store_true',help="Se detiene al encontrar el primer acceso válido")
parser.add_argument ("-S","--spraying", action='store_false',help="Analiza cada password para todos los usuarios y sigue con la siguiente")
parser.add_argument ("-L","--list", action='store_true',help="Lista los protocolos soportados")
parser.add_argument ("-e","--empty", action='store_true',help="Añade al proceso de prueba la contraseña vacia")
parser.add_argument ("-T","--delay" ,help="añade un delay entre cada prueba",default='0')
parser.add_argument("-v","--verbose", action='store_true', help='Activa el modo debug')
parser.add_argument("-q","--quiet", action='store_true', help='Desactiva todos los mensajesi de salida')

formatos=['console','csv','json','xml']


try:
 args=parser.parse_args() 
 targets=args.target_list   
 formato=args.fmt
 if formato not in formatos:
    if not args.quiet:
     print (messg(f"Error: Formato de salida {formato} incorrecto",'ERROR','red'))
     print (messg(f"La salida se mostrará por pantalla con el formato predeterminado",'INFO','blue'))
    formato='console'
 check_threads=check_int(args.threads,16)
 if check_threads[0] : 
    threads=check_threads[1]
    if threads > 0:
     if not args.quiet:
        print (messg(f"El proceso se ejecutara con {threads}  hilo",'INFO','blue'))
 else:
    threads=0
    if not args.quiet:
     print (messg(f"Error: Numero de threads especificado incorrecto.",'ERROR','red'))
     print (messg(f"El proceso se ejecutara con un solo hilo",'INFO','blue'))

 check_delay=check_int(args.delay,30)
 if check_delay[0] : 
    delay=check_delay[1]
 else:
    if not args.quiet:
     print (messg(f"Error: retardo especificado no válido.",'ERROR','red'))
     print (messg(f"El proceso se ejecutara sin aplicar retardo etre muestras",'INFO','blue'))
    delay=0

 parms['url_login'] = args.url
 users_file = args.user
 passwords_file = args.password
 parms['mensaje'] = args.message
 verbose = args.verbose
 delay=int(args.delay)
 parms['payload_fields']={}
 for item in args.input.split(','):
    parms['payload_fields'][item.split(':')[0]]=item.split(':')[1]
except Error as e:
    print (messg(f"Error {e}: interpretando la lista de parámetros",'ERROR','red'))

if args.agent=='NONE':
   parms['user-agent']=["Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36","Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"]
else:
 parms['user_agent']=args.agent.split(":")

'''
'''

def main():

 if not args.quiet:
      titulo ("\t| lockSmith |","Brute force Pentesting Tool, V 0.1","Author: Felix Castan Cid",'red','black')
 verbose=args.verbose and (not args.quiet)
 protocol=args.protocol.lower()
 if args.list:
     print (messg(f"Los protocolos soportados son: {list(functions.keys())}","+",'green'))
     return 0

 if protocol not in functions.keys():
     print (messg(f"El protocolo {protocol} no esta soportado","ERROR",'red'))
     print (messg(f"Los protocolos soportados son: {list(functions.keys())}","+",'green'))
     return 0
 if  verbose:
          print (f"Buscando credenciales para {parms['url_login']}")


 userpwList=bruteList(users_file,passwords_file, args.spraying,args.empty)
 if targets=='None':
     url_list=[f"{protocol}|{args.url}"]
 else:
     try:
         with (open (targets,'r')) as f:
               url_list=[line.strip() for line in f.readlines()]
     except Exception as e:
               print (messg(f"Error {e} abreiendo el fichero {targets}",'-','red'))
               exit ()
 encontrados=[]
 if not args.quiet:
    print (messg(f"Iniciando escaneo en {parms['url_login']}",'INFO','blue'))
 if threads==0:
   for url in url_list:
    protocol=url.split('|')[0]
    parms['url_login']=url.split('|')[1]
    encontrados+=bruteforce(userpwList,args.stop,parms,protocol,delay,args.verbose)
 else:   
   for url in url_list:
    protocol=url.split('|')[0]
    parms['url_login']=url.split('|')[1]
    encontrados+=bruteforce(userpwList,args.stop,parms,protocol,delay,args.verbose)

 #borrar salida=[]
 if not args.quiet:
    print (messg(f"Escaneo finalizado, se han encontrado {len(encontrados)} usuarios vulnerables",'INFO','blue'))
 if (formato=='console'):
    for item in encontrados:
      if "http" in protocol:
          print (messg(f"URL: {item[0]} Usuario:{item[1]} Password:{item[2]} Cookies: {item[3]}",'+','red'))
      else:
       print (messg(f"URL: {item[0]} Usuario:{item[1]} Password:{item[2]}",'+','red'))
     
 else:
    if "http" in protocol:
     printfmt(encontrados,('URL','Usuario','Password','cookies'),formato)
    else:
     printfmt(encontrados,('URL','Usuario','Password'),formato)

 if (threads > 1) and verbose:      
  for prueba in pruebas:
     print (prueba)
main()
