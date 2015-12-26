from flask import Flask, flash, render_template, request, redirect, url_for, abort
from rps import app, rps

from .database import Game, session
import os


@app.route("/")
@app.route("/game", methods=["GET"])
@app.route("/new_game", methods=["GET"])
def player1_choice_get():
    return render_template("player1.html")

@app.route("/", methods=["POST"])
@app.route("/game", methods=["POST"])
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
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    if game.move2:
        result = rps.compare([game.move1, game.move2])
        return render_template("result.html", game=game, result=result)
    # check if move2 is defined.
    # if it has been played, display the result
    else:
        return render_template("player2.html", game=game)

@app.route("/game/<id>", methods=["POST"])
def player2_choice(id):
    game = session.query(Game).get(id)
    possibilities = ["rock", "paper", "scissors"]
    move = request.form["move"]
    if move not in possibilities:
        flash("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])
        new_game = Game(move1=request.form["move"])
        session.add(new_game)
        session.commit()
        return redirect(url_for("player2_choice_get", id=new_game.id))
    else:
        game.move2=request.form["move"]
        session.add(game)
        session.commit()
        result = rps.compare([game.move1, game.move2])
        return render_template("result.html", game=game, result=result)
        
    