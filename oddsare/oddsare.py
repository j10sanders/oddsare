class InvalidNumberException(Exception):
    pass

def compare(moveA, moveB):
    """ 
    1 = player 1 wins (player 2 has to do dare)
    0 = nobody wins.
    """
    if moveA == moveB:
        return 1
    else:
        return 0
            
def valid_number(number, higher_bound):
    try:
        number = int(number)
    except ValueError:
        raise InvalidNumberException("That's not an integer...")
        
    valid_range = range(1, higher_bound + 1)
    if number not in valid_range:
        raise InvalidNumberException("Please choose from a number between 1 - {}".format(higher_bound))
    else:
        return number