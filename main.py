import os
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
import threading
from tkinter import ttk

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    entrada_carpeta.delete(0, tk.END)
    entrada_carpeta.insert(0, carpeta)

def descargar_video():
    enlace_youtube = entrada_enlace.get()
    carpeta_destino = entrada_carpeta.get()

    try:
        yt = YouTube(enlace_youtube)
        video = yt.streams.get_highest_resolution()

        if not carpeta_destino:
            resultado.delete(1.0, tk.END)
            resultado.insert(tk.END, "Debes seleccionar una carpeta de destino.")
            return

        os.makedirs(carpeta_destino, exist_ok=True)

        def descargar():
            video_descargado = video.download(carpeta_destino)
            resultado.delete(1.0, tk.END)
            resultado.insert(tk.END, f'Se ha descargado el video "{yt.title}" en la carpeta "{carpeta_destino}".')

        # Iniciar un hilo para la descarga del video
        thread = threading.Thread(target=descargar)
        thread.start()

    except Exception as e:
        resultado.delete(1.0, tk.END)
        resultado.insert(tk.END, f'Error: {str(e)}')

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Descargar Video de YouTube")
ventana.configure(bg="#222")  # Fondo oscuro

# Estilo personalizado para los elementos de la interfaz gráfica
estilo = ttk.Style()
estilo.configure("TButton", foreground="#000", background="#333")  # Texto negro, fondo oscuro
estilo.configure("TLabel", foreground="#fff", background="#222")  # Texto blanco, fondo oscuro
estilo.configure("TEntry", foreground="#000", background="#fff")  # Texto negro, fondo blanco

# Crear elementos de la interfaz
etiqueta_enlace = ttk.Label(ventana, text="Enlace de YouTube:")
etiqueta_enlace.pack(pady=10)

entrada_enlace = ttk.Entry(ventana, width=40)
entrada_enlace.pack()

etiqueta_carpeta_destino = ttk.Label(ventana, text="Carpeta de Destino:")
etiqueta_carpeta_destino.pack(pady=10)

entrada_carpeta = ttk.Entry(ventana, width=40)
entrada_carpeta.pack()

boton_seleccionar_carpeta = ttk.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta)
boton_seleccionar_carpeta.pack(pady=10)

boton_descargar = ttk.Button(ventana, text="Descargar Video", command=descargar_video)
boton_descargar.pack(pady=20)

resultado = tk.Text(ventana, wrap=tk.WORD, height=5, width=50, foreground="#fff", background="#222")  # Texto blanco, fondo oscuro
resultado.pack()

ventana.mainloop()
