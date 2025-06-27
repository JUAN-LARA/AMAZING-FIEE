import random
import pygame

class Flecha:
    def __init__(self, mapa_ancho, mapa_alto, imagen_flecha_path):
        try:
            self.flecha = pygame.image.load(imagen_flecha_path)  # Cargar la imagen
            self.flecha = pygame.transform.scale(self.flecha, (100, 50))  # Ajustar el tamaño
            print("Flecha cargada correctamente.")  # Mensaje si la imagen se carga correctamente
        except pygame.error as e:
            print(f"Error cargando la imagen de la flecha: {e}")
            
        self.ancho_mapa = mapa_ancho
        self.alto_mapa = mapa_alto
        self.ultimo_tiempo = 0
        self.intervalo = 3000  # 3 segundos en milisegundos

        # Inicializar la posición de la flecha
        self.x, self.y = self.generar_posicion_aleatoria()

    def generar_posicion_aleatoria(self):
        # Genera una posición aleatoria dentro del mapa
        x = random.randint(0, self.ancho_mapa - self.flecha.get_width())  # Asegúrate de que no se salga del mapa
        y = random.randint(0, self.alto_mapa - self.flecha.get_height())  # Lo mismo para la altura
        return x, y

    def dibujar(self, pantalla):
        # Comprobamos si ha pasado el intervalo de tiempo
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.ultimo_tiempo >= self.intervalo:
            # Actualizamos el tiempo de la última aparición
            self.ultimo_tiempo = tiempo_actual

            # Generamos la posición aleatoria solo cuando haya pasado el tiempo
            self.x, self.y = self.generar_posicion_aleatoria()

        # Dibujamos la flecha en la pantalla en la posición aleatoria
        pantalla.blit(self.flecha, (self.x, self.y))
