# Importamos las librerías necesarias
import flet as ft            # Para construir la interfaz gráfica
import pygame                # Para reproducir archivos de audio
import os                    # Para navegar en carpetas y rutas
import asyncio               # Para ejecutar tareas asincrónicas
from mutagen.mp3 import MP3  # Para obtener duración de archivos MP3

# Inicializamos el reproductor de audio de pygame
pygame.mixer.init()

# Clase Cancion: contiene ruta, título y duración de cada canción
class Cancion:
    def __init__(self, ruta):
        self.ruta = ruta
        self.titulo = os.path.basename(ruta)
        self.duracion = self.obtener_duracion()

    def obtener_duracion(self):
        try:
            audio = MP3(self.ruta)
            return audio.info.length  # Retorna duración en segundos
        except Exception as e:
            print(f"Error cargando duración: {e}")
            return 0

# Función principal donde se arma la interfaz
async def main(page: ft.Page):
    page.title = "Reproductor de Música"   
    page.padding = 20
    page.bgcolor = "transparent"# Fondo transparente, preparado para mostrar el degradado

    # Fondo con degradado azul oscuro
    background = ft.Container(
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#1a237e", "#0d47a1", "#1b1b1b"]
        )
    )

    # Capa negra semitransparente encima del fondo, simula blur
    blur_layer = ft.Container(
        expand=True,
        bgcolor=ft.Colors.with_opacity(0.5, "#000000")
    )

    # Activamos scroll en caso de pantallas pequeñas
    page.scroll = ft.ScrollMode.AUTO

    playlist = []         # Lista de canciones cargadas
    cancion_actual = 0    # Índice de la canción que se está reproduciendo

    # Componentes de la interfaz
    info_cancion = ft.Text(size=20, color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER, width=page.width)
    tiempo_recorrido = ft.Text("00:00", color=ft.colors.WHITE)
    duracion = ft.Text("00:00", color=ft.colors.WHITE)
    barra_de_progreso = ft.ProgressBar(value=0.0, width=300, color=ft.colors.WHITE)

    # Botones de control
    play_boton = ft.IconButton(icon=ft.icons.PLAY_ARROW, icon_color=ft.colors.WHITE)
    prev_boton = ft.IconButton(icon=ft.icons.SKIP_PREVIOUS, icon_color=ft.colors.WHITE)
    next_boton = ft.IconButton(icon=ft.icons.SKIP_NEXT, icon_color=ft.colors.WHITE)

    # Componente para seleccionar carpetas
    file_picker = ft.FilePicker(on_result=lambda e: cargar_carpeta(e))
    page.overlay.append(file_picker)

    # Botón para abrir el explorador de carpetas
    abrir_boton = ft.IconButton(
        icon=ft.icons.ADD,
        icon_color=ft.colors.WHITE,
        on_click=lambda _: file_picker.get_directory_path(
            dialog_title="Selecciona una carpeta con canciones"
        )
    )

    status_message = ft.Text("", color=ft.colors.BLUE)  # Mensaje de estado al usuario

    # Fila con los botones de control (play, siguiente, anterior)
    controles = ft.Row([prev_boton, play_boton, next_boton], alignment=ft.MainAxisAlignment.CENTER)
    
    # Fila con progreso, tiempo actual y duración
    fila_reproductor = ft.Row([tiempo_recorrido, barra_de_progreso, duracion], alignment=ft.MainAxisAlignment.CENTER)

    # Columna principal que organiza todos los controles
    columna = ft.Column(
        [info_cancion, fila_reproductor, controles, abrir_boton, status_message],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )

    # Apilamos el fondo degradado, blur y la caja del reproductor centrada
    page.add(
        ft.Stack(controls=[
            background,
            blur_layer,
            ft.Container(content=columna, alignment=ft.alignment.center, expand=True)
        ])
    )

    # Función que carga las canciones desde la carpeta seleccionada
    def cargar_carpeta(e):
        nonlocal playlist, cancion_actual
        if e.path:
            playlist = []
            for root, _, files in os.walk(e.path):
                for file in files:
                    if file.endswith(".mp3"):
                        playlist.append(Cancion(os.path.join(root, file)))
            if playlist:
                cancion_actual = 0
                cargar_cancion()
                actualizar_info()
                status_message.value = f"{len(playlist)} canciones cargadas"
            else:
                status_message.value = "No se encontraron canciones en la carpeta seleccionada"
            page.update()

    # Carga la canción actual en el reproductor de Pygame
    def cargar_cancion():
        try:
            pygame.mixer.music.load(playlist[cancion_actual].ruta)
        except Exception as e:
            status_message.value = f"Error: {str(e)}"
            page.update()

    # Reproduce o pausa la canción
    def play_pause(e):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            play_boton.icon = ft.icons.PLAY_ARROW
        else:
            if pygame.mixer.music.get_pos() == -1:
                cargar_cancion()
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
            play_boton.icon = ft.icons.PAUSE
        actualizar_info()
        page.update()

    # Cambia a la canción anterior o siguiente
    def cambiar_cancion(delta):
        nonlocal cancion_actual
        cancion_actual = (cancion_actual + delta) % len(playlist)
        cargar_cancion()
        pygame.mixer.music.play()
        actualizar_info()
        play_boton.icon = ft.icons.PAUSE
        page.update()

    # Actualiza el título y duración de la canción en pantalla
    def actualizar_info():
        if playlist:
            c = playlist[cancion_actual]
            info_cancion.value = c.titulo
            duracion.value = formatear_tiempo(c.duracion)
            barra_de_progreso.value = 0.0
            tiempo_recorrido.value = "00:00"
            page.update()

    # Convierte segundos en formato MM:SS
    def formatear_tiempo(segundos):
        m, s = divmod(int(segundos), 60)
        return f"{m:02}:{s:02}"

    # Actualiza la barra de progreso cada 0.5 segundos
    async def actualizar_progreso():
        while True:
            if pygame.mixer.music.get_busy() and playlist:
                tiempo = pygame.mixer.music.get_pos() / 1000
                if tiempo > 0:
                    barra_de_progreso.value = tiempo / playlist[cancion_actual].duracion
                    tiempo_recorrido.value = formatear_tiempo(tiempo)
                    page.update()
            await asyncio.sleep(0.5)

    # Eventos de los botones
    play_boton.on_click = play_pause
    prev_boton.on_click = lambda _: cambiar_cancion(-1)
    next_boton.on_click = lambda _: cambiar_cancion(+1)

    # Inicia la tarea asincrónica que actualiza el progreso
    asyncio.create_task(actualizar_progreso())

# Ejecuta la aplicación
ft.app(target=main)
