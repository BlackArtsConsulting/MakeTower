"""
MakeTower

Please leave questions and comments at the github repo where you found this.

Have fun!
Anthony Hauck | Black Arts Consulting
anthony@blackarts.co
"""

from hypar import glTF
from random import randint, uniform

from aecSpace.aecColor import aecColor
from aecSpace.aecShaper import aecShaper
from aecSpace.aecPoint import aecPoint
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpacer import aecSpacer

def makeTower(bldgWidth: float = 20, 
              bldgDepth: float = 20, 
              floorHeight: float = 3, 
              bldgLevels: int = 10, 
              plinthScale: float = 1.1):
    """
    Constructs a series of tower space distibution examples from a 
    combination of fixed and randomly set values and floor divisions.
    """
    spacer = aecSpacer()
    shaper = aecShaper()
    
    def full(point, xWidth, yDepth, zHeight, level):
        floor = aecSpace()
        floor.boundary = shaper.makeBox(point, xWidth, yDepth)
        floor.height = zHeight
        floor.level = level
        setColors([floor])
        return [floor]
    
    def halfDepth(point, xWidth, yDepth, zHeight, level):
        depth = yDepth * 0.5
        half1 = aecSpace()  
        half1.boundary = shaper.makeBox(point, xWidth, depth)
        half1.height = zHeight
        half1.level = level
        halfSpaces = [half1] + spacer.row(half1, xAxis = False)
        setColors(halfSpaces)
        return halfSpaces
    
    def halfWidth(point, xWidth, yDepth, zHeight, level):
        width = xWidth * 0.5
        half1 = aecSpace()  
        half1.boundary = shaper.makeBox(point, width, yDepth)
        half1.height = zHeight
        half1.level = level
        halfSpaces = [half1] + spacer.row(half1)
        setColors(halfSpaces)
        return halfSpaces
    
    def quarterDepth(point, xWidth, yDepth, zHeight, level):
        if randint(0, 1) == 0:
            depth = yDepth * 0.25
            scale = 3
        else:
            depth = yDepth * 0.75
            scale = 0.333333333       
        half1 = aecSpace()  
        half1.boundary = shaper.makeBox(point, xWidth, depth)
        half1.height = zHeight
        half1.level = level        
        halfSpaces = [half1] + spacer.row(half1, xAxis = False)
        halfSpaces[1].scale(1, scale, 1, halfSpaces[1].points_floor[0])
        setColors(halfSpaces)
        return halfSpaces
    
    def quarterWidth(point, xWidth, yDepth, zHeight, level):
        if randint(0, 1) == 0:
            width = xWidth * 0.25
            scale = 3
        else:
            width = xWidth * 0.75
            scale = 0.333333333       
        half1 = aecSpace()  
        half1.boundary = shaper.makeBox(point, width, yDepth)
        half1.height = zHeight
        half1.level = level        
        halfSpaces = [half1] + spacer.row(half1)
        halfSpaces[1].scale(scale, 1, 1, halfSpaces[1].points_floor[0])
        setColors(halfSpaces)
        return halfSpaces
    
    def setColors(halfSpaces):
        colors = [aecColor.blue, aecColor.orange, aecColor.purple, aecColor.yellow]
        colorPick = randint(0, 3)
        halfSpaces[0].color = colors[colorPick]
        if len(halfSpaces) == 1: return
        colors.reverse()
        halfSpaces[1].color = colors[colorPick]
    
    def makeFloor(point, xWidth, yDepth, zHeight, level):
        floorType = randint(0, 4)
        if floorType == 0: floorSpaces = full(point, xWidth, yDepth, zHeight, level)
        if floorType == 1: floorSpaces = halfDepth(point, xWidth, yDepth, zHeight, level)
        if floorType == 2: floorSpaces = halfWidth(point, xWidth, yDepth, zHeight, level)
        if floorType == 3: floorSpaces = quarterDepth(point, xWidth, yDepth, zHeight, level)
        if floorType == 4: floorSpaces = quarterWidth(point, xWidth, yDepth, zHeight, level)
        return floorSpaces
    
    def makeCore(point, xWidth, yDepth, zHeight): 
        xCoord = (point.x - 5) + (xWidth * 0.5)
        yCoord = (point.y + (yDepth * (randint(0, 9) * 0.1)))
        point = aecPoint(xCoord, yCoord, point.z)
        core = aecSpace()
        core.boundary = shaper.makeBox(point, 10, 20)
        core.height = zHeight
        core.color = aecColor.gray
        return core  
    
    plinth = aecSpace()
    point = aecPoint()
    plinth.boundary = shaper.makeBox(point, bldgWidth, bldgDepth)
    plinth.scale(plinthScale, plinthScale, 2, plinth.centroid_floor)
    plinth.height = (floorHeight * 2)
    plinth.color = aecColor.green
    core = makeCore(point, bldgWidth, bldgDepth, floorHeight * (bldgLevels + 3))
    level = (floorHeight * 2)
    x = 0
    floors = []
    while x < bldgLevels:
        floors = floors + makeFloor(point, bldgWidth, bldgDepth, floorHeight, level)
        level += floorHeight
        x += 1
    model = glTF()
    colorBlue = model.add_material(0.0, 0.631, 0.945, 0.9, 0.8, "Blue")
    colorGray = model.add_material(0.5, 0.5, 0.5, 0.9, 0.8, "Gray")
    colorGreen = model.add_material(0.486, 0.733, 0.0, 0.9, 0.8, "Green")
    colorOrange = model.add_material(0.964, 0.325, 0.078, 0.9, 0.8, "Orange")
    colorPurple = model.add_material(0.75, 0.07, 1.0, 0.9, 0.8, "Purple")    
    colorYellow = model.add_material(1.0, 0.733, 0.0, 0.9, 0.8, "Yellow")
    mesh = core.mesh_graphic
    model.add_triangle_mesh(mesh.vertices, mesh.normals, mesh.indices, colorGray)        
    mesh = plinth.mesh_graphic
    model.add_triangle_mesh(mesh.vertices, mesh.normals, mesh.indices, colorGreen)
    area = 0
    levels = 0
    for space in floors:
        area += space.area
        levels += 1
        spaceMesh = space.mesh_graphic
        colorIndex = randint(0, 3)
        if colorIndex == 0: color = colorBlue
        if colorIndex == 1: color = colorOrange
        if colorIndex == 2: color = colorPurple
        if colorIndex == 3: color = colorYellow      
        model.add_triangle_mesh(spaceMesh.vertices, spaceMesh.normals, spaceMesh.indices, color)   
    return {"model": model.save_base64(), 'computed':{'floors':levels, 'area':area}}   
#    model.save_glb('model.glb')
#
#makeTower(bldgWidth = uniform(20, 70), 
#          bldgDepth = uniform(20, 70), 
#          floorHeight = uniform(4, 6),
#          bldgLevels = randint(10, 60), 
#          plinthScale = uniform(1, 2.5))        
        


