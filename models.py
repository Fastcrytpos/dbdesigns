from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=True)
    moves = db.relationship('Move', backref='player')
    games_as_player1 = db.relationship('Game', foreign_keys='Game.player1_id', backref='player1')
    games_as_player2 = db.relationship('Game', foreign_keys='Game.player2_id', backref='player2')

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    moves = db.relationship('Move', backref='game')

# class Boardstate(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     bstate = db.Column(db.String, nullable=False)
#     boardstates = db.relationship('Boardstate', backref='moves')


class Move(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    startpos = db.Column(db.String(2), nullable=False)
    endpos = db.Column(db.String(2), nullable=False)
    bstate = db.Column(db.String, nullable=False)


   

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()


        player1 = Player(name="Player 1", email="player1@example.com", password="password1")
        player2 = Player(name="Player 2", email="player2@example.com", password="password2")
        db.session.add(player1)
        db.session.add(player2)
        db.session.commit()

      
        game1 = Game(player1_id=player1.id, player2_id=player2.id)
        db.session.add(game1)
        db.session.commit()

      
        board_state = [
            [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
            ['c', ' ', 'c', ' ', 'c', ' ', 'c', ' '],
            [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' '],
            [' ', 'p', ' ', 'p', ' ', 'p', ' ', 'p'],
            ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' ']
        ]
        board_state2 = [
            [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
            ['c', ' ', 'c', ' ', 'c', ' ', 'c', ' '],
            [' ', 'c', ' ', 'c', ' ', ' ', ' ', 'c'],
            [' ', ' ', ' ', ' ', ' ', ' ', 'c', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', 'p'],
            ['p', ' ', 'p', ' ', 'p', ' ', ' ', ' '],
            [' ', 'p', ' ', 'p', ' ', 'p', ' ', 'p'],
            ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' ']
        ]
        bstate_json = json.dumps(board_state)
        bstate_json2= json.dumps(board_state2)
        # boardstate1 = Boardstate(bstate=bstate_json)
        # db.session.add(boardstate1)
        # db.session.commit()

        
        move1 = Move(game_id=game1.id, player_id=player1.id, startpos='A3', endpos='B4',bstate=bstate_json)
        move2 = Move(game_id=game1.id, player_id=player2.id, startpos='C5', endpos='D6',bstate=bstate_json2)
        db.session.add(move1)
        db.session.add(move2)
        db.session.commit()

     
        print(f'Player 1: {player1}')
        print(f'Player 2: {player2}')
        print(f'Game 1: {game1}')
        # print(f'Boardstate 1: {boardstate1.bstate}')
        print(f'Move 1: {move1}')
        print(f'Move 2: {move2}')
