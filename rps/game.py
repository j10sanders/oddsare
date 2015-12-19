from flask import Flask, flash, render_template
from os import environ
from .database import Player1, Player2
import os

app = Flask(__name__)

@app.route("/compare")
def compare(moves):
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
    

@app.route("/player1/choice", methods=["GET"])
def player1_choice_get():
    return render_template("player1.html")

@app.route("/player1/choice", methods=["POST"])
def player1_choice():
    possibilities = ["rock","paper","scissors"]  
    #print("Let's play a game of Rock, Paper, Scissors!")
    player1 = input("What is player 1's move? ")
    while player1 not in possibilities:
        flash("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])
        

'''@app.route("/entry/add", methods=["GET"])
@login_required
def add_entry_get():
    return render_template("add_entry.html")

@app.route("/entry/add", methods=["POST"])
@login_required
def add_entry_post():
    entry = Entry(
        title=request.form["title"],
        content=request.form["content"],
        author=current_user
    )
    session.add(entry)
    session.commit()
    return redirect(url_for("entries"))
    '''

@app.route("/player2/choice")
def player2_choice():
    possibilities = ["rock","paper","scissors"]  
    player2 = input("What is player 2's move? ")
    while player2 not in possibilities:
        player2 = input("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])  
 
 
    compare.moves = [player1, player2]
    if compare.moves == 0:
        print("Player 1 wins!")
    elif compare.moves == 1:
        print("Player 2 wins!")
    else:
        print("You tied!")

def run():
    port = int(os.environ.get('PORT', 8080))
    print("https://jps-python-jonsanders-1.c9.io/")
    app.run(host='0.0.0.0', port=port)
    
