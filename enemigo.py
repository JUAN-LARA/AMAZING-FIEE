import pygame

class Enemigo:
    def __init__(self, nombre, imagenes_derecha, imagenes_izquierda, tamaño=50, x=0, y=0):
        self.nombre = nombre
        self.tamaño_pie = tamaño
        self.tamaño_agachado = tamaño  # Por compatibilidad, aunque probablemente no lo uses
        self.x = x
        self.y = y

        # Carga las imágenes de animación como listas de Surfaces
        self.imagen_derecha = [
            pygame.transform.scale(pygame.image.load(img_path), (tamaño, tamaño))
            for img_path in imagenes_derecha
        ]
        self.imagen_izquierda = [
            pygame.transform.scale(pygame.image.load(img_path), (tamaño, tamaño))
            for img_path in imagenes_izquierda
        ]

        self.direccion = "izquierda"
        self.frame = 0
        self.velocidad_y = 0

    def obtener_imagen_animada(self, direccion, frame):
        if direccion == "izquierda":
            return self.imagen_derecha[frame % len(self.imagen_derecha)]
        else:
            return self.imagen_izquierda[frame % len(self.imagen_izquierda)]