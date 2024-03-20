class Graph:
    def __init__(self, width=50, height=10, Symbol="o"):
        self.width = width
        self.height = height
        self.window = [[Symbol for y in range(self.width)] for x in range(self.height)]
        # self.window = [["o", "o", "o", "o", "o",],
        #               ["o", "o", "o", "o", "o", ],
        #               ["o", "o", "o", "o", "o", ],
        #               ["o", "o", "o", "o", "o", ],
        #               ["o", "o", "o", "o", "o", ],]
    
    def __repr__(self):
        ans = ""
        for i in range(self.height):
            for j in range(self.width):
                ans += self.window[i][j]
            ans += "\n"
        return ans
    
    def drawRect(self, Rx, Ry, Rw, Rh, Symbol="w"):
        for i in range(Rh):
            for j in range(Rw):
                self.window[i + Ry][j + Rx] = Symbol