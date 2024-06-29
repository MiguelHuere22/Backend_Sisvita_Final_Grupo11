FROM python:3.11

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar todos los archivos de la aplicación al contenedor
COPY ./ /app

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto en el que correrá la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación con Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${PORT}", "app:app"]
