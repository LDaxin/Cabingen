import os

#-changeable vars--------------------------------------------------------------------------
WoodThiknes = 1.9

CabinetWidth = 50
CabinetHeight = 70
CabinetDeeps = 34

Abstand = 0.4

BordAmount = 1 

TopBord = False
Door = True

ExplosionsView = True
#-Calculated Vars-------------------------------------------------------------------------

if ExplosionsView:
    explosion = 20
else:
    explosion = 0

DoorWidth = CabinetWidth - (Abstand*2)
DoorHeight = CabinetHeight - (Abstand*2)

if TopBord:
    heightMod = WoodThiknes
else:
    heightMod = 0

SideHeight = CabinetHeight - WoodThiknes - heightMod

BackWidth = CabinetWidth-(WoodThiknes*2)
BackHeight = CabinetHeight - WoodThiknes - heightMod 

BordWidth = CabinetWidth-(WoodThiknes*2)

TopBordWidth = CabinetWidth

if Door:
    DoorDistance = Abstand + WoodThiknes
    BordHeight = CabinetDeeps-Abstand-(WoodThiknes*2)
    TopBordHeight = CabinetDeeps-WoodThiknes-Abstand
    SideWidth = CabinetDeeps-Abstand-WoodThiknes 

else:
    DoorDistance = 0
    BordHeight = CabinetDeeps-Abstand-WoodThiknes
    TopBordHeight = CabinetDeeps
    SideWidth = CabinetDeeps

Lipping = (DoorWidth + DoorHeight)*2 + (SideHeight + TopBordWidth + CabinetDeeps)*4 + BordWidth*BordAmount

#-CadQuery---------------------------------------------------------------------------------
try:
    import cadquery

    cabinet = cadquery.Assembly()

    door = cadquery.Workplane().box(DoorWidth, WoodThiknes, DoorHeight, False).translate([Abstand, -explosion, Abstand])

    left = cadquery.Workplane().box(WoodThiknes, SideWidth, SideHeight, False).translate([-explosion, DoorDistance, WoodThiknes])

    right = cadquery.Workplane().box(WoodThiknes, SideWidth, SideHeight, False).translate([CabinetWidth-WoodThiknes+explosion, DoorDistance, WoodThiknes])

    back = cadquery.Workplane().box(BackWidth, WoodThiknes, BackHeight, False).translate([WoodThiknes, CabinetDeeps - WoodThiknes + explosion, WoodThiknes])

    bord = cadquery.Workplane().box(TopBordWidth,TopBordHeight, WoodThiknes, False).translate([ 0, DoorDistance, 0])
    cabinet.add(bord)

    for x in range(0, BordAmount +1):
        bord = cadquery.Workplane().box(BordWidth,BordHeight, WoodThiknes, False).translate([ WoodThiknes, DoorDistance, (CabinetHeight/(BordAmount+1))*x])
        cabinet.add(bord)

    if TopBord:
        bord = cadquery.Workplane().box(TopBordWidth,TopBordHeight, WoodThiknes, False).translate([ 0, DoorDistance, CabinetHeight-WoodThiknes])
        cabinet.add(bord)

    if Door:
        cabinet.add(door)
    cabinet.add(left)
    cabinet.add(right)
    cabinet.add(back)

    stl = cabinet.toCompound()
    NoCadquery = False
except ModuleNotFoundError:
    NoCadquery = True
    print("CadQuery is not installed if you want a stl view run pip3 install cadquery")

#Export----------------------------------------------------------------------------------
if not os.path.exists('./saves'):
    os.mkdir('./saves/', 0o777)

if not NoCadquery:
    cadquery.exporters.export(stl, './saves/view.stl')

name = 'cabinet_'+ str(CabinetWidth*10) + 'mmX' + str(CabinetDeeps*10) + 'mmX' + str(CabinetHeight*10) + '_bord_tikness_'+ str(WoodThiknes*10) +'mm'

with open('./saves/'+ name + '.txt', 'w') as f:
    f.writelines('Door: '+ str(DoorWidth*10) + 'mm X ' + str(DoorHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm\n')
    f.writelines('Back: '+ str(BackWidth*10) + 'mm X ' + str(BackHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm\n')
    f.writelines('Side: '+ str(SideWidth*10) + 'mm X ' + str(SideHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm  x2\n' )
    f.writelines('Bottom: '+ str(TopBordWidth*10) + 'mm X ' + str(TopBordHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm\n')
    if TopBord:
        f.writelines('Top: '+ str(TopBordWidth*10) + 'mm X ' + str(TopBordHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm\n')
    f.writelines('Bord: '+ str(BordWidth*10) + 'mm X ' + str(BordHeight*10) + 'mm X' + str(WoodThiknes*10) + 'mm  x'+str(BordAmount)+'\n')
    f.writelines('Lipping: '+ str(Lipping*10) + 'mm' )
