import subprocess
import time
import sys

class rdp():
     def __init__(self,ip,user,password='none',port=3389):
        self.ip=ip
        self.user=user
        self.password=password
        self.port=port

     def try_connect(self):
         CMD=f"xfreerdp3 /v:{self.ip} /u:{self.user} /p:{self.password} /port:{self.port} +auth-only /timeout:500 /cert:ignore"
         try:
            #salida=str(subprocess.check_output (CMD,shell=True).decode())[:-1]
            resultado = subprocess.run(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            salida_stdout = resultado.stdout.strip()  # Salida estándar
            salida_stderr = resultado.stderr.strip() 
            return resultado.returncode==0
         except Exception as e:
            return False

     def ping(self):
         try:
          subprocess.check_output ("ping -c 1 "+self.ip,shell=True)
          return True   
         except:   
             return False

