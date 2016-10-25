import sys
import random4_indies
import random4_map
from random4_nationgenparser import Random4NationgenParser
from Tkinter import Tk, Button, Label, Entry, StringVar, IntVar, BooleanVar, Checkbutton, Listbox, END, ANCHOR, E, W
from tkFileDialog import askopenfilename


def main(argv):
    if len(argv) == 1:
        root = Tk()
        root.title("Randominions 4")

        mapfilevar = StringVar()
        outfilevar = StringVar()
        outfilevar.set("newrandommap.map")
        modfilevar = StringVar()
        lvl1thronevar = IntVar()
        lvl1thronevar.set(0)
        lvl2thronevar = IntVar()
        lvl2thronevar.set(0)
        lvl3thronevar = IntVar()
        lvl3thronevar.set(0)

        landstartvar = IntVar()
        landstartvar.set(0)
        waterstartvar = IntVar()
        waterstartvar.set(0)
        coaststartvar = IntVar()
        coaststartvar.set(0)
        foreststartvar = IntVar()
        foreststartvar.set(0)
        swampstartvar = IntVar()
        swampstartvar.set(0)
        cavestartvar = IntVar()
        cavestartvar.set(0)

        indystrengthvar = IntVar()
        indystrengthvar.set(100)
        rarechancevar = IntVar()
        rarechancevar.set(10)
        magepowervar = IntVar()
        magepowervar.set(2)
        allowsacred = BooleanVar()
        allowsacred.set(False)

        Label(root, text="Map:").grid(row=0, sticky=E)
        Entry(root, width=50, textvariable=mapfilevar).grid(row=0, column=1)
        Label(root, text="Output map:").grid(row=4, sticky=E)
        Entry(root, width=50, textvariable=outfilevar).grid(row=4, column=1)
        Label(root, text="Nation mod file:").grid(row=5, sticky=E)
        Entry(root, width=50, textvariable=modfilevar).grid(row=5, column=1)

        Label(root, text="Rare indy chance(%):").grid(row=6, sticky=E)
        Entry(root, width=5, textvariable=rarechancevar).grid(row=6, column=1, sticky=W)
        Label(root, text="Indy strength(%):").grid(row=7, sticky=E)
        Entry(root, width=5, textvariable=indystrengthvar).grid(row=7, column=1, sticky=W)
        Label(root, text="Max nation mage power:").grid(row=8, sticky=E)
        Entry(root, width=5, textvariable=magepowervar).grid(row=8, column=1, sticky=W)
        Label(root, text="Allow sacred units:").grid(row=9, sticky=E)
        Checkbutton(root, variable=allowsacred).grid(row=9, column=1, sticky=W)

        Label(root, text="Level 1 thrones:").grid(row=0, column=3, sticky=E)
        Entry(root, width=3, textvariable=lvl1thronevar).grid(row=0, column=4)
        Label(root, text="Level 2 thrones:").grid(row=1, column=3, sticky=E)
        Entry(root, width=3, textvariable=lvl2thronevar).grid(row=1, column=4)
        Label(root, text="Level 3 thrones:").grid(row=2, column=3, sticky=E)
        Entry(root, width=3, textvariable=lvl3thronevar).grid(row=2, column=4)

        Label(root, text="Land nations:").grid(row=3, column=3, sticky=E)
        Entry(root, width=3, textvariable=landstartvar).grid(row=3, column=4)
        Label(root, text="Water nations:").grid(row=4, column=3, sticky=E)
        Entry(root, width=3, textvariable=waterstartvar).grid(row=4, column=4)
        Label(root, text="Coastal starts:").grid(row=5, column=3, sticky=E)
        Entry(root, width=3, textvariable=coaststartvar).grid(row=5, column=4)
        Label(root, text="Forest starts:").grid(row=6, column=3, sticky=E)
        Entry(root, width=3, textvariable=foreststartvar).grid(row=6, column=4)
        Label(root, text="Swamp starts:").grid(row=7, column=3, sticky=E)
        Entry(root, width=3, textvariable=swampstartvar).grid(row=7, column=4)
        Label(root, text="Cave starts:").grid(row=8, column=3, sticky=E)
        Entry(root, width=3, textvariable=cavestartvar).grid(row=8, column=4)

        Label(root, text="Indies:").grid(row=1, sticky=E)
        indylist = Listbox(root, width=50, height=4)
        indylist.grid(row=1, column=1, rowspan=3)

        Button(root, width=13, text="Choose Map", command=lambda : mapfilevar.set(askopenfilename(filetypes=[('Dominions 4 map files', '.map')]))).grid(row=0, column=2, sticky=W)
        Button(root, width=13, text="Choose Mod", command=lambda : modfilevar.set(askopenfilename(filetypes=[('Dominions 4 mod file', '.dm')]))).grid(row=5, column=2, sticky=W)
        Button(root, width=13, text="Add indies", command=lambda : indylist.insert(END,askopenfilename(filetypes=[('JSON files', '.json'), ('Domions 4 mod files', '.dm')]))).grid(row=1, column=2, sticky=W)
        Button(root, width=13, text="Remove selected", command=lambda : indylist.delete(ANCHOR)).grid(row=2, column=2, sticky=W)
        Button(root, width=10, text="Quit", command=root.destroy).grid(row=10, column=0)
        Button(root, width=10, text="Generate!", \
            command=lambda : runGenerator(mapfilevar.get(), indylist.get(0, END), outfilevar.get(), landstartvar.get(), waterstartvar.get(), \
                coaststartvar.get(), foreststartvar.get(), swampstartvar.get(), cavestartvar.get(), lvl1thronevar.get(), \
                lvl2thronevar.get(), lvl3thronevar.get(), rarechancevar.get(), indystrengthvar.get(), modfilevar.get(), magepowervar.get(), allowsacred.get())).grid(row=10, column=3)

        root.mainloop()

    elif len(argv) < 15:
        print "Usage: randominions4 mapfile targetmapfile indydefinition landnations waternations coaststarts foreststarts swampstarts cavestarts lvl1thrones lvl2thrones lvl3thrones rarechance indystrength"
    else:
        mapfile = argv[1]
        indyfile = argv[3]
        targetfile = argv[2]
        landcount = int(argv[4])
        watercount = int(argv[5])
        coaststarts = int(argv[6])
        foreststarts = int(argv[7])
        swampstarts = int(argv[8])
        cavestarts = int(argv[9])
        lvl1thrones = int(argv[10])
        lvl2thrones = int(argv[11])
        lvl3thrones = int(argv[12])
        rarechance = int(argv[13])
        strength = int(argv[14])

        runGenerator(mapfile, [indyfile], targetfile, landcount, watercount, coaststarts, foreststarts, swampstarts, cavestarts, lvl1thrones, lvl2thrones, lvl3thrones, rarechance, strength, None, None, None)


def runGenerator(mapfile, indyfiles, targetfile, landcount, watercount, coaststarts, foreststarts, swampstarts, cavestarts, lvl1thrones, lvl2thrones, lvl3thrones, rarechance, strength, modfile, magepower, allowsacred):
    indies = None
    if modfile is not None:
        indies = Random4NationgenParser(allowsacred, magepower,
                                        rarechance, strength)
        indies.parse(modfile)
    else:
        indies = random4_indies.Random4Indies(rarechance, strength)
    for indyfile in indyfiles:
        indies.readIndies(indyfile)
    randommap = random4_map.Random4Map(mapfile)
    randommap.position(landcount, watercount, coaststarts, foreststarts, swampstarts, cavestarts, lvl1thrones, lvl2thrones, lvl3thrones)
    randommap.populate(indies)
    randommap.writemap(targetfile)
    indies.writeModFile(targetfile)

if __name__ == "__main__":
    main(sys.argv)