import tkinter as tk
from tkinter import ttk, messagebox
import random


class SimuladorSO:

    def __init__(self, root):

        self.root = root
        self.root.title("Simulador Administrador de Tareas")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")


        self.procesos = []
        self.id_proceso = 1

        self.cpu_total = 800
        self.ram_total = 8192
        self.disco_total = 256000
        self.gpu_total = 4096

        self.cpu_usado = 0
        self.ram_usado = 0
        self.disco_usado = 0
        self.gpu_usado = 0



        titulo = tk.Label(
            root,
            text="SIMULADOR ADMINISTRADOR DE TAREAS",
            font=("Arial", 18, "bold"),
            bg="#f0f0f0",
            fg="#1f4e79"
        )

        titulo.pack(pady=10)


        frame_principal = tk.Frame(root, bg="#f0f0f0")
        frame_principal.pack(fill="both", expand=True, padx=10, pady=10)



        frame_tabla = tk.Frame(frame_principal)
        frame_tabla.pack(side="left", fill="both", expand=True)

        columnas = (
            "ID",
            "Usuario",
            "Prioridad",
            "CPU",
            "RAM",
            "Disco",
            "GPU"
        )

        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=20
        )

        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=90)

        self.tabla.pack(fill="both", expand=True)


        frame_derecho = tk.Frame(
            frame_principal,
            bg="white",
            relief="solid",
            bd=1
        )

        frame_derecho.pack(side="right", fill="y", padx=10)

        titulo_info = tk.Label(
            frame_derecho,
            text="Información del equipo",
            font=("Arial", 12, "bold"),
            bg="white"
        )

        titulo_info.pack(pady=10)



        tk.Label(
            frame_derecho,
            text="Procesador",
            bg="white"
        ).pack(anchor="w", padx=10)

        self.combo_cpu = ttk.Combobox(
            frame_derecho,
            values=[
                "Intel Core i5",
                "Intel Core i7",
                "Ryzen 5",
                "Ryzen 7"
            ]
        )

        self.combo_cpu.current(1)
        self.combo_cpu.pack(padx=10, pady=5)

        # ================================
        # RAM
        # ================================

        tk.Label(
            frame_derecho,
            text="Seleccionar RAM",
            bg="white"
        ).pack(anchor="w", padx=10)

        self.combo_ram = ttk.Combobox(
            frame_derecho,
            values=[
                "4 GB",
                "8 GB",
                "16 GB",
                "32 GB",
                "64 GB"
            ]
        )

        self.combo_ram.current(1)
        self.combo_ram.pack(padx=10, pady=5)

        # ================================
        # DISCO
        # ================================

        tk.Label(
            frame_derecho,
            text="Unidad de disco",
            bg="white"
        ).pack(anchor="w", padx=10)

        self.combo_disco = ttk.Combobox(
            frame_derecho,
            values=[
                "256 GB",
                "512 GB",
                "1 TB",
                "2 TB"
            ]
        )

        self.combo_disco.current(0)
        self.combo_disco.pack(padx=10, pady=5)

        # ================================
        # GPU
        # ================================

        tk.Label(
            frame_derecho,
            text="Tarjeta gráfica",
            bg="white"
        ).pack(anchor="w", padx=10)

        self.combo_gpu = ttk.Combobox(
            frame_derecho,
            values=[
                "2 GB",
                "4 GB",
                "6 GB",
                "8 GB"
            ]
        )

        self.combo_gpu.current(1)
        self.combo_gpu.pack(padx=10, pady=5)

        # ================================
        # BARRAS DE PROGRESO
        # ================================

        self.crear_barras(frame_derecho)

        # ================================
        # CONTROLES INFERIORES
        # ================================

        frame_controles = tk.Frame(root, bg="#f0f0f0")
        frame_controles.pack(fill="x", padx=10)

        tk.Label(
            frame_controles,
            text="Tipo de proceso"
        ).grid(row=0, column=0)

        self.combo_tipo = ttk.Combobox(
            frame_controles,
            values=[
                "Usuario",
                "Sistema",
                "Background"
            ]
        )

        self.combo_tipo.current(0)
        self.combo_tipo.grid(row=1, column=0, padx=10)

        tk.Label(
            frame_controles,
            text="Prioridad"
        ).grid(row=0, column=1)

        self.combo_prioridad = ttk.Combobox(
            frame_controles,
            values=[
                "Baja",
                "Normal",
                "Alta"
            ]
        )

        self.combo_prioridad.current(1)
        self.combo_prioridad.grid(row=1, column=1, padx=10)

        # ================================
        # BOTONES
        # ================================

        btn_agregar = tk.Button(
            frame_controles,
            text="Agregar tarea",
            bg="#4CAF50",
            fg="white",
            width=15,
            command=self.agregar_proceso
        )

        btn_agregar.grid(row=1, column=2, padx=10)

        btn_finalizar = tk.Button(
            frame_controles,
            text="Finalizar tarea",
            bg="#d9534f",
            fg="white",
            width=15,
            command=self.finalizar_proceso
        )

        btn_finalizar.grid(row=1, column=3, padx=10)

        btn_simular = tk.Button(
            frame_controles,
            text="Iniciar simulación",
            bg="#0275d8",
            fg="white",
            width=18,
            command=self.simular
        )

        btn_simular.grid(row=1, column=4, padx=10)

        # ================================
        # ESTADO
        # ================================

        self.label_estado = tk.Label(
            root,
            text="Tareas activas: 0",
            font=("Arial", 11),
            bg="#f0f0f0"
        )

        self.label_estado.pack(pady=10)

        # Enlazar eventos de comboboxes para actualizar hardware dinámicamente
        self.combo_cpu.bind("<<ComboboxSelected>>", self.actualizar_hardware)
        self.combo_ram.bind("<<ComboboxSelected>>", self.actualizar_hardware)
        self.combo_disco.bind("<<ComboboxSelected>>", self.actualizar_hardware)
        self.combo_gpu.bind("<<ComboboxSelected>>", self.actualizar_hardware)

        # Inicializar hardware y métricas por primera vez
        self.actualizar_hardware()


    def crear_barras(self, frame):

        tk.Label(frame, text="CPU", bg="white").pack(pady=5)
        self.barra_cpu = ttk.Progressbar(
            frame,
            length=250,
            maximum=self.cpu_total
        )
        self.barra_cpu.pack()

        tk.Label(frame, text="RAM", bg="white").pack(pady=5)
        self.barra_ram = ttk.Progressbar(
            frame,
            length=250,
            maximum=self.ram_total
        )
        self.barra_ram.pack()

        tk.Label(frame, text="DISCO", bg="white").pack(pady=5)
        self.barra_disco = ttk.Progressbar(
            frame,
            length=250,
            maximum=self.disco_total
        )
        self.barra_disco.pack()

        tk.Label(frame, text="GPU", bg="white").pack(pady=5)
        self.barra_gpu = ttk.Progressbar(
            frame,
            length=250,
            maximum=self.gpu_total
        )
        self.barra_gpu.pack()

        self.label_metricas = tk.Label(
            frame,
            text="",
            bg="white",
            justify="left",
            font=("Arial", 10)
        )

        self.label_metricas.pack(pady=20)

    # ================================
    # AGREGAR PROCESO
    # ================================

    def agregar_proceso(self):

        tipo = self.combo_tipo.get()
        prioridad = self.combo_prioridad.get()

        # Consumo aleatorio

        if tipo == "Usuario":
            cpu = random.randint(20, 40)
            ram = random.randint(300, 900)
            disco = random.randint(50, 150)
            gpu = random.randint(20, 120)

        elif tipo == "Sistema":
            cpu = random.randint(5, 15)
            ram = random.randint(100, 300)
            disco = random.randint(10, 60)
            gpu = random.randint(5, 30)

        else:
            cpu = random.randint(10, 25)
            ram = random.randint(150, 500)
            disco = random.randint(20, 100)
            gpu = random.randint(10, 50)

        # Validar recursos

        if self.ram_usado + ram > self.ram_total:
            messagebox.showerror(
                "Error",
                "Memoria RAM insuficiente"
            )
            return

        proceso = (
            self.id_proceso,
            tipo,
            prioridad,
            cpu,
            ram,
            disco,
            gpu
        )

        self.procesos.append(proceso)

        self.tabla.insert(
            "",
            "end",
            iid=str(self.id_proceso),
            values=proceso
        )

        self.id_proceso += 1

        self.actualizar_metricas()

    # ================================
    # FINALIZAR PROCESO
    # ================================

    def finalizar_proceso(self):

        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning(
                "Aviso",
                "Seleccione un proceso"
            )
            return

        for item in seleccionado:
            self.tabla.delete(item)

        self.procesos = []

        for hijo in self.tabla.get_children():

            valores = self.tabla.item(hijo)["values"]

            self.procesos.append(valores)

        self.actualizar_metricas()

    # ================================
    # ACTUALIZAR HARDWARE
    # ================================

    def actualizar_hardware(self, event=None):

        # Actualizar CPU total
        cpu_sel = self.combo_cpu.get()
        cpu_map = {
            "Intel Core i5": 600,
            "Intel Core i7": 800,
            "Ryzen 5": 600,
            "Ryzen 7": 800
        }
        self.cpu_total = cpu_map.get(cpu_sel, 800)

        # Actualizar RAM total
        ram_sel = self.combo_ram.get()
        ram_map = {
            "4 GB": 4096,
            "8 GB": 8192,
            "16 GB": 16384,
            "32 GB": 32768,
            "64 GB": 65536
        }
        self.ram_total = ram_map.get(ram_sel, 8192)

        # Actualizar Disco total
        disco_sel = self.combo_disco.get()
        disco_map = {
            "256 GB": 256000,
            "512 GB": 512000,
            "1 TB": 1000000,
            "2 TB": 2000000
        }
        self.disco_total = disco_map.get(disco_sel, 256000)

        # Actualizar GPU total
        gpu_sel = self.combo_gpu.get()
        gpu_map = {
            "2 GB": 2048,
            "4 GB": 4096,
            "6 GB": 6144,
            "8 GB": 8192
        }
        self.gpu_total = gpu_map.get(gpu_sel, 4096)

        # Actualizar límites de las barras de progreso
        self.barra_cpu.config(maximum=self.cpu_total)
        self.barra_ram.config(maximum=self.ram_total)
        self.barra_disco.config(maximum=self.disco_total)
        self.barra_gpu.config(maximum=self.gpu_total)

        # Actualizar la visualización de métricas
        self.actualizar_metricas()

    # ================================
    # ACTUALIZAR METRICAS
    # ================================

    def actualizar_metricas(self):

        self.cpu_usado = sum(p[3] for p in self.procesos)
        self.ram_usado = sum(p[4] for p in self.procesos)
        self.disco_usado = sum(p[5] for p in self.procesos)
        self.gpu_usado = sum(p[6] for p in self.procesos)

        self.barra_cpu["value"] = self.cpu_usado
        self.barra_ram["value"] = self.ram_usado
        self.barra_disco["value"] = self.disco_usado
        self.barra_gpu["value"] = self.gpu_usado

        ram_usado_gb = self.ram_usado / 1024
        ram_total_gb = self.ram_total / 1024

        self.label_metricas.config(
            text=
            f"CPU usado: {self.cpu_usado}/{self.cpu_total}\n"
            f"RAM usada: {ram_usado_gb:.2f}/{ram_total_gb:.2f} GB\n"
            f"Disco usado: {self.disco_usado}/{self.disco_total} MB\n"
            f"GPU usada: {self.gpu_usado}/{self.gpu_total} MB"
        )

        self.label_estado.config(
            text=f"Tareas activas: {len(self.procesos)}"
        )

    # ================================
    # SIMULACION
    # ================================

    def simular(self):

        for item in self.tabla.get_children():

            valores = list(self.tabla.item(item)["values"])

            # Variación aleatoria

            valores[3] = max(
                1,
                valores[3] + random.randint(-5, 5)
            )

            valores[4] = max(
                50,
                valores[4] + random.randint(-50, 50)
            )

            valores[5] = max(
                10,
                valores[5] + random.randint(-10, 10)
            )

            valores[6] = max(
                5,
                valores[6] + random.randint(-5, 5)
            )

            self.tabla.item(item, values=valores)

        self.procesos = []

        for hijo in self.tabla.get_children():

            valores = self.tabla.item(hijo)["values"]

            self.procesos.append(valores)

        self.actualizar_metricas()

        self.root.after(2000, self.simular)

# ================================
# EJECUTAR
# ================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SimuladorSO(root)

    root.mainloop()