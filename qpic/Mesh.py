from qpic.Device import Circuit, MZI


# ╔════════╦════════╦════════╦════════╦════════╦════════╗
# ║ (1,1)  ║        ║ (3,1)  ║        ║ (5,1)  ║        ║
# ╠════════╬════════╬════════╬════════╬════════╬════════╣
# ║        ║ (2,2)  ║        ║ (4,2)  ║        ║ (6,2)  ║
# ╠════════╬════════╬════════╬════════╬════════╬════════╣
# ║ (1,3)  ║        ║ (3,3)  ║        ║ (5,3)  ║        ║
# ╠════════╬════════╬════════╬════════╬════════╬════════╣
# ║        ║ (2,4)  ║        ║ (4,4)  ║        ║ (6,4)  ║
# ╠════════╬════════╬════════╬════════╬════════╬════════╣
# ║ (1,5)  ║        ║ (3,5)  ║        ║ (5,5)  ║        ║
# ╚════════╩════════╩════════╩════════╩════════╩════════╝

    
class ClementsMesh(Circuit):
    def __init__(self, dimension=2) -> None:
        super().__init__()
        self.dimension = dimension
        for xx in range(self.dimension):
            for yy in range(xx%2, self.dimension-1, 2):
                self.add(MZI(addr=[xx+1, yy+1]))

    def Route(self, dev):
        """
        Route the output port for a given phaseshifter
        """
        xx = range(dev.x+1, self.N+1) # x coordinate
        # y coordinate going down until edge
        y1 = [ dev.y-i-1 if dev.y-i > 1 else 1 for i in range(0, self.N - dev.x) ] 
        # y coordinate going up until edge
        y2 = [ dev.y+i+1 if dev.y+i < self.N-1 else self.N-1 for i in range(0, self.N - dev.x) ]
        route1, route2 = zip(xx, y1), zip(xx,y2)
        # exclude null phase shifters
        route1 = [ d for d in route1 if sum(d) % 2 == 0 ]
        route2 = [ d for d in route2 if sum(d) % 2 == 0 ]
        return route1, route2