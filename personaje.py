import pygame

class Personaje:
    def __init__(self, nombre, imagen_path, imagen_extra_path, tamaño_pie, tamaño_agachado):
        self.nombre = nombre
        self.tamaño_pie = tamaño_pie
        self.tamaño_agachado = tamaño_agachado

        # Carga los sprites de animación
        try:
            self.sprites = {
                "derecha": [
                    pygame.transform.scale(
                        pygame.image.load(f"imagenes/{nombre}_caminar_derecha_1.png"), (tamaño_pie, tamaño_pie)),
                    pygame.transform.scale(
                        pygame.image.load(f"imagenes/{nombre}_caminar_derecha_2.png"), (tamaño_pie, tamaño_pie)),
                ],
                "izquierda": [
                    pygame.transform.scale(
                        pygame.image.load(f"imagenes/{nombre}_caminar_izquierda_1.png"), (tamaño_pie, tamaño_pie)),
                    pygame.transform.scale(
                        pygame.image.load(f"imagenes/{nombre}_caminar_izquierda_2.png"), (tamaño_pie, tamaño_pie)),
                ]
            }
        except:
            print(f"Error cargando sprites de animación para {nombre}")
            self.sprites = {
                "derecha": [pygame.Surface((tamaño_pie, tamaño_pie)), pygame.Surface((tamaño_pie, tamaño_pie))],
                "izquierda": [pygame.Surface((tamaño_pie, tamaño_pie)), pygame.Surface((tamaño_pie, tamaño_pie))]
            }

        # Imagen extra opcional
        if imagen_extra_path:
            try:
                self.imagen_extra = pygame.image.load(imagen_extra_path)
            except:
                self.imagen_extra = pygame.Surface((400, 400), pygame.SRCALPHA)
        else:
            self.imagen_extra = pygame.Surface((400, 400), pygame.SRCALPHA)

    def obtener_imagen_animada(self, direccion, frame):
        return self.sprites[direccion][frame % 2]

    def obtener_imagen(self):
        # Devuelve la primera imagen
        return self.sprites["derecha"][0]

    def obtener_imagen_extra(self):
        return pygame.transform.scale(self.imagen_extra, (400, 400))