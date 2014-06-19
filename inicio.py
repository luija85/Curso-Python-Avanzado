#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb

# Establecemos la conexión (misma bd que la primera actividad)
Conexion = MySQLdb.connect(host='localhost', user='conan',passwd='crom', db='DBdeConan')

# Creamos el cursor
micursor = Conexion.cursor()

# Se crea la tabla 'Datos':
query="CREATE TABLE Datos (id INT, Nombre VARCHAR(100),Apellido VARCHAR(100),Profesion VARCHAR(100),Nivel_de_estudios VARCHAR(100),Telefono VARCHAR(9));"
micursor.execute(query)


# Ejecutamos 5 insert por medio de variables, creando los 5 registros
q1="INSERT INTO Datos (id,Nombre,Apellido,Profesion,Nivel_de_estudios,Telefono) VALUES (1, \"Antonio\",\"Jiménez\",\"Banquero\",\"Superior\",\"675131467\");"
q2="INSERT INTO Datos (id,Nombre,Apellido,Profesion,Nivel_de_estudios,Telefono) VALUES (2, \"Francisca\",\"Rodríguez\",\"Ama de casa\",\"Medio\",\"672896741\");"
q3="INSERT INTO Datos (id,Nombre,Apellido,Profesion,Nivel_de_estudios,Telefono) VALUES (3, \"Manuel\",\"Fuentes\",\"Carpintero\",\"Bajo\",\"689125784\");"
q4="INSERT INTO Datos (id,Nombre,Apellido,Profesion,Nivel_de_estudios,Telefono) VALUES (4, \"Javier\",\"Gómez\",\"Profesor\",\"Superior\",\"649217794\");"
q5="INSERT INTO Datos (id,Nombre,Apellido,Profesion,Nivel_de_estudios,Telefono) VALUES (5, \"Rosa\",\"Martín\",\"Peluquera\",\"Medio\",\"615525891\");"
micursor.execute(q1)
micursor.execute(q2)
micursor.execute(q3)
micursor.execute(q4)
micursor.execute(q5)

Conexion.commit()

