# 🎧 Reproductor de Música con Flet y Pygame
🔧 Tecnologías utilizadas
Flet: para construir la interfaz gráfica.

Pygame: para la reproducción de archivos de audio.

Mutagen: para leer metadatos de archivos MP3.

📦 Estructura general
1. Clase Cancion
Representa una canción con su ruta, título y duración.

2. Función main(page)
Función principal que construye la interfaz gráfica:

Configura el título, paddings y color de fondo de la ventana.

Define un degradado en el fondo con una capa semiopaca encima (simulando blur).

Crea los widgets: controles, barra de progreso, nombre de canción, etc.

🖼️ Interfaz
Stack: permite apilar elementos. Se usa para colocar el fondo, la capa blur y el reproductor.

Column: contiene los controles principales (información, progreso, botones).

Row: organiza los botones y el progreso horizontalmente.

FilePicker: abre un explorador de carpetas para seleccionar canciones.

🎵 Funcionalidad
📂 cargar_carpeta(e)
Carga todos los archivos .mp3 de la carpeta seleccionada y los agrega a la playlist.

Muestra un mensaje si no se encuentran canciones.

🔁 cargar_cancion()
Carga la canción seleccionada en Pygame.

▶️ play_pause(e)
Reproduce, pausa o retoma la canción.

⏭️ cambiar_cancion(delta)
Cambia de pista adelante o atrás.

🔄 actualizar_info()
Muestra en pantalla el título y duración de la canción.

⏱ formatear_tiempo(segundos)
Convierte segundos a formato MM:SS.

📶 actualizar_progreso()
Actualiza el progreso de la barra y el tiempo transcurrido cada 0.5 segundos.
