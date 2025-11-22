# Für User Input und UI
import pygame as p
import os
import SchachEngine

p.init()
WIDTH = HEIGHT = 512*2
DIMNESION = 8  # Weil 8x8
SQ_SIZE = HEIGHT // DIMNESION
MAX_FPS = 15  # Für Animation
IMAGES = {}

"""
Bilder Laden in einem Globalen Dictionary, damit nur 1 mal in Main geladen wird    
"""


def loadImages():
    # IMAGES['wP'] = p.image.load("Figuren/wp.png") # Nicht so optimal
    pieces = [
        "wQ",
        "wK",
        "wB",
        "wN",
        "wR",
        "wp",
        "bQ",
        "bK",
        "bB",
        "bN",
        "bR",
        "bp",
    ]  # besser
    for piece in pieces:
        try:
            image_path_png = os.path.join("Figuren_png/" + piece + ".png")
            IMAGES[piece] = p.transform.scale(
                p.image.load(image_path_png),
                (SQ_SIZE, SQ_SIZE),
            )
        except p.error:
            # Wenn das Laden der PNG fehlschlägt (z.B. Datei nicht gefunden), versuche die BMP-Version
            print(f"Warnung: {image_path_png} konnte nicht geladen werden. Versuche stattdessen die BMP-Version.")
            image_path_bmp = os.path.join("Figuren_bmp/" + piece + ".bmp")
            try:
                IMAGES[piece] = p.transform.scale(
                    p.image.load(image_path_bmp),
                    (SQ_SIZE, SQ_SIZE),
                )
            except p.error:
                # Wenn auch die BMP fehlschlägt
                print(f"Fehler: Weder {image_path_png} noch {image_path_bmp} konnten für {piece} geladen werden.")

"""
Main Driver der User Input liest und Grafik updatet
"""


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = SchachEngine.GameState()
    loadImages()  # Nur 1mal Laden was gut ist
    running = True
    sqselected = ()  # Kein Feld selected am Anfang (tuple: (row,col))
    playerClick = []  # Klicks des Users werden gespeichert (two tuples: [(6,4), (4,4)])

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqselected == (row, col):  # User clickt 2 mal dasselbe Feld
                    sqselected = ()  # unselect
                    playerClick = []  # unselect
                else:
                    sqselected = (row, col)
                    playerClick.append(sqselected)  # append für beide clicks
                if len(playerClick) == 2:
                    move = SchachEngine.Move(playerClick[0], playerClick[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqselected = ()  # reset user klick
                    playerClick = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Für die Game Grafik
"""


def drawGameState(screen, gs):
    drawBoard(screen)
    # Add highliting later
    drawPieces(screen, gs.board)


"""
Zeichnet pieces bzw die Felder auf board
"""


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMNESION):
        for c in range(DIMNESION):
            color = colors[((r + c) % 2)]
            p.draw.rect(
                screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            )


def drawPieces(screen, board):
    for r in range(DIMNESION):
        for c in range(DIMNESION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(
                    IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE)
                )


if __name__ == "__main__":
    main()
