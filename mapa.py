import pygame
import pytmx
from config import ANCHO, ALTO

class Mapa:
    def __init__(self, ruta):
        self.mapa_tiled = pytmx.load_pygame(ruta)
        self.tilewidth = self.mapa_tiled.tilewidth
        self.tileheight = self.mapa_tiled.tileheight

    def dibujar(self, pantalla, offset_x=0, offset_y=0):
        for layer in self.mapa_tiled.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.mapa_tiled.get_tile_image_by_gid(gid)
                    if tile:
                        pantalla.blit(
                            tile,
                            (x * self.tilewidth - offset_x, y * self.tileheight - offset_y)
                        )

    def verificar_colision(self, rect):
        # Busca la capa llamada "colisiones" (¡mismo nombre que en Tiled!)
        capa_colisiones = self.mapa_tiled.get_layer_by_name("colisiones")
        if not capa_colisiones:
            print("¡Error: No encontré la capa 'colisiones' en el mapa!")
            return False

        for obj in capa_colisiones:
            if hasattr(obj, 'x') and hasattr(obj, 'width'):
                obj_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                if rect.colliderect(obj_rect):
                    return True
        return False