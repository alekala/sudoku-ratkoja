# -*- coding: utf-8 -*-

import pygame, sys
from requests import get
from bs4 import BeautifulSoup

"""
board = [
    [4, 1, 0, 0, 8, 0, 0, 0, 3],
    [0, 7, 0, 0, 0, 1, 0, 4, 9],
    [5, 3, 6, 9, 0, 4, 0, 0, 0],
    [0, 6, 1, 0, 0, 0, 8, 0, 7],
    [0, 0, 0, 0, 6, 0, 0, 0, 0],
    [7, 0, 4, 0, 0, 0, 5, 9, 0],
    [0, 0, 0, 4, 0, 2, 9, 6, 8],
    [6, 8, 0, 1, 0, 0, 0, 7, 0],
    [9, 0, 0, 0, 7, 0, 0, 3, 5]
]
"""

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "lightGray": (200, 200, 200),
    "darkGray": (150, 150, 150),
    "blue": (0, 200, 255)
}

class Scraper:
    def __init__(self, site):
        self.site = site
        self.request = get(site)
        self.soup = BeautifulSoup(request.text, "html.parser")

class Button:
    def __init__(self, x, y, width, height, text="", function=None, color=(colors["lightGray"]), highlight=(colors["darkGray"])):
        self.image = pygame.Surface((width, height))
        self.pos = (x, y)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.text = text
        self.function = function
        self.color = color
        self.highlight = highlight
        self.highlighted = False
        self.font = pygame.font.SysFont("cambria", 60 // 4)
    
    """
    Tarkastaa onko nappulan päällä
    hiiri ja muuttaa `highlighted`
    sen mukaisesti
    """
    def update(self, mouse):
        if self.rect.collidepoint(mouse):
            self.highlighted = True
        else:
            self.highlighted = False

    """
    Piirtää nappulan annetulle
    `window` ikkunalle
    """
    def draw(self, window):
        fontPos = [460, 580]
        font = self.font.render(self.text, False, colors["black"])
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        fontPos[0] += (100 - fontWidth) // 2
        fontPos[1] += (60 - fontHeight) // 2
        if self.highlighted:
            self.image.fill(self.highlight)
        else:
            self.image.fill(self.color)
        window.blit(self.image, self.pos)
        window.blit(font, fontPos)

class Sudoku:
    def __init__(self, bo):
        pygame.init()
        self.bo = bo
        self.win = pygame.display.set_mode((580, 660))
        self.running = True
        self.mousePos = None
        self.buttons = []
        self.loadButtons()
        self.font = pygame.font.SysFont("cambria", 60 // 2)
        self.solved = False
        pygame.display.set_caption("Sudoku")

    """
    Ratkaisee sudokun ja visualisoi
    algoritmin liikkeet
    """
    def solve(self):
        bo = self.bo
        emptyFound = self.findEmptyCell(bo)
        if emptyFound:
            x, y = emptyFound
        else:
            return True

        for digit in range(1, 10):
            safe = self.checkConflict((x, y), bo, digit)
            if safe:
                bo[y][x] = digit
                self.draw()
                self.events()
                pygame.time.delay(5)
                if self.solve():
                    self.solved = True
                    return True
                bo[y][x] = 0

        return False
    
    """
    Etsii annetulta pelilaudalta
    `bo` tyhjän solun
    """
    def findEmptyCell(self, bo):
        for y in range(len(bo)):
            for x in range(len(bo[0])):
                if bo[y][x] is 0:
                    return x, y
        return None
    
    """
    Tarkastaa onko samassa rivissä,
    sarakkeessa tai 3x3 ruudussa
    vielä samaa numeroa
    """
    def checkConflict(self, pos, bo, num):
        # Tarkista rivi
        for index, x in enumerate(bo[pos[1]]):
            if x is num and pos[0] is not index:
                return False
        
        # Tarkista sarake
        # for index, y in enumerate(bo):
        #     if y[pos[0]] is num and pos[0] is not index:
        #         return False
        
        for index in range(0, len(bo)):
            if bo[index][pos[0]] is num and pos[0] is not index:
                return False

        # Tarkista ruutu
        groupX = pos[0] // 3
        groupY = pos[1] // 3
    
        for y in range(groupY * 3, groupY * 3 + 3):
            for x in range(groupX * 3, groupX * 3 + 3):
                if bo[y][x] is num and (x, y) is not pos:
                    return False
        
        return True

    """
    Pääsilmukka jolla ikkuna pyörii
    """
    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    """
    Hoitaa tapahtumat, kuten
    nappuloiden painallukset
    """
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.buttons[0].rect.collidepoint(self.mousePos):
                    self.solve()
    
    """
    Päivittää nappuloiden tilat sekä
    hiiren sijainnin nappulan tietoon
    """
    def update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(self.mousePos)

    """
    Piirtää ikkunan elementit
    """
    def draw(self):
        self.win.fill(colors["white"])
        self.drawGrid(self.win)
        for button in self.buttons:
            button.draw(self.win)
        self.drawNumbers(self.win)
        pygame.display.update()
    
    """
    Piirtää pysty- ja vaakaviivat
    ruudukolle
    """
    def drawGrid(self, window):
        pygame.draw.rect(window, colors["black"], (0 + 20, 0 + 20, 540, 540), 4)
        for i in range(0, 9):
            # Pystyviivat
            pygame.draw.line(window, colors["black"], (20 + (i * 60), 20),  (20 + (i * 60), 560), 4 if i % 3 == 0 else 1)
            # Vaakaviivat
            pygame.draw.line(window, colors["black"], (20, 20 + (i * 60)),  (560, 20 + (i * 60)), 4 if i % 3 == 0 else 1)
    
    """
    Piirtää numerot ruudukolle
    apumetodin `drawDigit` avulla
    """
    def drawNumbers(self, window):
        for x, row in enumerate(self.bo):
            for y, num in enumerate(row):
                if num is not 0:
                    pos = [(x * 60) + 20, (y * 60) + 20]
                    self.drawDigit(window, str(num), pos)

    """
    Luo nappulalle objektin
    """
    def loadButtons(self):
        self.buttons.append(Button(460, 580, 100, 60, text="Ratkaise", function=self.solve))
    
    """
    Piirtää yhden kirjaimen sekä
    laskee fontin koon
    """
    def drawDigit(self, window, text, pos, color=colors["black"]):
        font = self.font.render(text, False, color)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (60 - fontWidth) // 2
        pos[1] += (60 - fontHeight) // 2
        window.blit(font, pos)

if __name__ == "__main__":
    scraper = Scraper("https://www.websudoku.com/")
    board = scraper.getBoard()
    gui = Sudoku(board)
    gui.run()
