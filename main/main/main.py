from tkinter import Tk, Canvas, Frame
import time
import random

def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):

    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return Canvas.create_polygon(points, **kwargs, smooth=True)

class Tile:

    roc = 50
    Color = {
        2: "#eee4da",
        4: "#ede0c8",
        8: "#f2b179",
        16: "#f59563",
        32: "#f67c5f",
        64: "#f65e3b",
        128: "#edcf72",
        256: "#edcc61",
        512: "#edc850",
        1024: "#edc53f",
        2048: "#edc22e"
    }

    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.deltax = 0
        self.deltay = 0
        self.val = 2 if random.randint(0,100) < 96 else 4
        self.ref = None
        self.refTxt = None
        self.discard = False
        self.shifts = 0
        self.mirror = None

    def combine(self, other):
        self.val = self.val*2
        other.dispose(self)
        return True

    def dispose(self, other):
        self.mirror = other
        self.discard = True
        return True

    def setRef(self, id, txt):
        self.ref = id
        self.refTxt = txt
        return True

    def shift(self):
        if (self.shifts >= Tile.roc):
            self.completeShift()
            self.shifts = 0
        if self.newx == self.x and self.y == self.newy and self.discard:
            return False
        elif self.newx != self.x or self.y != self.newy:
            self.x = self.x + self.deltax
            self.y = self.y + self.deltay
            self.shifts = self.shifts + 1
            return True
        else:
            return True

    def completeShift(self):
        self.x = round(self.x)
        self.y = round(self.y)
        return True

    def changePosition(self, pos):
        self.newx = pos[0]
        self.newy = pos[1]
        self.deltax = (self.newx - self.x)/Tile.roc
        self.deltay = (self.newy - self.y)/Tile.roc
        return True

class UI:
    def __init__(self, master, gameController):
        self.master = master
        self.master.title ("2048")
        self.master.geometry('{}x{}'.format(314, 314))
    
        self.canv = Canvas(master, width=305, height=305)
        self.canv.focus_set()
        self.canv.bind("<Key>", gameController.move)
        self.canv.pack()
        self.canv.create_rectangle(0,0,305,305, fill="#bcaea0")

        # Create the Gridlines
        self.defineGrid()

    def round_rectangle(self, x1, y1, x2, y2, radius=8, **kwargs):

        points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

        return self.canv.create_polygon(points, **kwargs, smooth=True)

    def defineGrid(self):
        for r in range(0,4,1):
            for c in range(0,4,1):
                self.round_rectangle(r*75 + 8, c*75 + 8, r*75 + 75, c*75 + 75, fill="#cebfb0")
        return True

    def drawTiles(self, tiles):
        self.canv.delete("tiles")
        for t in tiles:
            xStart = t.x*75
            yStart = t.y*75
            sq = self.round_rectangle(xStart + 8,yStart + 8, xStart + 75, yStart + 75, fill=Tile.Color[t.val], tags="tiles")
            lab = self.canv.create_text(xStart + 42, yStart + 42, fill="black", text=str(t.val), tags="tiles")
            t.setRef(sq, lab)
        return True

    def moveTiles(self, game):
        for i in range(0, Tile.roc + 1, 1):
            time.sleep(0.001)
            ind = 0
            for ind in range(0, len(game.tiles), 1):
                if (ind >= len(game.tiles)):
                    break
                if not game.tiles[ind].shift():
                    game.tiles = game.tiles[0:ind] + game.tiles[ind+1:len(game.tiles)]
                self.canv.update()
            self.drawTiles(game.tiles)
            #self.canv.move(tile.ref, x, y)
            #self.canv.move(tile.refTxt, x, y)
        for t in game.tiles:
            if t.shifts > 2:
                if not t.shift():
                    game.tiles = game.tiles[0:ind] + game.tiles[ind+1:len(game.tiles)]
            self.canv.update()
        self.drawTiles(game.tiles)
        return True


class Game:
    def __init__(self):
        root = Tk()
        self.display = UI(root, self)
        self.gridPosOpts = []
        for x in range(0, 4, 1):
            for y in range(0, 4, 1):
                self.gridPosOpts = self.gridPosOpts + [[x,y]]
        self.tiles = []
        self.working = False
        root.mainloop()

    def move(self, event):
        if self.working:
            return False
        self.working = True
        dir = event.keycode
        tiles = [[],[],[],[]]  # List for each segment
        if dir == 40 or dir == 38:  # Vertical
            for t in self.tiles:
                tiles[t.x] = tiles[t.x] + [t]
            sorting = "y"
            flow = True if dir == 40 else False
        elif dir == 37 or dir == 39:  # Horizontal
            for t in self.tiles:
                tiles[t.y] = tiles[t.y] + [t]
            sorting = "x"
            flow = True if dir == 39 else False
        else:
            return False
        # Sort the tiles for combination
        tS = buildSort(sorting)
        ind = 0
        discard = []
        for ord in tiles:
            ord.sort(key = tS, reverse = flow)
            # Now combine
            for v in range(0, len(ord) - 1, 1):
                # Check to break on modified array
                if v + 1 >= len(ord):
                    break
                if ord[v].val == ord[v+1].val:
                    (ord[v+1]).combine(ord[v])
                    discard = discard + [ord[v]]
                    ord = ord[0:v] + ord[v+1:len(ord)]
            for v in range(0, len(ord), 1):
                if flow:
                    pos = 3 - v
                else:
                    pos = v
                if sorting == "y":
                    ord[v].changePosition([ord[v].x, pos])
                else:
                    ord[v].changePosition([pos, ord[v].y])
            tiles[ind] = ord
            ind = ind + 1
        for t in discard:
            t.changePosition([t.mirror.newx, t.mirror.newy])
        self.tiles = tiles[0] + tiles[1] + tiles[2] + tiles[3] + discard
        self.display.moveTiles(self)
        # 40 Down
        # 38 Up
        # 37 Left
        # 39 Right
        self.addTile()
        self.drawTiles()
        self.working = False
        return True

    def findEmptyPos(self):
        opts = list(self.gridPosOpts)
        if len(opts) == len(self.tiles):
            return False
        for t in self.tiles:
             i = 0
             for p in opts:
                 if (p[0] == t.x and p[1] == t.y):
                     opts = opts[0:i] + opts[i+1:len(opts)]
                     break
                 i = i + 1
        # Select one from remaining
        return opts[random.randint(0,len(opts)-1)]

    def addTile(self):
        pos = self.findEmptyPos()
        if pos == False:
            print("Game Over!")
            return False
        self.tiles = self.tiles + [Tile(pos)]
        return True

    def drawTiles(self):
        self.display.drawTiles(self.tiles)
        return True


def buildSort(dir):
    def tileSort(a):
        return getattr(a, dir)
    return tileSort
game = Game()