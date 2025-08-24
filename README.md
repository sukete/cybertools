**Locksmith** es una herramienta desarrollada en Python para realizar **ataques de fuerza bruta** contra diferentes servicios y protocolos, incluyendo aplicaciones web, bases de datos y servicios de red como SSH y RDP.  

El proyecto nació como práctica de laboratorio y se ha ampliado con múltiples funcionalidades que lo convierten en un framework flexible, extensible y con medidas evasivas para evitar detecciones básicas.

---

## 🚀 Características principales

### 1. Métodos de ataque
- **Aplicaciones web**:
  - Análisis de respuesta HTML (ej. detección de mensajes como `Login Failed`).
  - Redirecciones HTTP (`http_redirect`).
  - Formularios y APIs modernas con payloads en JSON (`http_json`).
- **Bases de datos**: soporte inicial para **MySQL** (extensible a otros).
- **Servicios de red**: ataques de fuerza bruta a **SSH** y **RDP**.

### 2. Funcionalidades evasivas
- **Password Spraying**: evita bloqueos de cuenta espaciando los intentos por usuario.  
- **Delay configurable**: añade un retardo entre intentos.  
- **User-Agent spoofing**: simula distintos navegadores reales de manera aleatoria.  

### 3. Opciones de generalización
- `-i`: define el formato del payload a enviar (nombre de campos de usuario, contraseña, CSRF token, etc.).  
- `-m`: define la condición de fallo (cadena en la respuesta o página de redirección).  

### 4. Opciones adicionales
- `-s`: detener la búsqueda al primer positivo.  
- `-e`: añade la contraseña vacía al diccionario.  
- `-f`: formato de salida (consola, CSV o JSON).  
- `-q`: modo silencioso (solo resultados).  
- `-t num`: ejecución multihilo.  
- `-v`: modo verbose para depuración.  
- `-a`: lista de user-agents personalizados.  

---

## 📦 Instalación

```bash
git clone https://github.com/tuusuario/locksmith.git
cd locksmith
pip install -r requirements.txt
```

---

## ⚙️ Uso básico

### Definir objetivo
- Un único objetivo:
  ```bash
  python locksmith.py -u http://victima.com/login.php
  ```
- Lista de objetivos:
  ```bash
  python locksmith.py -l targets.txt
  ```

### Diccionarios de ataque
- Usuarios (`-U`)  
- Contraseñas (`-P`)  

Ejemplo:
```bash
python locksmith.py -u http://victima.com/login.php -U users.txt -P passwords.txt -m "Login Failed"
```

---

## 🌐 Ejemplos de uso

### 1. Ataque a formulario web tradicional
```bash
python locksmith.py -u http://dvwa/login.php -U users.txt -P passwords.txt -m "Login Failed" -p http_form
```

### 2. Ataque basado en redirecciones
```bash
python locksmith.py -u http://dvwa/login.php -U users.txt -P passwords.txt -p http_redirect -m "login.php"
```

### 3. Ataque contra API REST (JSON)
Ejemplo de login típico en JSON:
```http
POST /api/login HTTP/1.1
Content-Type: application/json

{
  "user": "juan",
  "pass": "1234"
}
```

Ejecución:
```bash
python locksmith.py -u http://victima.com/api/login -U users.txt -P passwords.txt -p http_json -i '{"username":"user","password":"pass"}' -m "error"
```

---

## 📊 Salida de resultados

Dependiendo del formato elegido (`-f`), Locksmith genera:
- **Consola** (por defecto).  
- **CSV** con resultados exportables.  
- **JSON** para integraciones automáticas.  

Ejemplo:
```
[+] Found valid credentials:
    user: admin
    password: 123456
```

---

## 🛡️ Medidas evasivas en acción

- **Password Spraying**:  
  En lugar de probar todas las contraseñas contra un único usuario, Locksmith recorre la lista de contraseñas aplicándolas a todos los usuarios de forma rotativa.  

- **Delay entre intentos**:
  ```bash
  python locksmith.py -u http://victima.com/login -U users.txt -P passwords.txt --delay 3
  ```
  Cada intento espera 3 segundos antes de lanzar el siguiente.  

# 🕵️ WebBurglar

**WebBurglar** (Asaltante de Webs) es una herramienta desarrollada en Python para la **recolección de información y análisis de aplicaciones web**, con el objetivo de facilitar la detección de vulnerabilidades y preparar distintos ataques.  

A lo largo del curso se han implementado funcionalidades de **webscraping, enumeración y explotación básica**, convirtiéndola en un recurso útil para auditorías y pruebas de seguridad.

---

## 🚀 Características principales

### 1. Web Scraping
- Extrae todos los **enlaces internos** al mismo dominio.  
- Permite configurar la **profundidad de búsqueda** con `-D`.  
- Con `-e` muestra también los enlaces externos (pero sin seguirlos).  

### 2. Listado de Formularios
- Analiza formularios encontrados en la web, mostrando:  
  - Campos visibles.  
  - Campos ocultos.  
- Permite construir payloads basados en la estructura real del formulario.  
- Compatible con el parámetro `-D` para analizar páginas accesibles desde la URL inicial.  

### 3. Directory Listing
- Detecta y enumera directorios sin archivo de índice (ej. `index.html`).  
- Expone posibles archivos sensibles como:  
  - Código fuente.  
  - Respaldos.  
  - Configuraciones.  
  - Credenciales.  

### 4. LFI (Local File Inclusion)
- Permite lanzar ataques de **inclusión local de archivos**.  
- Parámetros principales:  
  - `-u`: URL a atacar.  
  - `-p`: payload (archivo objetivo a leer).  
  - `-F`: campo GET vulnerable.  
  - `-D`: profundidad de directorios.  

Ejemplo:  
```bash
python webburglar.py -u http://victima.com/vuln.php -F page -p etc/hosts -D 4
```
Generará el payload:  
```
../../../../etc/hosts
```

---

## ⚙️ Parámetros adicionales

- `-C`: permite pasar una cookie de sesión válida para acceder a recursos autenticados.  
- `-D`: nivel de recursividad tanto para webscraping como para ataques LFI.  

---

## 📦 Instalación

```bash
git clone https://github.com/tuusuario/webburglar.git
cd webburglar
pip install -r requirements.txt
```

---

## 🌐 Ejemplos de uso

### 1. WebScraping recursivo
```bash
python webburglar.py -u http://victima.com -D 2
```

### 2. Mostrar también enlaces externos
```bash
python webburglar.py -u http://victima.com -D 1 -e
```

### 3. Listado de formularios en la web
```bash
python webburglar.py -u http://victima.com/form.php -D 1
```

### 4. Ataque LFI a `/etc/passwd`
```bash
python webburglar.py -u http://victima.com/vuln.php -F file -p etc/passwd -D 5
```

### 5. Acceso con cookie de sesión
```bash
python webburglar.py -u http://victima.com/panel -C "PHPSESSID=abc123"
```

---

## 📊 Salida de resultados

La aplicación presenta los resultados de forma clara en consola, mostrando:
- Listados de enlaces.  
- Formularios detectados.  
- Archivos y directorios enumerados.  
- Contenido extraído mediante LFI.  




## ⚠️ Aviso legal

Este software se ha desarrollado **con fines académicos y de auditoría de seguridad**.  
El uso de esta herramienta contra sistemas sin autorización expresa es **ilegal** y puede tener consecuencias penales.  
El autor no se hace responsable del uso indebido de la herramienta.  

---

## 📚 Roadmap

- [ ] Ampliar soporte a otros protocolos (FTP, SMTP, POP3).  
- [ ] Añadir soporte para proxys y rotación de IPs.  
- [ ] Mejorar la interfaz CLI con `argparse` avanzado.  
- [ ] Añadir integración con bases de datos para almacenar resultados.
- [ ] Añadir soporte para detección de XSS reflejado en formularios.  
- [ ] Exportar resultados en formatos JSON y CSV.  
- [ ] Integración con proxys y rotación de cabeceras.  
- [ ] Automatizar payloads comunes para LFI.  

---

## ✨ Créditos

Desarrollado en Python por Felix Alberto Castan Cid  
Inspirado en prácticas de **seguridad ofensiva** y herramientas de pentesting como Hydra, Medusa y Burp Intruder.
