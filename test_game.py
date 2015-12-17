from game import compare

def test_compare():
    assert compare(["rock", "paper"]) == 1
    assert compare(["paper", "paper"]) is None
    assert compare(["rock", "scissors"]) == 0
    