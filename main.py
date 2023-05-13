from random import randint, choice

class Dot:
    "Класс точки, координаты по вертикали и горизонтали"
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x}, {self.y})"

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"

class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку"

class BoardWrongShipException(BoardException):
    pass

class Ship:
    """Класс корабля, параметры: длина корабля, точка его начала
    и булевое значение, определяющее ориентацию корабля по горизонтали/вертикали"""
    def __init__(self, dlina: int, nos: Dot, gorizont: bool):
        self.dlina = dlina
        self.nos = nos
        self.gorizont = gorizont
        self.hp = dlina

    @property
    def dots(self):
        list_ship = []
        for i in range(self.dlina):
            _x = self.nos.x
            _y = self.nos.y
            if self.gorizont:
                _y += i
            else:
                _x += i
            list_ship.append(Dot(_x, _y))
        return list_ship

    def shooting(self, shot):
        return shot in self.dots

class Board:
    """Класс доски, параметры: булевое значение, определяющее,
    скрыта доска или нет, а также длина стороны доски"""
    def __init__(self, hid = False, len_of_side = 6):
        self.hid = hid
        self.len_of_side = len_of_side
        self.field = [['O']*len_of_side for _ in range(len_of_side)]
        self.ships = []
        self.busy = []
        self.count_ships = 7

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"
        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, a: int):
        return not((0<= a.x-1 < self.len_of_side) and (0<= a.y-1 < self.len_of_side))

    def contour(self, ship: Ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x-1][cur.y-1] = "-"
                    self.busy.append(cur)

    def add_ship(self, ship: Ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()
        for v in ship.dots:
            _x = v.x
            _y = v.y
            self.field[_x-1][_y-1] = "■"
            self.busy.append(v)
        self.ships.append(ship)
        self.contour(ship)

    def shot(self, dot: Dot):
        if self.out(dot):
            raise BoardOutException()
        if dot in self.busy:
            raise BoardUsedException()
        self.busy.append(dot)
        for ship in self.ships:
            _x = dot.x - 1
            _y = dot.y - 1
            if ship.shooting(dot):
                self.field[_x][_y] = "X"
                ship.hp -= 1
                if ship.hp == 0:
                    self.contour(ship, verb=True)
                    self.count_ships -= 1
                    print("Этот корабль затоплен.")
                    return True

                else:
                    print("Этот корабль ранен!")
                    return True
        self.field[_x][_y] = "-"
        print("Вы промахнулись!")
        return False

    def zero_busy(self):
        self.busy = []

class Player:
    """Класс игрока, параметрами являются две доски - своя и противника"""
    def __init__(self, my_board: Board, enemy_board: Board):
        self.my_board = my_board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        while True:
            try:
                aim = self.ask()
                repeat = self.enemy_board.shot(aim)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        _x = randint(1,6)
        _y = randint(1,6)
        dot = Dot(_x, _y)
        print(f"Ход компьютера: {dot.x} {dot.y}")
        return dot

class User(Player):
    def ask(self):
        while True:
            _x = input("Ходите! Введите координату x: ")
            _y = input("Введите координату y: ")
            if not(_x.isdigit()) or not(_y.isdigit()):
                print(" Введите числа! ")
                continue
            _x = int(_x)
            _y = int(_y)
            dot = Dot(_x, _y)
            print(f"Ход игрока: {dot.x} {dot.y}")
            return dot

class Game:
    """Класс игры, тут прописана вся игровая логика"""
    def __init__(self):
        user = self.random_board()
        comp = self.random_board()
        comp.hid = True
        self.ai = AI(comp, user)
        self.us = User(user, comp)

    def random_board(self):
        board = None
        while board is None:
            board = self.create_board()
        return board

    def create_board(self):
        board = Board()
        count = 0
        list_ships = [3,2,2,1,1,1,1]
        for d in list_ships:
            while True:
                count += 1
                if count > 1000:
                    return None

                ship = Ship(d, Dot(randint(1, 6), randint(1, 6)), choice([True, False]))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.zero_busy()
        return board

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 1
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.my_board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.my_board)
            if num % 2 != 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1
            if self.ai.my_board.count_ships == 0:
                print("-" * 20)
                print(self.ai.my_board)
                print("Пользователь выиграл!")
                print(f'У Вас осталось {self.us.my_board.count_ships} живых кораблей')
                break

            if self.us.my_board.count_ships == 0:
                print("-" * 20)
                print(self.us.my_board)
                print("Компьютер выиграл!")
                print(f'У компа осталось {self.ai.my_board.count_ships} живых кораблей')
                break
            num += 1

    def game(self):
        self.greet()
        self.loop()

game = Game()
game.game()