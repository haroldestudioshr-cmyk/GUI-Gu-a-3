import time
import os
import tkinter as tk
from archivo import impresion
from robot import robot


class Aplicacion:
    def __init__(self, root):
        # Ventana principal de la aplicacion.
        self.root = root
        self.root.geometry("500x600")
        self.root.title("Lab 3")
        self.root.configure(bg="#bfdcc3")

        # Intenta cargar el icono sin detener el programa si no existe.
        try:
            self.root.iconbitmap(default="mi_icono.ico")
        except Exception:
            try:
                self.root.iconbitmap("mi_icono.ico")
            except Exception:
                pass

        # Las impresiones se guardan como objetos de la clase impresion.
        self.pila_impresiones = []
        self.opcion_impresion = tk.IntVar(value=1)

        # Cada pagina es un Frame distinto de la ventana.
        self.pagina1 = tk.Frame(self.root, bg="#bfdcc3")
        self.pagina2 = tk.Frame(self.root, bg="#bfdcc3")
        self.pagina3 = tk.Frame(self.root, bg="#bfdcc3")

        # Referencias a los controles que se actualizan despues de crearlos.
        self.panel_arriba = None
        self.panel_izq = None
        self.panel_der = None
        self.estado_impresion = None
        self.cola_label = None
        self.form_frame = None
        self.entrada_nombre = None
        self.entrada_hojas = None
        self.entrada_tiempo = None
        self.boton_quitar_primero = None
        self.boton_quitar_esp = None
        self.label_quitar_nombre = None
        self.entrada_quitar = None
        # Las acciones del robot se guardan como objetos de la clase robot.
        self.pila_robot = []
        self.accion_robot = tk.StringVar(value="")
        self.estado_robot = None
        self.lista_robot = None
        self.entrada_tiempo_robot = None
        self.boton_agregar_robot = None
        self.boton_ejecutar_robot = None
        self.robot_ejecutando = False

        # Construye las tres paginas y muestra primero la pagina de inicio.
        self.crear_ventana_inicio()
        self.crear_ventana_impresion()
        self.crear_ventana_robot()
        self.ir_a(self.pagina1)

    # Crea la pantalla inicial, muestra el logo y conecta cada boton con su pagina.
    def crear_ventana_inicio(self):
        tk.Label(self.pagina1, text="bienvenido a la aplicacion", font=("Arial", 20), bg="#bfdcc3").place(x=120, y=50)
        tk.Button(self.pagina1, text="impresion", font=("Arial", 12), bg="gray", command=self.cambiar_im).place(x=220, y=150, width=100, height=50)
        tk.Button(self.pagina1, text="robot", font=("Arial", 12), bg="gray", command=self.cambiar_ro).place(x=220, y=250, width=100, height=50)

        try:
            foto = tk.PhotoImage(file="umnges.png")
            tk.Label(self.pagina1, image=foto, bg="#bfdcc3").place(x=20, y=30)
            foto.image = foto
        except Exception:
            pass

    # Crea los controles de impresion, el formulario de documentos y el panel de la cola.
    def crear_ventana_impresion(self):
        self.panel_arriba = tk.Frame(self.pagina2, bg="#bfdcc3", width=450, height=110)
        self.panel_arriba.place(x=25, y=20)

        try:
            foto_impresora = tk.PhotoImage(file="impresora.png")
            tk.Label(self.panel_arriba, image=foto_impresora, bg="#bfdcc3").place(x=0, y=0)
            foto_impresora.image = foto_impresora
        except Exception:
            self.panel_arriba.configure(bg="gray")

        self.panel_izq = tk.Frame(self.pagina2, bg="#bfdcc3")
        self.panel_izq.place(x=20, y=180, width=180, height=320)

        tk.Radiobutton(self.panel_izq, text="imprimir", variable=self.opcion_impresion, value=1, command=self.revisar, bg="#bfdcc3").place(x=20, y=20)
        tk.Radiobutton(self.panel_izq, text="agregar", variable=self.opcion_impresion, value=2, command=self.revisar, bg="#bfdcc3").place(x=20, y=70)
        tk.Radiobutton(self.panel_izq, text="quitar", variable=self.opcion_impresion, value=3, command=self.revisar, bg="#bfdcc3").place(x=20, y=120)

        self.panel_der = tk.Frame(self.pagina2, bg="#d9eee0", width=250, height=320, bd=2, relief="raised")
        self.panel_der.place(x=220, y=180)

        self.estado_impresion = tk.Label(self.panel_der, text="Selecciona una opcion", fg="black", font=("Arial", 12), justify="left", wraplength=220, bg="#d9eee0")
        self.estado_impresion.place(x=12, y=20)

        self.cola_label = tk.Label(self.panel_der, text="Cola vacia", font=("Arial", 10), justify="left", wraplength=220, bg="#d9eee0")
        self.cola_label.place(x=12, y=250)

        self.form_frame = tk.Frame(self.panel_der, bg="#d9eee0")
        self.form_frame.place(x=10, y=60, width=220, height=170)
        self.form_frame.place_forget()

        tk.Label(self.form_frame, text="Nombre", bg="#d9eee0").place(x=0, y=0)
        self.entrada_nombre = tk.Entry(self.form_frame)
        self.entrada_nombre.place(x=90, y=0, width=120)

        tk.Label(self.form_frame, text="Hojas", bg="#d9eee0").place(x=0, y=35)
        self.entrada_hojas = tk.Entry(self.form_frame)
        self.entrada_hojas.place(x=90, y=35, width=120)

        tk.Label(self.form_frame, text="Tiempo", bg="#d9eee0").place(x=0, y=70)
        self.entrada_tiempo = tk.Entry(self.form_frame)
        self.entrada_tiempo.place(x=90, y=70, width=120)

        self.boton_confirmar = tk.Button(self.form_frame, text="Confirmar", bg="green", fg="white", command=self.agregar_a_pila)
        self.boton_confirmar.place(x=40, y=120, width=120, height=35)

        tk.Button(self.pagina2, text="volver", bg="gray", command=self.volver).place(x=350, y=520, width=100, height=50)

        self.revisar()

    # Elimina los controles de quitar para que no sigan visibles al cambiar de opcion.
    def ocultar_controles_quitar(self):
        if self.boton_quitar_primero is not None:
            self.boton_quitar_primero.destroy()
            self.boton_quitar_primero = None
        if self.boton_quitar_esp is not None:
            self.boton_quitar_esp.destroy()
            self.boton_quitar_esp = None
        if self.label_quitar_nombre is not None:
            self.label_quitar_nombre.destroy()
            self.label_quitar_nombre = None
        if self.entrada_quitar is not None:
            self.entrada_quitar.destroy()
            self.entrada_quitar = None

    # Saca el primer objeto de la lista porque ese documento llego primero a la cola.
    def quitar_primero(self):
        if not self.pila_impresiones:
            self.mostrar_estado("No hay trabajos para quitar", "red")
            self.mostrar_cola()
            return

        # pop(0) retira el primer trabajo porque la impresion funciona como cola.
        trabajo = self.pila_impresiones.pop(0)
        self.mostrar_estado(f"Se quitó: {trabajo.get_nom()}", "orange")
        self.mostrar_cola()

    # Busca por nombre en la lista y elimina solamente el primer documento que coincide.
    def quitar_especifico(self):
        if self.entrada_quitar is None:
            self.mostrar_estado("No hay entrada para nombre", "red")
            return

        nombre = self.entrada_quitar.get().strip()
        if nombre == "":
            self.mostrar_estado("Escribe el nombre para quitar", "red")
            return

        encontrado = False
        nueva_cola = []

        # Conserva todos los documentos excepto el primero que coincide.
        for documento in self.pila_impresiones:
            if documento.get_nom() == nombre and not encontrado:
                encontrado = True
                self.mostrar_estado(f"Se eliminó: {documento.get_nom()}", "orange")
            else:
                nueva_cola.append(documento)

        if encontrado:
            self.pila_impresiones = nueva_cola
            self.mostrar_cola()
            self.entrada_quitar.delete(0, tk.END)
        else:
            self.mostrar_estado("No existe ese documento en la cola", "red")
            self.mostrar_cola()

    # Crea la pagina del robot, sus acciones y la pila de instrucciones.
    def crear_ventana_robot(self):
        # Cabecera con la imagen del robot.
        panel_robot_arriba = tk.Frame(self.pagina3, bg="#bfdcc3", width=450, height=80)
        panel_robot_arriba.place(x=25, y=60)

        ruta_robot = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ROBOT.png")
        try:
            foto_robot = tk.PhotoImage(file=ruta_robot)
            tk.Label(panel_robot_arriba, image=foto_robot, bg="#bfdcc3").place(x=0, y=0)
            panel_robot_arriba.foto_robot = foto_robot
        except tk.TclError:
            panel_robot_arriba.configure(bg="gray")

        # Botones para elegir que accion se agregara a la pila.
        panel_opciones = tk.Frame(self.pagina3, bg="#bfdcc3")
        panel_opciones.place(x=20, y=160, width=180, height=250)

        tk.Label(panel_opciones, text="Elige una accion", font=("Arial", 12), bg="#bfdcc3").place(x=15, y=10)
        tk.Radiobutton(panel_opciones, text="Caminar", variable=self.accion_robot, value="caminar", bg="#bfdcc3").place(x=35, y=60)
        tk.Radiobutton(panel_opciones, text="Escanear", variable=self.accion_robot, value="escanear", bg="#bfdcc3").place(x=35, y=105)

        # Panel derecho: formulario, lista de acciones y boton de ejecucion.
        panel_robot = tk.Frame(self.pagina3, bg="#d9eee0", width=250, height=320, bd=2, relief="raised")
        panel_robot.place(x=220, y=160)

        self.estado_robot = tk.Label(panel_robot, text="Selecciona una accion", font=("Arial", 11), justify="left", wraplength=220, bg="#d9eee0")
        self.estado_robot.place(x=12, y=15)

        tk.Label(panel_robot, text="Tiempo en segundos", bg="#d9eee0").place(x=12, y=55)
        self.entrada_tiempo_robot = tk.Entry(panel_robot)
        self.entrada_tiempo_robot.place(x=12, y=80, width=105)

        self.boton_agregar_robot = tk.Button(panel_robot, text="Agregar", bg="green", fg="white", command=self.agregar_accion_robot)
        self.boton_agregar_robot.place(x=125, y=78, width=105, height=28)

        self.lista_robot = tk.Label(panel_robot, text="Pila vacia", font=("Arial", 10), justify="left", anchor="nw", wraplength=220, bg="#d9eee0")
        self.lista_robot.place(x=12, y=125, width=220, height=80)

        self.boton_ejecutar_robot = tk.Button(panel_robot, text="Ejecutar pila", bg="blue", fg="white", command=self.ejecutar_siguiente_robot)
        self.boton_ejecutar_robot.place(x=55, y=220, width=140, height=35)

        tk.Button(self.pagina3, text="volver", bg="gray", command=self.volver).place(x=350, y=520, width=100, height=50)

    # Agrega la accion seleccionada a la pila con el tiempo que indique el usuario.
    def agregar_accion_robot(self):
        accion = self.accion_robot.get()
        tiempo_valor = self.entrada_tiempo_robot.get().strip()

        if accion == "":
            self.mostrar_estado_robot("Selecciona caminar o escanear", "red")
            return

        try:
            tiempo = float(tiempo_valor)
        except ValueError:
            self.mostrar_estado_robot("El tiempo debe ser un numero", "red")
            return

        if tiempo <= 0:
            self.mostrar_estado_robot("El tiempo debe ser mayor que cero", "red")
            return

        # append agrega la nueva accion al final para conservar el orden de llegada.
        self.pila_robot.append(robot("Robot", accion, tiempo))
        self.entrada_tiempo_robot.delete(0, tk.END)
        if self.robot_ejecutando:
            self.mostrar_estado_robot(f"Accion agregada: {accion}. Se ejecutara despues de la actual", "orange")
        else:
            self.mostrar_estado_robot(f"Accion agregada: {accion}", "green")
        self.mostrar_pila_robot()

    # Ejecuta la cima de la pila y vuelve a revisar cuando termina su tiempo.
    def ejecutar_siguiente_robot(self):
        if not self.pila_robot:
            self.mostrar_estado_robot("No hay acciones en la pila", "red")
            self.mostrar_pila_robot()
            return

        # pop(0) retira la primera accion agregada: comportamiento FIFO.
        accion = self.pila_robot.pop(0)
        self.mostrar_estado_robot(f"{accion.get_tipo().capitalize()} durante {accion.get_tiempo()} segundos", "blue")
        self.mostrar_pila_robot()
        self.robot_ejecutando = True
        self.boton_ejecutar_robot.config(state=tk.DISABLED)
        # after espera sin congelar la ventana y recibe el tiempo en milisegundos.
        tiempo_ms = max(1, int(accion.get_tiempo() * 1000))
        self.root.after(tiempo_ms, self.terminar_accion_robot)

    def terminar_accion_robot(self):
        # Cuando termina una accion, ejecuta automaticamente la siguiente.
        self.boton_ejecutar_robot.config(state=tk.NORMAL)
        if self.pila_robot:
            self.mostrar_estado_robot("Accion terminada. Continua con la pila", "green")
            self.ejecutar_siguiente_robot()
        else:
            self.robot_ejecutando = False
            self.mostrar_estado_robot("Pila ejecutada completamente", "green")

    def mostrar_estado_robot(self, mensaje, color="black"):
        self.estado_robot.config(text=mensaje, fg=color)

    def mostrar_pila_robot(self):
        # La lista se muestra en el orden en que se ejecutaran las acciones.
        if not self.pila_robot:
            texto = "Pila vacia"
        else:
            acciones = [f"{accion.get_tipo()} ({accion.get_tiempo()} s)" for accion in self.pila_robot]
            texto = "Pila (primero en ejecutar):\n" + "\n".join(acciones)

        self.lista_robot.config(text=texto)

    # Oculta las tres paginas y vuelve a mostrar solo el Frame recibido como parametro.
    def ir_a(self, pagina):
        # Oculta todas las paginas y muestra solamente la pagina solicitada.
        self.pagina1.pack_forget()
        self.pagina2.pack_forget()
        self.pagina3.pack_forget()
        pagina.pack(fill="both", expand=True)

    # Muestra la pagina de impresion y llama a revisar para actualizar sus controles.
    def cambiar_im(self):
        # Abre la pagina de impresion.
        self.ir_a(self.pagina2)
        self.revisar()

    # Muestra la pagina que contiene los botones del robot.
    def cambiar_ro(self):
        # Abre la pagina del robot.
        self.ir_a(self.pagina3)

    # Cambia nuevamente al Frame de inicio sin borrar la cola de documentos.
    def volver(self):
        # Regresa al menu principal sin borrar ninguna lista.
        self.ir_a(self.pagina1)

    # Borra el texto de nombre, hojas y tiempo despues de agregar un documento.
    def limpiar_campos(self):
        # Deja vacios los campos del formulario de impresion.
        if self.entrada_nombre is not None:
            self.entrada_nombre.delete(0, tk.END)
        if self.entrada_hojas is not None:
            self.entrada_hojas.delete(0, tk.END)
        if self.entrada_tiempo is not None:
            self.entrada_tiempo.delete(0, tk.END)

    # Cambia el mensaje y el color del Label que informa el estado de la impresora.
    def mostrar_estado(self, mensaje, color="black"):
        # Cambia el mensaje y el color del estado de la impresora.
        if self.estado_impresion is not None:
            self.estado_impresion.config(text=mensaje, fg=color)

    # Recorre la lista y muestra los nombres de todos los documentos que siguen pendientes.
    def mostrar_cola(self):
        # Muestra los nombres de los documentos que siguen en la cola.
        if not self.pila_impresiones:
            texto = "Cola vacia"
        else:
            texto = "Cola: " + ", ".join(doc.get_nom() for doc in self.pila_impresiones)

        if self.cola_label is not None:
            self.cola_label.config(text=texto)

    # Lee el formulario, valida sus numeros, crea una impresion y la agrega al final de la lista.
    def agregar_a_pila(self):
        # Lee, valida y agrega un documento.
        if self.entrada_nombre is None or self.entrada_hojas is None or self.entrada_tiempo is None:
            return

        nombre_valor = self.entrada_nombre.get().strip()
        hojas_valor = self.entrada_hojas.get().strip()
        tiempo_valor = self.entrada_tiempo.get().strip()

        if nombre_valor == "" or hojas_valor == "" or tiempo_valor == "":
            self.mostrar_estado("Completa todos los campos", "red")
            return

        try:
            hojas_int = int(hojas_valor)
            tiempo_int = int(tiempo_valor)
        except ValueError:
            self.mostrar_estado("Los campos de hojas y tiempo deben ser numeros", "red")
            return

        if hojas_int <= 0 or tiempo_int <= 0:
            self.mostrar_estado("Hojas y tiempo deben ser mayores que cero", "red")
            return

        self.pila_impresiones.append(impresion(nombre_valor, hojas_int, tiempo_int))

        self.mostrar_estado(f"Documento agregado: {nombre_valor}. Faltan {len(self.pila_impresiones)}", "green")
        self.mostrar_cola()
        self.limpiar_campos()

    # Decide que controles mostrar y que accion ejecutar segun el valor del Radiobutton.
    def revisar(self):
        # Decide que controles mostrar segun la opcion seleccionada.
        if self.opcion_impresion.get() == 1:
            self.form_frame.place_forget()
            self.ocultar_controles_quitar()
            if not self.pila_impresiones:
                self.mostrar_estado("No hay trabajos en la cola para imprimir", "red")
                self.mostrar_cola()
                return

            while self.pila_impresiones:
                trabajo_actual = self.pila_impresiones.pop(0)
                nombre = trabajo_actual.get_nom()
                hojas = trabajo_actual.get_hoj()
                tiempo_por_pagina = trabajo_actual.get_tiempo()

                for pagina in range(1, hojas + 1):
                    faltan = len(self.pila_impresiones)
                    self.mostrar_estado(
                        f"Imprimiendo pagina {pagina} de {hojas} de {nombre} "
                        f"({tiempo_por_pagina} s por pagina) - faltan {faltan} trabajos",
                        "blue",
                    )
                    self.mostrar_cola()
                    self.root.update()
                    # Cada pagina tarda el tiempo indicado en el formulario.
                    time.sleep(tiempo_por_pagina)

            self.mostrar_estado("Ya no quedan trabajos por imprimir", "green")
            self.mostrar_cola()

        elif self.opcion_impresion.get() == 2:
            self.form_frame.place(x=10, y=60, width=220, height=170)
            self.ocultar_controles_quitar()
            self.mostrar_estado("Agrega un documento a la cola", "black")
            self.mostrar_cola()

        elif self.opcion_impresion.get() == 3:
            self.form_frame.place_forget()
            self.ocultar_controles_quitar()
            self.mostrar_estado("Elige quitar en la fila", "black")
            self.mostrar_cola()

            self.boton_quitar_primero = tk.Button(self.panel_der, text="Quitar primero", bg="orange", fg="white", command=self.quitar_primero)
            self.boton_quitar_primero.place(x=55, y=60, width=140, height=35)

            self.label_quitar_nombre = tk.Label(self.panel_der, text="Nombre a quitar", bg="#d9eee0")
            self.label_quitar_nombre.place(x=60, y=110)
            self.entrada_quitar = tk.Entry(self.panel_der)
            self.entrada_quitar.place(x=55, y=135, width=140)

            self.boton_quitar_especifico = tk.Button(self.panel_der, text="Quitar nombre", bg="orange", fg="white", command=self.quitar_especifico)
            self.boton_quitar_especifico.place(x=55, y=170, width=140, height=35)
if __name__ == "__main__":
    app = tk.Tk()
    Aplicacion(app)
    app.mainloop()
