#!/usr/bin/python
# -*- coding: utf-8 -*-

from gi.repository import Gtk
import os, MySQLdb, string
os.system("clear")

# Establecemos la conexión (misma bd que la primera actividad)
Conexion = MySQLdb.connect(host='localhost', user='conan',passwd='crom', db='DBdeConan')

# Creamos el cursor
micursor = Conexion.cursor()

# LA SIGUIENTE FUNCIÓN GUARDA LOS DATOS EN UN VECTOR. CADA COMPONENTE SERÁ UNA TUPLA CORRESPONDIENTE A CADA FILA DE LA TABLA CON LA QUE 
# SE TRABAJE ('Datos' EN ESTE CASO)
def registros(query="SELECT * FROM Datos;"):
	micursor.execute(query)
	nuevoreg=micursor.fetchone()
	registros=[]
	
	while nuevoreg!=None:
		registros.append(nuevoreg)
		nuevoreg=micursor.fetchone()
	return registros


# LA SIGUIENTE FUNCIÓN REASIGNA LOS IDENTIFICADORES APROPIADOS A LOS DATOS DE LA TABLA CUANDO SE ELIMINE ALGUNO. ESTO EVITARÁ QUE SI SE 
# CREAN DATOS NUEVOS SE REPITAN LOS IDENTIFICADORES
def reidentificar():
	registro=registros()
	ide=[]
	for i in range(len(registro)):
		ide.append(str(registro[i][0]))
	for i in range(len(registro)):
		query="UPDATE Datos SET id="+"\""+str(i+1)+"\" WHERE id="+"\""+ide[i]+"\";"
		micursor.execute(query)
		registro=registros()
	return registro


# LA SIGUIENTE FUNCIÓN SERÁ USADA PARA OBTENER LOS VALORES DEL COMBOBOX. SEGÚN HE LEÍDO EN 
#http://www.pygtk.org/pygtk2tutorial-es/sec-ComboBoxAndComboboxEntry.html
#PARECE QUE NO HAY UN MÉTODO DIRECTO PARA OBTENER VALORES DEL COMBOBOX'''
def get_active_text(combobox):
	model = combobox.get_model()
	active = combobox.get_active()
	if active < 0:
		return 'No especificado'
	return model[active][0]

# CON ESTA FUNCIÓN SE IMPRIMIRÁN LOS VALORES DE LA TABLA ADECUADAMENTE
def imprime_registros(query,x):
	registro=registros(query)
	for j in range(len(x)):
		txt=''
		for i in range(len(registro)):
			txt=txt+str(registro[i][j])+"\n"
		x[j].get_buffer().set_text(txt)

# ESTA FUNCIÓN SE USA PARA QUE LOS VALORES SE BORREN CADA VEZ QUE SE REALIZA UNA ACCIÓN
# LA CONDICIÓN if i==x[4] SE TRATA A PARTE YA QUE CORRESPONDERÁ AL COMBOBOX, QUE NO TIENE EL METODO set_text
def valores_en_blanco(x):
	for i in x:
		if i==x[5]:
			i.set_active(-1)
		else:
			i.set_text('')

################################################################################
def detecta_numero(x):
	if x!='None':
		for i in x:
			if i not in string.digits:
				return ''
			else:
				return x
	else:
		return 'None'
################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

class Handler:
	builder=None
	def __init__(self):
		# Iniciamos el GtkBuilder para tirar del fichero de glade
		self.builder = Gtk.Builder()
		self.builder.add_from_file("interfaz.glade")
		self.handlers = {
			"onDeleteWindow": self.onDeleteWindow,
			"display_crear": self.display_crear,
			"display_obtener": self.display_obtener,
			"display_actualizar": self.display_actualizar,
			"display_borrar": self.display_borrar,
			"display_salir": self.display_salir,
			"display_about": self.display_about,
			"on_btn1_clicked": self.on_btn1_clicked,
			"onCloseAboutDialog": self.onCloseAboutDialog,
			"continuar" : self.continuar
		}

		# Conectamos las señales e iniciamos la aplicación
		self.builder.connect_signals(self.handlers)
		self.window = self.builder.get_object("window1")
		self.about = self.builder.get_object("aboutdialog1")
		self.campos=[]
		for i in range(6):
			self.campos.append(self.builder.get_object("textview%s" % str(i+1)))
		self.warning = self.builder.get_object("messagedialog1")
		self.entradas=[]
		for i in range(1,6):
			self.entradas.append(self.builder.get_object("entry%s" % str(i)))
		self.entradas.append(self.builder.get_object("combobox1"))
		self.window.show_all()
		self.window.resize(600,600)	


##################################################################
	def onDeleteWindow(self, *args):
		Conexion.commit()
		Gtk.main_quit(*args)
##################################################################
	def display_crear(self,window):
		nuevos_datos=[str(self.entradas[0].get_text())]
		for i in range(1,5):
			nuevos_datos.append(str(self.entradas[i].get_text()))
		nuevos_datos.append(str(get_active_text(self.entradas[5])))

		n=len(registros())+1
		query="INSERT INTO Datos (id,Nombre,Apellido,Profesion,Nivel_de_estudios,Telefono) VALUES (\""+str(n)+"\",\""+nuevos_datos[1]+"\",\""+nuevos_datos[2]+"\",\""+nuevos_datos[3]+"\",\""+nuevos_datos[5]+"\",\""+nuevos_datos[4]+"\");"
		micursor.execute(query)
		valores_en_blanco(self.entradas)
		imprime_registros("SELECT * FROM Datos;",self.campos)
##################################################################
	def continuar(self,window):
		self.warning.hide()
##################################################################
	def display_obtener(self,window):
		query='SELECT * FROM Datos WHERE '
		camposnovacios=0
		variables=['id','Nombre','Apellido','Profesion','Nivel_de_estudios','Telefono']
		ide=detecta_numero(str(self.entradas[0].get_text()))
		if str(ide) not in ['','None']:
			camposnovacios+=1
			string=variables[0]+' = \"'+str(ide)+'\" AND '
			query+=string
		for i in range(1,5):
			if str(self.entradas[i].get_text())!='':
				camposnovacios+=1
				string=variables[i]+' = \"'+self.entradas[i].get_text()+'\" AND '
				query+=string

		if str(get_active_text(self.entradas[5]))!='No especificado':
				camposnovacios+=1
				string=variables[i]+' = \"'+str(get_active_text(self.entradas[5]))+'\" AND '
				query+=string

		if camposnovacios==0:
			query='SELECT * FROM Datos     '
		query=query[0:len(query)-5]+';'
		print "LA ORDEN DE SQL SOLICITADA ES\n\n"+query+"\n"
		
		imprime_registros(query,self.campos)
		valores_en_blanco(self.entradas)
##################################################################
	def display_actualizar(self,window):
		nuevos_datos=[]
		for i in range(5):
			nuevos_datos.append(str(self.entradas[i].get_text()))
		nuevos_datos.append(str(get_active_text(self.entradas[5])))
		query="UPDATE Datos SET "
		camposnovacios=0
		variables=['id','Nombre','Apellido','Profesion','Telefono','Nivel_de_estudios']
		for i in range(1,5):
			if str(self.entradas[i].get_text())!='':
				query+=variables[i]+"=\""+str(self.entradas[i].get_text())+"\" , "
		if str(get_active_text(self.entradas[5]))!='No especificado':
			query+=variables[5]+"=\""+str(get_active_text(self.entradas[5]))+"\" , "

		query=query[0:len(query)-2]+"WHERE id = "+nuevos_datos[0]+";"
		print query

		if str(nuevos_datos[0]) in ['','None']:
			self.warning.show()
		else:			
			micursor.execute(query)

		valores_en_blanco(self.entradas)
		imprime_registros("SELECT * FROM Datos;",self.campos)
##################################################################
	def display_borrar(self,window):
		ide=detecta_numero(str(self.entradas[0].get_text()))
		if str(ide) not in ['','None']:
			query="DELETE FROM Datos WHERE id="+str(ide)+";"
			micursor.execute(query)
			reidentificar()#Cuando se borra un registro automáticamente se reasignan los ids
		valores_en_blanco(self.entradas)
		imprime_registros("SELECT * FROM Datos;",self.campos)
##################################################################
	def display_salir(self,*args):
		query="DROP TABLE Datos;"
		micursor.execute(query)
		Gtk.main_quit(*args)
##################################################################
	def on_btn1_clicked(self, window):
		imprime_registros("SELECT * FROM Datos;",self.campos)
##################################################################
	def display_about(self,window):
		self.about.show()
##################################################################
	def onCloseAboutDialog(self,window,data=None):
		self.about.hide()

##################################################################
##################################################################
##################################################################

def main():
	window = Handler()
	Gtk.main()
	return 0

if __name__ == '__main__':
	main()
