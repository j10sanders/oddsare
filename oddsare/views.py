from flask import Flask, flash, render_template, request, redirect, url_for, abort
from oddsare import app, oddsare
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
    dare = request.form["dare"]
    new_game = Game(dare=request.form["dare"])
    session.add(new_game)
    session.commit()
    return redirect(url_for("player2_choice_get", id=new_game.id))

@app.route("/game/<id>", methods=["GET"])
def player2_choice_get(id):
    # loads the game by id
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    if game.odds:
        result = oddsare.oddsare([game.dare, game.odds])
        return render_template("result.html", game=game, result=result)
    # check if odds is defined.
    # if it has been played, display the result
    else:
        return render_template("player2.html", game=game)

@app.route("/game/<id>", methods=["POST"])
def player2_choice(id):
    game = session.query(Game).get(id)
    possibilities = list(range(1, 101))
    dare = request.form["dare"]
    if dare not in possibilities:
        flash("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])
        new_game = Game(dare=request.form["dare"])
        session.add(new_game)
        session.commit()
        return redirect(url_for("player2_choice_get", id=new_game.id))
    else:
        game.odds=request.form["dare"]
        session.add(game)
        session.commit()
        result = oddsare.compare([game.dare, game.odds])
        return render_template("result.html", game=game, result=result)
    