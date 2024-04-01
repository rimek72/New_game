# coding=utf-8


"""
Gra w kolko i krzyzyk
"""

import pygame
import pygame.locals
import logging

# Konfiguracja modulu logowania
logging_format = '%(asctime)s %(levelname)-7s | %(module)s.%(funcName)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=logging_format, datefmt='%H:%M:%S')
logging.getLogger().setLevel(logging.INFO)


class Board(object):
    """
    Plansza do gry
    """

    def __init__(self, width):
        """
        Konstruktor planszy do gry. przygotowuje okienko
        :param width: szerokosz w pikselach
        """
        self.surface = pygame.display.set_mode((width, width), 0, 32)
        pygame.display.set_caption("Kółko i Krzyżyk")

        # musimy zaincjowac mechnizmy wybory fntow w pygame
        pygame.font.init()
        font_path = pygame.font.match_font("arial")
        self.font = pygame.font.Font(font_path, 48)

        # tablica znacznikow 3x3 w formie listy
        self.markers = [None] * 9

    def draw(self, *args):

        """
        Rysuje okno gry
        :param args:
        :return:
        """
        background = [0, 0, 0]
        self.surface.fill(background)
        self.draw_net()
        self.draw_markers()
        self.draw_score()
        for drawable in args:
            drawable.draw_on(self.surface)
        # dopier nastupje rysowanie
        # w oknie gry, wczewsniej tylko parametry
        pygame.display.update()

    def draw_net(self):
        """
        Rysuje siatke linii na planszy
        :return:
        """
        color = (255, 255, 255)
        width = self.surface.get_width()
        for i in range(1, 3):
            pos = width / 3 * i
            # linia pozioma
            pygame.draw.line(self.surface, color, (0, pos), (width, pos), 1)
            # lini pionowa
            pygame.draw.line(self.surface, color, (pos, 0), (pos, width), 1)

    def player_move(self, x, y):
        """
        ustawia znacznik gracza X na podstawie wspolrzednych

        :param x:
        :param y:
        :return:
        """
        cell_size = self.surface.get_width() / 3
        x /= cell_size
        y /= cell_size
        self.markers[int(x) + int(y) * 3] = player_marker(True)

    def draw_markers(self):
        """
        rysuje znaczniki graczy
        :return:
        """
        box_side = self.surface.get_width() / 3
        for x in range(3):
            for y in range(3):
                marker = self.markers[x + y * 3]
                if not marker:
                    continue
                # zmianiamy wspolrzedne znacznika
                # na wspolrzedne w pikselach dla centrum pola
                center_x = x * box_side + box_side / 2
                center_y = y * box_side + box_side / 2

                self.draw_text(self.surface, marker, (center_x, center_y))

    def draw_text(self, surface, text, center, color=(180, 180, 180)):
        """
        Rysuje wskazany tekst we wskazanym miejscu
        :param surface:
        :param text:
        :param center:
        :param color:
        :return:
        """
        text = self.font.render(text, True, color)
        rect = text.get_rect()
        rect.center = center
        surface.blit(text, rect)

    def draw_score(self):
        """
        Sprawdza czy gra zostala skonczona i rysuje wlasciwy komunikat
        :return:
        """
        if check_win(self.markers, True):
            score = u"Wygrałeś(aś)"
        elif check_win(self.markers, True):
            score = u"Przegrałeś(aś)"
        elif None not in self.markers:
            score = u"Remis"
        else:
            return

        i = self.surface.get_width() / 2
        self.draw_text(self.surface, score, center=(i, i), color=(255, 26, 26))


class TicTacToeGame(object):
    """
    łączy wszystkie elementy gry
    """

    def __init__(self, width, ai_turn=False):
        """
        przygotwanie ustawien gry
        :param width:
        :param ai_turn:
        """
        pygame.init()
        # zegar ktorego uzjemy do kontrolowania szybkosci rysowania kolejnych klatek gry
        self.fps_clock = pygame.time.Clock()

        self.board = Board(width)
        self.ai = Ai(self.board)
        self.ai_turn = ai_turn

    def run(self):
        """
        Główna pętla gry
        :return:

        """
        while not self.handle_events():
            # dzialanie w petli do momentu otrzymania sygnalu do wyjscia
            self.board.draw()

            if self.ai_turn:
                self.ai.make_turn()
                self.ai_turn = False

            self.fps_clock.tick(15)

    def handle_events(self):
        """
        Obługa zdarzeń systemowych, tutaj kontrola myszka
        :return: True jezeli sygnal wyjscia z gry
        """
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True

            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                if self.ai_turn:
                    # jesli jest trwa ruch komputera to ignorujemy zdarzenie
                    continue
                # pobierz aktualna pozycje kursora
                x, y = pygame.mouse.get_pos()
                self.board.player_move(x, y)
                self.ai_turn = True


# to jest test

class Ai(object):
    """
    kieruje ruchami komputera na podstawie analizy polozenia znacznikow
    """

    def __init__(self, board):
        self.board = board

    def make_turn(self):
        """
        wykonuje ruch komputera
        :return:
        """
        if not None in self.board.markers:
            # brak dostępnych ruchów
            return
        logging.debug("PLansza: %s" % self.board.markers)
        move = self.next_move(self.board.markers)
        self.board.markers[move] = player_marker(False)

    @classmethod
    def next_move(cls, markers):
        """
        Wybierz nastepny ruch komputera na podstawie wskazanaje planszy
        """
        # pobierz dostepne ruch z ocena
        moves = cls.score_moves(markers, False)
        # wybierz najlepszy ruch
        score, move = max(moves, key=lambda m: m[0])
        logging.info("Dostępne ruchy: %s", moves)
        logging.info("Wybrany ruch: %x, %s", move, score)
        return move

    @classmethod
    def score_moves(cls, markers, x_player):
        """
        Ocena rekurencyjne mozliwe ruchy
        :param markers: plansza na podstawie ktorej analizowane sa nasze ruchy
        :param x_player: True jezeli ruch dotyczy gracza X
        :return:
        """
        # wybieramy wszystki mozliwe ruchy
        available_moves = (i for i, m in enumerate(markers) if m is None)
        for move in available_moves:
            from copy import copy
            # tworzymy kopie planszy aby wykonac ruch testowy
            proposal = copy(markers)
            proposal[move] = player_marker(x_player)

            # sprawdzamy czy ktos wygrywa gracz ktorego ruch testujemy
            if check_win(proposal, x_player):
                # dodajemy punkty jesli to my wygrywamy
                score = -1 if x_player else 1
                yield score, move
                continue

            # ruch jest neutralny sprawdzamy rekurencyjnie kolejne ruchy
            next_moves = list(cls.score_moves(proposal, not x_player))
            if not next_moves:
                yield 0, move
                continue
            # rozdzielamy wyniki od ruchow
            scores, moves = zip(*next_moves)
            yield sum(scores), move


def player_marker(x_player):
    """
    funkcja pomconicza zwracajaca znaczniki graczy
    :param x_player: True dla gracza X false dla gracza 0
    :return: znak gracza
    """
    return "X" if x_player else "0"


def check_win(markers, x_player):
    """
    sprawdza czy przakazany zestaw znacznikow gry oznacza zwyciestoe
    :param marker: jednowymiarowa sekwencja znacznikow w
    :param x_player: True dla gracza X Falso dla gracza 0
    :return:
    """
    win = [player_marker(x_player)] * 3
    seq = range(3)

    # definujemy funkcje pomocnicza pobierajaca znacznik
    # na podstawie współrzędnych z i y

    def marker(xx, yy):
        return markers[xx + yy * 3]

    # sprawdzamy każdy rząd
    for x in seq:
        row = [marker(x, y) for y in seq]
        if row == win:
            return True
    # sprawdzamy każdą kolumnę
    for y in seq:
        col = [marker(x, y) for x in seq]
        if col == win:
            return True

    # sprawdzamy przekatne
    diagonali1 = [marker(i, i) for i in seq]
    diagonali2 = [marker(i, abs(i - 2)) for i in seq]
    if diagonali1 == win or diagonali2 == win:
        return True


if __name__ == "__main__":
    game = TicTacToeGame(300)
    game.run()
