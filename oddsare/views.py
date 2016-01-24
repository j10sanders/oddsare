from flask import Flask, flash, render_template, request, redirect, url_for, abort
from oddsare import app, oddsare
from oddsare.oddsare import InvalidNumberException
from .database import Game, session, User
import os
from flask.ext.login import login_user , logout_user , current_user , login_required
from werkzeug.security import check_password_hash

@app.route("/register", methods=["GET"])
def register_get():
    return render_template('register.html')

@app.route("/register", methods=["POST"])
def register_post():
    user = User(username=request.form['username'], password=request.form['password'], email=request.form['email'])
    session.add(user)
    session.commit()
    flash('User successfully registered')
    return redirect(url_for('login_get'))
    
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
    if current_user.is_authenticated:
        return render_template("player1dare.html")
    else:
        return render_template("anonplayer1dare.html")

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
    elif game.odds:
        return redirect(url_for("player1_dare_get", id=id))
    return render_template("player2setrange.html", game=game)

@app.route("/game/<id>", methods=["POST"])
def player2_odds(id):
    game = session.query(Game).get(id)
    try:
        odds = oddsare.valid_number(request.form["odds"], 100)
    except InvalidNumberException as e:
        flash(str(e), "danger")
        return redirect(url_for("player2_range_get", id=id))
    if current_user.is_authenticated and game.player1 != current_user.id:
        game.player2 = current_user.id
    else:
        player1 = session.query(User).get(1)
        print(player1.username)
    game.odds = odds
    session.add(game)
    session.commit()
    #print(game.player1(users.id))
    #print(game.player2.name)
    return redirect(url_for("player2_choice_get", id=id))
    
    
@app.route("/game/<id>/player2choice", methods=["GET"])
def player2_choice_get(id):
    # loads the game by id
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    elif game.move1:
        return redirect(url_for("player1_choice_get", id=id))
    else:
        return render_template("player2choice.html", game=game)
        
@app.route("/game/<id>/player2choice", methods=["POST"])
def player2_choice(id):
    game = session.query(Game).get(id)
    try:
        move1 = oddsare.valid_number(request.form["move1"], game.odds)
    except InvalidNumberException as e:
        flash(str(e), "danger")
        return redirect(url_for("player2_choice_get", id=id))
    game.move1=move1
    session.add(game)
    session.commit()
    return redirect(url_for("player1_choice_get", id=id))
        
@app.route("/game/<id>/player1choice", methods=["GET"])
def player1_choice_get(id):
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    elif game.move2:
        return render_template("result.html", game=game, result=result, id=id)
    else:
        return render_template("player1choice.html", game=game)

@app.route("/game/<id>/player1choice", methods=["POST"])
def player1_choice(id):
    game = session.query(Game).get(id)
    try:
        move2 = oddsare.valid_number(request.form["move2"], game.odds)
    except InvalidNumberException as e:
        flash(str(e), "danger")
        return redirect(url_for("player2_choice_get", id=id))
    game.move2=move2
    session.add(game)
    session.commit()
    result = oddsare.compare(game.move1, game.move2)
    return render_template("result.html", game=game, result=result, id=id)
        
@app.route("/game/<id>/rebound", methods=["GET"])
def player1_rebound_get(id):
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    elif game.rebound:
        return redirect(url_for("player1_choice2_get", id=id))
    return render_template("player1rebound.html", game=game)
    
@app.route("/game/<id>/rebound", methods=["POST"])
def player1_rebound(id):
    game = session.query(Game).get(id)
    try:
        rebound = oddsare.valid_number(request.form["rebound"], game.odds)
    except InvalidNumberException as e:
        flash(str(e), "danger")
        return redirect(url_for("player1_rebound_get", id=id))
    game.rebound = rebound
    session.add(game)
    session.commit()
    return redirect(url_for("player1_choice2_get", id=id))
        
@app.route("/game/<id>/player1choice2", methods=["GET"])
def player1_choice2_get(id):
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    elif game.move3:
        return redirect(url_for("player2_choice2_get", id=id))
    else:
        return render_template("player1choice2.html", game=game)
        
@app.route("/game/<id>/player1choice2", methods=["POST"])
def player1_choice2(id):
    game = session.query(Game).get(id)
    try:
        move3 = oddsare.valid_number(request.form["move3"], game.rebound)
    except InvalidNumberException as e:
        flash(str(e), "danger")
        return redirect(url_for("player1_choice2_get", id=id))
    game.move3=move3
    session.add(game)
    session.commit()
    return redirect(url_for("player2_choice2_get", id=id))
        
@app.route("/game/<id>/player2choice2", methods=["GET"])
def player2_choice2_get(id):
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    elif game.move4:
        return render_template("reboundresult.html", game=game, result=result, id=id)    
    else:
        return render_template("player2choice2.html", game = game)
        
@app.route("/game/<id>/player2choice2", methods=["POST"])
def player2_choice2(id):
    game = session.query(Game).get(id)
    try:
        move4 = oddsare.valid_number(request.form["move4"], game.rebound)
    except InvalidNumberException as e:
        flash(str(e), "danger")
        return redirect(url_for("player2_choice2_get", id=id))
    game.move4=move4
    session.add(game)
    session.commit()
    result = oddsare.compare(game.move3, game.move4)
    return render_template("reboundresult.html", game=game, result=result, id=id)