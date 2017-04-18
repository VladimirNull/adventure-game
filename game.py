import earth,hero,os,board
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template,flash
from contextlib import closing
import time
from werkzeug.datastructures import ImmutableMultiDict

games = []

class Saver_bro(object):
    def __init__(self):
        import threading
        self.boards = []
        self.list_players = []
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True 
        thread.start()
    def run(self):
        import time
        while True:
            self.refresh()
            for player in self.list_players:
               player.save()
            time.sleep(3)
    def refresh(self):
        self.list_players = list_players

class Boarder_bro(object):
    def __init__(self):
        import threading
        self.boards = []
        self.list_players = []
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True 
        thread.start()
    def __str__(self):
        out = "mover - >"
        for board in self.boards:
            out+=str(board.id)+" <-> "
        return out
    def run(self):
        import time
        while True:
            self.refresh()
            for board in self.boards:
                if board.sunrise() == True:
                    board.locked = True
                    board.shuffle_players()
                    board.drop_off_orcs()
                    board.drop_off_players()
                    gaming[str(board.id)] = Gamer_bro(board)
                    games.append(gaming[str(board.id)])
                if board.stink() == True:
                    list_boards.remove(board)
            for player in self.list_players:
                if player.place == 1 and player.health < player.max_health:
                    player
            time.sleep(0.5)
    def refresh(self):
        self.boards = list_boards
        self.list_players = list_players

class Hideout_bro(object):
    def __init__(self):
        import threading
        self.list_players = []
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True 
        thread.start()
    def run(self):
        import time
        while True:
            self.refresh()
            for player in self.list_players:
                if player.place == 1 and player.health < player.max_health:
                    player.health += 1
            time.sleep(4)
    def refresh(self):
        self.list_players = list_players

class Hospital_bro(object):
    def __init__(self):
        import threading
        self.list_players = []
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True 
        thread.start()
    def run(self):
        import time
        while True:
            self.refresh()
            for player in self.list_players:
                if player.place == 2:
                    if player.health < player.max_health:
                        player.health += 1
                    else:                  
                        if player.prison < 1:                    
                            player.place = 1
                        else:
                            player.place = 4
            time.sleep(2)
    def refresh(self):
        self.list_players = list_players

class Police_bro(object):
    def __init__(self):
        import threading
        self.list_players = []
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True 
        thread.start()
    def run(self):
        import time
        while True:
            self.refresh()
            for player in self.list_players:
                if player.place == 4:
                    if player.prison > 0:
                        player.prison -= 1
                    else:
                        player.place = 1
            time.sleep(5)
    def refresh(self):
        self.list_players = list_players

class Gamer_bro(object):
    def __init__(self,board):
        import threading
        self.board = board
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True 
        thread.start()
    def __str__(self):
        return True
    def run(self):
        import time
        while self.board.heroes_left()!=0:
            self.board.collect_players()
            while self.board.walking_players_left()!=0:
                self.board.preparing_drop_dice()
                while self.board.dice_dropped == False:
                    self.board.waiting_drop()
                while self.board.dice > 0:
                    self.board.move()
                    self.board.reach_destination()
                    self.board.lose(from_player=True)
                self.board.remove_walked_player()
            self.board.collect_bots()
            time.sleep(1)            
            while self.board.walking_bots_left()!=0:
                self.board.drop_dice()
                while self.board.dice > 0:
                    self.board.bot_action()
                self.board.remove_walked_bot()
        self.board.wash_and_clean()
    def refresh(self):
        import game
        self.boards = list_boards
        self.list_players = list_players
    

DATABASE = "heroes.dat"
SECRET_KEY = 'rtjeortuertjeqrotDFGjhqeortpeqrtvADFGjh934utv34t0AAAAAAAAAAeqrtujSJRT0AAAAAAAAAAeqrjtoqerjtojgSRTJqj0WI3RNNNNNNNNNN284250RR4KK0T0E'
list_boards = []
list_players = []
app = Flask(__name__)
app.config.from_object(__name__)
# big bros
saving = Saver_bro()
boarding = Boarder_bro()
hiding = Hideout_bro()
hospitaling = Hospital_bro()
policing = Police_bro()

gaming = {}
request_movies = [1,2,3,4,5,6,7,8,9]

def generate_world():
    import earth
    earth = earth.Earth(10,10)
    return earth
    
def board_by_id(board_id):
    answ = "empty"    
    for board in list_boards:
        if board.id == board_id:
            answ = str(board)
    return answ
def board_as_object(board_id):
    answ = False   
    for board in list_boards:
        if board.id == board_id:
            answ = board
    return answ

def logged_player_as_object():
    try:
        check_player = session['logged']
    except:
        return False
    answ = False
    for player in list_players:
        if check_player == player.name:
            answ = player
    return answ
    
def dump_player_to_JSON(values="short"):
    player = logged_player_as_object() 
    answ = {}    
    if values=="short":    
        answ['name'] = player.name
        answ['bag'] = player.bag
        answ['tote'] = player.tote
        answ['carrying'] = player.carrying
        answ['overtote'] = player.overtote
        answ['max_health'] = player.max_health
        answ['health'] = player.health
        answ['hit'] = player.hit
        answ['defence'] = player.defence
        answ['score'] = player.score
        answ['exp'] = player.exp
        answ['place'] = player.place
        answ['prison'] = player.prison
    elif values=="hideout":
        answ['name'] = player.name
        answ['bag'] = player.bag
        answ['tote'] = player.tote
        answ['carrying'] = player.carrying
        answ['overtote'] = player.overtote
        answ['max_health'] = player.max_health
        answ['health'] = player.health
        answ['hit'] = player.hit
        answ['defence'] = player.defence
        answ['score'] = player.score
        answ['exp'] = player.exp
        answ['place'] = player.place
        answ['chest'] = player.chest
    elif values=="user_info":
        answ['name'] = player.name
        answ['tote'] = player.tote
        answ['carrying'] = player.carrying
        answ['bag'] = player.bag
        answ['max_health'] = player.max_health
        answ['health'] = player.health
        answ['hit'] = player.hit
        answ['defence'] = player.defence
        answ['score'] = player.score
        answ['exp'] = player.exp
        answ['place'] = player.place
    return answ
    
@app.route('/404')
def p404():
    return render_template('404.html')
@app.route('/')
def check_login():
    print("check login")
    if logged_player_as_object()==False:
        return render_template('login.html',login=login)
    else:
        return render_template('hideout.html',login=logged_player_as_object().name)
        
@app.route('/',methods=['GET', 'POST'])
def index():
    if logged_player_as_object()==False:
        return render_template('login.html',login=login)
    return render_template('game.html',login=logged_player_as_object().name)
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        tmp_player = str(request.form['username'])
        tmp_names = []
        for tmp in list_players:
            tmp_names.append(tmp.name)
        if tmp_player not in tmp_names:
            player = hero.Hero(tmp_player)
            if player.load():
                session['logged'] = player.name
                list_players.append(player)
                login = session['logged']
                return redirect(url_for('streets'))
            else:
                session['logged'] = player.name
                list_players.append(player)
                player.save()
                login = session['logged']
                return redirect(url_for('hideout'))
        else:
            error = "already logged"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session['logged'] = "guest"
	return redirect(url_for('index'))

@app.route('/game/frame_boards')  
def frame_boards():
    try:
        join = self.logged_player_as_object.current_board
    except:
        join = None
    out = []
    for board in list_boards:
        out.append([board.id,board.players])
    return render_template('frame_boards.html',tv_screen=(out,join))

@app.route('/game',methods=['GET', 'POST'])  
def game_main():
    player = logged_player_as_object()
    if player == False:
        return redirect(url_for('login'))
    import board
    if player.place == 3:
        if request.method == 'POST':
            req_method = request.form
            if 'type_game' in req_method:
                check = str(req_method.getlist('type_game')[0])
                if check == "1":
                    if logged_player_as_object().current_board == None:
                        earth = generate_world()    
                        board = board.BoardWalk(earth,[])
                        board.join(logged_player_as_object())
                        list_boards.append(board)
                        return redirect(url_for('game_screen',id_board = board.id))
                if check == "2":
                    if logged_player_as_object().current_board == None:
                        earth = generate_world()    
                        board = board.BoardWalk(earth,[],mode = "coop")
                        board.join(logged_player_as_object())
                        list_boards.append(board)
                        return redirect(url_for('game_screen',id_board = board.id))
        return render_template('game.html')
    else:
        view = dump_player_to_JSON()
        return render_template('no_game.html',view = view, because=player.place)

@app.route('/game/silence.html', methods=['GET', 'POST'])
def silence():
    player = logged_player_as_object()
    id_board = player.current_board
    board = board_as_object(id_board)
    if logged_player_as_object()==False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        req_method = request.form
        if 'del_item' in req_method:
            item = str(req_method.getlist('del_item')[0])
            player.remove_from_bag(item)
        if 'use_item' in req_method:
            if board!=False:
                use_item = str(req_method.getlist('use_item')[0])
                print("using item --------"+str(use_item))
                board.player_using_item(use_item)
        if 'drop_dice' in req_method:
            if board!=False:
                drop_dice = str(req_method.getlist('drop_dice')[0])
                print("drop_dice --------"+str(drop_dice))
                if drop_dice == "1":
                    board.drop_dice(from_player=True)
    return render_template('empty.html')
    

@app.route('/game/<id_board>', methods=['GET', 'POST'])
def game_screen(id_board):
    player = logged_player_as_object()
    board = board_as_object(id_board)
    if logged_player_as_object()==False:
        return redirect(url_for('login'))
    if not id_board:
        id_board = ""
    if board!=False:
        if request.method == 'POST':
            req_method = request.form
            print str(req_method)
            if 'move' in req_method:
                id_move = str(req_method.getlist('move')[0])
                action = str(req_method.getlist('action')[0])
                time_move = time.time()
                logged_player_as_object().card_move = [int(id_move),time_move,action]
                print "in post "+str(logged_player_as_object().card_move)
                return render_template('game.html',tv_screen=("one",board_by_id(id_board),id_board))
            if 'join' in req_method:
                check = str(req_method.getlist('join')[0])
                if check == "1":
                    print "this is logged_player_as_object "+str(logged_player_as_object())
                    board_as_object(id_board).join(logged_player_as_object())
                    return redirect(url_for('game_screen',id_board = board_as_object(id_board).id))
            if 'escape' in req_method:
                check = str(req_method.getlist('escape')[0])
                if check == "1":
                    print "escape "+str(logged_player_as_object())
                    board_as_object(id_board).escape(logged_player_as_object())
                    return redirect(url_for('game_main'))
        return render_template('game.html',id_board = board_as_object(id_board).id)
    else:
        return redirect(url_for('p404'))

@app.route('/game/<id_board>/screen.html', methods=['GET', 'POST'])
def screen_window(id_board):
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    board = board_as_object(id_board)
    if board!=False:
        if request.method == 'POST':
            view = board_as_object(id_board).show_tv(player.x,player.y)
            check = time.time()
            animate = board.animate
            #print("ANIMATE = "+str(animate))
            return render_template('game_screen.html',view=view,check=check,animate=animate)
    else:
        return render_template('notv.html')
        
@app.route('/streets.html', methods=['GET', 'POST'])
def streets():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    if player.current_board != None:
        return render_template('game.html',id_board = player.current_board)
    print("player place ="+str(player.place))
    if player.place == 1:
        player.place = 3
    return render_template('streets.html',look="1")
    
@app.route('/streets_content.html', methods=['GET','POST'])
def streets_content():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        req_method = request.form
        if 'show' in req_method:
            check = str(req_method.getlist('show')[0])
            if check == "1":
                if player.place == 3:
                    try_join = "fail"                   
                    view_boards = []
                    view = dump_player_to_JSON()
                    if player.current_board == None:
                        try_join = "ok"
                    for board in list_boards:
                        if board.locked == True:
                            locked = "1"
                        else:
                            locked = "0"
                        view_boards.append([board.id,board.players,board.mode,locked])
                    return render_template('streets_content.html',view=view,view_boards=view_boards,try_join=try_join,looking = player.name)
                else:
                    view = dump_player_to_JSON()
                    return render_template('no_streets.html',view=view,because=player.place)
        
@app.route('/game/<id_board>/control.html', methods=['GET', 'POST'])
def screen_control(id_board):
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        board = board_as_object(id_board)
        if board!=False: 
            view = ""
            show_control = "0"
            if board.now_walk == player.name:
                view = board_as_object(id_board).around(player,mode = 2)
                show_control = "1"
            return render_template('game_control.html',view=view,show_control=show_control)
        else:
            return render_template('empty.html')
    
@app.route('/game/<id_board>/info.html', methods=['GET', 'POST'])
def board_info(id_board):
    if logged_player_as_object()==False:
        return redirect(url_for('login'))
    if request.method == 'POST':      
        board = board_as_object(id_board)
        if board!=False:
            if board.mode == 2:
                view = []
                view.append(board.players)
                view.append(board.winners)
                view.append(board.losers)
                view.append(board.now_walk)
                view.append(board.dice)
                player = logged_player_as_object()
                show_minimap = board.minimap(player.name,player.x,player.y)
                view.append(show_minimap)                
                if player not in board.players and board.locked == False and player.health > 0:
                    welcome = [True,id_board]
                else:
                    welcome = [False,id_board]
                return render_template('info.html',view=view,id_board=id_board, mode="2", welcome=welcome)
            elif board.mode == 1:
                info_board = []
                info_board.append(board.id)
                info_board.append(board.now_walk)
                info_board.append(board.dice)
                info_board.append(int(board.auto_drop))
                player = logged_player_as_object()
                show_minimap = board.minimap(player.name,player.x,player.y)
                view = dump_player_to_JSON()
                waiting_drop = "2"
                if board.now_walk == player.name and board.dice_dropped == False:
                    waiting_drop = "1"
                if board.now_walk == player.name and board.dice_dropped == True:
                    waiting_drop = "0"
                return render_template('info.html',info_board=info_board,show_minimap=show_minimap,view=view,mode="1",waiting_drop=waiting_drop)
        else:
            return render_template('empty.html')

@app.route('/hideout.html', methods=['GET', 'POST'])
def hideout():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    if player.current_board == None and player.place == 3:
        player.place = 1
    return render_template('hideout.html',look="2")
        
@app.route('/hideout_content.html', methods=['GET', 'POST'])
def hideout_content():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        req_method = request.form
        if 'show' in req_method:
            check = str(req_method.getlist('show')[0])
            if check == "1":
                print("player place ="+str(player.place))
                if player.place == 1:
                    view = dump_player_to_JSON(values="hideout")
                    return render_template('hideout_content.html',view=view,here="1")
                else:
                    view = dump_player_to_JSON()
                    return render_template('no_hideout.html',view=view,because=player.place)
        if 'unload_bag_to_chest' in req_method:
            print('unload_bag_to_chest')
            check = str(req_method.getlist('unload_bag_to_chest')[0])
            if check == "1":
                if player.place == 1:
                    player.unload_bag_to_chest()
                    view = dump_player_to_JSON(values="hideout")
                    return render_template('hideout_content.html',view=view,here="1")
        if 'to_chest' in req_method:
            print('to_chest')
            item = str(req_method.getlist('to_chest')[0])
            player.item_to_chest(item)
            if player.place == 1:
                view = dump_player_to_JSON(values="hideout")
                return render_template('hideout_content.html',view=view,here="1")
        if 'to_bag' in req_method:
            item = str(req_method.getlist('to_bag')[0])
            player.item_to_bag(item)
            if player.place == 1:
                view = dump_player_to_JSON(values="hideout")
                return render_template('hideout_content.html',view=view,here="1")
            
            

@app.route('/hospital.html', methods=['GET', 'POST'])
def hospital():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    return render_template('hospital.html',look="3")
    
@app.route('/hospital_content.html', methods=['GET', 'POST'])
def hospital_content():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        req_method = request.form
        if 'show' in req_method:
            check = str(req_method.getlist('show')[0])
            if check == "1":
                print("player place ="+str(player.place))
                if player.place == 2:
                    view = dump_player_to_JSON()
                    return render_template('hospital_content.html',view=view,here="1")
                else:
                    view = dump_player_to_JSON()
                    return render_template('no_hospital.html',view=view,because=player.place)

@app.route('/prison.html', methods=['GET', 'POST'])
def prison():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    return render_template('prison.html',look="4")
    
@app.route('/prison_content.html', methods=['GET', 'POST'])
def prison_content():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        req_method = request.form
        if 'show' in req_method:
            check = str(req_method.getlist('show')[0])
            if check == "1":
                if player.place == 4:
                    view = dump_player_to_JSON()
                    return render_template('prison_content.html',view=view,here="1")
                else:
                    view = dump_player_to_JSON()
                    return render_template('no_prison.html',view=view,because=player.place)

@app.route('/user_info.html', methods=['GET', 'POST'])
def user_info():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    view = dump_player_to_JSON(values="user_info")
    return render_template('user_info.html',view=view)

@app.route('/user_info_hideout.html', methods=['GET', 'POST'])
def user_info_hideout():
    player = logged_player_as_object()
    if player==False:
        return redirect(url_for('login'))
    view = dump_player_to_JSON(values="user_info")
    return render_template('user_info_hideout.html',view=view)
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
