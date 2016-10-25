import random
from sets import Set
from random4_indies import Random4Indies

# DOMINIONS 4 CAN HANDLE REFERENCES TO NAMES OF MAX LENGTH 35

terrains = ["plains", "farm", "forest", "mountain", "waste", "swamp",
            "cave", "coast"]

reservednames = ["General", "Castellan", "Spy", "Scout", "Assassin",
                 "Warchief", "Warden", "High Priest", "Colonel",
                 "Lieutenant", "Warlord", "Spearmaster", "Cardinal",
                 "Rishi"]


class Random4NationgenParser(Random4Indies):

    def __init__(self, allowsacred, magestrength, rarechance, strength):
        Random4Indies.__init__(self, rarechance, strength)
        self.allowsacred = allowsacred
        self.magestrength = magestrength
        self.neededunits = []
        self.weapons = dict()
        self.armor = dict()
        self.units = dict()

    def parse(self, natgenfile):
        sites = dict()
        nations = dict()
        with open(natgenfile) as infile:
            while True:
                line = infile.readline()
                if not line:
                    break
                if line.startswith('#newweapon '):
                    self.weapons[line.split(' ')[1].strip()] = \
                        self.parseWeapon(infile, line)
                elif line.startswith('#newarmor '):
                    self.armor[line.split(' ')[1].strip()] = \
                        self.parseArmor(infile, line)
                elif line.startswith('#newmonster '):
                    self.units[line.split(' ')[1].strip()] = \
                        self.parseUnit(infile, line)
                elif line.startswith('#newsite '):
                    self.parseSite(infile, sites)
                elif line.startswith('#selectnation '):
                    nations[line.split(' ')[1].strip()] = \
                        self.parseNation(infile, sites)

        pops = []

        for nation in nations:
            poptype = dict()
            poptype['terrain'] = terrains
            commanders = []
            i = random.randint(2, 3)
            while i > 0:
                com = random.choice(nations[nation]['commanders'])
                if self.units[com]['power'] < self.magestrength and \
                        com not in commanders:
                    commanders.append(com)
                    i -= 1
            troops = []
            i = random.randint(2, 4)
            while i > 0:
                unit = random.choice(nations[nation]['units'])
                if ((self.units[unit]['sacred'] and self.allowsacred) or
                        not self.units[unit]['sacred']) and unit not in troops:
                    troops.append(unit)
                    i -= 1

            poptype['commander'] = []
            poptype['recruitable_commanders'] = []
            for com in commanders:
                count = -(-(self.strength * 50) // self.units[com]['cost'])
                name = self.units[com]['name']
                poptype['commander'].append({'type': name, 'count': count})
                poptype['recruitable_commanders'].append(name)
                self.neededunits.append(com)

            poptype['unit'] = []
            poptype['recruitable_units'] = []
            poptype['pd'] = []
            for unit in troops:
                try:
                    count = -(-(self.strength * 100) //
                              self.units[unit]['cost'])
                    name = self.units[unit]['name']
                    poptype['unit'].append({'type': name, 'count': count * 2})
                    poptype['pd'].append({'type': name, 'count': count})
                    poptype['recruitable_units'].append(name)
                    self.neededunits.append(unit)
                except ZeroDivisionError:
                    print(self.units[unit])

            poptype['pd_commander'] = poptype['recruitable_commanders'][0]
            poptype['index'] = str(self.index)
            self.index += 1
            self.allpop.append(poptype)
            pops.append(poptype)

        for terrain in self.poptypes:
            for poptype in pops:
                self.poptypes[terrain].append(poptype)

    def parseWeapon(self, infile, firstline):
        text = firstline
        secondary = None
        while True:
            line = infile.readline()
            if not line:
                break
            text += line
            if line.startswith("#secondaryeffect"):
                secondary = line.split(' ')[1].strip()
            elif line.strip() == "#end":
                return {'secondary': secondary, 'text': text}

    def parseArmor(self, infile, firstline):
        text = firstline
        while True:
            line = infile.readline()
            if not line:
                break
            text += line
            if line.strip() == "#end":
                return {'text': text}

    def parseUnit(self, infile, firstline):
        text = firstline
        cost = 0
        name = None
        sacred = False
        power = 0
        shapes = []
        weapons = []
        armor = []
        while True:
            line = infile.readline()
            if not line:
                break
            if line.strip() == "#end":
                return {'name': name, 'cost': cost,
                        'sacred': sacred, 'power': power,
                        'shapes': shapes, 'armor': armor,
                        'weapons': weapons, 'text': text}
            elif line.startswith('#name '):
                name = line.split(' ', 1)[1].strip('" \n\r')[:35]
                continue
            text += line
            if line.startswith('#gcost '):
                cost = int(line.split(' ')[1])
            elif line.startswith('#copystats ') or \
                    line.startswith('#firstshape ') or \
                    line.startswith('#secondshape ') or \
                    line.startswith('#secondtmpshape ') or \
                    line.startswith('#shapechange '):
                shapes.append(line.split(' ')[1].strip())
            elif line.startswith('#armor '):
                armor.append(line.split(' ')[1].strip())
            elif line.startswith('#weapon '):
                weapons.append(line.split(' ')[1].strip())
            elif line.startswith('#magicskill '):
                power += int(line.split(' ')[2].strip())
            elif line.startswith('#custommagic '):
                power += int(line.split(' ')[2].strip()) / 100
            elif line.strip() == "#holy":
                sacred = True

    def parseSite(self, infile, sites):
        name = None
        units = []
        commanders = []
        while True:
            line = infile.readline()
            if not line:
                break
            if line.startswith('#name '):
                name = line.split(' ', 1)[1].strip()
            elif line.startswith('#homemon '):
                num = line.split(' ')[1].strip()
                if self.units.get(num) is not None:
                    units.append(num)
            elif line.startswith('#homecom '):
                num = line.split(' ')[1].strip()
                if self.units.get(num) is not None:
                    commanders.append(num)
            elif line.strip() == "#end":
                sites[name] = {'units': units, 'commanders': commanders}
                break

    def parseNation(self, infile, sites, ):
        name = None
        units = []
        commanders = []
        while True:
            line = infile.readline()
            if not line:
                break
            if line.startswith('#startsite '):
                site = line.split(' ', 1)[1].strip()
                units += sites[site]['units']
                commanders += sites[site]['commanders']
            elif line.startswith('#name '):
                name = line.split(' ', 1)[1].strip('" \r\n')
            elif line.startswith('#addrecunit '):
                num = line.split(' ')[1].strip()
                if self.units.get(num) is not None:
                    units.append(num)
            elif line.startswith('#addreccom '):
                num = line.split(' ')[1].strip()
                if self.units.get(num) is not None:
                    commanders.append(num)
            elif line.strip() == "#end":
                for unit in units:
                    if self.units[unit] is not None and \
                       self.units[unit]['name'] in reservednames:
                        self.units[unit]['name'] = \
                            (name + self.units[unit]['name'])[:35]
                for unit in commanders:
                    if self.units[unit] is not None and \
                       self.units[unit]['name'] in reservednames:
                        self.units[unit]['name'] = \
                            (name + " " + self.units[unit]['name'])[:35]
                return {'name': name, 'units': units, 'commanders': commanders}

    def writeModFile(self, modfile):

        units = Set()
        for unit in self.neededunits:
            for shape in self.units[unit]['shapes']:
                units.add(shape)
            units.add(unit)

        weapons = Set()
        armors = Set()
        for unit in units:
            if self.units.get(unit) is not None:
                for weapon in self.units[unit]['weapons']:
                    weapons.add(weapon)
                for armor in self.units[unit]['armor']:
                    armors.add(armor)

        while True:
            newweapons = Set()
            for weapon in weapons:
                if self.weapons.get(weapon) is not None:
                    if self.weapons[weapon]['secondary'] is not None and \
                       self.weapons[weapon]['secondary'] not in weapons:
                        newweapons.add(self.weapons[weapon]['secondary'])
            if len(newweapons) > 0:
                weapons |= newweapons
            else:
                break

        with open(modfile + '.dm', 'w') as ofile:
            self.writeHeader(ofile, modfile)

            for armor in armors:
                if self.armor.get(armor) is not None:
                    ofile.write(self.armor[armor]['text'])
            for weapon in weapons:
                if self.weapons.get(weapon) is not None:
                    ofile.write(self.weapons[weapon]['text'])
            for unit in units:
                if self.units.get(unit) is not None:
                    ofile.write(self.units[unit]['text'])
                    if self.units[unit]['name'] is not None:
                        ofile.write('#name "' +
                                    self.units[unit]['name'] + '"\n')
                    ofile.write('#end\n')

            self.writePoptype(ofile)


if __name__ == "__main__":
    print("This file is not intended to be run as stand alone!")
