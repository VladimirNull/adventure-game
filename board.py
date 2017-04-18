import earth,hero,os,random,bots,itertools,math,time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class BoardWalk(object):
    # name weight type value cost
    # types:
    #   1 cennosti
    #   2 health
    #   3 movies
    #   
    goods=[['royal',5,1,0,500],['tumba',4,1,0,100],['podsvechnik',3,1,0,50],['keglya',2,1,0,10],['chasi',1,1,0,100],['small aptechka',1,2,5,5000],['normal aptechka',1,2,10,10000],['koffein',1,3,10,5000]]
    def __init__(self,earth,players,mode = "single"):
        self.id = earth.id
        self.earth = earth
        self.players = players
        self.make_metric()
        self.dice = 0
        self.winners = []
        self.losers = []
        self.bots = []
        self.walking_players = []
        self.last_in_round_walked = None
        self.walking_bots = []
        self.movie = []
        self.locked = False
        self.birth = time.time()
        self.now_walk = None
        self.time_to_stink = 10
        self.dice_dropped = False
        self.start_waiting_dice = time.time()
        self.auto_drop = 0
        self.animate = ""
        # mode
        # 1 single game for one player, no joiners, no view for others
        # 2 coop mode, others all welcome
        if mode == "single":
            self.time_to_start = 1
            self.mode = 1
        elif mode == "coop":
            self.time_to_start = 20
            self.mode = 2
    def cell_by_xy(self,x,y):
        index = self.earth.x*y
        index += x
        if x >= 0 and x < self.earth.x and y >= 0 and y < self.earth.y:
            return self.earth.cells[int(index)]
        else:
            return False
    def show_tv(self,center_x=2,center_y=2):
        #os.system('clear')
        out = ""
        #priglashenie v igru
        if self.locked == False:
            try:
                out = "waiting players</br>"
                for player in self.players:
                    out += str(player)+"</br>"
            except:
                out = "welcome!!!"
        #doska v processe igri
        elif self.players!=[] and self.locked == True:
            out = ""            
            n = 4
            show_x = []
            show_y = []
            for i in range(-n,n+1):
                show_x.append((center_x-1)+i)
                show_y.append((center_y-1)+i)
            for row in show_y:
                for line in show_x:                    
                    cell = self.cell_by_xy(line,row)
                    if cell!=False:
                        if cell.viscosity == 5:
                            out += "<div class='cell_plate-5'>"
                        elif cell.viscosity == 1:
                            out += "<div class='cell_plate-1'>"
                        elif cell.viscosity == 3:
                            out += "<div class='cell_plate-3'>"
                        elif cell.viscosity == 2:
                            out += "<div class='cell_plate-2'>"
                        elif cell.viscosity == 4:
                            out += "<div class='cell_plate-4'>"
                        if self.earth.win_x == cell.x and self.earth.win_y == cell.y:
                            out += "<div class='cell_exit'></div>" 
                        for hero in self.players:
                            max_health = 20
                            moves_left = ""
                            if hero.x == cell.x and hero.y == cell.y and hero.name!=self.now_walk:
                                out += "<div class='hero'><div class='hero-name'>"+str(hero.name)+"</div></div>"
                            if hero.x == cell.x and hero.y == cell.y and hero.name==self.now_walk:
                                out += "<div class='hero' id='moving_obj'>moving<div class='hero-name'>"+str(hero.name)+"</div></div>"
                        for bot in self.bots:
                            if bot.x == cell.x and bot.y == cell.y and bot.name!=self.now_walk:
                                out += "<div class='bot_waiting'></div>"
                            if bot.x == cell.x and bot.y == cell.y and bot.name==self.now_walk:
                                out += "<div class='bot_waiting' id='moving_obj'>moving</div>"
                        out += "</div>"
                    else:
                        out += "<div class='cell_plate-6'></div>  "
                out = out + "<div class='divide'></div>"
            i = 0
            bottom_stroke = ""
        
            out = out + bottom_stroke +"</br>"
        #igra okonchena, vivod pobediteley i proigravshih
        elif self.players==[] and self.locked == True:            
            try:
                out += "</br>winners</br>"
                for winner in self.winners:
                    out+=winner.name
            except:
                out += "</br>no winners</br>"
            try:
                out += "</br>losers</br>"
                for loser in self.losers:
                    out+=loser.name
            except:
                out += "</br>no losers</br>"
        return out        
    def minimap(self,name_player,center_x=2,center_y=2):
        n = 12
        out = ""
        show_x = []
        show_y = []
        for i in range(-n,n+1):
            show_x.append((center_x-1)+i)
            show_y.append((center_y-1)+i)
        for row in show_y:
            for line in show_x:
                cell = self.cell_by_xy(line,row)
                if cell!=False:
                    if cell.viscosity == 5:
                        out += "<div class='minimap_5'>"
                    elif cell.viscosity == 1:
                        out += "<div class='minimap_1'>"
                    elif cell.viscosity == 3:
                        out += "<div class='minimap_3'>"
                    elif cell.viscosity == 2:
                        out += "<div class='minimap_2'>"
                    elif cell.viscosity == 4:
                        out += "<div class='minimap_4'>"
                    if self.earth.win_x == cell.x and self.earth.win_y == cell.y:
                        out += "<div class='minimap_win'></div>"
                    for bot in self.bots:
                        if bot.x == cell.x and bot.y == cell.y:
                            out += "<div class='minimap_bot'></div>"
                    #print("cell x == "+str(cell.x)+" and center x == "+str(center_x))
                    if center_x == cell.x and center_y == cell.y:
                        out += "<div class='minimap_hero_self'></div>"
                    out += "</div>"
                else:
                    out += "<div class='minimap_6'></div>"
            out = out + "<div class='divide'></div>"
        return out
     
    def bot_animate_dict(self,x,y):
        index = "i"+str(int(x))+str(int(y))
        #print "index ==== " + str(index)
        pm = {
        "i-11":["$('#moving_obj').animate({'top': '+=64px','left': '-=64px'}, 700 );"],
        "i01":["$('#moving_obj').animate({'top': '+=64px'}, 700 );"],
        "i11":["$('#moving_obj').animate({'top': '+=64px','left': '+=64px'}, 700 );"],
        "i-10":["$('#moving_obj').animate({'left': '-=64px'}, 700 );"],
        "i00":[""],
        "i10":["$('#moving_obj').animate({'left': '+=64px'}, 700 );"],
        "i-1-1":["$('#moving_obj').animate({'top': '-=64px','left': '-=64px'}, 700 );"],
        "i0-1":["$('#moving_obj').animate({'top': '-=64px'}, 700 );"],
        "i1-1":["$('#moving_obj').animate({'top': '-=64px','left': '+=64px'}, 700 );"]
        }
        return pm[str(index)][0]
    def bot_hit_dict(self,x,y):
        index = "i"+str(int(x))+str(int(y))
        #print "index ==== " + str(index)
        pm = {
        "i-11":["$('#moving_obj').animate({'top': '+=30px','left': '-=30px'},100).animate({'top': '-=30px','left': '+=30px'},200).animate({'top': '+=55px','left': '-=55px'},100).animate({'top': '-=55px','left': '+=55px'},200);"],
        "i01":["$('#moving_obj').animate({'top': '+=30px'}, 100 ).animate({'top': '-=30px'}, 200 ).animate({'top': '+=55px'}, 100 ).animate({'top': '-=55px'}, 200 );"],
        "i11":["$('#moving_obj').animate({'top': '+=30px','left': '+=30px'}, 100 ).animate({'top': '-=30px','left': '-=30px'}, 200 ).animate({'top': '+=55px','left': '+=55px'}, 100 ).animate({'top': '-=55px','left': '-=55px'}, 200 );"],
        "i-10":["$('#moving_obj').animate({'left': '-=30px'}, 100 ).animate({'left': '+=30px'}, 200 );"],
        "i00":[""],
        "i10":["$('#moving_obj').animate({'left': '+=30px'}, 100 ).animate({'left': '-=30px'}, 200 ).animate({'left': '+=55px'}, 100 ).animate({'left': '-=55px'}, 200 );"],
        "i-1-1":["$('#moving_obj').animate({'top': '-=30px','left': '-=30px'},100 ).animate({'top': '+=30px','left': '+=30px'},200 ).animate({'top': '-=55px','left': '-=55px'},100 ).animate({'top': '+=55px','left': '+=55px'},200 );"],
        "i0-1":["$('#moving_obj').animate({'top': '-=30px'}, 100 ).animate({'top': '+=30px'}, 200 ).animate({'top': '-=55px'}, 100 ).animate({'top': '+=55px'}, 200 );"],
        "i1-1":["$('#moving_obj').animate({'top': '-=30px','left': '+=30px'}, 100 ).animate({'top': '+=30px','left': '-=30px'}, 200 ).animate({'top': '-=55px','left': '+=55px'}, 100 ).animate({'top': '+=55px','left': '-=55px'}, 200 );"]
        }
        return pm[str(index)][0]
    def around(self,creature,mode = 1):
        # mode:
        # 1 default, full show around
        # 2 for controlpad, only index and action
        pm = {
            "1":['-1','1','w',"$('#moving_obj').animate({'top': '+=64px','left': '-=64px'}, 700 );"],
            "2":['0','1','w',"$('#moving_obj').animate({'top': '+=64px'}, 700 );"],
            "3":['1','1','w',"$('#moving_obj').animate({'top': '+=64px','left': '+=64px'}, 700 );"],
            "4":['-1','0','w',"$('#moving_obj').animate({'left': '-=64px'}, 700 );"],
            "5":['0','0','r',""],
            "6":['1','0','w',"$('#moving_obj').animate({'left': '+=64px'}, 700 );"],
            "7":['-1','-1','w',"$('#moving_obj').animate({'top': '-=64px','left': '-=64px'}, 700 );"],
            "8":['0','-1','w',"$('#moving_obj').animate({'top': '-=64px'}, 700 );"],
            "9":['1','-1','w',"$('#moving_obj').animate({'top': '-=64px','left': '+=64px'}, 700 );"],
            "0":['0','0','d',""]
            }
        pm_pad = []
        pm_pad_tmp = []
        x = creature.x
        y = creature.y     
        place = self.cell_by_xy(x-1,y-1)
        try:        
            place_viscosity = place.viscosity
        except:
            place_viscosity = 1
        for i in list(range (1,5))+list(range(6,10)):
            try_x = x+int(pm[str(i)][0])
            try_y = y+int(pm[str(i)][1])
            if self.wall(try_x,try_y)==True:
                pm[str(i)]=[int(pm[str(i)][0]),int(pm[str(i)][1]),'s']
            if self.occupied(try_x,try_y)!=False:
                pm[str(i)]=[int(pm[str(i)][0]),int(pm[str(i)][1]),'h',self.occupied(try_x,try_y),self.bot_hit_dict(int(pm[str(i)][0]),int(pm[str(i)][1]))]
            if mode == 2:
                pm_pad_tmp.append([str(i),pm[str(i)][2]])
        pm[str(5)]=[int(pm[str(5)][0]),int(pm[str(5)][1]),str(place_viscosity)]
        if mode == 1:
            return pm
        elif mode == 2:            
            #print place
            for i in (7,8,9,4,5,6,1,2,3):
                if i == 5:
                    pm_pad.append([5,str(place_viscosity)])
                for pad in pm_pad_tmp:
                    if int(pad[0]) == i:
                        pm_pad.append(pad)
                        pm_pad_tmp.remove(pad)
            return pm_pad
            
    def around_players(self,creature):
        pm = {
            "1":['-1','1','w'],
            "2":['0','1','w'],
            "3":['1','1','w'],
            "4":['-1','0','w'],
            "6":['1','0','w'],
            "7":['-1','-1','w'],
            "8":['0','-1','w'],
            "9":['1','-1','w']
            }
        x = creature.x
        y = creature.y
        
        for i in list(range(1,5))+list(range(6,10)):
            try_x = x+int(pm[str(i)][0])
            try_y = y+int(pm[str(i)][1])
            if self.occupied_player(try_x,try_y)!=False:
                pm[str(i)]=[int(pm[str(i)][0]),int(pm[str(i)][1]),'h',self.occupied_player(try_x,try_y)]
        return pm
    def move(self):
        player = self.walking_players[0]
        go = self.around(player)
        action = False
        waiting_default_time = 9000
        waiting_time = time.time()
        player.card_move=[]
        while action == False:
            time.sleep(0.2)
            self.now_walk = player.name
            if (time.time()-waiting_time) > (waiting_default_time-9):
                razn = "%.0f" % (waiting_time+waiting_default_time-time.time())
                self.now_walk = player.name + str(razn) + str(" hurry")
            if (time.time()-waiting_time) > (waiting_default_time-3):
                self.now_walk = player.name + str(razn) + str(" snuffle")
            if (time.time()-waiting_time) > waiting_default_time:
                action = 's'
                player.health -= int(self.dice)
                self.dice = 0
                self.now_walk = None
                break
            if player.card_move!=[]:
                index_go, timer_go, doing = player.card_move
                try:
                    action = go[str(index_go)][2]
                except:
                    action = False
                #print action
                if action == 'w':
                    """ WALK """
                    #self.movie.append(["w",str(player),player.x,player.y,int(go[str(index_go)][0]),int(go[str(index_go)][1])])
                    self.animate = go[str(index_go)][3]
                    time.sleep(0.5)
                    self.animate = ""
                    player.x = player.x + int(go[str(index_go)][0])
                    player.y = player.y + int(go[str(index_go)][1])
                    self.dice = self.dice - int(self.earth.show_viscosity(player.x,player.y))
                    player.health -= 1
                elif action == 'h':
                    """ HIT """
                    self.animate = go[str(index_go)][4]
                    time.sleep(0.5)
                    self.animate = ""
                    self.hit(player,go[str(index_go)][3])
                    self.dice = 0
                elif action == 'd':
                    """ DIG """
                    pass
                elif str(action) == doing:
                    """ AHAHAHHA """
                    if doing == "4":
                        self.stealing(player,"butovo")
                        #print("rush Butovo")
                    if doing == "3":
                        self.stealing(player,"house")
                        #print("rush house")
                    player.health += int(self.dice)
                    self.dice = 0
                else:
                    pass
                    #print ("nothing")
        player.card_move=[]
    
    def stealing(self,player,district):
        gen_fail = random.randint(1,10)
        if gen_fail != 1:
            n_goods = random.randint(1,3)
            for i in range (1,n_goods):
                player.bag.append(self.goods[random.randint(0,len(self.goods)-1)])
            player.reloading_bag()
        else:
            pass
            #print("FAIL")
        
    def make_metric(self):
        i = 1
        for player in self.players:
            player.metric = i
            if i == 1:
                player.walk = 1
            else:
                player.walk = 0
            #print ("i="+str(i)+" "+str(player.name) +" metric  "+ str(player.metric)+" walking"+str(player.walk))
            i = i + 1
    def preparing_drop_dice(self):
        self.dice = 0
        self.auto_drop = 9
        player = self.walking_player()
        if player!=False:        
            self.now_walk = player.name
            self.dice_dropped = False
            self.start_waiting_dice = time.time()
    def waiting_drop(self):
        time.sleep(1)
        #print("waiting_drop "+str(time.time()-self.start_waiting_dice))
        self.auto_drop = 10 - (time.time()-self.start_waiting_dice)
        if self.auto_drop < 1:
            player = self.walking_player()
            if player!=False:
                player.health -= 10
                self.lose(from_player=True)
                self.remove_walked_player()
                if self.walking_players_left() != 0:
                    self.preparing_drop_dice()
                else:
                    self.dice_dropped = True
                    self.dice = 0
    def drop_dice(self,from_player=False):
        self.dice_dropped = True
        cub1 = random.randint(1,6)
        cub2 = random.randint(1,6)
        koeff = 0
        if from_player == True:
            player = self.walking_player()            
            koeff = player.overtote
        self.dice = (cub1-koeff) + (cub2-koeff)        
    def heroes_left(self):
        i = 0
        for player in self.players:
            i += 1
        if i!=0:
            return i
        else:
            return False
    def walking_player(self):
        #print("walking players == "+str(len(self.walking_players)))
        if len(self.walking_players)==0:
            if len(self.players)==0:
                return False
            else:
                return self.players[int(len(self.players)-1)]
        else:
            return self.walking_players[0]
    def not_walking_players(self):
        not_walk = []
        for player in self.players:
            if player != self.walking_player():
                not_walk.append(player)
        return not_walk
    def next_player(self, turn = True):       
        if self.players!=[]:
            list_metric = []
            round_end = False
            for player in self.players:
                list_metric.append(player.metric)
            walk_player = self.walking_player()
            #print ("list metric: " + str(list_metric))
            
            now_metric = walk_player.metric
            now_index = list_metric.index(now_metric)
            #print("now index"+str(now_index))
            
            next_index = now_index + 1
            #print("next index"+str(next_index))
            
            len_metric = len(list_metric)
            
            if next_index > (len_metric-1):
                next_index = 0
                round_end = True
            now_metric = list_metric[next_index]
            if turn == True:
                for player in self.players:
                    if now_metric == player.metric:
                        player.walk = 1
                    else:
                        player.walk = 0
            return round_end 
        else:
            #print("no players left")
            return False
            
    def behind_player(self):
        if self.players!=[]:
            list_metric = []
            for player in self.players:
                list_metric.append(player.metric)
            walk_player = self.walking_player()
            #print ("list metric: " + str(list_metric))
            
            now_metric = walk_player.metric
            now_index = list_metric.index(now_metric)
            #print("now index"+str(now_index))
            
            behind_index = now_index - 1
            #print("behind_index"+str(behind_index))
            
            len_metric = len(list_metric)
            
            if behind_index < 0:
                behind_index = (len_metric-1)
            now_metric = list_metric[behind_index]
            for player in self.players:
                if now_metric == player.metric:
                    player.walk = 1
                else:
                    player.walk = 0
        else:
            #print("no players left")
            return False
            
    def reach_destination(self):
        answ = False
        walking_player = self.walking_player()
        if walking_player.x == self.earth.win_x and walking_player.y == self.earth.win_y:
            ended_player = walking_player
            ended_player.place = 1
            self.dice = 0
            self.winners.append(ended_player)
            if len(self.winners) == 1:
                ended_player.score += 100
            elif len(self.winners) == 2:
                ended_player.score += 50
            elif len(self.winners) == 3:
                ended_player.score += 15
            else:
                ended_player.score += 5
            ended_player.save()
            ended_player.current_board = None
            self.players.remove(ended_player)
            answ = True
        return answ
    def lose(self,from_player=False,busted=0):
        tmp_players = []
        if from_player == False:
            for player in self.players:
                if player.health < 1:
                    player.prison = busted
                    player.place = 2
                    self.losers.append(player)
                    player.save()
                    player.current_board = None
                else:
                    tmp_players.append(player)
            self.players = tmp_players
        elif from_player == True:
            for player in self.players:
                if player.health < 1 and player==self.walking_player():
                    self.dice = 0
                    self.losers.append(player)
                    player.save()
                    player.current_board = None
                    player.place = 2
                else:
                    tmp_players.append(player)
            self.players = tmp_players            
                        
    def look_neighbors(self,player):
        neighbors = []
        pm = self.around(player)
        for i in range (1,5)+range(6,10):
            action = pm[str(i)][2]
            if action == 'h':
                neighbors.append(pm[str(i)][3])
        return neighbors
    def occupied(self,x,y):
        answ = False
        for player in self.players:
            if x == player.x and y == player.y:
                answ = player
        for bot in self.bots:
            if x == bot.x and y == bot.y:
                answ = bot
        return answ
    def occupied_player(self,x,y):
        answ = False
        for player in self.players:
            if x == player.x and y == player.y:
                answ = player
        return answ
    def occupied_bot(self,x,y):
        answ = False
        for bot in self.bots:
            if x == bot.x and y == bot.y:
                answ = bot
                #print("occupied bot!!!!!!!")
        return answ
    def wall(self,x,y):
        bx = self.earth.x
        by = self.earth.y
        out = False
        if (x==0 and y==(by+1))or(y==(by+1))or(x==(bx+1) and y==(by+1))or(x==(bx+1))or(x==(bx+1) and y==0)or(y==0)or(x==0 and y==0)or(x==0):
            out = True
        return out
    def hit(self,attacker,defender,bot_attack=False):
        attack_points = attacker.hit + self.dice
        defend_points = defender.defence
        hit_points = attack_points - defend_points
        if hit_points < 1:
            hit_points = 1
        defender.health -= hit_points
        if defender.health < 1:
            self.die_bots()
            if bot_attack==False:
                self.lose()
            else:
                self.lose(busted=attacker.busted)

    def drop_off_orcs(self):
        for i in range(1,8):
            drop = False
            while drop == False:
                x = random.randint(1,self.earth.x)
                y = random.randint(1,self.earth.y)
                #print (x,y,self.occupied(x,y))
                if self.occupied(x,y) == False:
                    self.bots.append(bots.Orc(x,y))
                    drop = True
    def die_bots(self):
        for bot in self.bots:
            if bot.health<1:
                del self.bots[(self.bots.index(bot))]
    def collect_players(self):
        if len(self.players)!=0:
            for player in self.players:
                self.walking_players.append(player)
            self.last_in_round_walked = self.walking_players[int(len(self.walking_players)-1)]
        else:
            self.walking_players=False
    def collect_bots(self):
        for bot in self.bots:
            self.walking_bots.append(bot)
    def walking_players_left(self):
        i = 0
        if self.walking_players!=False:
            for player in self.walking_players:
                i+=1
        return i
    def walking_bots_left(self):
        i = 0
        for bot in self.walking_bots:
            i+=1
        return i
        
    def bot_action(self):
        direct_x = 0
        direct_y = 0
        bot = self.walking_bots[0]
        hit_zone = None
        targets = None
        bot.walk = 1
        self.animate = ""
        self.now_walk = str(bot.name)
        time.sleep(0.1)
        if self.hit_zone(bot) != []:
            hit_zone = self.hit_zone(bot)
            bot.anger = 2
            whom_hit = hit_zone[random.randint(0,(len(hit_zone))-1)]
            animate = self.bot_hit_dict(whom_hit[1],whom_hit[2])
            self.animate = animate
            time.sleep(0.9)
            self.animate = ""
            self.hit(bot,whom_hit[0],bot_attack=True)
            self.dice = 0
            direct_x = 0
            direct_y = 0
        if self.search_target(bot) != []:
            bot.anger = 1
            targets = self.search_target(bot)
            target = targets[random.randint(0,len(targets)-1)]
            #print (str(bot.name)+" wish "+str(target)+" dice="+str(self.dice))
            direction = self.search_direction(bot,target)
            direct_x = direction[0]
            direct_y = direction[1]  
            animate = self.bot_animate_dict(direct_x,direct_y)
            self.animate = animate
            time.sleep(0.5)
            self.animate = ""
        if hit_zone == None and targets == None:
            bot.anger = 0
            pm = self.around(bot)
            go = []
            for i in list(range (1,5))+list(range(6,10)):
                action = pm[str(i)][2]
                if action == 'w':
                    go.append([pm[str(i)][0],pm[str(i)][1]])
                    random_direction = go[random.randint(0,(len(go)-1))]
            direct_x = int(random_direction[0])
            direct_y = int(random_direction[1])
            animate = self.bot_animate_dict(direct_x,direct_y)
            self.animate = animate
            time.sleep(0.5)
            self.animate = ""
        bot.x += direct_x
        bot.y += direct_y
        self.dice = self.dice - int(self.earth.show_viscosity(bot.x,bot.y))
        bot.walk = 0
        
    def search_direction(self,source,target):
        directions = []
        x1 = source.x
        x2 = target.x
        y1 = source.y
        y2 = target.y        
        diff_x = x2 - x1
        diff_y = y2 - y1
        
        if diff_x!=0:
            koeff_x = round((diff_x/math.fabs(diff_x)),0)
        else:
            koeff_x = 0
        if diff_y!=0:
            koeff_y = round(diff_y/math.fabs(diff_y))
        else:
            koeff_y = 0            
        if koeff_x == 0:
            directions.append([0,koeff_y])
        else:
            directions.append([koeff_x,koeff_y])
            if diff_x<diff_y:
                directions.append([0,koeff_y])                   
        if koeff_y == 0:
            directions.append([koeff_x,0])
        else:
            directions.append([koeff_x,koeff_y])
            if diff_x>diff_y:
                directions.append([koeff_x,0])
        for i in range(1,10):
            try_return = directions[random.randint(0,(len(directions)-1))]
            if self.occupied_bot(x1+try_return[0],y1+try_return[1])==False:
                #print "RETURN!!! ======= "+str(try_return)
                return try_return
        #print("RETURN ZEEEEEEEERO!!!")
        return [0,0]
        
    def remove_walked_bot(self):
        del self.walking_bots[0]
    def remove_walked_player(self):
        self.now_walk = None
        if len(self.walking_players)!=0:
            del self.walking_players[0]
    def hit_zone(self,bot):
        x = bot.x
        y = bot.y
        target = []
        waves = [bots.Orc.hit_zone]
        for wave in waves:
            for check in wave:
                if self.occupied_player(x+check[0],y+check[1])!=False:
                    target.append([self.occupied_player(x+check[0],y+check[1]),check[0],check[1]])
            if target!=[]:
                break
        return target
    def search_target(self,bot):
        x = bot.x
        y = bot.y        
        target = []
        waves = [bots.Orc.first_alert,bots.Orc.second_alert,bots.Orc.last_alert]
        for wave in waves:
            for check in wave:
                if self.occupied_player(x+check[0],y+check[1])!=False:
                    target.append(self.occupied_player(x+check[0],y+check[1]))
            if target!=[]:
                break
        return target
    def make_path(self,target,bot):
        bot_x = bot.x
        bot_y = bot.y
        tar_x = target.x
        tar_y = target.y
        
    def show_movie(self):
        #self.movie.append(["h",str(attaker),attaker_x,attaker_y,str(defender),defender_x,defender_y])
        #self.movie.append(["w",str(player),player.x,player.y,int(go[str(index_go)][0]),int(go[str(index_go)][1])])
        #self.movie.append(["w",str(bot),bot.x,bot.y,direct_x,direct_y])
        #for frame in self.movie:
         #   if frame[0] == "w":
          #      print "walk"
           # if frame[0] == "h":
            #    print "hit"
        return (self)
    def join(self,player):
        if self.locked == False:
            if (player not in self.players and player.current_board==None) or (player not in self.winners and player.current_board==None) or (player not in self.losers and player.current_board==None):
                if self.players == []:
                    self.birth = time.time()
                self.players.append(player)
                player.current_board = self.id
                player.place = 3
                #print("JOIN!!!!")
                return True
        else:
            return False
    def escape(self,player):
        if player in self.players and self.locked == False:
            self.players.remove(player)
            player.place = 1
            player.current_board = None
    def wash_and_clean(self):
        #time to fame
        time.sleep(10)        
        #open for new games
        self.locked = False
        self.birth = time.time()
        self.winners = []
        self.losers = []

    def sunrise(self):
        if (time.time() - self.birth) > self.time_to_start and self.players!=[] and self.locked == False:
            return True
        else:
            return False
    def sunset(self):
        time.sleep(20)
    def stink(self):
        if (time.time() - self.birth) > self.time_to_stink and self.players==[] and self.locked == False:
            return True
        else:
            return False
    def shuffle_players(self):
        random.shuffle(self.players)
        self.players[0].walk = 1
        metric = 1
        for player in self.players:
            player.metric = metric
            metric += 1
    def drop_off_players(self):
        for player in self.players:
            drop = False
            while drop == False:
                x = random.randint(1,self.earth.x)
                y = random.randint(1,self.earth.y)
                #print (x,y,self.occupied(x,y))
                if self.occupied(x,y) == False:
                    player.x = x
                    player.y = y
                    drop = True
    def player_using_item(self,using_item):
        #print("using item --------"+str(using_item))
        player = self.walking_player()
        #print player.bag
        for item in player.bag:
            if item[0] == using_item:
                if item[2]==2:
                    player.health += item[3]
                    player.bag.remove(item)
                    break
                elif item[2]==3:
                    self.dice += item[3]
                    player.bag.remove(item)
                    break
        player.reloading_bag()
        