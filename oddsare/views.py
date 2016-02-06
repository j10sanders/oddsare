from flask import Flask, flash, render_template, request, redirect, url_for, abort
from oddsare import app, oddsare, validateuser
from oddsare.oddsare import InvalidNumberException
from oddsare.validateuser import IntegrityError
from .database import Game, session, User
import os
from flask.ext.login import login_user , logout_user , current_user , login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError



@app.route("/register", methods=["GET"])
def register_get():
    return render_template('register.html')

@app.route("/register", methods=["POST"])
def register_post():
    try: 
        user = User(username=request.form["username"], password=generate_password_hash(request.form["password"]), email=request.form["email"])
        session.add(user)
        session.commit()
        flash("User successfully registered")
        login_user(user)
        return redirect(request.args.get('next') or url_for("player1_dare_get"))
    except IntegrityError:
        flash("The username or email was already taken.  This app isn't sophisticated enough to let you reset a password, so just register a new user", "danger")
        return redirect(url_for("register_get"))
    
@app.route("/")
@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]
    user = session.query(User).filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))
    login_user(user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for("player1_dare_get"))
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(request.args.get('next') or url_for("login_get"))
    

@app.route("/game", methods=["GET"])
@app.route("/new_game", methods=["GET"])
@login_required
def player1_dare_get():
    return render_template("player1dare.html")


@app.route("/", methods=["POST"])
@app.route("/game", methods=["POST"])
@app.route("/new_game", methods=["POST"])
def player1_dare():
    if current_user.is_authenticated:
        game = Game(dare=request.form["dare"], player1=current_user.id)
    else:
        game = Game(dare=request.form["dare"])
    session.add(game)
    session.commit()
    logout_user()
    flash(game.user1.username + ", your dare was saved.  Now the other player needs to login.  You can send them this URL, or pass your device to them.")
    return redirect(url_for('login_get') + "?next=" + url_for("player2_range_get", id=game.id))
    #return redirect(url_for("player2_range_get", id=game.id))

@app.route("/game/<id>", methods=["GET"])
@login_required
def player2_range_get(id):
    # loads the game by id
    game = session.query(Game).get(id)
    if game is None:
        abort(404)
    elif game.odds:
        return redirect(url_for("player1_dare_get", id=id))
    game.player2 = current_user.id
    return render_template("player2setrange.html", game=game)

@app.route("/game/<id>", methods=["POST"])
def player2_odds(id):
    game = session.query(Game).get(id)
    try:
        odds = oddsare.valid_number(request.form["odds"], 100)
    except InvalidNumberException as e:
        flash(str(e), "danger")
        return redirect(url_for("player2_range_get", id=id))
    #if current_user.is_authenticated and game.player1 != current_user.id:
        #game.player2 = current_user.id
    print(game.user1.username)
    print(game.user2.username)
    logout_user()
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
    #print(game.player1.username)
    game.move1=move1
    session.add(game)
    session.commit()
    flash(game.user2.username + ", your odds and your choice are saved.  Now " + game.user1.username + " needs to pick a number.  You can send them this URL, or pass your device to them.")
    return redirect(url_for("player1_choice_get", id=id))
        
@app.route("/game/<id>/player1choice", methods=["GET"])
def player1_choice_get(id):
    game = session.query(Game).get(id)
    player1 = session.query(User).get(game.player1)
    if game is None:
        abort(404)
    elif game.move2:
        return render_template("result.html", game=game, result=result, id=id)
    else:
        return render_template("player1choice.html", game=game, player1=player1)

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
        return render_template("player2choice2.html", game=game)
        
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
    
@app.route("/stats", methods=["GET"])
def stats_get():
    username = session.query(User.username).order_by(User.username).all()
    print(username)
    dare = session.query(Game.dare).order_by(Game.dare).all()
    print(dare)
    #ref = db.session.query(reference).filter(reference.parent == 1).all())
    #game = session.query(Game.dare).order_by(Game.dare).all()
    return render_template("stats.html",  username=username, dare=dare)
