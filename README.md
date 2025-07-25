# REST API con Redis

URL del proyecto (API) desplegado: https://redis-api-dev-api.azurewebsites.net/

Proyecto para la clase de **sistemas expertos**, el cual consiste en realizar una REST API utilizando
los siguientes recursos de azure:

- Data Factory
- Container Registry
- App Service Plan
- App Service
- SQL Server
- Redis Cache
- Application Insights

Además el proyecto utiliza otras herramientas como ser:

- Firebase
- JWT (Json Web Tokens)

## Requerimientos básicos

- El proyecto fue realizado con python **3.13.5**, por lo que si no tienes esta versión se sugiere actializar.
- Se sugiere utilizar un entorno virtual

## Correr el proyecto local

- Crear un archivo .env en la raíz de la carpeta del proyecto que contenga las variables especificadas en el archivo **.example.env**
- Crear una carpeta **secrets** en la carpeta raíz del proyecto que contenga el archivo **secrets.json** con el secret de firebase para utilizar su servicio de autenticación
- Instalar las dependencias necesarias
  ```bash
  pip install -r requirements.txt
  ```
- Correr el programa
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8080 --reload
  ```

## Utilizar los endpoints

Los únicos endpoints que necesitan token de JWT en el Header Authentication son los endpoints para crear el producto y para obtener los usuarios creados, es decir:

- POST {{DOMINIO}}/products
- GET {{DOMINIO}}/users

### Utilizando el archivo api.http

- Los endpoints están especificados en el archivo **api.http** y se pueden ejecutar instalando el plugin **RestClient** en VSCODE.
RestClient puede ser instalado con el siguiente comando al abrir VSCODE quick open (ctr + p):
  ```bash
  ext install humao.rest-client
  ```
- Recordar cambiar el valor de la variable DOMAIN de acuerdo al caso 

### Utilizando Postman

- importar el archivo postman.json en tu cuenta de postman
- Se utiliza la variable DOMAIN  
