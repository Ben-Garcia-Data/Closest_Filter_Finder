import json
import csv

class filter:
    def __init__(self, number, RGB, name, description):
        self.number = number
        self.rgb = RGB
        self.name = name
        self.description = description

    def diff(self, r2, g2, b2):
        r1 = self.rgb[0]
        g1 = self.rgb[1]
        b1 = self.rgb[2]

        R = r1 - r2
        Rmean = (r1 + r2) / 2
        G = g1 - g2
        B = b1 - b2

        self.difference = (2 + (Rmean) / 256) * (R ** 2) + 4 * (G ** 2) + (2 + ((255 - Rmean) / 256)) * (B ** 2)

def hex2rgb(hex):
    return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))

def CreateFilterColours():

    with open('lee.json', 'r') as infile:
        lee = json.load(infile)['ul']['li']

    with open('Rosco.json', 'r') as infile:
        rosco = json.load(infile)['div']['div']


    arr = []

    for i in lee:
        rgb = list(hex2rgb(i['@style'][-6:]))
        arr.append(filter("L"+str(i['a']['#text']), rgb,i['span']['strong'], i['span']['#text']))

    for i in rosco:
        h = i['div'][0]['div'][0]['a']['span'][0]['@style'][-7:-1]
        num = i['div'][0]['div'][1]['p'][1]['a']['#text'][:4]
        name = i['div'][0]['div'][1]['p'][1]['a']['#text'][4:]
        try:
            desc = i['div'][2]['div']['p']
        except KeyError:
            desc = "No Description"
        rgb = list(hex2rgb(h))
        arr.append(filter(num, rgb,name, desc))

    with open('filters.csv', 'w', newline='') as csvfile:
        fieldnames = arr[0].__dict__.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for line in arr:
            writer.writerow(line.__dict__)

# CreateFilterColours()

def CompareColours():
    import csv
    arr = []
    with open('filters.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rgb = row['rgb'][1:-1].replace(" ","").split(",")
            arr.append(filter(row['number'],[int(rgb[0]),int(rgb[1]),int(rgb[2])],row['name'],row['description']))

    def CalculateDifferences():

        def GetInput():

            def GetInputMethod():
                method = input("RGB or Hex? (E.G. 255,29,0 OR #ff1e00\n").lower()
                if "r" in method and "g" in method and "b" in method:
                    return RGBinput()
                elif "hex" in method:
                    return hexinput()
                else:
                    print("Sorry, I didn't recognise that. Please respond either 'RGB' OR 'Hex'")
                    return GetInputMethod()

            def RGBinput():
                print("Input data in number form only without quotation marks E.G. 50 or 255\n")
                red = int(input("What is your Red Value?\n"))
                blue = int(input("What is your Blue Value?\n"))
                green = int(input("What is your Green Value?\n"))

                if not all(255 >= x >=0 for x in [red,green,blue]):
                    print("Sorry, values must be within the bounds of 0-255")
                    return RGBinput()


                return [red,green,blue]

            def hexinput():
                hexideminal = input("What is your Hexidecimal value? E.G. #ffa900\n")
                return hex2rgb(hexideminal[1:])

            return GetInputMethod()

        rgbvalues = GetInput()

        for i in arr:
            i.diff(rgbvalues[0],rgbvalues[1],rgbvalues[2])

        SortedList = sorted(arr, key=lambda x: x.difference)

        for count, i in enumerate(SortedList):
            print(i.number, i.rgb)
            if count > 10:
                break



    CalculateDifferences()


CompareColours()