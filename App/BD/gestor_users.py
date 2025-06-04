import sqlite3
import random
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
DB_PATH = "BD/indicadores.db"

class Usuario:
    # Constructor de la clase
    def __init__(self, username, contraseña):
        username= username
        contraseña= contraseña


    # Crear usuario
    def crear_usuario(username, contraseña, email):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Introducir indicador seleccionado
        cursor.execute(
            """INSERT INTO usuarios (username, contraseña, email) 
            VALUES (?, ?, ?)""", (username, contraseña, email)
        )
        # Cerrar conexion
        conex.commit()
        conex.close()

    # Para comprobar que la contraseña cumpla las condiciones: mín 6 car., 1 may, 1 nº
    def contraseña_valida(pwd):
        if len(pwd) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres"
        if not any(c.isupper() for c in pwd):
            return False, "La contraseña debe contener al menos una letra mayúscula"
        if not any(c.isdigit() for c in pwd):
            return False, "La contraseña debe contener al menos un número"
        return True, ""
    
    # Cambiar la contraseña
    def set_pwd_email(new_pwd, email):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute("UPDATE usuarios SET contraseña=? WHERE email=?", (new_pwd, email))
        # Cerrar conexion
        conex.commit()
        conex.close()

    # Para comprobar que no hay ningun username así
    def username_existe(username):
        # Conectar con la db
        conex = sqlite3.connect(DB_PATH)
        cursor = conex.cursor()
        # Comprobar si ya hay algún username así
        cursor.execute("SELECT 1 FROM usuarios WHERE username = ?", (username,))
        # Cerrar conexion
        resultado = cursor.fetchone()
        conex.close()
        # True si existe en la bd, False si no
        return resultado is not None 
    
    # Para comprobar que no hay ningun email así
    def email_existe(email):
        # Conectar con la db
        conex = sqlite3.connect(DB_PATH)
        cursor = conex.cursor()
        # Comprobar si ya hay algún email así
        cursor.execute("SELECT 1 FROM usuarios WHERE email = ?", (email,))
        # Cerrar conexion
        resultado = cursor.fetchone()
        conex.close()
        # True si es valido, False si no (ocupado)
        return resultado is not None 
    
    # Función para saber la contraseña del usuario
    def get_pwd(username):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute(f"SELECT contraseña FROM usuarios WHERE username=?", (username,))
        res_fetch= cursor.fetchone()
        res= res_fetch[0]
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        return res
    
    # Función para cambiar la contraseña de un usuario
    def set_pwd(new_pwd, username):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute("UPDATE usuarios SET contraseña=? WHERE username=?", (new_pwd, username))
        # Cerrar conexion
        conex.commit()
        conex.close()
    
    # Función para saber el nombre de usuario teniendo el correo
    def get_username(email):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute("SELECT username FROM usuarios WHERE email=?", (email,))
        res_fetch= cursor.fetchone()
        res= res_fetch[0]
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        return res
    
    # Función para saber el correo del usuario
    # Función para saber el nombre de usuario teniendo el correo
    def get_email(username):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute("SELECT email FROM usuarios WHERE username=?", (username,))
        res_fetch= cursor.fetchone()
        res= res_fetch[0]
        # Cerrar conexion
        conex.commit()
        conex.close()
        # Devolver res
        return res

# Función para cambiar la contraseña de un usuario
    def set_email(new_email, username):
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        # Obtenerlo
        cursor.execute("UPDATE usuarios SET email=? WHERE username=?", (new_email, username))
        # Cerrar conexion
        conex.commit()
        conex.close()

    # Comprobar que el username y la contraseña son correctos
    def inicio_ok(username, pwd):
        # Comprobar que el usuario existe
        if not Usuario.username_existe(username):
            return False, "No existe ninguna cuenta con ese nombre de usuario"
        else:
            if (pwd==Usuario.get_pwd(username)):
                return True, ""
            else:
                return False, "Contraseña incorrecta"
            
    # Mandar correo con código de validación
    def mandar_email(email):
        res=""
        # Código, nº random
        codigo= f"{random.randint(1000, 9999)}"
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        # Creamos mensaje
        msg = MIMEMultipart()
        msg["From"] = "perfil.estrategiapp@gmail.com.com"
        msg["To"] = email
        msg["Subject"] = "Perfil EstrategIApp - Código de Verificación"
        msg.attach(MIMEText(f"Tu código de verificación es: {codigo}", "plain"))

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login("perfil.estrategiapp@gmail.com", "kewl dsej snoe bgbo")
                server.send_message(msg)
                res= True
        except Exception as e:
            res= False
        return res, codigo
    
    # Comprobar que el email sea correcto
    def email_ok(email):
        if Usuario.email_existe(email):
            return False, "Este correo electrónico ya está en uso por un usuario"
        else:
            if not re.search(r"@gmail\.com$", email):
                return False, "Correo incorrecto, debe ser un correo de gmail (@gmail.com)"
            else: 
                return True, ""

    # Mandar contraseña nueva al correo
    def mandar_pwd(email):
        pwd = "".join(
                [
                    random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),  # 1 mayúscula
                    random.choice("1234567890"),  # 1 número
                    "".join(
                        random.choice(
                            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                        )
                        for _ in range(4)
                    ),  # 4 caracteres aleatorios
                ]
            )
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        # Creamos mensaje
        msg = MIMEMultipart()
        msg["From"] = "perfil.estrategiapp@gmail.com"
        msg["To"] = email
        msg["Subject"] = "Perfil EstrategIApp - Nueva Contraseña"
        msg.attach(MIMEText(f"""
Tu nueva contraseña es: {pwd}

No olvides tu usuario para iniciar sesión: {Usuario.get_username(email)}
Recuerda que puedes cambiar tu contraseña en ajustes.
""", "plain"))
        # Lo mandamos
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login("perfil.estrategiapp@gmail.com", "kewl dsej snoe bgbo")
                server.send_message(msg)
                res= True
        except Exception as e:
            res= False
        # Sustituimos la contraseña por la generada
        Usuario.set_pwd_email(pwd, email)
        return res, pwd





    # AUX PARA VER USERS
    def ver_db():
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()
        cursor.execute("SELECT * FROM usuarios")
        users = cursor.fetchall()
        for u in users:
            username, pwd, email = u
            print(f"Username: {username}")
            print(f"Contraseña: {pwd}")
            print(f"Email: {email}")
        # Cerrar conexión
        conex.commit()
        conex.close()

    # AUX PARA BORRAR USUARIOS
    def borrar_users():
        # Conectar con la db
        conex= sqlite3.connect(DB_PATH)
        cursor= conex.cursor()        
        # Vaciar
        cursor.execute("DELETE FROM usuarios")
        # Cerrar conexion
        conex.commit()
        conex.close()
