# Operaciones por Lotes en Dalle

Para utilizar el script correctamente, en primer lugar, se deben instalar las dependencias correctas. Para esto se puede utilizar el archivo `requirements.txt` con el siguiente comando:

```
python pip install -r requirements.txt
```

Ademas, se debe crear un archivo `.env` que tenga la misma estructura expuesta en el archivo `.env.example`. En las variables de entorno se tienen los siguientes parametros:

- **ROOT_PATH:** Ruta correspondiente al directorio en donde se ha creado la carpeta que contiene toda la informacion sobre las imagenes. Se recomienda que el directorio utilizado sea el de "Fotos" (En windows la ruta seria como: 'C:\Users\user_name\Pictures')
- **PICTURE_FOLDER:** Nombre de la carpeta contenedora de las imagenes originales y las variaciones que se van a generar con la ejecucion de este script.
- **EMAIL:** Correo electronico utilizado para hacer login en la plataforma
- **PASSWORD:** Contraseña utilizada para hacer login en la plataforma
- **DB_NAME:** Nombre de la base de datos que se utilizara para guardar el progreso de la generacion de imagenes


Finalmente, luego de llenar la informacion necesaria en el archivo .env debes ir hasta la carpeta `PICTURE_FOLDER` y crear dentro de ella otra carpeta llamada `originals`(en esta nueva carpeta se deben guardar las fotos originales). Es decir, las fotos originales van a quedar guardadas en una ruta similar a la siguiente:

```
C:\Users\user_name\Pictures\PICTURE_FOLDER\originals
```


Luego de cumplir con ambas condiciones se puede utilizar el script.
