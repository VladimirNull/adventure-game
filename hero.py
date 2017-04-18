class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Hero(object):
    def __init__(self,name):
        import random
        self.name = name
        self.max_health = 20
        self.health = 15
        self.bag = [['keglya', 2], ['podsvechnik', 3], ['chasi', 1]]
        # limit load
        self.carrying = 15
        # now weight in bag
        self.tote = 0
        self.overtote = 0
        self.chest = [['keglya', 2], ['podsvechnik', 3], ['chasi', 1]]
        self.hit = 5
        self.defence = 5
        self.moves = 5
        self.x = 0
        self.y = 0
        self.board = ""
        self.metric = 0
        self.walk = 0
        self.score = 0
        self.exp = 0
        self.card_move = []
        self.current_board = None
        self.prison = 0
        #places
        # 1 ubezhishe
        # 2 hospital
        # 3 game
        # 4 prison
        self.place = 1
    def __str__(self):
        return self.name
    def save(self):
        import pickle, shelve
        db = shelve.open("heroes.dat")
        db[self.name] = self
        try:
            db.sync()
            answer = True
        except:
            print("Cant sync")
            answer = False
        return answer
    def load(self):
        import pickle, shelve
        db = shelve.open("heroes.dat")
        try:
            hero = db[self.name]
        except:
            hero = False
        if hero:
            self.name = hero.name
            self.max_health = hero.max_health
            self.health = 1000
            self.bag = hero.bag
            self.chest = hero.chest
            self.hit = hero.hit
            self.defence = hero.defence
            self.moves = hero.moves
            self.score = hero.score
            self.exp = hero.exp
            self.walk = 0
            self.metric = 0
            self.card_move = []
            self.current_board = None
            self.place = 1
            self.carrying = hero.carrying
            self.tote = hero.tote
            self.overtote = hero.overtote
            self.prison = 1
            return True
        else:
            return False
    def kach(self):
        self.hit += 5
    def rest(self):
        pass
    def reloading_bag(self):
        weight = 0
        koeff = 0
        if self.bag!=[]:
            for item in self.bag:
                weight += item[1]
        if self.tote > self.carrying:
            koeff = int(round(6*((float(self.tote) - float(self.carrying))/float(self.carrying))))
            print ("koeff="+str(koeff))
            if koeff > 5:
                koeff = 6
        self.tote = weight
        self.overtote = koeff
    def remove_from_bag(self,del_item):
        for item in self.bag:
            if item[0] == del_item:
                self.bag.remove(item)
                break
        self.reloading_bag()
    def unload_bag_to_chest(self):
        for item in self.bag:
            self.chest.append(item)
        self.bag = []
        self.reloading_bag()
    def item_to_chest(self,moving_item):      
        for item in self.bag:
            if item[0] == moving_item:
                self.chest.append(item)
                self.bag.remove(item)
                break
        self.reloading_bag()
    def item_to_bag(self,moving_item):    
        print('to_bag')
        for item in self.chest:
            if item[0] == moving_item:
                self.bag.append(item)
                self.chest.remove(item)
                break
        self.reloading_bag()
        
        
        
        