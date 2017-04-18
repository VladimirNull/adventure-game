import random
class Cell(object):
    def __init__(self,x,y,gen):
        # 5 river
        # 4 Butovo
        # 3 kotteges
        # 2 park
        # 1 road
        #
        viscosity = gen
        hp = random.randint(1,10)
        if hp == 5:
            hp = True
        else:
            hp = False
        self.land = gen
        self.viscosity = viscosity
        self.hp = hp
        self.x = x
        self.y = y
    def __str__(self):
        land = self.land
        if land == 1:
            out1 = "^"+str(self.viscosity)+"^"
        elif land == 2:
            out1 = "_"+str(self.viscosity)+"_"
        elif land == 3:
           out1 = "|"+str(self.viscosity)+"|"
        elif land == 4:
            out1 = "."+str(self.viscosity)+"."
        elif land == 5:
            out1 = "~"+str(self.viscosity)+"~"
        out2 = " "
        if self.hp == True:
            out2 = "+"
        return " "+out1+out2
        #return " ]"+str(self.x)+":"+str(self.y)+"[ "

class Earth(object):
    def __init__(self,x,y):
        id_board = "";
        for i in range(0,8):
            nmb = random.randint(0,9)
            id_board += str(nmb)
        self.id = id_board
        self.x = int(x)
        self.y = int(y)
        self.cells = []
        blueprint = self.blueprint_land_generator()
        for g in range(1,y+1):
            for i in range(1,x+1):
                try:
                    gen = blueprint[str(str(i)+":"+str(g))]
                except:
                    gen = 1
                cell = Cell(i,g,gen)
                self.cells.append(cell)
        self.win_x = random.randint(1,x)
        self.win_y = random.randint(1,y)
        print("earth created "+self.id)
    def blueprint_land_generator(self,difficult = "easy"):
        blueprint = {}
        if difficult == "easy":
            #drop park points
            park_point = []
            for i in range(1,30):
                park_point_x = random.randint(1,self.x)
                park_point_y = random.randint(1,self.y)
                park_point.append([park_point_x,park_point_y])
            #grow parks
            for park in park_point:
                kk = random.randint(5,25)
                x = park[0]
                y = park[1]
                for i in range(1,kk):
                    blueprint[str(str(x)+":"+str(y))] = 2
                    if (i % 2) == 0:                        
                        x = x + random.randint(0,1)
                        y = y + random.randint(0,1)
                    else:
                        x = x + random.randint(-1,1)
                        y = y + random.randint(-1,1)
            #drop houses
            house_point = []
            for i in range(1,10):

                house_point_x = random.randint(1,round(self.x/3))
                house_point_y = random.randint(1,self.y)
                house_point.append([house_point_x,house_point_y])
                
                house_point_x = random.randint(round(self.x/3),round(self.x/3)*2)
                house_point_y = random.randint(1,self.y)
                house_point.append([house_point_x,house_point_y])
                
                house_point_x = random.randint(round(self.x/3)*2,self.x)
                house_point_y = random.randint(1,self.y)
                house_point.append([house_point_x,house_point_y])
            #grow houses
            for house in house_point:
                x = house[0]
                y = house[1]
                length = random.randint(5,10)
                direction = random.randint(0,1)
                if direction == 0:
                    for i in range(1,length):
                        blueprint[str(str(x)+":"+str(y))] = 3
                        y += 1
                elif direction == 1:
                    for i in range(1,length):
                        blueprint[str(str(x)+":"+str(y))] = 3
                        x += 1
            #drop butovo
            butovo_point = []
            for i in range(1,5):

                butovo_point_x = random.randint(1,round(self.x/3))
                butovo_point_y = random.randint(1,self.y)
                butovo_point.append([butovo_point_x,butovo_point_y])
                
                butovo_point_x = random.randint(round(self.x/3),round(self.x/3)*2)
                butovo_point_y = random.randint(1,self.y)
                butovo_point.append([butovo_point_x,butovo_point_y])
                
                butovo_point_x = random.randint(round(self.x/3)*2,self.x)
                butovo_point_y = random.randint(1,self.y)
                butovo_point.append([butovo_point_x,butovo_point_y])
            #grow houses
            for butovo in butovo_point:
                x = butovo[0]
                y = butovo[1]
                length = random.randint(4,10)
                direction = random.randint(0,1)
                if direction == 0:
                    for i in range(1,length):
                        blueprint[str(str(x)+":"+str(y))] = 4
                        y += 1
                elif direction == 1:
                    for i in range(1,length):
                        blueprint[str(str(x)+":"+str(y))] = 4
                        x += 1
            #drop river
            river_point = []
            for i in range(1,3):

                river_point_x = random.randint(1,round(self.x/3))
                river_point_y = random.randint(1,self.y)
                river_point.append([river_point_x,river_point_y])
                
                river_point_x = random.randint(round(self.x/3),round(self.x/3)*2)
                river_point_y = random.randint(1,self.y)
                river_point.append([river_point_x,river_point_y])
                
                river_point_x = random.randint(round(self.x/3)*2,self.x)
                river_point_y = random.randint(1,self.y)
                river_point.append([river_point_x,river_point_y])
            #grow houses
            for river in river_point:
                x = river[0]
                y = river[1]
                length = random.randint(20,40)
                direction = random.randint(0,1)
                if direction == 0:
                    for i in range(1,length):
                        blueprint[str(str(x)+":"+str(y))] = 5
                        y += 1
                elif direction == 1:
                    for i in range(1,length):
                        blueprint[str(str(x)+":"+str(y))] = 5
                        x += 1
        return blueprint
            
    def show_viscosity(self,x,y):
        viscosity = 0
        for cell in self.cells:
            if cell.x == x and cell.y == y:
                viscosity = cell.viscosity
        return viscosity
    def land_hero(self,hero):
        x_hero_land = random.randint(1,self.x)
        y_hero_land = random.randint(1,self.y)
        hero.x = x_hero_land
        hero.y = y_hero_land
        hero.board = self.id
        print (hero.name+" landed to "+str(hero.x)+":"+str(hero.y))
             