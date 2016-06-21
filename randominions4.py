import sys
import random4_indies
import random4_map

def main(argv):
    if len(argv) < 10:
        print "Usage: randominions4 mapfile targetmapfile indydefinition landnations waternations lvl1thrones lvl2thrones lvl3thrones rarechance"
    else:
        mapfile = argv[1]
        indyfile = argv[3]
        targetfile = argv[2]
        landcount = int(argv[4])
        watercount = int(argv[5])
        lvl1thrones = int(argv[6])
        lvl2thrones = int(argv[7])
        lvl3thrones = int(argv[8])
        rarechance = int(argv[9])

        indies = random4_indies.Random4Indies(indyfile, rarechance)
        randommap = random4_map.Random4Map(mapfile)
        randommap.position(landcount, watercount, lvl1thrones, lvl2thrones, lvl3thrones)
        randommap.populate(indies)
        randommap.writemap(targetfile)
        indies.writeModFile(targetfile)

if __name__ == "__main__":
    main(sys.argv)