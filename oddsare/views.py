from flask import Flask, flash, render_template, request, redirect, url_for, abort
from oddsare import app, oddsare
from .database import Game, session
import os

@app.route("/")
@app.route("/game", methods=["GET"])
@app.route("/new_game", methods=["GET"])
def player1_dare_get():
    return render_template("player1dare.html")

@app.route("/", methods=["POST"])
@app.route("/game", methods=["POST"])
@app.route("/new_game", methods=["POST"])
def player1_dare():
    dare = request.form["dare"]
    new_game = Game(dare=request.form["dare"])
    session.add(new_game)
    session.commit()
    return redirect(url_for("player2_range_get", id=new_game.id))

@app.route("/game/<id>", methods=["GET"])
def player2_range_get(id):
    # loads the game by id
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    '''if game.odds:
        result = oddsare.oddsare([game.dare, game.move1, game.move2])
        return render_template("result.html", game=game, result=result)'''
    # check if odds is defined.
    # if it has been played, display the result
    #else:
    return render_template("player2setrange.html", game=game)

@app.route("/game/<id>", methods=["POST"])
def player2_odds(id):
    game = session.query(Game).get(id)
    odds = int(request.form["odds"])
    if odds >100 or odds < 2:
        flash("That's not a possibility.  Please choose from a number between 2-100")
        return redirect(url_for("player2_odds_get", id=id))
    else:
        game.odds = odds
        session.add(game)
        session.commit()
        return redirect(url_for("player2_choice_get", id=id))
    
    

@app.route("/game/<id>/player2choice", methods=["GET"])
def player2_choice_get(id):
    print(id)
    # loads the game by id
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    else:
        return render_template("player2odds.html", game=game)
        
@app.route("/game/<id>/player2choice", methods=["POST"])
def player2_choice(id):
    game = session.query(Game).get(id)
    possibilities = [range(0, game.odds)]
    move1 = request.form["move1"]
    if odds not in possibilities:
        flash("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])
        new_game = Game(move1=request.form["move1"])
        session.add(new_game)
        session.commit()
        return redirect(url_for("player2_choice_get", id=new_game.id))
    else:
        game.odds=request.form["odds"]
        session.add(game)
        session.commit()
        return render_template("player1odds.html", game=game)