# Utiliza la imagen base de Python 3.9
FROM python:3.9

ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia los archivos de requisitos al directorio de trabajo
COPY requirements/ /code/requirements

# Instala las dependencias comunes a todos los entornos
RUN pip install -r requirements/base.txt

# Instala las dependencias específicas del entorno local de desarrollo
RUN pip install -r requirements/local.txt

# Copia el resto de los archivos de la aplicación al directorio de trabajo
COPY . /code/

# Expone el puerto 8080 del contenedor (ajusta el puerto según sea necesario)
EXPOSE 8080

# Define el comando predeterminado para ejecutar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]