import subprocess
import time
import sys
import requests
from bs4 import BeautifulSoup
from sukolib import *
import time
import random
from urllib.parse import urljoin
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import ast

import requests

#url = "https://www.ibm.com"
#response = requests.get(url, verify=False)  # No verifica el certificado
#print(response.status_code)

suffix=["co","edu",'gob','net','mil','org','gov','nom','info']
known_ports={'http':'80','https':'443','ftp':'21'}
uagent_headers=["Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36","Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Mobile/15E148 Safari/604.1","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41"]


class urlsuko():
     def __init__(self,url):
        self.url=url
        lurl=self.url.split('/')
        if lurl[0][-1]==':':
            self.protocol=lurl[0][0:-1]
            target=lurl[2].split(':')
        else:
            self.protocol='http'
            target=lurl[0].split(':')
            self.url=f"{self.protocol}://{self.url}"
        if len(target)>1:
            self.port=target[1]
            
        elif self.protocol in known_ports.keys():
            self.port=known_ports[self.protocol]
        else:
            self.port='80'
        if len(target[0].split('.'))>2:    
          if target[0].split('.')[-2] in suffix:
            self.domain='.'.join(target[0].split('.')[-3:])
          else:
            self.domain='.'.join(target[0].split('.')[-2:])
        else:
            self.domain=target[0]
        self.cookies={}
        self.uagent=random.choice(uagent_headers)

     def get_domain(self):
         return self.domain
         
     def get_protocol(self):
         return self.protocol
         
     def get_port(self):
         return self.port
         
     def ping(self):
         pass

     def setURL (self,url):
         self.url=url

     def getURL(self,allow_redirects=True,timeout=(1,3)):
         session = requests.Session()
         session.headers['User-Agent']=self.uagent
         for name,value in self.cookies.items():
                session.cookies.set(name,value)
         try:
            response = session.get((self.url),allow_redirects=allow_redirects,verify=False,timeout=timeout)
            return True,response
         except Exception as e:
            return False,f"Error {e} accediendo a la URL {self.url}"
        
     def same_domain(self,url):
         o=urlsuko(url)
         return self.get_domain()==o.get_domain()

     def check(self):
         return True
     
     def get_cookies(self):
         return self.cookies

     def set_cookies(self,cookie_str):
         self.cookies = ast.literal_eval(cookie_str)

     def set_uagent(self,uagent):
         self.uagent=uagent

     def get_uagent(self):
         return self.uagent

     def getLinks(self):
         link_list=set()
         status,response=self.getURL()
         if not status:
             print (messg(response,'-','red'))
             return link_list
         soup = BeautifulSoup(response.text, 'html.parser')
         for a in soup.find_all('a', href=True):
             href = a['href']
             link = urljoin(self.url, href)
             if link.startswith("http://") or link.startswith("https://"):
                link_list.add(link)
         return link_list
 
     def getFiles(self):
         file_list=set()
         status,response=self.getURL()
         if not status:
             return file_list
         soup = BeautifulSoup(response.text, 'html.parser')
         for a in soup.find_all('a', href=True):
             href = a['href']
             file_list.add(a['href'])
         return file_list

     def login(self,payload,token_name,verbose=False):
         try:
            session = requests.Session()
            session.headers['User-Agent']=self.uagent
            response = session.get((self.url),verify=False)
         except:
            return False,f"Error {e} accediendo a {self.getURL()}" 
         soup = BeautifulSoup(response.text, 'html.parser')
         token_input = soup.find('input', {'name': token_name})
         if token_input:
            payload[token_name] = token_input['value']
         else:
             print("no token input")
         try:
          post_response=session.post(self.url, data=payload)
          if verbose:
             #print(session.cookies)
             print(post_response.headers.get("Set-Cookie"))
          self.cookies=session.cookies.get_dict()
          return True,post_response,session.cookies
         except Exception as e:
          return False,f"Error {e} accediendo a {self.getURL()}" 
