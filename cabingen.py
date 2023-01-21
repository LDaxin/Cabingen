import cadquery
import os

#changebal Vars
WoodThiknes = 1.9

CabinetfWidth = 50
CabinetfHeight = 70
CabinetfDeeps = 34

Abstand = 0.4

BordAmount = 3 

TopBord = False

#Calculated Vars

DoorWidth = CabinetfWidth - (Abstand*2)
DoorHeight = CabinetfHeight - (Abstand*2)

if TopBord:
    heightMod = WoodThiknes
else:
    heightMod = 0

SideWidth = CabinetfDeeps-Abstand-WoodThiknes 
SideHeight = CabinetfHeight - WoodThiknes - heightMod

BackWidth = CabinetfWidth-(WoodThiknes*2)
BackHeight = CabinetfHeight - WoodThiknes - heightMod 

BordWidth = CabinetfWidth-(WoodThiknes*2)
BordHeight = CabinetfDeeps-Abstand-WoodThiknes

TopBordWidth = CabinetfWidth
TopBordHeight = CabinetfDeeps-WoodThiknes-Abstand


# XYZ
cabinet = cadquery.Assembly()
door = cadquery.Workplane().box(DoorWidth, WoodThiknes, DoorHeight, False).translate([Abstand, 0, Abstand])

left = cadquery.Workplane().box(WoodThiknes, SideWidth, SideHeight, False).translate([0, (Abstand + WoodThiknes), WoodThiknes])

right = cadquery.Workplane().box(WoodThiknes, SideWidth, SideHeight, False).translate([CabinetfWidth-WoodThiknes, Abstand+WoodThiknes, WoodThiknes])

back = cadquery.Workplane().box(BackWidth, WoodThiknes, BackHeight, False).translate([WoodThiknes, CabinetfDeeps - WoodThiknes, WoodThiknes])

bord = cadquery.Workplane().box(TopBordWidth,TopBordHeight, WoodThiknes, False).translate([ 0, Abstand+WoodThiknes, 0])
cabinet.add(bord)

for x in range(0, BordAmount +1):
    bord = cadquery.Workplane().box(BordWidth,BordHeight, WoodThiknes, False).translate([ WoodThiknes, Abstand+WoodThiknes, (CabinetfHeight/(BordAmount+1))*x])
    cabinet.add(bord)

if TopBord:
    bord = cadquery.Workplane().box(TopBordWidth,TopBordHeight, WoodThiknes, False).translate([ 0, Abstand+WoodThiknes, CabinetfHeight-WoodThiknes])
    cabinet.add(bord)

cabinet.add(door)
cabinet.add(left)
cabinet.add(right)
cabinet.add(back)

stl = cabinet.toCompound()

if not os.path.exists('./saves'):
    os.mkdir('./saves/', 0o777)

cadquery.exporters.export(stl, './saves/view.stl')

name = 'cabinet_'+ str(CabinetfWidth*10) + 'mmX' + str(CabinetfDeeps*10) + 'mmX' + str(CabinetfHeight*10) + '_bord_tikness_'+ str(WoodThiknes*10) +'mm'

with open('./saves/'+ name + '.txt', 'w') as f:
    f.writelines('Door: '+ str(DoorWidth*10) + 'mm X ' + str(DoorHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm\n')
    f.writelines('Side: '+ str(SideWidth*10) + 'mm X ' + str(SideHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm  x2\n' )
    f.writelines('Bottom: '+ str(TopBordWidth*10) + 'mm X ' + str(TopBordHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm\n')
    if TopBord:
        f.writelines('Top: '+ str(TopBordWidth*10) + 'mm X ' + str(TopBordHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm\n')
    f.writelines('Bord: '+ str(BordWidth*10) + 'mm X ' + str(BordHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm  x'+str(BordAmount)+'\n')
