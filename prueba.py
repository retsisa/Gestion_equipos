import sqlite3
from werkzeug.security import generate_password_hash
conn=sqlite3.connect("Python-SQLite/Gestion_Equipos/instance/Gestion_equipos.db")

cursor=conn.cursor()

dat=cursor.execute("SELECT * FROM usuarios").fetchall()
print(dat)

# Reemplaza 'usuarios' con el nombre de tu tabla
columnas = cursor.execute("PRAGMA table_info(equipos);").fetchall()

for columna in columnas:
    print(f"Nombre: {columna[1]}, Tipo: {columna[2]}, Es PK: {columna[5]}")

# Usuarios con sus roles
'''usuarios = [
    ("Admin1", "1234", "admin"),
    ("Profesor1", "1234", "profesor"),
    ("Estudiante1", "1234", "estudiante"),
    ("Tecnico1", "1234", "tecnico")
]

# Insertar usuarios con hash
for username, password, rol in usuarios:
    cursor.execute("INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)",
                   (username, generate_password_hash(password), rol))

conn.commit()'''
conn.close()

print("Usuarios insertados correctamente.")


conn.close()
'''
from pyzbar.pyzbar import decode
from PIL import Image

def leer_qr(ruta_imagen):
    datos = decode(Image.open(ruta_imagen))
    for d in datos:
        print("Contenido del QR:", d.data.decode('utf-8'))

leer_qr("static/qrs/PC-1_qr.png")


import qrcode

# Datos a modificar
datos_modificados = "https://nuevo-enlace.com"

# Crear el QR
qr = qrcode.QRCode(
    version=1,  # tamaño del QR, puedes modificar este valor si es necesario
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,  # tamaño de cada bloque del QR
    border=4,  # grosor del borde
)

qr.add_data(datos_modificados)
qr.make(fit=True)

# Crear la imagen del QR
img = qr.make_image(fill='black', back_color='white')

# Guardar el QR generado
img.save("qr_modificado.png")'''


