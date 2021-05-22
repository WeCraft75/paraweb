class vzletisce:

    # konstruktor
    def __init__(self, ime, smer, hitrost, sunki, vreme, x, y):
        self.ime = ime
        self.smer = smer
        self.hitrost = hitrost
        self.sunki = sunki
        self.vreme = vreme
        self.x = x
        self.y = y

    # get metode za vsak atribut
    def getIme(self):
        return self.ime

    def getSmer(self):
        return self.smer

    def getHitrost(self):
        return self.hitrost

    def getSunki(self):
        return self.sunki

    def getVreme(self):
        return self.vreme

    def getX(self):
        return self.x

    def getY(self):
        return self.y