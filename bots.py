class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Orc(object):
    all_hit_zone = []
    all_first_alert = []
    all_second_alert = []
    first_alert = []
    second_alert = []  
    hit_zone = []
    for i in range(-1,2):
        for g in range(-1,2):
            all_hit_zone.append([i,g])
    for tmp in all_hit_zone:
        if tmp not in [0,0]:
            hit_zone.append(tmp)
    for i in range(-2,3):
        for g in range(-2,3):
            all_first_alert.append([i,g])
    for tmp in all_first_alert:
        if tmp not in all_hit_zone:
            first_alert.append(tmp)
    for i in range(-3,4):
        for g in range(-3,4):
            all_second_alert.append([i,g])
    for tmp in all_first_alert:
        if tmp not in all_second_alert:
            second_alert.append(tmp)
    last_alert = [[2,-4],[1,-4],[0,-4],[-1,-4],[-2,-4],[-4,-2],[-4,-1],[-4,-1],[-4,0],[-4,1],[-4,2],[-2,4],[-1,4],[0,4],[1,4],[2,4],[4,2],[4,1],[4,0],[4,-1],[4,-2]]

    def __init__(self,x,y):
        import random
        self.name = "bot-"+str(random.randint(0,100))
        self.health = 5
        self.hit = 5
        self.defence = 5
        self.x = x
        self.y = y
        self.target = []
        self.anger = 0
        self.walk = 0
        self.busted = 10
    def __str__(self):
        if self.anger == 0:
            return "<div class='anger_0'>bt"+str(self.name)+"</div>"
        elif self.anger == 1:
            return "<div class='anger_1'>bt"+str(self.name)+"</div>"
        elif self.anger == 2:
            return "<div class='anger_2'>bt"+str(self.name)+"</div>"