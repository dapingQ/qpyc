class ClementsMesh:

    def __init__(self, N) -> None:
        self.N = N
        # self.metas 

    @property
    def matrix(self):
        pass

    def Route(self, PS):
        """
        Route the output port for a given phaseshifter
        """
        xx = range(PS.x+1, self.N+1) # x coordinate
        # y coordinate going down until edge
        y1 = [ PS.y-i-1 if PS.y-i > 1 else 1 for i in range(0, self.N - PS.x) ] 
        # y coordinate going up until edge
        y2 = [ PS.y+i+1 if PS.y+i < self.N-1 else self.N-1 for i in range(0, self.N - PS.x) ]
        route1, route2 = zip(xx, y1), zip(xx,y2)
        # exclude null phase shifters
        route1 = [ d for d in route1 if sum(d) % 2 == 0 ]
        route2 = [ d for d in route2 if sum(d) % 2 == 0 ]
        return route1, route2

    # def Port(self, )

    # def _load(self, )
    # def
    #  