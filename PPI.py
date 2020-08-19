import ctypes
from typing import List, Iterable


class FakeDLL:

    def __init__(self, *args):
        pass

    @staticmethod
    def openportW(*args):
        pass

    @staticmethod
    def closeportW(*args):
        pass

    @staticmethod
    def sendcommandW(com):
        print(com)


class Print:
    """
    Печать производится вызовом методов экземпляра класса после инициализации.
    print_label, print_multiple
    С помощью методов new_line и retreat можно управлять положением ленты.
    """

    def __init__(self, dll_path="TSCLIB/x64/TSCLIB.dll", port='USB'):
        """
        Подключение библиотеки, можно указать путь к .dll и порт подключения.
        """
        self.tsc = ctypes.WinDLL(dll_path)  # FakeDLL()
        self.port = port
        self.column = 0
        self.columns = 2
        self.completed = True

    @staticmethod
    def __conf_com():
        return """DIRECTION 1

DPI=VAL(GETSETTING$("SYSTEM","INFORMATION","DPI"))
PAPER_HEIGHT=VAL(GETSETTING$("CONFIG", "TSPL", "PAPER SIZE"))
PAPER_WIDTH=VAL(GETSETTING$("CONFIG","TSPL","PAPER WIDTH"))
H=PAPER_HEIGHT
W=PAPER_WIDTH
COL_SP=24

DX=0
MX=10
MX2=20
MY=10
MY2=20
W2=W-MX*2-MX2*2
H2=H-MY*2-MY2*2
"""

    @staticmethod
    def __print_com(name, author, code, columns=2, column=0):
        return """TITLE$="Lyceum N.1 library"
TITLE_FONT$="2"
TITLE_X=1
TITLE_Y=1

NAME$="{name}"
NAME_FONT$="2"
NAME_X=1
NAME_Y=1

AUTHOR$="{author}"
AUTHOR_FONT$="1"
AUTHOR_X=1
AUTHOR_Y=1

CODE$="{code}"

SHIFT {shift}, 0
BOX DX+MX,MY,DX+W-MX,H-MY,4

X=MX+MX2-10
Y=MY+MY2-10
REM BOX DX+X,Y,DX+X+W2+20,Y+40,2

BLOCK DX+X,Y,W2+20,40,TITLE_FONT$,0,TITLE_X,TITLE_Y,0,0,1,TITLE$

X=MX+MX2-10
Y=MY+MY2+30
REM BOX DX+X,Y,DX+X+W2+20,Y+25,2

BLOCK DX+X,Y,W2+20,25,AUTHOR_FONT$,0,AUTHOR_X,AUTHOR_Y,0,3,1,AUTHOR$

X=MX+MX2
Y=MY+MY2+55
REM BOX DX+X,Y,DX+X+W2+10,Y+50,2

BLOCK DX+X,Y,W2+10,50,NAME_FONT$,0,NAME_X,NAME_Y,0,0,1,NAME$

X=MX+MX2-10
Y=MY+MY2+105
BARCODE DX+X,Y,"128",28,1,0,2,2,0,CODE$
""".format(
            name=name,
            author=author,
            code=code,
            shift=f'(PAPER_WIDTH+COL_SP)*({(1 - columns) / 2 + column})',
        )

    def conf_com(self):
        """
        Команда настройки перед печатью
        """
        return self.__conf_com()

    def print_com(self, name, author, code):
        """
        Команда прорисовки элементов каждой этикетки
        """
        return self.__print_com(name,
                                author,
                                code,
                                columns=self.columns,
                                column=self.column)

    def retreat(self, n=1):
        """
        Отмотать ленту назад на n этикеток.
        """
        self.tsc.openportW(self.port)
        self.tsc.sendcommandW(
            'BACKFEED VAL(GETSETTING$("CONFIG", "TSPL", "PAPER SIZE"))*{0}+'
            'VAL(GETSETTING$("CONFIG", "TSPL", "GAP SIZE"))*{0}'.format(n + 2)
        )
        self.tsc.sendcommandW('HOME')
        self.tsc.closeport()

    def __next(self):
        self.column = (self.column + 1) % self.columns

    def new_line(self):
        """
        Начать печатать с новой линии этикеток.
        """
        self.tsc.openportW(self.port)
        self.tsc.sendcommandW(
            'FORMFEED (VAL(GETSETTING$("CONFIG", "TSPL", "PAPER SIZE"))+VAL(GETSETTING$("CONFIG", "TSPL", "GAP SIZE")))'
        )
        self.tsc.closeport()
        self.column = 0

    def print_label(self, name, author, code):
        """
        Печать на последней свободной этикетке.
        """
        if self.column > 0:
            self.retreat(1)
        self.tsc.openportW(self.port)
        self.tsc.sendcommandW("CLS")
        for i in (self.conf_com() + self.print_com(name, author, code)).split('\n'):
            self.tsc.sendcommandW(i)
        self.tsc.sendcommandW("PRINT 1")
        self.__next()
        self.tsc.closeport()

    def print_multiple(self, books: List[Iterable[str]]):
        """
        Множественная печать, books - список данных о каждой книге в формате [name, author, code]
        """
        if self.column > 0:
            self.retreat(1)
        n_books = len(books)
        coms = self.conf_com().split('\n')
        for n, book in enumerate(books):
            if n == 0 or self.column == 0:
                coms.append("CLS")
            coms.extend(self.print_com(*book).split('\n'))
            if n == n_books - 1 or self.column == self.columns - 1:
                coms.append("PRINT 1")
            self.__next()
        self.tsc.openportW(self.port)
        for i in coms:
            self.tsc.sendcommandW(i)
        self.tsc.closeport()


import random

# tsc = FakeDLL()
# print_labels(*data)
# p = Print()
# p.print_multiple(list(zip(*data)))
# p.print_label('Mu-mu', 'Turgenev', random.randint(1000000, 9999999))
# p.print_label('Mu-mu', 'Turgenev', random.randint(1000000, 9999999))
# p.print_label('Mu-mu', 'Turgenev', random.randint(1000000, 9999999))
