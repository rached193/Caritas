__author__ = 'Aron'

from Tkinter import Tk, BOTH,RIGHT ,LEFT, LabelFrame,TRUE, FALSE,Toplevel,StringVar, Spinbox, END
from ttk import Frame, Button, Style, Label, Entry, Combobox
from tkintertable import TableCanvas, TableModel
import mysql.connector
from mysql.connector import errorcode
import fpdf

class Example(Frame):
    counter = 0

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent

        self.initUI()

    def nuevoVoluntario(self, nombre, apellidos, dni, direccion, correo_electronico, localidad_id, estudio_id,
                        parroquial_id, proyecto_id, telefono_1, telefono_2, genero, fecha_nacimiento,t,estado,id):
        global cnx
        cursor = cnx.cursor()
        if estado:
            query = (
                "INSERT INTO caritas.voluntario (nombre, apellidos, dni, direccion, correo_electronico, localidad_id, estudio_id, parroquial_id, proyecto_id, telefono_1, telefono_2, genero, fecha_nacimiento) VALUES ('%s','%s','%s','%s','%s','%d','%d','%d','%d','%s','%s','%s','%s')" % (
                    nombre, apellidos, dni, direccion, correo_electronico, localidad_id, estudio_id, parroquial_id,
                    proyecto_id,
                    telefono_1, telefono_2, genero, fecha_nacimiento))
        else:
            query = (
                "UPDATE caritas.voluntario SET nombre = ('%s'), apellidos = ('%s'), dni = ('%s'), direccion = ('%s'), correo_electronico = ('%s'), localidad_id = ('%d'), estudio_id = ('%d'), parroquial_id = ('%d'),proyecto_id = ('%d'), telefono_1 = ('%s'), telefono_2 = ('%s'), genero = ('%s'), fecha_nacimiento = ('%s') WHERE id = ('%d')"
                % ( nombre, apellidos, dni, direccion, correo_electronico, localidad_id, estudio_id, parroquial_id,proyecto_id, telefono_1, telefono_2, genero, fecha_nacimiento,id))
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        t.destroy()

    def getEstudios(self):
        global cnx
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM estudio e")
        cursor.execute(query)
        valores = []
        strings = []
        for row in cursor:
            valores.append(row['id'])
            strings.append(row['nombre'])

        cursor.close()
        self.listadoEstudios = [strings, valores]

    def getParroquial(self):
        global cnx
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM parroquial e")
        cursor.execute(query)
        valores = []
        strings = []
        for row in cursor:
            valores.append(row['id'])
            strings.append(row['nombre'])

        cursor.close()
        self.listadoParroquial = [strings, valores]

    def getPais(self):
        global cnx
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM pais e")
        cursor.execute(query)
        valores = []
        strings = []
        for row in cursor:
            valores.append(row['id'])
            strings.append(row['nombre'])

        cursor.close()
        self.listadoPais = [strings, valores]

    def nuevoEstudio(self):
        t = Toplevel(self)
        t.wm_title("Estudio")

        Label(t, text="Nombre").grid(row=0, column=1)
        E2 = Entry(t)
        E2.grid(row=1, column=1)

        button1 = Button(t, text="Cancelar", command=lambda: t.destroy())
        button2 = Button(t, text="Guardar", command=lambda: self.nuevaEntradaEstudios(E2.get(), t))
        button3 = Button(t, text="Borrar", command=lambda: self.BorrarEstudios(E2.get(), t))
        button3.config(state="disabled")

        button1.grid(row=2, column=0)
        button2.grid(row=2, column=1)
        button3.grid(row=2, column=2)

    def nuevoPais(self):
        t = Toplevel(self)
        t.wm_title("Pais")

        Label(t, text="Nombre").grid(row=0, column=1)
        E2 = Entry(t)
        E2.grid(row=1, column=1)

        button1 = Button(t, text="Cancelar", command=lambda: t.destroy())
        button2 = Button(t, text="Guardar", command=lambda: self.nuevaEntradaPais(E2.get(), t))
        button3 = Button(t, text="Borrar", command=lambda: self.BorrarPais(E2.get(), t))
        button3.config(state="disabled")

        button1.grid(row=2, column=0)
        button2.grid(row=2, column=1)
        button3.grid(row=2, column=2)

    def nuevaParroquia(self):
        t = Toplevel(self)
        t.wm_title("Parroquial")

        Label(t, text="Nombre").grid(row=0, column=1)
        E2 = Entry(t)
        E2.grid(row=1, column=1)

        button1 = Button(t, text="Cancelar", command=lambda: t.destroy())
        button2 = Button(t, text="Guardar", command=lambda: self.nuevaEntradaParroquia(E2.get(), t))
        button3 = Button(t, text="Borrar", command=lambda: self.BorrarParroquial(E2.get(), t))
        button3.config(state="disabled")

        button1.grid(row=2, column=0)
        button2.grid(row=2, column=1)
        button3.grid(row=2, column=2)

    def editarEstudio(self):
        t = Toplevel(self)
        t.wm_title("Estudio")

        Label(t, text="Nombre").grid(row=0, column=1)
        E2 = Entry(t)
        E2.insert(END, self.selectorEstudios.get())
        E2.grid(row=1, column=1)

        nombreOld = self.selectorEstudios.get()


        button1 = Button(t, text="Cancelar", command=lambda: t.destroy())
        button2 = Button(t, text="Guardar", command=lambda: self.actualizarEstudio(nombreOld, E2.get(), t))
        button3 = Button(t, text="Borrar", command=lambda: self.BorrarEstudios(E2.get(), t))

        button1.grid(row=2, column=0)
        button2.grid(row=2, column=1)
        button3.grid(row=2, column=2)

    def editarPais(self):
        t = Toplevel(self)
        t.wm_title("Pais")

        Label(t, text="Nombre").grid(row=0, column=1)
        E2 = Entry(t)
        E2.insert(END, self.selectorPais.get())
        E2.grid(row=1, column=1)

        nombreOld = self.selectorPais.get()

        button1 = Button(t, text="Cancelar", command=lambda: t.destroy())
        button2 = Button(t, text="Guardar", command=lambda: self.actualizarPais(nombreOld, E2.get(), t))
        button3 = Button(t, text="Borrar", command=lambda: self.BorrarPais(E2.get(), t))

        button1.grid(row=2, column=0)
        button2.grid(row=2, column=1)
        button3.grid(row=2, column=2)

    def editarParroquia(self):
        t = Toplevel(self)
        t.wm_title("Estudio")

        Label(t, text="Nombre").grid(row=0, column=1)
        E2 = Entry(t)
        E2.insert(END, self.selectorParroquial.get())
        E2.grid(row=1, column=1)

        nombreOld = self.selectorParroquial.get()

        button1 = Button(t, text="Cancelar", command=lambda: t.destroy())
        button2 = Button(t, text="Guardar", command=lambda: self.actualizarParroquia(nombreOld, E2.get(), t))
        button3 = Button(t, text="Borrar", command=lambda: self.BorrarParroquial(E2.get(), t))

        button1.grid(row=2, column=0)
        button2.grid(row=2, column=1)
        button3.grid(row=2, column=2)

    def actualizarPais(self, nombreOld, nombreN, t):
        global cnx
        cursor = cnx.cursor()
        query = ("UPDATE caritas.pais SET nombre= ('%s') WHERE nombre = ('%s')" % (nombreN, nombreOld))
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        self.getPais()
        self.selectorPais['values'] = self.listadoPais[0]

        t.destroy()

    def actualizarEstudio(self, nombreOld, nombreN, t):
        global cnx
        cursor = cnx.cursor()
        query = ("UPDATE caritas.estudio SET nombre= ('%s') WHERE nombre = ('%s')" % (nombreN, nombreOld))
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        self.getEstudios()
        self.selectorEstudios['values'] = self.listadoEstudios[0]

        t.destroy()

    def actualizarParroquia(self, nombreOld, nombreN, t):
        global cnx
        cursor = cnx.cursor()
        query = ("UPDATE caritas.parroquial SET nombre= ('%s') WHERE nombre = ('%s')" % (nombreN, nombreOld))
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        self.getParroquial()
        self.selectorParroquial['values'] = self.listadoParroquial[0]

        t.destroy()

    def BorrarEstudios(self, nombre, t):
        global cnx
        cursor = cnx.cursor()
        query = ("DELETE FROM caritas.estudio WHERE nombre = ('%s')" % nombre)
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        self.getEstudios()
        self.selectorEstudios['values'] = self.listadoEstudios[0]

        t.destroy()

    def BorrarPais(self, nombre, t):
        global cnx
        cursor = cnx.cursor()
        query = ("DELETE FROM caritas.pais WHERE nombre = ('%s')" % nombre)
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        self.getPais()
        self.selectorPais['values'] = self.listadoPais[0]

        t.destroy()

    def BorrarParroquial(self, nombre, t):
        global cnx
        cursor = cnx.cursor()
        query = ("DELETE FROM caritas.parroquial WHERE nombre = ('%s')" % nombre)
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        self.getParroquial()
        self.selectorParroquial['values'] = self.listadoParroquial[0]

        t.destroy()

    def nuevaEntradaEstudios(self, nombre, t):
        global cnx
        cursor = cnx.cursor()
        query = ("INSERT INTO caritas.estudio (nombre) VALUE ('%s')" % nombre)
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        self.getEstudios()
        self.selectorEstudios['values'] = self.listadoEstudios[0]

        t.destroy()

    def nuevaEntradaPais(self, nombre, t):
        global cnx
        cursor = cnx.cursor()
        query = ("INSERT INTO caritas.pais (nombre) VALUE ('%s')" % nombre)
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        self.getPais()
        self.selectorPais['values'] = self.listadoPais[0]

        t.destroy()

    def nuevaEntradaParroquia(self, nombre, t):
        global cnx
        cursor = cnx.cursor()
        query = ("INSERT INTO caritas.parroquial (nombre) VALUE ('%s')" % nombre)
        cursor.execute(query)
        cnx.commit()
        cursor.close()

        self.getParroquial()
        self.selectorParroquial['values'] = self.listadoParroquial[0]

        t.destroy()

    def ventanaVoluntarios(self,row):

        id = -1
        guardar = TRUE
        # Creamos una ventana nueva
        t = Toplevel(self)
        t.wm_title("Crear Voluntario")

        # Etiqueta y entrada de nombre
        Label(t, text="Nombre").grid(row=0)
        entradaNombre = Entry(t)
        entradaNombre.grid(row=0, column=1,sticky = "ew")

        # Etiqueta y entrada de apellidos
        Label(t, text="Apellidos").grid(row=1)
        entradaApellidos = Entry(t)
        entradaApellidos.grid(row=1, column=1,sticky = "ew")

        # Etiqueta y entrada de DNI
        Label(t, text="DNI").grid(row=2)
        entradaDNI = Entry(t)
        entradaDNI.grid(row=2, column=1,sticky = "ew")

        # Etiqueta y entrada de Dirreccion
        Label(t, text="Direccion").grid(row=3)
        entradaDireccion = Entry(t)
        entradaDireccion.grid(row=3, column=1)

        # Etiqueta y seleccion de Estudios
        Label(t, text="Estudios").grid(row=4)
        box_value = StringVar()
        self.getEstudios()
        self.selectorEstudios = Combobox(t, textvariable=box_value, state='readonly')
        self.selectorEstudios['values'] = self.listadoEstudios[0]
        self.selectorEstudios.configure(width=25)
        self.selectorEstudios.current(0)
        self.selectorEstudios.grid(row=4, column=1)

        botonEditarEstudios = Button(t, text="Editar", command=self.editarEstudio)
        botonNuevosEstudios = Button(t, text="Nuevo", command=self.nuevoEstudio)
        botonEditarEstudios.grid(row=4, column=2)
        botonNuevosEstudios.grid(row=4, column=3)

        # Etiqueta y seleccion de Genero
        Label(t, text="Genero").grid(row=5)
        seleccionGenero = Combobox(t, values=["Masculino (M)", "Femenino (F)"], state='readonly')
        seleccionGenero.grid(row=5, column=1)

        # Etiqueta y seleccion de Parroquial
        Label(t, text="Parroquial").grid(row=6)
        box_value = StringVar()
        self.getParroquial()
        self.selectorParroquial = Combobox(t, textvariable=box_value, state='readonly')
        self.selectorParroquial['values'] = self.listadoParroquial[0]
        self.selectorParroquial.configure(width=25)
        self.selectorParroquial.current(0)
        self.selectorParroquial.grid(row=6, column=1)

        botonEditarParroquial = Button(t, text="Editar", command=self.editarParroquia)
        botonNuevaParroqual = Button(t, text="Nuevo", command=self.nuevaParroquia)
        botonEditarParroquial.grid(row=6, column=2)
        botonNuevaParroqual.grid(row=6, column=3)

        # Etiqueta y seleccion de Correo
        Label(t, text="Correo").grid(row=0, column=4)
        entradaCorreo = Entry(t)
        entradaCorreo.grid(row=0, column=5)

        Label(t, text="Telefono 1").grid(row=1, column=4)
        entradaTelefono1 = Entry(t)
        entradaTelefono1.grid(row=1, column=5)

        Label(t, text="Telefono 2").grid(row=2, column=4)
        entradaTelefono2 = Entry(t)
        entradaTelefono2.grid(row=2, column=5)

        # Etiqueta y entrada de Fecha
        Label(t, text="Fecha").grid(row=3, column=4)
        entradaAno = Entry(t)
        entradaMes = Entry(t)
        entradaDia = Entry(t)
        entradaAno.grid(row=3, column=5)
        entradaMes.grid(row=3, column=6)
        entradaDia.grid(row=3, column=7)

        # Etiqueta y seleccion de Pais
        Label(t, text="Pais").grid(row=4, column=4)
        box_value = StringVar()
        self.getPais()
        self.selectorPais = Combobox(t, textvariable=box_value, state='readonly')
        self.selectorPais['values'] = self.listadoPais[0]
        self.selectorPais.configure(width=25)
        self.selectorPais.current(0)
        self.selectorPais.grid(row=4, column=5)

        botonEditarPais = Button(t, text="Editar", command=self.editarPais)
        botonNuevaPais = Button(t, text="Nuevo", command=self.nuevoPais)
        botonEditarPais.grid(row=4, column=6)
        botonNuevaPais.grid(row=4, column=7)

        #Rellenamos los cambos si estamos editando
        if row > -1:
            voluntario = self.table.model.getRecordAtRow(row)
            entradaNombre.insert(END,voluntario['nombre'])
            entradaApellidos.insert(END,voluntario['apellidos'])
            entradaCorreo.insert(END,voluntario['correo_electronico'])
            entradaTelefono1.insert(END,voluntario['telefono_1'])
            entradaTelefono2.insert(END,voluntario['telefono_2'])
            entradaDireccion.insert(END,voluntario['direccion'])
            entradaDNI.insert(END,voluntario['dni'])
            self.selectorEstudios.set(voluntario['estudio'])
            self.selectorParroquial.set(voluntario['parroquial'])
            guardar = FALSE
            id = voluntario['id']





        button5 = Button(t, text="Guardar", command=lambda: self.nuevoVoluntario(entradaNombre.get(),
                                                                                 entradaApellidos.get(),entradaDNI.get(),entradaDireccion.get(),
                                                                                 entradaCorreo.get(),1,self.listadoEstudios[1][self.selectorEstudios.current()],
                                                                                 self.listadoParroquial[1][self.selectorParroquial.current()],
                                                                                 1,entradaTelefono1.get(),entradaTelefono2.get(),"M","2001-01-01",t,guardar,id))
        button6 = Button(t, text="Cancelar", command=t.destroy)

        button5.grid(row=7, column=4)
        button6.grid(row=7, column=5)


    def validarVoluntario(self, nombre, apellidos, dni, direccion, correo_electronico, localidad_id, estudio_id,
                        parroquial_id, proyecto_id, telefono_1, telefono_2, genero, fecha_nacimiento,t,estado,id):

        guarda = True
        error = ""

        if len(nombre)<3 :
            error = error + "Nombre debe tener mas de 2 caracteres\n"
            guarda = False

        if len(apellidos)<3 :
            error = error + "Apellidos debe tener mas de 2 caracteres\n"
            guarda = False
            17764662

        if len(dni)==9 and dni[8].isalpha() and dni[0-7].isdigit():
            error = error + "Dni tiene el formato NNNNNNNNX donde N es un digito y X una letra \n"
            guarda = False

        if len(telefono_1)==0:
            telefono_1=0

        if len(telefono_1)==0:
            telefono_1=0

        if guarda:self.nuevoVoluntario(nombre, apellidos, dni, direccion, correo_electronico, localidad_id, estudio_id,
                        parroquial_id, proyecto_id, telefono_1, telefono_2, genero, fecha_nacimiento,t,estado,id)




    def ventanaImprimir(self):
        t = Toplevel(self)
        t.wm_title("Imprimir")

        Label(t, text="Numero de Copias por etiqueta").pack()
        w = Spinbox(t, from_=1, to=10)
        w.pack()

        buttonImprimir = Button(t, text="Imprimir",  command=lambda:self.imprimir(int(w.get()),t))
        buttonImprimir.pack()

    def agregarListado(self,numero):
        voluntario = self.table.model.getRecordAtRow(numero)
        modelNuevo = TableModel()

        modelNuevo.addColumn("nombre")
        modelNuevo.addColumn("apellidos")
        modelNuevo.addColumn("dni")
        modelNuevo.addColumn("direccion")
        modelNuevo.addColumn("correo_electronico")
        modelNuevo.addColumn("estudio")
        modelNuevo.addColumn("parroquial")
        modelNuevo.addColumn("proyecto")
        modelNuevo.addColumn("genero")
        modelNuevo.addColumn("fecha_nacimiento")
        modelNuevo.addColumn("telefono_1")
        modelNuevo.addColumn("telefono_2")

        arrayListado = self.selectTable.getModel().data
        valores = {}
        i=1
        for values in arrayListado:
            valores['row',i]=arrayListado['row',i]
            i+=1
        valores['row',i]=voluntario
        modelNuevo.importDict(valores)

        self.selectTable.updateModel(modelNuevo)
        self.selectTable.redrawTable()

    def quitarListado(self,numero):
        voluntario = self.selectTable.model.getRecordAtRow(numero)
        modelNuevo = TableModel()

        modelNuevo.addColumn("nombre")
        modelNuevo.addColumn("apellidos")
        modelNuevo.addColumn("dni")
        modelNuevo.addColumn("direccion")
        modelNuevo.addColumn("correo_electronico")
        modelNuevo.addColumn("estudio")
        modelNuevo.addColumn("parroquial")
        modelNuevo.addColumn("proyecto")
        modelNuevo.addColumn("genero")
        modelNuevo.addColumn("fecha_nacimiento")
        modelNuevo.addColumn("telefono_1")
        modelNuevo.addColumn("telefono_2")

        print numero

        arrayListado = self.selectTable.getModel().data
        valores = {}
        i=1
        for values in arrayListado:
            if numero+1 != i:
                valores['row',i]=arrayListado['row',i]
            i+=1
        modelNuevo.importDict(valores)

        self.selectTable.updateModel(modelNuevo)
        self.selectTable.redrawTable()

    def imprimir(self,numero,label):
        pdf = fpdf.FPDF(format='letter')
        pdf.add_page()
        pdf.set_font("Arial", size=14)

        indice=1
        columna=1
        fila=0
        p=0
        for ficha in self.listadoSeleccionado:
            row = self.listadoSeleccionado['row',indice]
            for x in range(0, numero):
                if p==9:
                    pdf.add_page()
                    p=0
                else:
                    p+=1

                texto = 'Nombre: %s\nApellidos: %s\nDireccion: %s\nTelefono: %s' %(row["nombre"],row["apellidos"],row["direccion"],row["telefono_1"])
                pdf.multi_cell(65, 10,texto,align='C')
                pdf.set_xy(70*columna,60*fila +10)
                columna = columna + 1
                if columna == 4:
                    columna=1
                    fila=fila+1
                    pdf.set_xy(10,60*fila +10)

            indice = indice + 1
        pdf.output("tutorial.pdf")

        label.destroy()

    def buscar(self,nombre,apellidos):

        modelCompleto = TableModel()
        modelNuevo = TableModel()

        modelNuevo.addColumn("nombre")
        modelNuevo.addColumn("apellidos")
        modelNuevo.addColumn("dni")
        modelNuevo.addColumn("direccion")
        modelNuevo.addColumn("correo_electronico")
        modelNuevo.addColumn("estudio")
        modelNuevo.addColumn("parroquial")
        modelNuevo.addColumn("proyecto")
        modelNuevo.addColumn("genero")
        modelNuevo.addColumn("fecha_nacimiento")
        modelNuevo.addColumn("telefono_1")
        modelNuevo.addColumn("telefono_2")

        self.listilla= queryAllVoluntarios()
        modelCompleto.importDict(self.listilla)
        searchterms = [('nombre', nombre, 'contains', 'AND'),('apellidos', apellidos, 'contains', 'AND')]
        result=modelCompleto.getDict(modelCompleto.columnNames, filters=searchterms)
        modelNuevo.importDict(result)
        self.listadoSeleccionado = result
        self.table.updateModel(modelNuevo)
        self.table.redrawTable()

    def eventoClic(self):
        print "Clicado"
        return


    def initUI(self):

        self.parent.title("Caritas")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        frameMenu = Frame(self)
        frameMenu.pack(fill="both", expand="0", side=RIGHT)

        labelBusqueda = LabelFrame(frameMenu, text="Busqueda")
        labelBusqueda.pack(fill="x",expand =1)

        labelVoluntarios = LabelFrame(frameMenu)
        labelVoluntarios.pack(fill="both",expand =0)

        frameTabla = Frame(self)
        frameTabla.pack(fill="both", expand="1", side=LEFT)

        labelTabla = LabelFrame(frameTabla)
        labelTabla.pack(fill="both", expand="1")

        labelBotonera = LabelFrame(frameTabla)
        labelTabla.pack(fill="both", expand="1")

        labelSelect = LabelFrame(frameTabla)
        labelSelect.pack(fill="both", expand="1")

        model = TableModel()
        modelSelect = TableModel()

        model.addColumn("nombre")
        model.addColumn("apellidos")
        model.addColumn("dni")
        model.addColumn("direccion")
        model.addColumn("correo_electronico")
        model.addColumn("estudio")
        model.addColumn("parroquial")
        model.addColumn("proyecto")
        model.addColumn("genero")
        model.addColumn("fecha_nacimiento")
        model.addColumn("telefono_1")
        model.addColumn("telefono_2")

        modelSelect.addColumn("nombre")
        modelSelect.addColumn("apellidos")
        modelSelect.addColumn("dni")
        modelSelect.addColumn("direccion")
        modelSelect.addColumn("correo_electronico")
        modelSelect.addColumn("estudio")
        modelSelect.addColumn("parroquial")
        modelSelect.addColumn("proyecto")
        modelSelect.addColumn("genero")
        modelSelect.addColumn("fecha_nacimiento")
        modelSelect.addColumn("telefono_1")
        modelSelect.addColumn("telefono_2")

        #Tabla Voluntarios
        self.listilla= queryAllVoluntarios()
        model.importDict(self.listilla)
        self.table = TableCanvas(labelTabla, model=model,editable=False)
        self.table.createTableFrame()
        self.table.handle_double_click(self.eventoClic)

        #Tabla Seleccionados
        self.selectTable = TableCanvas(labelSelect, model=modelSelect,editable=False)
        self.selectTable.createTableFrame()
        self.listadoSeleccionado = []

        L1 = Label(labelBusqueda, text="Nombre")
        L1.pack()
        E1 = Entry(labelBusqueda)
        E1.pack()

        L2 = Label(labelBusqueda, text="Apellidos")
        L2.pack()
        E2 = Entry(labelBusqueda)
        E2.pack()

        botonArriba = Button(labelVoluntarios, text="Agregar al listado",  command=lambda:self.agregarListado(self.table.getSelectedRow()))
        botonArriba.pack()
        botonAbajo = Button(labelVoluntarios, text="Quitar del listado",  command=lambda:self.quitarListado(self.selectTable.getSelectedRow()))
        botonAbajo.pack()

        button = Button(labelBusqueda, text="Buscar", command=lambda: self.buscar(E1.get(),E2.get()))
        button.pack()

        button = Button(labelVoluntarios, text="Nuevo Voluntario",  command=lambda:self.ventanaVoluntarios(-1))
        button.pack()

        buttonEditar = Button(labelVoluntarios, text="Editar Voluntario",  command=lambda:self.ventanaVoluntarios(self.table.getSelectedRow()))
        buttonEditar.pack()

        buttonImprimir = Button(labelVoluntarios, text="Imprimir",  command=lambda:self.ventanaImprimir())
        buttonImprimir.pack()





def conectar():
    global cnx
    try:
        cnx = mysql.connector.connect(user='root', password='admin',
                                      host='127.0.0.1',
                                      database='caritas')

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        return cnx


def queryAllVoluntarios():
    global cnx
    cursor = cnx.cursor(dictionary=True)
    #query = ("SELECT * FROM voluntario v")
    query = ("""SELECT v.id, v.nombre,v.apellidos,v.dni,v.direccion,v.correo_electronico,e.nombre as estudio,
          p.nombre as parroquial, pr.nombre as proyecto, v.telefono_1,v.telefono_2,v.genero,v.fecha_nacimiento
          FROM voluntario v
           JOIN estudio e
            ON v.estudio_id = e.id
           JOIN parroquial p
            ON v.parroquial_id = p.id
           JOIN parroquial pr
            ON v.proyecto_id = pr.id
""")


    cursor.execute(query)
    valores = {}
    i = 0
    for voluntario in cursor:
        i+=1
        voluntario['fecha_nacimiento'] = str(voluntario['fecha_nacimiento'])
        valores['row',i]=voluntario
        #valores['row',i]={'nombre':voluntario['nombre'],'apellidos':voluntario['apellidos'],'estudio':voluntario['estudio']}

    cursor.close()
    return valores


def main():
    global cnx
    root = Tk()
    root.geometry("900x600+100+100")
    cnx = conectar()
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
