import requests
from bs4 import BeautifulSoup
import csv
import ftplib

# Realizar la solicitud GET a la página de cartelera de cine de elpais.com
url = "https://elpais.com/cultura/cartelera/"
response = requests.get(url)

# Crear un objeto BeautifulSoup para analizar el HTML
soup = BeautifulSoup(response.content, "html.parser")

# Buscar todos los elementos <a> que contienen la información de las películas en cartelera
cartelera = soup.find_all("a", {"class": "ce_c"})
   
# Crear un archivo CSV para guardar los datos extraídos
with open("cartelera.csv", "w", newline="") as f_output:
    csv_writer = csv.writer(f_output)

    # Escribir los encabezados de las columnas en el archivo CSV
    csv_writer.writerow(["Nombre de la película", "URL"])

    # Iterar sobre cada película en cartelera y extraer el nombre y la URL
    for pelicula in cartelera:
        # Extraer el nombre de la película
        nombre = pelicula.find("h2", {"class": "titulo"}).get_text()

        # Extraer la URL de la película
        url = pelicula["href"]

        # Escribir el nombre y la URL de la película en el archivo CSV
        csv_writer.writerow([nombre, url])

# Publicar el archivo CSV en un servicio FTP
ftp_host = "172.17.0.2"
ftp_user = "Kinepolis"
ftp_password = "123456"
ftp_dir = "/public_html"

ftp = ftplib.FTP(ftp_host, ftp_user, ftp_password)
ftp.cwd(ftp_dir)

with open("cartelera.csv", "rb") as f:
    ftp.storbinary("STOR cartelera.csv", f)

ftp.quit()
