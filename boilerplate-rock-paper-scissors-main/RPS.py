# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

#def player(prev_play, opponent_history=[]):
#    opponent_history.append(prev_play)
#
#    guess = "R"
#    if len(opponent_history) > 2:
#        guess = opponent_history[-2]
#
#    return guess
import random

def player(prev_play, opponent_history=[]):
    if prev_play:
        opponent_history.append(prev_play)

    if not hasattr(player, "history"):
        player.history = []
        player.table_2 = {}

    history = player.history
    if prev_play:
        history.append(prev_play)

    if len(history) < 3:
        return random.choice(["R", "P", "S"])

    # Update 2-step transition table based on last seen pair -> latest play
    key2 = "".join(history[-3:-1])
    if key2 not in player.table_2:
        player.table_2[key2] = {"R": 0, "P": 0, "S": 0}
    player.table_2[key2][history[-1]] += 1

    # Predict opponent's next move using last two plays
    last2 = "".join(history[-2:])
    if last2 in player.table_2 and sum(player.table_2[last2].values()) > 0:
        counts = player.table_2[last2]
        prediction = max(counts, key=counts.get)
    else:
        prediction = random.choice(["R", "P", "S"])

    counter = {"R": "P", "P": "S", "S": "R"}
    return counter[prediction]


def eeplayer(prev_play):

    if not hasattr(player, "opp_history"):
        player.opp_history = []
        player.my_history = []
        player.table_2 = {}

    if prev_play:
        player.opp_history.append(prev_play)

    # First few moves
    if len(player.my_history) < 3:
        move = random.choice(["R", "P", "S"])
        player.my_history.append(move)
        return move

    # -----------------------------
    # Learn OUR move patterns
    # Abbey uses our last 2 moves
    # -----------------------------
    key = "".join(player.my_history[-3:-1])

    if key not in player.table_2:
        player.table_2[key] = {"R": 0, "P": 0, "S": 0}

    player.table_2[key][player.my_history[-1]] += 1

    # -----------------------------
    # Simulate Abbey
    # -----------------------------
    last_two = "".join(player.my_history[-2:])

    predicted_us = None

    if last_two in player.table_2:
        counts = player.table_2[last_two]

        if sum(counts.values()) > 0:
            predicted_us = max(counts, key=counts.get)

    # Abbey's counter
    abbey_counter = {
        "R": "P",
        "P": "S",
        "S": "R"
    }

    # Move that beats Abbey's move
    beat = {
        "R": "P",
        "P": "S",
        "S": "R"
    }

    if predicted_us:
        abbey_move = abbey_counter[predicted_us]
        move = beat[abbey_move]
    else:
        move = random.choice(["R", "P", "S"])

    player.my_history.append(move)
    return move


