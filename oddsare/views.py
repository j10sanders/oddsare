from flask import Flask, flash, render_template, request, redirect, url_for, abort
from oddsare import app, oddsare
from .database import Game, session, User
import os
from flask.ext.login import login_user , logout_user , current_user , login_required
from werkzeug.security import check_password_hash

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("player1_dare_get"))
    
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
    if current_user.is_authenticated:
        new_game = Game(dare=request.form["dare"], player1=current_user.id)
    else:
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
    # check if odds is defined.
    # if it has been played, display the result
    #else:
    return render_template("player2setrange.html", game=game)

@app.route("/game/<id>", methods=["POST"])
def player2_odds(id):
    game = session.query(Game).get(id)
    odds = 0
    try:
        odds = int(request.form["odds"])
    except ValueError:
        flash("That's not an integer.")
    if odds >100 or odds < 2:
        flash("Please choose from a number between 2-100")
        return redirect(url_for("player2_range_get", id=id))
    else:
        game.odds = odds
        session.add(game)
        session.commit()
        return redirect(url_for("player2_choice_get", id=id))
    
    
@app.route("/game/<id>/player2choice", methods=["GET"])
def player2_choice_get(id):
    # loads the game by id
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    else:
        return render_template("player2choice.html", game=game)
        
@app.route("/game/<id>/player2choice", methods=["POST"])
def player2_choice(id):
    game = session.query(Game).get(id)
    #possibilities = [range(0, game.odds)]
    move1 = 0
    try:
        move1 = int(request.form["move1"])
    except ValueError:
        flash("That's not an integer.")
    if move1 > game.odds or move1 < 1:
        flash("Please choose a number between (or equal to): 1 and " + str(game.odds))
        return redirect(url_for("player2_choice_get", id=id))
    else:
        game.move1=move1
        session.add(game)
        session.commit()
        return redirect(url_for("player1_choice_get", id=id))
        
@app.route("/game/<id>/player1choice", methods=["GET"])
def player1_choice_get(id):
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    else:
        return render_template("player1choice.html", game=game)

@app.route("/game/<id>/player1choice", methods=["POST"])
def player1_choice(id):
    game = session.query(Game).get(id)
    #possibilities = [range(0, game.odds)]
    try:
        move2 = int(request.form["move2"])
    except ValueError:
        flash("That's not an integer.")
    if move2 > game.odds or move2 < 1:
        flash("Please choose a number between (or equal to): 1 and " + str(game.odds))
        return redirect(url_for("player1_choice_get", id=id))
    else:
        game.move2=move2
        session.add(game)
        session.commit()
        result = oddsare.compare(game.move1, game.move2)
        return render_template("result.html", game=game, result=result, id=id)
        
        
@app.route("/game/<id>/rebound", methods=["GET"])
def player1_rebound_get(id):
    # loads the game by id
    game = session.query(Game).get(id)
    # check if odds is defined.
    # if it has been played, display the result
    #else:
    return render_template("player1rebound.html", game=game)
    
@app.route("/game/<id>/rebound", methods=["POST"])
def player1_rebound(id):
    game = session.query(Game).get(id)
    # loads the game by id
    rebound = 0 
    try:
        rebound = int(request.form["rebound"])
    except ValueError:
        flash("That's not an integer.")
    if rebound > game.odds or rebound < 2:
        flash("Please choose a number between (or equal to): 1 and " + str(game.odds))
        return redirect(url_for("player1_rebound_get", id=id))
    else:
        game.rebound = rebound
        session.add(game)
        session.commit()
        return redirect(url_for("player1_choice2_get", id=id))
        
@app.route("/game/<id>/player1choice2", methods=["GET"])
def player1_choice2_get(id):
    # loads the game by id
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    else:
        return render_template("player1choice2.html", game=game)
        
@app.route("/game/<id>/player1choice2", methods=["POST"])
def player1_choice2(id):
    game = session.query(Game).get(id)
    #possibilities = [range(0, game.odds)]
    move3 = 0
    try:
        move3 = int(request.form["move3"])
    except ValueError:
        flash("That's not an integer.")
    if move3 > game.rebound or move3 < 1:
        flash("Please choose a number between (or equal to): 1 and " + str(game.rebound))
        return redirect(url_for("player1_choice2_get", id=id))
    else:
        game.move3=move3
        session.add(game)
        session.commit()
        return redirect(url_for("player2_choice2_get", id=id))
        
@app.route("/game/<id>/player2choice2", methods=["GET"])
def player2_choice2_get(id):
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    else:
        return render_template("player2choice2.html", game=game)

@app.route("/game/<id>/player2choice2", methods=["POST"])
def player2_choice2(id):
    game = session.query(Game).get(id)
    try:
        move4 = int(request.form["move4"])
    except ValueError:
        flash("That's not an integer.")
    if move4 > game.rebound or move4 < 1:
        flash("Please choose a number between (or equal to): 1 and " + str(game.rebound))
        return redirect(url_for("player2_choice2_get", id=id))
    else:
        game.move4=move4
        session.add(game)
        session.commit()
        result = oddsare.compare(game.move3, game.move4)
        return render_template("reboundresult.html", game=game, result=result, id=id)