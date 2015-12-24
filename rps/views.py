from flask import Flask, flash, render_template, request, redirect, url_for
from rps import app

from .database import Player, Game, session
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
@app.route("/player1", methods=["GET"])
def player1_choice_get():
    return render_template("player1.html")

@app.route("/player1", methods=["POST"])
def player1_choice():
    possibilities = ["rock","paper","scissors"]
    move = request.form["move"]
    if move not in possibilities:
        flash("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])
        return redirect(url_for("player1_choice_get"))
    else: 
        player_move = Game(
            player="Player1",
            move=request.form["move"]
            )
        session.add(player_move)
        session.commit()
        return redirect(url_for("player2_choice_get"))

@app.route("/player2", methods=["GET"])
def player2_choice_get():
    return render_template("player2.html")

@app.route("/player2", methods=["POST"])
def player2_choice():
    possibilities = ["rock","paper","scissors"]
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
 



    
