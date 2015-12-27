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
            
        