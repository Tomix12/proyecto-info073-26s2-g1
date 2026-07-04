# Importamos módulos requeridos
import os
import random

import pygame

# Estados del juego
ESTADO_INICIO = "inicio"
ESTADO_INSTRUCCIONES = "instrucciones"
ESTADO_JUGANDO = "jugando"
ESTADO_DERROTA = "derrota"
ESTADO_VICTORIA = "victoria"
NIVEL=1
MAX_NIVELES=3
CONFIG_NIVELES = {
    1: {
        "vidas": 3,
        "tiempo": 40000,
        "obstaculos": 5,
        "fuegos": 2,
        "orbes": 2,
        "retraso":260,
        "animacion":200
    },

    2: {
        "vidas": 2,
        "tiempo": 45000,
        "obstaculos": 8,
        "fuegos": 4,
        "orbes": 3,
        "retraso":250,
        "animacion":180
    },

    3: {
        "vidas": 2,
        "tiempo": 40000,
        "obstaculos": 11,
        "fuegos": 6,
        "orbes": 4,
        "retraso":200,
        "animacion":140
    }
}
# Rutas a la carpeta de imágenes de pantallas
DIR_PANTALLAS = os.path.join(os.path.dirname(__file__), "data", "pantallas")

# Se específica el nombre del archivo para cada imagen de pantalla.
# El formato de imagen utilizado puede ser PNG, JPG/JPEG, BMP, o GIF.
PANTALLA_INICIO = "pantalla_inicio.bmp"
PANTALLA_INSTRUCCIONES = "pantalla_instrucciones.bmp"
PANTALLA_VICTORIA = "pantalla_victoria.bmp"
PANTALLA_DERROTA = "pantalla_derrota.bmp"

# Para evitar que el jugador se mueva demasiado rápido
RETRASO = 100

# Códigos de cada elemento del tablero
VACIO = 0
OBSTACULO = 1
JUGADOR = 2
PUERTA = 3
ORBE = 4
PLACA = 5
FUEGO = 6


# Tamaño del tablero
# Si se cambian estas constantes, se debe modificar la definición
# del tablero que se encuentra1 en función reiniciar().
FILAS = 15
COLUMNAS = 15

def aparecer_varios(tablero, id_elem1, id_elem2, distancia, cantidad):
    for num in range(cantidad):
        aparecer_restringido(tablero, id_elem1, id_elem2, distancia)

def aparecer_aleatorio(tablero, id_elem):
    """
    Coloca un elemento en una casilla vacía aleatoria del tablero.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
        - id_elem: El número identificador del elemento que queremos colocar.

    Retorna:
        - (columna, fila): Tupla que indica posición en la que se colocó el elemento.
    """

    # Debemos detectar los espacios vacíos, para ello recorremos
    # el tablero y almacenamos tuplas de (columna, fila) las posiciones
    # en las que un elemento "VACIO" (el número 0 en este caso) se encuentre.
    vacios = []

    # Forma vista en clases de recorrer el arreglo multidimensional.
    # Tanto fila como columna son números.
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            # Obtenemos el elemento que se encuentra en esa fila y columna.
            elem_pos = tablero[fila][columna]

            if elem_pos == VACIO:
                # Al utilizar los paréntesis () dentro de la función, lo estaremos
                # añadiendo como una tupla con la estructura (columna, fila).
                vacios.append((columna, fila))

    # También se puede utilizar comprensión de listas para rellenar el arreglo
    # a la vez que lo recorremos:
    #
    # vacios = [
    #     (columna, fila)
    #     for fila in range(FILAS)
    #     for columna in range(COLUMNAS)
    #     if tablero[fila][columna] == VACIO
    # ]

    # Si no hay casillas vacías, retornamos un valor especial.
    if len(vacios) == 0:
        return -1, -1

    # Usando la función random.choice(lista) podremos obtener una tupla
    # aleatoria desde el arreglo "vacios" que definimos anteriormente.
    columna, fila = random.choice(vacios)

    # Finalmente, colocamos el elemento al poner su número en la casilla
    # del tablero correspondiente.
    tablero[fila][columna] = id_elem

    return columna, fila

def aparecer_restringido(tablero, id_elem1, id_elem2, distancia):
    if isinstance(id_elem2, int):
        id_elem2 = (id_elem2,)
    vacios = []

    for fila in range(FILAS):
        for columna in range(COLUMNAS):

            if tablero[fila][columna] != VACIO:
                continue

            permitido = True

            for f in range(FILAS):
                for c in range(COLUMNAS):

                    if tablero[f][c] in id_elem2:

                        if (columna-c)**2 + (fila-f)**2 <= distancia**2:
                            permitido = False
                            break

                if not permitido:
                    break

            if permitido:
                vacios.append((columna, fila))

    if len(vacios) == 0:
        return -1, -1

    columna, fila = random.choice(vacios)
    tablero[fila][columna] = id_elem1

    return columna, fila

def poblar_tablero(tablero,nivel):
    datos = CONFIG_NIVELES[nivel]
    aparecer_varios(
        tablero,
        OBSTACULO,
        (OBSTACULO, JUGADOR),
        1,
        datos["obstaculos"]
    )
    aparecer_varios(
        tablero,
        ORBE,
        (ORBE, JUGADOR),
        6,
        datos["orbes"]
    )
    aparecer_varios(
        tablero,
        FUEGO,
        (FUEGO, JUGADOR),
        3,
        datos["fuegos"]
    )
def refrescar_tablero(screen, tablero, fondo, roca, sprite_actual, sprite_puerta, sprite_fuego, sprite_manzana, sprite_placa,nivel,vidas,tiempo_restante):
    """
    Dibuja el estado actual del tablero en la pantalla.

    Parámetros:
        - screen: La pantalla sobre la cual estamos dibujando.
        - tablero: El tablero con sus posiciones actuales.
    """

    # Rellena la pantalla con el color gris, básicamente pintando
    # por encima de lo que estaba anteriormente.
    screen.blit(fondo, (0,0))# modifique el codigo que pinta para que en vez de pintar la pantalla ponga la imagen 

    # Podemos calcular el tamaño en pixeles que tendrá cada
    # casilla al dividir tanto la altura de la pantalla (screen.get_height())
    # como el ancho (screen.get_width()) por la cantidad de filas y columnas respectivamente.
    # Por ejemplo en este caso alto_elem sería 800 / 15 = 53.3, lo que nos indica que la
    # altura de cada elemento es de 53.3 píxeles.
    alto_elem = screen.get_height() / FILAS
    ancho_elem = screen.get_width() / COLUMNAS
    # Como el jugador es un círculo, se necesita el radio.
    radio = ancho_elem / 2

    # Posición en eje "y" en unidad de píxeles.
    pos_y = 0

    for i in range(FILAS):
        # Posición en eje "x" en unidad de píxeles.
        pos_x = 0
        for j in range(COLUMNAS):
            if tablero[i][j] == OBSTACULO:
                roca_escalada = pygame.transform.scale(roca,(int(ancho_elem)*1.4, int(alto_elem)*1.4))
                screen.blit(roca_escalada,(pos_x,pos_y))
            elif tablero[i][j] == JUGADOR:
                 screen.blit(sprite_actual,(pos_x,pos_y))
                
            elif tablero[i][j] == ORBE: 
                screen.blit(sprite_manzana, (pos_x, pos_y))
            elif tablero[i][j] == FUEGO:
                 screen.blit(sprite_fuego, (pos_x, pos_y))
            elif tablero[i][j] == PUERTA:
                screen.blit(sprite_puerta, (pos_x, pos_y))
            elif tablero[i][j] == PLACA:
                screen.blit(sprite_placa,(pos_x,pos_y))
            # Estamos recorriendo los píxeles de la pantalla, por lo que
            # debemos sumar el ancho y altura en pixeles de cada elemento que
            # ya hayamos recorrido para avanzar al siguiente.
            pos_x += ancho_elem
        pos_y += alto_elem

    fuente = pygame.font.SysFont("Arial", 22)

    texto = fuente.render(
    f"Nivel {nivel}    Vidas: {vidas}    Tiempo: {tiempo_restante}",
             True,
             (255,255,255)
            )

    screen.blit(texto,(10,10))
    
    
    # Refresca el contenido que se ve en pantalla.
    pygame.display.flip()


def cambiar_direccion(keys, direccion_actual):
    """
    Cambia la dirección del jugador.

    Parámetros:
        - keys: Arreglo de teclas presionadas.
        - direccion_actual: La dirección en la que estaba avanzando justo antes de analizar
            si hubo un cambio de dirección.

    Retorna:
        - direccion_actual: La nueva dirección del jugador.
    """

    # Tecla W
    if keys[pygame.K_w]:
        # La tupla nos indica que horizontalmente (columnas) no hará nada (0) y
        # que verticalmente (filas) disminuirá el índice en el tablero (-1).
        return (0, -1)

    # Tecla S
    if keys[pygame.K_s]:
        # En este caso avanzará a través de las filas del tablero.
        return (0, 1)

    # Tecla A
    if keys[pygame.K_a]:
        # Retrocede por las columnas del tablero.
        return (-1, 0)

    # Tecla D
    if keys[pygame.K_d]:
        # Avanza por las columnas del tablero.
        return (1, 0)

    # Si no se presiona ninguna de las teclas anteriores, la dirección
    # será la misma que la anterior.
    return direccion_actual


def avanzar(tablero, pos_jugador, direccion):
    """
    Avanza el jugador un paso en la dirección dada.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
        - pos_jugador: Tupla con la posición actual (índice con
            estructura (columna, fila)) del jugador en el tablero.
        - direccion: Tupla con la dirección en la que está avanzando actualmente el jugador.

    Retorna:
        - (resultado, nueva_pos_jugador): Retorna el resultado que se obtiene
            al avanzar (derrota, victoria o "ok" (no cambia de pantalla)) y la nueva posición del jugador.
    """

    # Obtenemos los componentes "x" e "y" de cada tupla recibida
    # con información de la dirección y posición del jugador.
    dir_col, dir_fila = direccion
    ind_actual_col, ind_actual_fila = (
        pos_jugador  # Tupla (columna, fila) que representa los índices en el tablero.
    )

    # Aplicamos la dirección a la posición del jugador.
    ind_nueva_col = ind_actual_col + dir_col
    ind_nueva_fila = ind_actual_fila + dir_fila

    # Verificamos que no haya choque con el borde del tablero.
    if not (0 <= ind_nueva_col < COLUMNAS and 0 <= ind_nueva_fila < FILAS):
        return "derrota", pos_jugador

    # Obtenemos el elemento que se encuentre en el tablero en la nueva posición del jugador.
    pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

    if pos_elem == OBSTACULO:
        return "derrota", pos_jugador

    if pos_elem == PUERTA:
        return "victoria", (ind_nueva_col, ind_nueva_fila)
    
    if pos_elem == ORBE:
        tablero[ind_actual_fila][ind_actual_col] = VACIO
        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR
        return "orbe", (ind_nueva_col, ind_nueva_fila)
   
    if pos_elem == FUEGO:
        tablero[ind_actual_fila][ind_actual_col] = VACIO
        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR
        return "fuego", (ind_nueva_col, ind_nueva_fila)
   
    if pos_elem == PLACA:
        tablero[ind_actual_fila][ind_actual_col] = VACIO
        tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR
        return "placa", (ind_nueva_col, ind_nueva_fila)
    # Movimiento normal, si es que no encontramos manzana ni obstáculo.
    tablero[ind_actual_fila][ind_actual_col] = VACIO
    tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR

    return "ok", (ind_nueva_col, ind_nueva_fila)
def reiniciar(nivel):
    """
    Crea un nuevo tablero y estado para una nueva partida.

    Retorna:
        - (tablero, pos_jugador): Tablero nuevo y la nueva posición aleatoria del jugador.
            pos_jugador corresponda a una tupla (columna, fila) donde columna y fila son índices
            de matriz tablero.
    """

    # Si se modifica constante FILAS o COLUMNAS al inicio, también
    # se debe modificar este arreglo de tablero con los valores correspondientes.
    # Esto puede ser mejorado usando dos bucles "for" anidados o comprensión de listas.
    tablero = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    # Usando dos bucles "for" anidados se haría de la siguiente manera:
    # tablero = []
    # for _ in range(FILAS):
    #     fila_tablero = []
    #
    #     for _ in range(COLUMNAS):
    #         fila_tablero.append(VACIO)
    #
    #     tablero.append(fila_tablero)
    # Otra manera usando comprensión de listas:
    # tablero = [[VACIO] * COLUMNAS for _ in range(FILAS)]
    # El _ en el "for" indica que no usamos la variable con la que iteramos.

    poblar_tablero(tablero, nivel)

    # Colocamos al jugador en una posición aleatoria.
    pos_jugador = aparecer_aleatorio(tablero, JUGADOR)

    return tablero, pos_jugador


def mostrar_pantalla(screen, nombre_archivo):
    """
    Carga una imagen y la muestra escalada a la ventana.

    Parámetros:
        - screen: La pantalla donde colocaremos la imagen.
        - nombre_archivo: El nombre del archivo de la imagen.
    """

    ruta = os.path.join(DIR_PANTALLAS, nombre_archivo)

    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, screen.get_size())

        # Dibujamos la imagen en la pantalla en la coordenada (0, 0).
        screen.blit(imagen, (0, 0))

        # Refrescamos pantalla.
        pygame.display.flip()
    except FileNotFoundError:
        # Fallback de seguridad en caso de que las imágenes no existan aún
        screen.fill("black")
        pygame.display.flip()
        print(f"Advertencia: No se encontró la imagen {ruta}")


def main():
    pygame.init()
    pygame.mixer.music.load("data/sonidos/musica.mp3")
    pygame.mixer.music.set_volume(0.5)  # 0.0 a 1.0
    sonido_orbe = pygame.mixer.Sound("data/sonidos/orbe.wav")
    sonido_placa = pygame.mixer.Sound("data/sonidos/placa.wav")
    DIR_BACKGROUND= os.path.join(os.path.dirname(__file__),"data","background","Fondo.jpg") #Esto es del fondo en carpeta background que subire
    fondo=pygame.image.load(DIR_BACKGROUND)         #Nota de Tomás: este codigo carga el directorio del fondo  
    fondo= pygame.transform.scale(fondo, (800, 800)) #Este codigo transforma la escala de la imagen a 800x800 pixeles(aunque lo cambie antes de ingresaar)
    DIR_roca=os.path.join("data","sprites","OBSTACULO.png")#Nota tomás: ruta de la roca     
    screen= pygame.display.set_mode((800, 800))#Esta es la escala en la que correra el juego(no la imagen)
    # por aqui importamos los archivos sprites de los mvimentos de los personajes
    frente=[pygame.image.load("data/personaje/01.png").convert_alpha(),pygame.image.load("data/personaje/02.png").convert_alpha(), pygame.image.load("data/personaje/03.png").convert_alpha(), pygame.image.load("data/personaje/04.png").convert_alpha()]
    espalda=[pygame.image.load("data/personaje/05.png").convert_alpha(),pygame.image.load("data/personaje/06.png").convert_alpha(), pygame.image.load("data/personaje/07.png").convert_alpha(), pygame.image.load("data/personaje/08.png").convert_alpha()]
    izquierda=[pygame.image.load("data/personaje/09.png").convert_alpha(),pygame.image.load("data/personaje/10.png").convert_alpha(), pygame.image.load("data/personaje/11.png").convert_alpha(), pygame.image.load("data/personaje/12.png").convert_alpha()]
    derecha=[pygame.image.load("data/personaje/13.png").convert_alpha(),pygame.image.load("data/personaje/14.png").convert_alpha(), pygame.image.load("data/personaje/15.png").convert_alpha(), pygame.image.load("data/personaje/16.png").convert_alpha()]
    #Definimos el tamaño de celda para ajustar la escala del mono a la celda y no hayan incosistencias  
    tam_celda=800//15
    sprite_puerta = pygame.image.load("data/sprites/puerta.png").convert_alpha()
    sprite_puerta = pygame.transform.scale(sprite_puerta, (tam_celda, tam_celda))
    sprite_fuego = pygame.image.load("data/sprites/fuego.png").convert_alpha()
    sprite_fuego = pygame.transform.scale(sprite_fuego, (tam_celda, tam_celda))
    sprite_manzana = pygame.image.load("data/sprites/orbe.png").convert_alpha()
    sprite_manzana = pygame.transform.scale(sprite_manzana, (tam_celda, tam_celda))
    sprite_placa = pygame.image.load("data/sprites/placa.png").convert_alpha()
    sprite_placa = pygame.transform.scale(sprite_placa, (tam_celda, tam_celda))
    frente=[pygame.transform.scale(s,(tam_celda, tam_celda)) for s in frente]
    espalda=[pygame.transform.scale(s,(tam_celda, tam_celda)) for s in espalda]
    izquierda=[pygame.transform.scale(s,(tam_celda, tam_celda)) for s in izquierda]
    derecha=[pygame.transform.scale(s,(tam_celda, tam_celda)) for s in derecha]
    roca=pygame.image.load(DIR_roca).convert_alpha()
    # Establecemos el título de la ventana.
    pygame.display.set_caption("Crimson")

    running = True

    estado = ESTADO_INICIO
    tablero = []
    pos_jugador = (0, 0)
    direccion = (0, 0)
    frame_actual=0
    tiempo_animacion = 0
    velocidad_animacion = 120
    sprite_actual= frente[0]
    tiempo_ultimo_mov = 0
    NIVEL = 1
    VIDAS = CONFIG_NIVELES[NIVEL]["vidas"]
    RETRASO = CONFIG_NIVELES[NIVEL]["retraso"]
    NUM_ORBES = 0
    NUM_PLACAS = 0
    velocidad_animacion =CONFIG_NIVELES[NIVEL]["animacion"]
    tiempo_inicio = None
    cronometro_activo = False
    TIEMPO_LIMITE = CONFIG_NIVELES[NIVEL]["tiempo"]
    mostrar_pantalla(screen, PANTALLA_INICIO)
    tiempo_restante = TIEMPO_LIMITE // 1000

    # Este es el bucle principal del juego, todo lo que sucede en el juego
    
    # está aquí.
    while running:
        # Se analizan los eventos del bucle actual.
        for evento in pygame.event.get():
            # Si es que se quiere cerrar la ventana.
            if evento.type == pygame.QUIT:
                running = False

            # Si es que se presiona alguna tecla.
            if evento.type == pygame.KEYDOWN:
                if estado == ESTADO_INICIO:
                    if evento.key == pygame.K_SPACE:
                        NIVEL=1
                        tablero, pos_jugador=reiniciar(NIVEL)
                        VIDAS=CONFIG_NIVELES[NIVEL]["vidas"]
                        TIEMPO_LIMITE = CONFIG_NIVELES[NIVEL]["tiempo"]
                        RETRASO=CONFIG_NIVELES[NIVEL]["retraso"]
                        velocidad_animacion=CONFIG_NIVELES[NIVEL]["animacion"]
                        tiempo_restante=TIEMPO_LIMITE//1000
                        direccion = (0, 0)
                        # Obtiene tiempo en milisegundos
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        pygame.mixer.music.play(-1)
                        tiempo_inicio = None
                        cronometro_activo = False
                        refrescar_tablero(screen, tablero, fondo, roca, sprite_actual, sprite_puerta, sprite_fuego, sprite_manzana, sprite_placa, NIVEL,VIDAS,tiempo_restante)
                    elif evento.key == pygame.K_i:
                        estado = ESTADO_INSTRUCCIONES
                        mostrar_pantalla(screen, PANTALLA_INSTRUCCIONES)

                elif estado == ESTADO_INSTRUCCIONES:
                    estado = ESTADO_INICIO
                    mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado in (ESTADO_DERROTA, ESTADO_VICTORIA):
                    if evento.key == pygame.K_r:
                        NIVEL=1
                        tablero, pos_jugador = reiniciar(NIVEL)
                        VIDAS= CONFIG_NIVELES[NIVEL]["vidas"]
                        TIEMPO_LIMITE=CONFIG_NIVELES[NIVEL]["tiempo"]
                        RETRASO=CONFIG_NIVELES[NIVEL]["retraso"]
                        NUM_ORBES=0
                        velocidad_animacion=CONFIG_NIVELES[NIVEL]["animacion"]
                        tiempo_restante=TIEMPO_LIMITE//1000
                        direccion = (0, 0)
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        pygame.mixer.music.play(-1)
                        tiempo_inicio = None
                        cronometro_activo = False
                        refrescar_tablero(screen, tablero, fondo, roca, sprite_actual, sprite_puerta, sprite_fuego, sprite_manzana, sprite_placa,NIVEL,VIDAS,tiempo_restante)

                    if evento.key == pygame.K_ESCAPE:
                        estado = ESTADO_INICIO
                        mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado == ESTADO_JUGANDO:
                    keys=pygame.key.get_pressed()
                    if not cronometro_activo and (
                        keys[pygame.K_w] or
                        keys[pygame.K_s] or
                        keys[pygame.K_a] or
                        keys[pygame.K_d]
                    ):
                        tiempo_inicio = pygame.time.get_ticks()
                        cronometro_activo = True
                    if keys[pygame.K_w]:
                        direccion=(0,-1)
                        sprite_actual=espalda[frame_actual]
                    elif keys[pygame.K_s]:
                        direccion=(0,1)
                        sprite_actual=frente[frame_actual]          
                    elif keys[pygame.K_a]:
                        direccion=(-1,0)
                        sprite_actual=izquierda[frame_actual]
                    elif  keys[pygame.K_d]:
                        direccion=(1,0) 
                        sprite_actual=derecha[frame_actual]
                                

        if estado == ESTADO_JUGANDO:
          tiempo_actual = pygame.time.get_ticks()  # En milisegundos
          if cronometro_activo:
            tiempo_transcurrido = tiempo_actual - tiempo_inicio
            tiempo_restante=max(0,(TIEMPO_LIMITE-tiempo_transcurrido)//1000)

            if tiempo_transcurrido >= TIEMPO_LIMITE:
                    pygame.mixer.music.stop()
                    estado = ESTADO_DERROTA
                    mostrar_pantalla(screen, PANTALLA_DERROTA)
          #animacion
        if direccion != (0,0) and tiempo_actual - tiempo_animacion >= velocidad_animacion:
            frame_actual = (frame_actual + 1) % 4
            tiempo_animacion = tiempo_actual
            if direccion == (0,-1):
                sprite_actual = espalda[frame_actual]
            elif direccion==(0,1):
                sprite_actual=frente[frame_actual]
            elif direccion==(-1,0):
                sprite_actual=izquierda[frame_actual]
            elif direccion==(1,0):
                sprite_actual=derecha[frame_actual]
            refrescar_tablero(screen, tablero, fondo, roca, sprite_actual, sprite_puerta, sprite_fuego, sprite_manzana, sprite_placa,NIVEL,VIDAS,tiempo_restante)
 
            if direccion != (0, 0) and tiempo_actual - tiempo_ultimo_mov >= RETRASO:
                resultado, pos_jugador = avanzar(tablero, pos_jugador, direccion)
                if direccion==(0,-1):
                    sprite_actual=espalda[frame_actual]
                elif direccion==(0,1):
                    sprite_actual=frente[frame_actual]
                elif direccion==(-1,0):
                    sprite_actual=izquierda[frame_actual]
                elif direccion==(1,0):
                    sprite_actual=derecha[frame_actual]
                if resultado == "derrota":
                    pygame.mixer.music.stop()
                    estado = ESTADO_DERROTA
                    mostrar_pantalla(screen, PANTALLA_DERROTA)
                    NIVEL=1
                    VIDAS=CONFIG_NIVELES[NIVEL]["vidas"]
                    RETRASO=CONFIG_NIVELES[NIVEL]["retraso"]
                    velocidad_animacion=CONFIG_NIVELES[NIVEL]["animacion"]
                    NUM_ORBES=0
                    NUM_PLACAS=0
                    NIVEL=1
                    TIEMPO_LIMITE=CONFIG_NIVELES[NIVEL]["tiempo"]
                    tiempo_restante= TIEMPO_LIMITE//1000
                    cronometro_activo= False
                    tiempo_inicio= None
                    direccion=(0,0)
                elif resultado == "victoria":
                    if NIVEL < MAX_NIVELES:

                        NIVEL += 1

                        tablero, pos_jugador = reiniciar(NIVEL)

                        VIDAS = CONFIG_NIVELES[NIVEL]["vidas"]
                        TIEMPO_LIMITE = CONFIG_NIVELES[NIVEL]["tiempo"]
                        tiempo_ultimo_mov=pygame.time.get_ticks()
                        tiempo_restante= TIEMPO_LIMITE//1000

                        NUM_ORBES = 0
                        NUM_PLACAS = 0
                        if NIVEL == 1:
                            RETRASO = CONFIG_NIVELES[NIVEL]["retraso"]
                            velocidad_animacion = CONFIG_NIVELES[NIVEL]["animacion"]

                        elif NIVEL == 2:
                            RETRASO = CONFIG_NIVELES[NIVEL]["retraso"]
                            velocidad_animacion = CONFIG_NIVELES[NIVEL]["animacion"]

                        elif NIVEL == 3:
                            RETRASO = CONFIG_NIVELES[NIVEL]["retraso"]
                            velocidad_animacion = CONFIG_NIVELES[NIVEL]["animacion"]

                        direccion = (0, 0)

                        tiempo_inicio = None
                        cronometro_activo = False

                        refrescar_tablero(screen,tablero,fondo,roca,sprite_actual, sprite_puerta,sprite_fuego, sprite_manzana ,sprite_placa,NIVEL,VIDAS,tiempo_restante )

                    else:

                     pygame.mixer.music.stop()

                     estado = ESTADO_VICTORIA

                     mostrar_pantalla(screen,PANTALLA_VICTORIA )
                     NIVEL = 1
                     VIDAS = CONFIG_NIVELES[NIVEL]["vidas"]
                     TIEMPO_LIMITE=CONFIG_NIVELES[NIVEL]["tiempo"]
                     RETRASO = CONFIG_NIVELES[NIVEL]["retraso"]
                     velocidad_animacion=CONFIG_NIVELES[NIVEL]["animacion"]
                     direccion=(0,0)
                     cronometro_activo= False
                     tiempo_inicio= None
                     NUM_ORBES = 0
                     NUM_PLACAS = 0
                elif resultado == "orbe":
                    sonido_orbe.play() 
                    NUM_ORBES += 1
                    if NIVEL==1:
                      RETRASO -= 30
                      velocidad_animacion -=20
                    elif NIVEL==2:
                        RETRASO-=20
                        velocidad_animacion-=10
                    elif NIVEL==3:
                        RETRASO-=15
                        velocidad_animacion-=9    
                    if NUM_ORBES == CONFIG_NIVELES[NIVEL]["orbes"]:
                        aparecer_restringido(tablero, PLACA, JUGADOR, 5)
                        aparecer_varios(tablero, FUEGO, (FUEGO,JUGADOR), 2, 2)
                    tiempo_ultimo_mov = tiempo_actual
                    refrescar_tablero(screen, tablero, fondo, roca, sprite_actual, sprite_puerta, sprite_fuego, sprite_manzana, sprite_placa,NIVEL,VIDAS,tiempo_restante)
                elif resultado == "placa":
                    sonido_placa.play()
                    NUM_ORBES=0
                    NUM_PLACAS += 1

                    if NUM_PLACAS < 3:
                        aparecer_varios(tablero, ORBE, (ORBE,JUGADOR), 6, CONFIG_NIVELES[NIVEL]["orbes"])
                        aparecer_varios(tablero, FUEGO, (FUEGO,JUGADOR), 2, 2)

                    if NUM_PLACAS == 3:
                        aparecer_restringido(tablero, PUERTA, JUGADOR, 7)
                        aparecer_varios(tablero, FUEGO, (FUEGO,JUGADOR), 2, 2)

                    tiempo_ultimo_mov = tiempo_actual
                    refrescar_tablero(screen, tablero, fondo, roca, sprite_actual, sprite_puerta, sprite_fuego, sprite_manzana, sprite_placa,NIVEL,VIDAS,tiempo_restante)

                elif resultado == "fuego":
                    VIDAS -= 1
                    if RETRASO != CONFIG_NIVELES[NIVEL]["retraso"]:
                      if NIVEL==1:
                        RETRASO += 30
                        velocidad_animacion +=20
                      elif NIVEL==2:
                          RETRASO+=20
                          velocidad_animacion+=10
                      elif NIVEL==3:
                          RETRASO+=15
                          velocidad_animacion+=9                   
                    tiempo_ultimo_mov = tiempo_actual
                    refrescar_tablero(screen, tablero, fondo, roca, sprite_actual, sprite_puerta, sprite_fuego, sprite_manzana, sprite_placa,NIVEL,VIDAS,tiempo_restante)

                    if VIDAS == 0:
                        estado = ESTADO_DERROTA
                        pygame.mixer.music.stop()
                        mostrar_pantalla(screen, PANTALLA_DERROTA)
                        VIDAS=CONFIG_NIVELES[NIVEL]["vidas"]
                        RETRASO=CONFIG_NIVELES[NIVEL]["retraso"]
                        velocidad_animacion=CONFIG_NIVELES[NIVEL]["animacion"]
                        NUM_ORBES=0
                        NUM_PLACAS=0

                else:
                    tiempo_ultimo_mov = tiempo_actual
                    refrescar_tablero(screen, tablero, fondo, roca, sprite_actual, sprite_puerta, sprite_fuego, sprite_manzana, sprite_placa,NIVEL,VIDAS,tiempo_restante)

    pygame.quit()


if __name__ == "__main__":
    main()