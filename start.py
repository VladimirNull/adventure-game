import earth,hero,os,board
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template,flash
from contextlib import closing
import time


DATABASE = "heroes.dat"
SECRET_KEY = 'rtjeortuertjeqrotDFGjhqeortpeqrtvADFGjh934utv34t0-eqrtujSJRT0-eqrjtoqerjtojgSRTJqj0WI3R=284250=4=0T0E'
list_boards = []
list_players = []

app = Flask(__name__)
app.config.from_object(__name__)

    

@app.route('/')
def index():
    login = "guest"
    if session['logged']:
        login = session['logged']
    return render_template('index.html',login=login,o=o)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        tmp_player = str(request.form['username'])
        player = hero.Hero(tmp_player)
        if player.load():
            session['logged'] = player.name
            list_players.append(player)
            return render_template('hideout.html', player=player,welcome="welcome back")
        else:
            session['logged'] = player.name
            list_players.append(player)
            player.save()
            return render_template('hideout.html', player=player,welcome="hello, new thief!!")
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	session['logged'] = "guest"
	return redirect(url_for('index'))
   
def generate_world():
    import earth
    earth = earth.Earth(18,10)
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
    answ = False
    for player in list_players:
        if session['logged'] == player.name:
            answ = player
    return answ

@app.route('/game_show/list_boards')  
def show_list_boards():
    out = []
    for board in list_boards:
        out.append(board.id)
    return render_template('game.html',tv_screen=("list",out))    
    
@app.route('/game_show/<id_board>', methods=['GET', 'POST'])
def show_boards(id_board):
    if request.method == 'POST':
        if request.form['join'] == "1":
            board_as_object(id_board).join(logged_player_as_object())
    return render_template('game.html',tv_screen=("one",board_by_id(id_board),id_board))
    
@app.route('/game', methods=['GET', 'POST'])  
def game():
    import board
    if request.method == 'POST':
        if request.form['start'] == "1":
            earth = generate_world()    
            board = board.BoardWalk(earth,[logged_player_as_object()])
            board.drop_off_orcs()
            list_boards.append(board)
            return render_template('game.html',tv_screen=("one",str(board),board.id))
    return render_template('game.html',tv_screen="BLYA")
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')