import json
import random

terrainlists = lambda : {"plains": [], "farm": [], "forest": [], "mountain": [], "waste": [], "swamp": [], "cave": [], "water": [], "deepwater": [], "coast": []}

class Random4Indies:

    def __init__(self, rarechance, strength):

        self.rarechance = rarechance
        self.strength = strength // 100
        self.poptypes = terrainlists()
        self.rares = terrainlists()
        self.throne_guards = {key: terrainlists() for key in xrange(1, 4)}
        self.allpop = []
        self.index = 25
        random.seed()

    def readIndies(self, sourcefile):
        with open(sourcefile, 'r') as infile:
            data = json.load(infile)

        if data.get('poptypes') is not None:
            for entry in data['poptypes']:
                entry['index'] = str(self.index)
                for terrain in entry['terrain']:
                    if self.poptypes.get(terrain) is None:
                        print "Error: found unknown terrain " + terrain + " in " + sourcefile
                    else:
                        self.poptypes[terrain].append(entry)
                self.allpop.append(entry)
                self.index += 1

        if data.get('rares') is not None:
            for entry in data['rares']:
                for terrain in entry['terrain']:
                    if self.rares.get(terrain) is None:
                        print "Error: found unknown terrain " + terrain + " in " + sourcefile
                    else:
                        self.rares[terrain].append(entry)

        if data.get('throne_guards') is not None:
            for level in data['throne_guards']:
                for entry in data['throne_guards'][level]:
                    for terrain in entry['terrain']:
                        if self.throne_guards[int(level)].get(terrain) is None:
                            print "Error: found unknown terrain " + terrain + " in " + sourcefile
                        else:
                            self.throne_guards[int(level)][terrain].append(entry)

    def getPoptypeForTerrain(self, terrains):
        choices = []
        for terrain in terrains:
            if self.poptypes[terrain] is not None:
                choices = choices + self.poptypes[terrain]

        result = None

        while True:
            poptype = random.choice(choices)
            if poptype.get('rare') is not None:
                if random.random() < poptype['rare']:
                    result = poptype
                    break
                else:
                    continue
            else:
                result = poptype
                break

        return result

    def getRaresForTerrain(self, terrains):
        choices = []
        for terrain in terrains:
            if self.rares[terrain] is not None:
                choices = choices + self.rares[terrain]

        result = None

        while True:
            rare = random.choice(choices)
            if rare.get('rare') is not None:
                if random.random() < rare['rare']:
                    result = rare
                    break
                else:
                    continue
            else:
                result = rare
                break

        return result

    def getThroneGuardsForTerrain(self, terrains, throne_level, throne_tags):
        choices = [choice for terrain in terrains for choice in self.throne_guards[throne_level][terrain]]
        filtered = [f for tag in throne_tags for f in choices if f.get('tags') is not None and tag in f['tags']]

        if len(filtered) != 0:
            choices = filtered

        result = None

        while True:
            guards = random.choice(choices)
            if guards.get('rare') is not None:
                if random.random() < guards['rare']:
                    result = guards
                    break
                else:
                    continue
            else:
                result = guards
                break

        return result

    def getUnitsForEntry(self, entry):
        stringList = []
        for commander in entry['commander']:
            for i in xrange(1 if commander.get('count') is None else commander['count']):
                # generate one each time due to possible random attributes
                stringList += self.getCommanderString(commander)

        for unit in entry['unit']:
            count = max(int(random.randrange(int(unit['count']*0.7), int(unit['count']*1.3)) * self.strength), 1)
            stringList += '#units ' + str(count) + ' ' + self.getString(unit['type']) + '\n'

        return ''.join(stringList)


    def getIndiesFor(self, terrains, throne_level, throne_tags):
        poptype = self.getPoptypeForTerrain(terrains)
        stringList = []

        stringList += '#poptype ' + poptype['index'] + '\n'

        stringList += self.getUnitsForEntry(poptype)

        if random.random() * 100 < self.rarechance:
            rare = self.getRaresForTerrain(terrains)
            stringList += self.getUnitsForEntry(rare)

        if throne_level > 0:
            throneguards = self.getThroneGuardsForTerrain(terrains, throne_level, throne_tags)
            stringList += self.getUnitsForEntry(throneguards)

        return ''.join(stringList)


    def getCommanderString(self, commander):
        stringList = []
        stringList += '#commander ' + self.getString(commander['type']) + '\n'
        if commander.get('items') is not None:
            stringList += '#randomequip ' + str(commander['items']) + '\n'
        if commander.get('name') is not None:
            stringList += '#comname "' + random.choice(commander['name']) + '"\n'
        if commander.get('xp') is not None:
            stringList += '#xp ' + str(commander['xp']) + '\n'
        if commander.get('magic') is not None:
            for path in commander['magic']:
                stringList += '#mag_' + path + ' ' + str(commander['magic'][path]) + '\n'

        return ''.join(stringList)

    def writeModFile(self, modfile):

        with open(modfile + '.dm', 'w') as ofile:
            self.writeHeader(ofile)
            self.writePoptype(ofile)

    def writeHeader(self, ofile, modfile):
        ofile.write('#modname "Random indies for ' + modfile + '"\n')
        ofile.write('#description "Random indies for ' + modfile + '"\n')
        ofile.write('#version 100\n')
        ofile.write('#domversion 350\n')

    def writePoptype(self, ofile):
        for poptype in self.allpop:
            ofile.write('\n')
            ofile.write('#selectpoptype ' + str(poptype['index']) + '\n')
            ofile.write('#clearrec\n')
            ofile.write('#cleardef\n')

            ofile.write('#defcom1 ' + self.getString(poptype['pd_commander']) + '\n')

            prefix = ['', 'b', 'c']
            for pd in xrange(min(len(poptype['pd']), 3)):
                ofile.write('#defunit1' + prefix[pd] + ' ' + self.getString(poptype['pd'][pd]['type']) + '\n')
                ofile.write('#defmult1' + prefix[pd] + ' ' + str(poptype['pd'][pd]['count']) + '\n')

            for reccom in poptype['recruitable_commanders']:
                ofile.write('#addreccom ' + self.getString(reccom) + '\n')

            for recunit in poptype['recruitable_units']:
                ofile.write('#addrecunit ' + self.getString(recunit) + '\n')

            ofile.write('#end\n')

    def getString(self, item):
        if isinstance(item, basestring):
            return '"' + item + '"'
        return str(item)

if __name__ == "__main__":
    print "This file is not intended to be run as stand alone!"