from flask import Flask, flash, render_template, request, redirect, url_for
from rps import app

from .database import Player1, Player2, session
import os


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
    

#@app.route("/")
@app.route("/player1", methods=["GET"])
def player1_choice_get():
    return render_template("player1.html")

@app.route("/player1", methods=["POST"])
def player1_choice():
      
    #print("Let's play a game of Rock, Paper, Scissors!")
    #player1 = input("What is player 1's move? ")
    possibilities = ["rock","paper","scissors"]
    move = Player1(
        title=request.form["title"]
    )
    if move not in possibilities:
        flash("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])
        return redirect(url_for("player1_choice_get"))
    session.add(move)
    session.commit()
    return redirect(url_for("player2_choice_get"))

@app.route("/player2", methods=["GET"])
def player2_choice_get():
    return render_template("player2.html")

@app.route("/player2/choice", methods=["POST"])
def player2_choice():
    possibilities = ["rock","paper","scissors"]  
    player2 = input("What is player 2's move? ")
    while player2 not in possibilities:
        flash("That's not a possibility.  Please choose from " + str(possibilities)[1:-1])
    move = Player2(
        title=request.form["title"]
    )
    session.add(move)
    session.commit()
    return redirect(url_for("player2"))
 
    '''compare.moves = [player1, player2]
    if compare.moves == 0:
        print("Player 1 wins!")
    elif compare.moves == 1:
        print("Player 2 wins!")
    else:
        print("You tied!")'''


    
