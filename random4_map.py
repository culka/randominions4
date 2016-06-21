import random

TERRAIN_MASK = {
    "SMALL": 1,
    "LARGE": 2,
    "WATER": 4,
    "FRESH_WATER": 8,
    "MOUNTAIN": 16,
    "SWAMP": 32,
    "WASTE": 64,
    "FOREST": 128,
    "FARM": 256,
    "NOSTART": 512,
    "MANY_SITES": 1024,
    "DEEP_SEA": 2048,
    "CAVE": 4096,
    "BORDER_MOUNTAIN": 4194304,
    "RESERVED": 8388608,
    "THRONE": 16777216,
    "START": 33554432,
    "SITES_FIRE": 8192,
    "SITES_AIR": 16384,
    "SITES_WATER": 32768,
    "SITES_EARTH": 65536,
    "SITES_ASTRAL": 131072,
    "SITES_DEATH": 262144,
    "SITES_NATURE": 524288,
    "SITES_BLOOD": 1048576,
    "SITES_HOLY": 2097152
}

CONNECTION_TYPE = {
    "NORMAL": 0,
    "MOUNTAIN": 1,
    "RIVER": 2,
    "IMPASSABLE": 3
}

CONNECTION_THRESHOLD = 4

THRONES = {
    1: range(779,790) + range(792,796) + range(798,804) + [1025, 1026],
    2: [790, 791, 796, 797, 1017, 1024] + range(804,817),
    3: range(817,821) + [1018] + range(1021,1024)
}

class Province:

    def __init__(self):

        self.connections = {}
        self.terrain = 0
        self.name = None
        self.throne = None
        self.throne_level = 0
        self.indies = None

    def setName(self, new_name):
        self.name = new_name

    def getName(self):
        return self.name

    def getTerrain(self):
        return self.terrain

    def setTerrain(self, new_terrain):
        self.terrain = int(new_terrain)

    def getIndyTerrains(self):
        terrains = []
        if self.hasTerrain('WATER'):
            if self.hasTerrain('DEEP_SEA'):
                terrains.append('deepwater')
            else:
                terrains.append('water')
        else:
            if self.hasTerrain('MOUNTAIN') or self.hasTerrain('BORDER_MOUNTAIN'):
                terrains.append('mountain')
            if self.hasTerrain('FOREST'):
                terrains.append('forest')
            if self.hasTerrain('CAVE'):
                terrains.append('cave')
            if self.hasTerrain('WASTE'):
                terrains.append('waste')
            if self.hasTerrain('SWAMP'):
                terrains.append('swamp')
            if self.hasTerrain('FARM'):
                terrains.append('farm')

        if len(terrains) == 0:
            terrains.append('plains')

        return terrains


    def addNoStart(self):
        self.terrain = self.terrain | TERRAIN_MASK['NOSTART']

    def hasTerrain(self, type):
        return (self.terrain & TERRAIN_MASK[type]) == TERRAIN_MASK[type]

    def addConnection(self, target):
        self.connections[target] = 0

    def setConnectionType(self, target, type):
        self.connections[target] = type

    def properConnectionCount(self, provinces):
        count = 0
        iswater = (self.terrain & TERRAIN_MASK['WATER']) == TERRAIN_MASK['WATER']
        for connection in self.connections:
            if self.connections[connection] == 0 and iswater == provinces[connection].hasTerrain('WATER'):
                count += 1
        return count

    def getConnections(self):
        return [x for x in self.connections]

    def addThrone(self, level, thrones):
        self.throne_level = level
        while True:
            choice = random.choice(THRONES[level])
            if choice not in thrones:
                self.throne = choice
                thrones.append(choice)
                break

    def getThrone(self):
        return self.throne

    def getThroneLevel(self):
        return self.throne_level

    def setIndies(self, new_indies):
        self.indies = new_indies

    def getIndies(self):
        return self.indies

class Random4Map:

    def __init__(self, mapfile):

        self.title = "TITLE"
        self.description = "DESCRIPTION"
        self.imagefile = ""
        self.wrap = None
        self.provinces = {}
        self.thrones = []
        self.start_positions_land = set()
        self.start_positions_water = set()

        self.connections = []
        self.specialconnections = []

        with open(mapfile, 'r') as infile:
            for orig_line in infile:
                line = orig_line.strip()
                if line.startswith("#"):
                    items = line.split(" ", 1)
                    if items[0] == "#terrain":
                        provnum, terr = items[1].split(" ")
                        if self.provinces.get(int(provnum)) == None:
                            self.provinces[int(provnum)] = Province()
                        self.provinces[int(provnum)].setTerrain(terr)
                    elif items[0] == "#landname":
                        provnum, name = items[1].split(" ", 1)
                        if self.provinces.get(int(provnum)) == None:
                            self.provinces[int(provnum)] = Province()
                        self.provinces[int(provnum)].setName(name)
                    elif items[0] == "#neighbour":
                        self.connections.append(items[1].split(" "))
                    elif items[0] == "#neighbourspec":
                        self.specialconnections.append(items[1].split(" "))
                    elif items[0] == "#dom2title":
                        self.title = items[1]
                    elif items[0] == "#imagefile":
                        self.imagefile = items[1]
                    elif items[0] ==  "#description":
                        self.description = items[1]
                    elif items[0] == "#wraparound":
                        self.wrap = "xy"

        for connection in self.connections:
            self.provinces[int(connection[0])].addConnection(int(connection[1]))
            self.provinces[int(connection[1])].addConnection(int(connection[0]))

        for connection in self.specialconnections:
            self.provinces[int(connection[0])].setConnectionType(int(connection[1]), int(connection[2]))
            self.provinces[int(connection[1])].setConnectionType(int(connection[0]), int(connection[2]))


    def writemap(self, target):
        with open(target, 'w') as ofile:
            ofile.write("#dom2title " + self.title + "\n")
            ofile.write("#description " + self.description + "\n")
            ofile.write("#imagefile " + self.imagefile + "\n")
            if self.wrap is not None:
                if self.wrap == "xy":
                    ofile.write("#wraparound\n")

            for province in self.provinces:
                ofile.write("#terrain " + str(province) + " " + str(self.provinces[province].getTerrain()) + "\n")
                name = self.provinces[province].getName()
                if name is not None:
                    ofile.write("#landname " + str(province) + " " + name + "\n")

            for connection in self.connections:
                ofile.write("#neighbour " + connection[0] + " " + connection[1] + "\n")

            for spec in self.specialconnections:
                ofile.write("#neighbourspec " + spec[0] + " " + spec[1] + " " + spec[2] + "\n")

            ofile.write("\n")

            for province in [x for x in self.provinces if self.provinces[x].getIndies() is not None]:
                ofile.write('#land ' + str(province) + '\n') 
                ofile.write(self.provinces[province].getIndies())

    def position(self, landnations, waternations, lvl1thrones, lvl2thrones, lvl3thrones):

        thrones = set()
        potential_land = set()
        potential_water = set()

        for province in self.provinces:
            if self.provinces[province].hasTerrain("START"):
                if self.provinces[province].hasTerrain('WATER'):
                    self.start_positions_water.append(province)
                else:
                    self.start_positions_land.append(province)
            elif self.provinces[province].hasTerrain("THRONE"):
                thrones.add(province)
            elif self.provinces[province].properConnectionCount(self.provinces) >= CONNECTION_THRESHOLD:
                if self.provinces[province].hasTerrain('WATER'):
                    potential_water.add(province)
                else:
                    potential_land.add(province)

        attempts = 20

        # mark a radius of 2 around known start positions
        no_go = set([y for x in self.start_positions_land | self.start_positions_water for y in self.provinces[x].getConnections()])
        no_go |= set([y for x in no_go for y in self.provinces[x].getConnections()])

        potential_land -= no_go
        potential_water -= no_go

        while len(self.start_positions_land) < landnations or len(self.start_positions_water) < waternations:

            attempts -= 0

            if attempts == 0:
                raise RuntimeError("Gave up trying to find starting positions")

            new_land_starts = []
            new_water_starts = []

            if len(self.start_positions_land) < landnations:
                new_land_starts = self.findStarts(potential_land, no_go, landnations - len(self.start_positions_land))
                if new_land_starts is None:
                    continue

            if len(self.start_positions_water) < waternations:
                new_water_starts = self.findStarts(potential_water, no_go, waternations - len(self.start_positions_water))
                if new_water_starts is None:
                    continue

            self.start_positions_land |= set(new_land_starts)
            self.start_positions_water |= set(new_water_starts)

        potential_thrones = set(x for x in self.provinces) - self.start_positions_water - self.start_positions_land - thrones
        
        for province in [x for x in self.provinces if x not in self.start_positions_land | self.start_positions_water]:
            self.provinces[province].addNoStart()

        while len(thrones) < (lvl1thrones + lvl2thrones + lvl3thrones):
            choice = random.sample(potential_thrones, 1)[0]
            thrones.add(choice)
            potential_thrones.remove(choice)

        thrones_in_game = []
        throne_req = [lvl1thrones, lvl2thrones, lvl3thrones]

        for i in xrange(len(throne_req)):
            for j in xrange(throne_req[i]):
                choice = random.sample(thrones, 1)[0]
                thrones.remove(choice)
                self.provinces[choice].addThrone(i + 1, thrones_in_game)


    def findStarts(self, potential, no_go, count):
        if len(potential) == 0:
            return None

        # Attempt 10 different random setups before giving up
        for i in xrange(10):

            choice = random.sample(potential, 1)[0]
            if count == 1:
                return [choice]


            no_go2 = set(self.provinces[choice].getConnections())
            no_go2 |= set([y for x in no_go for y in self.provinces[x].getConnections()])

            nxt = self.findStarts(potential - no_go2, no_go2, count - 1)

            if nxt is not None:
                return [choice] + nxt

        return None

    def populate(self, indies):

        for province in [x for x in self.provinces if x not in (self.start_positions_land | self.start_positions_water)]:
            terrains = self.provinces[province].getIndyTerrains()
            throne = self.provinces[province].getThroneLevel()
            self.provinces[province].setIndies(indies.getIndiesFor(terrains, throne))

if __name__ == "__main__":
    print "This file is not intended to be run as stand alone!"