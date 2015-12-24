from flask import Flask, flash, render_template, request, redirect, url_for
from rps import app

from .database import Game, session
import os


'''@app.route("/compare", methods="GET")
def compare(moves):
    moves = session.query(Entry)
    entries = session.query(Entry)
        entries = entries.order_by(Entry.datetime.desc())
    if moves[0] == moves[1]:
        return None
    elif moves == ["rock", "paper"]:
        return 1
    elif moves == ["rock", "scissors"]:
        return 0
    elif moves == ["scissors", "rock"]:
        return 1
    elif moves == ["scissors", "paper"]:
        return 0
    elif moves == ["paper", "scissors"]:
        return 1
    elif moves == ["paper", "rock"]:
        return 0
            compare.moves = [player1, player2]
    if compare.moves == 0:
        print("Player 1 wins!")
    elif compare.moves == 1:
        print("Player 2 wins!")
    else:
        print("You tied!")'''


#@app.route("/")
@app.route("/new_game", methods=["GET"])
def player1_choice_get():
    return render_template("player1.html")

@app.route("/new_game", methods=["POST"])
def player1_choice():
    possibilities = ["rock", "paper", "scissors"]
    move = request.form["move"]
    if move not in possibilities:
        flash("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])
        return redirect(url_for("player1_choice_get"))
    else:
        new_game = Game(move1=request.form["move"])
        session.add(new_game)
        session.commit()
        return redirect(url_for("player2_choice_get", id=new_game.id))

@app.route("/game/<id>", methods=["GET"])
def player2_choice_get(id):
    # loads the game by id
    game = Game.query.get(id)
    # check if move2 is defined.
    # if it has been played, display the result
    return render_template("player2.html", game=game)

@app.route("/game/<id>", methods=["POST"])
def player2_choice():
    possibilities = ["rock", "paper", "scissors"]
    move = request.form["move"]
    if move not in possibilities:
        flash("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])
        return redirect(url_for("player2_choice_get"))
    else:
        player_move = Player(
            name="Player2",
            move=request.form["move"]
            )
        session.add(player_move)
        session.commit()
        return redirect(url_for("compare"))