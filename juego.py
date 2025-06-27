import pygame
import sys
import os  # se añade para que la musica no se importe defrente desde la caparte del ordenador 
from mapa import Mapa
from personaje import Personaje
from config import ANCHO, ALTO, COLORES, TILE_SIZE
import personaje
import time
from flecha import Flecha 
import random

CARPETA_BASE = os.path.dirname(__file__)
CARPETA_SONIDOS = os.path.join(CARPETA_BASE, "ost_amazing fiee(sonido musica )")
CARPETA_IMAGENES = os.path.join(CARPETA_BASE, "imagenes")
CARPETA_FUENTE = os.path.join(CARPETA_BASE, "assets")
class Juego:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        #sonido salto
        self.sonido_salto = pygame.mixer.Sound(os.path.join(CARPETA_SONIDOS, "sound_salto.mp3"))
        self.sonido_salto.set_volume(0.7)
        #sonido game over 
        self.sonido_gameover = pygame.mixer.Sound(os.path.join(CARPETA_SONIDOS, "game_over.mp3"))
        self.sonido_gameover.set_volume(0.7)
        self.flecha = Flecha(800, 600, "Flamethrower.gif")  # Asegúrate de poner la ruta correcta de la imagen


        # Inicialización de pygame y demás...
       # self.transicion_fluida = pygame.image.load("/mnt/data/0cddce1b-09c7-46c3-a46d-b6554f83e922.gif").convert_alpha()  # Cargar el GIF
        #self.transicion_rect = self.transicion_fluida.get_rect(center=(ANCHO // 2, ALTO // 2))  # Ajusta su posición central en la pantalla





        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Amazing FIEE")
        #fondo fiee 
        self.fondo_juego = pygame.image.load(os.path.join(CARPETA_IMAGENES, "foto_fiee.png")).convert()
        self.fondo_juego = pygame.transform.scale(self.fondo_juego, (ANCHO, ALTO))

        self.COLORES = {'BLANCO': (255,255,255), 'NEGRO': (0,0,0), 'AMARILLO': (255,255,0)}
        self.fuente = pygame.font.SysFont("assets/PressStart2P.ttf", 60, bold=True)
        self.fuente_boton = pygame.font.SysFont("assets/PressStart2P.ttf", 50)
        self.fondo = pygame.image.load("imagenes/portada.png").convert()
        self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        self.num_tiles_x = ANCHO // TILE_SIZE
        self.mapa = Mapa("mapa.tmx")  # Carga el mapa de Tiled
        #sonido colision
        self.sonido_colision = pygame.mixer.Sound(os.path.join(CARPETA_SONIDOS, "golpe_sound_effect.mp3"))  
        self.sonido_colision.set_volume(0.7)
        
        self.personajes = [
            Personaje("arturito", "personaje1.png", "arturito_extra.png", 80, 55),
            Personaje("erquigod", "erquigod.png", "erquigod_extra.png", 80, 55)
        ]
        
        self.enemigos = [
            Personaje("enemigo1", "imagenes/enemigo1_caminar_derecha_1.png", None, 50, 35),
            Personaje("enemigo1", "imagenes/enemigo1_caminar_derecha_1.png", None, 50, 35),
            Personaje("enemigo1", "imagenes/enemigo1_caminar_derecha_1.png", None, 50, 35),
            Personaje("enemigo1", "imagenes/enemigo1_caminar_derecha_1.png", None, 50, 35),
            Personaje("enemigo1", "imagenes/enemigo1_caminar_derecha_1.png", None, 50, 35),
            
            
        ]
        self.enemigos_pos = [
              [100, 300],  # Plataforma superior izquierda
              [600, 400],
              [250, 600],
              [896, 832],
              [622, 1570],
              
              
        ]
        self.seleccion_personaje = 0
        self.gravedad = 0.5
        self.velocidad_movimiento = 5
        self.clock = pygame.time.Clock()
        self.HITBOX_OFFSET_X_NORMAL = 35
        self.HITBOX_OFFSET_X_AGACHADO = 10
        self.HITBOX_OFFSET_Y = 15
        self.camara_offset_x = 0
        self.camara_offset_y = 0
        self.camara_suavidad = 0.1
        self.alto_mapa = 2240  # Alto total de tu mapa en píxeles
        self.ancho_mapa = 2880  # Ancho total de tu mapa en píxeles

    def dibujar(self):
        self.pantalla.blit(self.fondo, (0, 0))  # Fondo del juego
        self.flecha.dibujar(self.pantalla)  # Llama al método dibujar de la clase Flecha
        pygame.display.flip()  # Actualiza la pantalla



    def mostrar_texto(self, texto, y, color='BLANCO', fuente='fuente'):
        render = getattr(self, fuente).render(texto, True, self.COLORES[color])
        self.pantalla.blit(render, (ANCHO//2 - render.get_width()//2, y))

    def pantalla_inicio(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.mostrar_texto("Bienvenido a Amazing FIEE:", ALTO//4)
        self.mostrar_texto("Presiona ESPACIO para Iniciar", ALTO//2, fuente='fuente_boton')
        pygame.display.update()
        pygame.mixer.music.load(os.path.join(CARPETA_SONIDOS, "ost _de _menu.mp3"))
        pygame.mixer.music.play(-1)
        self.esperar_tecla()

    def pantalla_seleccion_personaje(self):
        self.pantalla.blit(self.fondo, (0, 0))
        self.mostrar_texto("Selecciona tu personaje", 100, 'BLANCO')
        pos_personajes = [
            (ANCHO // 4 - 150, ALTO // 2 - 100),  # Arturito (izquierda)
            (3 * ANCHO // 4 - 50, ALTO // 2 - 100)  # Erquigod (derecha)
        ]
        archivos_imagenes = ["imagenes/personaje1.png", "imagenes/erquigod.png"]

        for i, personaje in enumerate(self.personajes):
            tamaño = 250 if self.seleccion_personaje == i else 200
            imagen = pygame.image.load(archivos_imagenes[i])
            imagen = pygame.transform.scale(imagen, (tamaño, tamaño))
            self.pantalla.blit(imagen, pos_personajes[i])
            texto_nombre = self.fuente_boton.render(personaje.nombre.capitalize(), True, self.COLORES['BLANCO'])
            x_pos = pos_personajes[i][0] + (tamaño // 2) - (texto_nombre.get_width() // 2)
            y_pos = ALTO // 2 + 160
            self.pantalla.blit(texto_nombre, (x_pos, y_pos))
                                    
        pygame.display.update()

    def pantalla_personaje_seleccionado(self, personaje_seleccionado):
        self.pantalla.fill(self.COLORES['NEGRO'])  
        personaje = self.personajes[personaje_seleccionado]
        try:
            imagen = personaje.obtener_imagen_extra()
            self.pantalla.blit(imagen, (ANCHO//2 - imagen.get_width()//2, ALTO//2 - imagen.get_height()//2))
        except:
            pass
        self.mostrar_texto(f"Has seleccionado a {personaje.nombre.capitalize()}", ALTO//2 + 200, 'AMARILLO')
        self.mostrar_texto("Presiona ESPACIO para iniciar el juego", ALTO//2 + 250, 'AMARILLO', 'fuente_boton')
        pygame.display.update()
        self.esperar_tecla()
    #pantalla de carga a mano 
    def mostrar_pantalla_carga(self, musica=None):
        frames = []
        carpeta_frames = os.path.join(CARPETA_IMAGENES, "pantalla de carga")
        for i in range(1, 16):
            frame_path = os.path.join(carpeta_frames, f"frame_{i:04}.png")
            if os.path.exists(frame_path):
                imagen = pygame.image.load(frame_path).convert_alpha()
                imagen = pygame.transform.scale(imagen, (ANCHO, ALTO))
                frames.append(imagen)
        if not frames:
            print("⚠️ No se encontraron imágenes de carga.")
            return
        #musica de carga
        if musica:
            ruta = os.path.join(CARPETA_SONIDOS, musica)
            print(f"🎵 Reproduciendo: {ruta}")  # Para depurar
            if os.path.exists(ruta):
                pygame.mixer.music.load(ruta)
                pygame.mixer.music.set_volume(0.9)
                pygame.mixer.music.play()
            else:
                print("⚠️ No se encontró el archivo de música.")
        tiempo_total = 4
        fps = 24
        frame_actual = 0
        duracion_frame = 1 / fps
        tiempo = 0
        reloj = pygame.time.Clock()
        while tiempo < tiempo_total:
            self.pantalla.fill((0, 0, 0))
            self.pantalla.blit(frames[frame_actual % len(frames)], (0, 0))
            pygame.display.flip()
            reloj.tick(fps)
            frame_actual += 1
            tiempo += duracion_frame   
    def transicion_apertura_circular(self, duracion=1.2):
        reloj = pygame.time.Clock()
        ancho, alto = self.pantalla.get_size()
        centro = (ancho // 2, alto // 2)
        radio_maximo = int((ancho ** 2 + alto ** 2) ** 0.5)

        tiempo = 0
        while tiempo < duracion:
            progreso = tiempo / duracion
            radio_actual = int(radio_maximo * progreso)

        # Dibujamos la pantalla actual (puede ser la última del fondo o carga)
            self.pantalla.blit(self.fondo_juego, (0, 0))  # o lo que quieras mostrar

        # Capa negra con agujero transparente circular en el centro
            overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 255))
            pygame.draw.circle(overlay, (0, 0, 0, 0), centro, radio_actual)
            self.pantalla.blit(overlay, (0, 0))

            pygame.display.flip()
            tiempo += reloj.tick(60) / 1000.0  
    def transicion_apertura_circular_con_fondo(self, fondo_mapa, duracion=1.2):
        reloj = pygame.time.Clock()
        ancho, alto = self.pantalla.get_size()
        centro = (ancho // 2, alto // 2)
        radio_maximo = int((ancho ** 2 + alto ** 2) ** 0.5)

        tiempo = 0
        while tiempo < duracion:
            progreso = tiempo / duracion
            radio_actual = int(radio_maximo * progreso)

         # Mostrar el fondo del mapa (precargado)
            self.pantalla.blit(fondo_mapa, (0, 0))

        # Crea una capa negra con un agujero circular transparente
            overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 255))
            pygame.draw.circle(overlay, (0, 0, 0, 0), centro, radio_actual)
            self.pantalla.blit(overlay, (0, 0))

            pygame.display.flip()
            tiempo += reloj.tick(60) / 1000.0
        #fin de carga de pantalla                

    def esperar_tecla(self, tecla=pygame.K_SPACE):
        esperando = True
        while esperando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == tecla:
                    esperando = False

    def iniciar_juego(self, personaje_seleccionado):

        tiempo_inicio = pygame.time.get_ticks()  # Guardamos el tiempo de inicio del juego
        mapa_cambiado = False  # Bandera para verificar si el mapa ya fue cambiado



        pygame.mixer.music.stop()
        #musica del juego  
        pygame.mixer.music.load(os.path.join(CARPETA_SONIDOS, "Musica_principal_juego.mp3" ))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        personaje = self.personajes[personaje_seleccionado]
        tamaño_normal = personaje.tamaño_pie
        tamaño_agachado = personaje.tamaño_agachado

        # Estado inicial del jugador
        x = TILE_SIZE * 22  # Puedes dejar esto igual para mantener el margen izquierdo
        y = TILE_SIZE * 2  # Esto colocará al personaje cerca de la parte superior
        velocidad_y = 0
        salto_base = -6
        salto_extra = -6
        tiempo_carga_max = 0.3
        tiempo_presionado = 0
        puede_saltar = True
        agachado = False
        orientacion = "izquierda"
        en_suelo = True
        imagenes = self.cargar_animaciones(personaje, tamaño_normal, tamaño_agachado)
        indice_animacion = 0
        tiempo_animacion = 0

        # --------- SISTEMA DE VIDAS ---------
        vidas = 30

        fuente_vidas = pygame.font.SysFont("assets/PressStart2P.ttf", 50, bold=True)

        # Animación de enemigos
        direcciones_iniciales = [-1, -1, -1]
        enemigos_estados = []
        for idx, enemigo in enumerate(self.enemigos):
            sentido = direcciones_iniciales [idx % len(direcciones_iniciales)]
            enemigos_estados.append({
                "limite_izquierda":300,
                "limite_derecha":1000,
                "personaje": enemigo,
                "x": self.enemigos_pos[idx][0],
                "y": self.enemigos_pos[idx][1],
                "direccion": "izquierda" if sentido > 0  else "derecha",
                "frame": 0,
                "tiempo_anim": 0,
                "sentido": sentido,
                "velocidad_y": 0,
                "gravedad": 0.8,
                "en_suelo": False
            })

        corriendo = True
        while corriendo and vidas > 0:
            dt = self.clock.tick(60) / 1000.0
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

  

            hitbox_jugador = pygame.Rect(
                        x + self.HITBOX_OFFSET_X_NORMAL,
                        y + self.HITBOX_OFFSET_Y,
                        tamaño_normal - 2*self.HITBOX_OFFSET_X_NORMAL,
                        tamaño_normal - self.HITBOX_OFFSET_Y
)

# Definir las coordenadas de cambio de mapa
            x_destino = 2736.00  # Por ejemplo, cambiar de mapa cuando el jugador llega a x = 500
            y_destino = 2198.67  # Y = 600

            if hitbox_jugador.colliderect(pygame.Rect(x_destino, y_destino, 1, 1)) and not mapa_cambiado:

                #pantalla de carga
                self.mostrar_pantalla_carga("musica_de_carga.mp3")

                self.mapa = Mapa("mapa2.tmx")  # Cambiar al mapa 2
                self.ancho_mapa = 1340  # Nuevo ancho del mapa
                self.alto_mapa = 670   # Nuevo alto del mapa
                x = 900  # Teletransporta al jugador a la posición x = 1034
                y = 300   # Teletransporta al jugador a la posición y = 358
                mapa_cambiado = True

                #cambio de mapa
                fondo_mapa = pygame.Surface((ANCHO, ALTO))
                fondo_mapa.blit(self.fondo_juego, (0, 0))
                self.mapa.dibujar(fondo_mapa, 0, 0)
                self.transicion_apertura_circular_con_fondo(fondo_mapa)

            hitbox_offset_x = self.HITBOX_OFFSET_X_AGACHADO if agachado else self.HITBOX_OFFSET_X_NORMAL
            teclas = pygame.key.get_pressed()
            movimiento_x = 0
            velocidad_actual = self.velocidad_movimiento
            if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
                velocidad_actual *= 2  # o 2.0 para más velocidad

            if teclas[pygame.K_a]:
                movimiento_x = -velocidad_actual
                orientacion = "izquierda"
            if teclas[pygame.K_d]:
                movimiento_x = velocidad_actual
                orientacion = "derecha"
            altura_actual = tamaño_agachado if agachado else tamaño_normal
            objetivo_x = x - ANCHO // 2 + altura_actual // 2
            objetivo_y = y - ALTO // 2 + altura_actual // 2
            objetivo_x = max(0, min(objetivo_x, self.ancho_mapa - ANCHO))
            objetivo_y = max(0, min(objetivo_y, self.alto_mapa - ALTO))
            self.camara_offset_x += (objetivo_x - self.camara_offset_x) * self.camara_suavidad
            self.camara_offset_y += (objetivo_y - self.camara_offset_y) * self.camara_suavidad
            nueva_x = x + movimiento_x
            altura_actual = tamaño_agachado if agachado else tamaño_normal

            hitbox_actual = pygame.Rect(
                x + hitbox_offset_x,
                y + self.HITBOX_OFFSET_Y,
                altura_actual - 2*hitbox_offset_x,
                altura_actual - self.HITBOX_OFFSET_Y
            )

            if movimiento_x != 0:
                hitbox_temp = hitbox_actual.copy()
                hitbox_temp.x = nueva_x + hitbox_offset_x
                if not self.mapa.verificar_colision(hitbox_temp):
                    x = nueva_x
                else:
                    if movimiento_x > 0:
                        tile_colision = (hitbox_temp.right // TILE_SIZE) * TILE_SIZE
                        x = tile_colision - (altura_actual - hitbox_offset_x) - 1
                    else:
                        tile_colision = ((hitbox_temp.left // TILE_SIZE) + 1) * TILE_SIZE
                        x = tile_colision - hitbox_offset_x

            if en_suelo:
                if teclas[pygame.K_SPACE] and puede_saltar:
                    tiempo_presionado = min(tiempo_presionado + dt, tiempo_carga_max)
                elif not teclas[pygame.K_SPACE] and tiempo_presionado > 0:
                    velocidad_y = salto_base + (salto_extra * (tiempo_presionado/tiempo_carga_max))
                    self.sonido_salto.play()
                    en_suelo = False
                    tiempo_presionado = 0
                    puede_saltar = False
            else:
                puede_saltar = True

            nuevo_agachado = teclas[pygame.K_s]
            #mejorar las fisicas de agarcha
            if nuevo_agachado and not agachado:
                agachado = True
                y += tamaño_normal - tamaño_agachado

            elif not nuevo_agachado and agachado:
                hitbox_parado = pygame.Rect(
                    x + self.HITBOX_OFFSET_X_NORMAL,
                    y - (tamaño_normal - tamaño_agachado) + self.HITBOX_OFFSET_Y,
                    tamaño_normal - 2*self.HITBOX_OFFSET_X_NORMAL,
                    tamaño_normal - self.HITBOX_OFFSET_Y
                )
                if not self.mapa.verificar_colision(hitbox_parado):
                    agachado = False
                    y -= tamaño_normal - tamaño_agachado

            if not en_suelo:
                velocidad_y += self.gravedad
                y += velocidad_y

            hitbox_actual.y = y + self.HITBOX_OFFSET_Y

            if self.mapa.verificar_colision(hitbox_actual):
                if velocidad_y > 0:
                    y = ((hitbox_actual.bottom // TILE_SIZE) * TILE_SIZE - altura_actual)
                    en_suelo = True
                    velocidad_y = 0 #se agrego  para evitar que se pegue a algun techo si choca la cabeza
                elif velocidad_y < 0:
                    y = ((hitbox_actual.top // TILE_SIZE) + 1) * TILE_SIZE - self.HITBOX_OFFSET_Y
                velocidad_y = 0
            else:
                en_suelo = False
            x = max(0, min(x, self.ancho_mapa - altura_actual))
            y = max(0, min(y, self.alto_mapa - altura_actual))

            if y > self.alto_mapa:  # Usa el alto total del mapa (2240px) en lugar de ALTO
                x, y = ANCHO//2 - tamaño_normal//2, 0  # Opcional: Ajusta estas coordenadas si quieres
                velocidad_y = 0

            tiempo_animacion += dt
            if abs(movimiento_x) > 0 and tiempo_animacion > 0.1:
                indice_animacion = (indice_animacion + 1) % 2
                tiempo_animacion = 0

            # --- ANIMACIÓN Y MOVIMIENTO DE ENEMIGOS (con gravedad sobre plataforma) ---
            # --- ANIMACIÓN Y MOVIMIENTO DE ENEMIGOS (con gravedad sobre plataforma) ---
            for estado in enemigos_estados:
                # Movimiento horizontal con rebote en obstáculos
                enemigo_rect = pygame.Rect(
                       estado["x"], estado["y"], estado["personaje"].tamaño_pie, estado["personaje"].tamaño_pie
                )
                next_rect = enemigo_rect.move(estado["sentido"] * 2, 0)
                cambiar_sentido = False 
                # Limita el movimiento al ancho del mapa y rebote en obstáculos
                if (estado["x"] <=  estado["limite_izquierda"] and estado["sentido"]< 0) or \
                   (estado["x"] + estado["personaje"].tamaño_pie >= estado["limite_derecha"] and estado["sentido"] >0) or \
                   self.mapa.verificar_colision(next_rect):
                   estado["sentido"] *= -1
                   estado["direccion"] = "derecha" if estado["sentido"] > 0 else "izquierda"
                   cambiar_sentido = True 
                if not cambiar_sentido:
                     estado["x"] += estado["sentido"]*2
                estado["x"] = max(estado["limite_izquierda"], min(estado["x"], estado["limite_derecha"] - estado["personaje"].tamaño_pie))

                # Gravedad y plataformas para enemigos
                enemigo_rect = pygame.Rect(
                    estado["x"], estado["y"], estado["personaje"].tamaño_pie, estado["personaje"].tamaño_pie
                )
                enemigo_rect_abajo = enemigo_rect.move(0, 1)
                if not self.mapa.verificar_colision(enemigo_rect_abajo):
                    estado["velocidad_y"] += self.gravedad
                    estado["y"] += estado["velocidad_y"]
                    estado["en_suelo"] = False
                else:
                    # Ajusta para que el enemigo quede justo sobre la plataforma
                    estado["y"] = (int((estado["y"] + estado["personaje"].tamaño_pie) // TILE_SIZE) * TILE_SIZE) - estado["personaje"].tamaño_pie
                    estado["velocidad_y"] = 0
                    estado["en_suelo"] = True

                estado["tiempo_anim"] += dt
                if estado["tiempo_anim"] > 0.2:
                    estado["frame"] = (estado["frame"] + 1) % 2
                    estado["tiempo_anim"] = 0

            # --------- INTERACCIÓN: COLISIÓN JUGADOR-ENEMIGO ---------
            jugador_rect = pygame.Rect(
                x + hitbox_offset_x,
                y + self.HITBOX_OFFSET_Y,
                altura_actual - 2*hitbox_offset_x,
                altura_actual - self.HITBOX_OFFSET_Y
            )
            for estado in enemigos_estados:
                enemigo_rect = pygame.Rect(
                    estado["x"],
                    estado["y"],
                    estado["personaje"].tamaño_pie,
                    estado["personaje"].tamaño_pie
                )
                if jugador_rect.colliderect(enemigo_rect):
                    vidas -= 1
                    self.sonido_colision.play()
                    # Opcional: reposicionar al jugador para evitar múltiples pérdidas de vida instantáneas
                    x, y = ANCHO//2 - tamaño_normal//2, 0
                    velocidad_y = 0
                    break

                # Verificar pozos de muerte (si existe la capa)
                try:
                    for obj in self.mapa.mapa_tiled.get_layer_by_name("muerte"):
                        if hasattr(obj, 'x'):
                            muerte_rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                            if jugador_rect.colliderect(muerte_rect):
                                vidas -= 1
                                x, y = ANCHO//2, 0  # Reinicia en posición segura
                                self.sonido_gameover.play()  # Opcional: sonido al morir
                                break
                except:
                    pass  # Si no existe la capa, ignora

            # ===== DIBUJADO =====
            self.pantalla.blit(self.fondo_juego, (0, 0)) #self.pantalla.fill(self.COLORES['NEGRO'])
            self.mapa.dibujar(self.pantalla, self.camara_offset_x, self.camara_offset_y)
            # Jugador
            if agachado:
                img_key = f'agachado_{orientacion}'
                img = imagenes[img_key]
            else:
                img = imagenes[orientacion][indice_animacion]
            self.pantalla.blit(img, (x - self.camara_offset_x, y - self.camara_offset_y))
            pygame.draw.rect(
                self.pantalla, (255, 0, 0),
                (x - self.camara_offset_x + hitbox_offset_x,
                 y - self.camara_offset_y + self.HITBOX_OFFSET_Y,
                 altura_actual - 2*hitbox_offset_x,
                 altura_actual - self.HITBOX_OFFSET_Y),
                1
            )
            # Enemigos animados
            for estado in enemigos_estados:
                enemigo_img = estado["personaje"].obtener_imagen_animada(estado["direccion"], estado["frame"])
                self.pantalla.blit(
                    enemigo_img,
                    (estado["x"] - self.camara_offset_x, estado["y"] - self.camara_offset_y)
                )
                pygame.draw.rect(
                    self.pantalla, (255, 0, 255),
                    (estado["x"] - self.camara_offset_x, estado["y"] - self.camara_offset_y,
                     estado["personaje"].tamaño_pie, estado["personaje"].tamaño_pie),
                    1
                )

            # --------- MOSTRAR VIDAS ---------
            vidas_texto = fuente_vidas.render(f"Vidas: {vidas}", True, (255, 0, 0))
            self.pantalla.blit(vidas_texto, (20, 20))

            pygame.display.flip()

        # Si se sale del bucle porque vidas == 0, mostrar mensaje de game over
        if vidas == 0:
            pygame.mixer.music.stop()
            #se argrego sonido game over 
            self.sonido_gameover.play()
            duracion = int(self.sonido_gameover.get_length() * 1000)  # en milisegundos
            self.pantalla.fill((0, 0, 0))

            gameover = self.fuente.render("GAME OVER", True, (255, 0, 0))
            self.pantalla.blit(gameover, (ANCHO//2 - gameover.get_width()//2, ALTO//2 - gameover.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(duracion)

    def cargar_animaciones(self, personaje, tamaño_normal, tamaño_agachado):
        try:
            return {
                'izquierda': [
                    pygame.transform.scale(pygame.image.load(f"imagenes/{personaje.nombre}_caminar_izquierda_1.png"), (tamaño_normal, tamaño_normal)),
                    pygame.transform.scale(pygame.image.load(f"imagenes/{personaje.nombre}_caminar_izquierda_2.png"), (tamaño_normal, tamaño_normal))
                ],
                'derecha': [
                    pygame.transform.scale(pygame.image.load(f"imagenes/{personaje.nombre}_caminar_derecha_1.png"), (tamaño_normal, tamaño_normal)),
                    pygame.transform.scale(pygame.image.load(f"imagenes/{personaje.nombre}_caminar_derecha_2.png"), (tamaño_normal, tamaño_normal))
                ],
                'agachado_izquierda': pygame.transform.scale(
                    pygame.image.load(f"imagenes/{personaje.nombre}_agachado_izquierda.png"), (tamaño_agachado, tamaño_agachado)),
                'agachado_derecha': pygame.transform.scale(
                    pygame.image.load(f"imagenes/{personaje.nombre}_agachado_derecha.png"), (tamaño_agachado, tamaño_agachado))
            }
        except:
            print(f"Error cargando animaciones para {personaje.nombre}")
            animaciones = {}
            for dir in ['izquierda', 'derecha']:
                animaciones[dir] = [pygame.Surface((tamaño_normal, tamaño_normal)) for _ in range(2)]
            for dir in ['agachado_izquierda', 'agachado_derecha']:
                animaciones[dir] = pygame.Surface((tamaño_agachado, tamaño_agachado))
            return animaciones

    def calcular_posicion_inicial(self, x, y, tamaño):
        tile_x = x // TILE_SIZE
        for tile_y in range(len(self.mapa.mapa_data)):
            if self.mapa.mapa_data[tile_y][tile_x] == 0:
                return tile_y * TILE_SIZE - tamaño
        return ALTO - tamaño

    def juego(self):
        self.pantalla_inicio()
        corriendo = True
        while corriendo:
            self.pantalla_seleccion_personaje()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_a:
                        self.seleccion_personaje = (self.seleccion_personaje - 1) % len(self.personajes)
                    elif evento.key == pygame.K_d:
                        self.seleccion_personaje = (self.seleccion_personaje + 1) % len(self.personajes)
                    elif evento.key == pygame.K_SPACE:
                        self.pantalla_personaje_seleccionado(self.seleccion_personaje)

                            # 1 Mostrar pantalla de carga animada 
                        self.mostrar_pantalla_carga("musica_de_carga.mp3")

                        #    2 Crear una vista previa del mapa 1 (como fondo)
                        fondo_mapa = pygame.Surface((ANCHO, ALTO))
                        fondo_mapa.blit(self.fondo_juego, (0, 0))
                        self.mapa.dibujar(fondo_mapa, 0, 0)

                         # 3 Hacer transición con círculo que se abre al centro
                        self.transicion_apertura_circular_con_fondo(fondo_mapa)

                        # 4 Ahora sí inicia el juego
                        self.iniciar_juego(self.seleccion_personaje)
                        corriendo = False             
        pygame.quit()
        sys.exit()