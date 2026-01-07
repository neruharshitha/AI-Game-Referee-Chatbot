from state import GameState

def validate_move(args, state: GameState):
    move = args.get("move", "")
    if move not in ["rock", "paper", "scissors", "bomb"]:
        return {"valid": False, "reason": "Invalid move! Round wasted."}
    if move == "bomb" and state.user_bomb_used:
        return {"valid": False, "reason": "Bomb already used! Round wasted."}
    return {"valid": True, "reason": "Move accepted"}

def resolve_round(args, state: GameState):
    user_move = args.get("user_move")
    bot_move = args.get("bot_move")

    if user_move == "bomb" and bot_move == "bomb":
        return {"winner": "draw"}
    if user_move == "bomb":
        return {"winner": "user"}
    if bot_move == "bomb":
        return {"winner": "bot"}
    if user_move == bot_move:
        return {"winner": "draw"}

    if (user_move == "rock" and bot_move == "scissors") or \
       (user_move == "paper" and bot_move == "rock") or \
       (user_move == "scissors" and bot_move == "paper"):
        return {"winner": "user"}
    return {"winner": "bot"}

def update_game_state(args, state: GameState):
    user_move = args.get("user_move")
    bot_move = args.get("bot_move")
    winner = args.get("winner")

    if user_move == "bomb":
        state.user_bomb_used = True
    if bot_move == "bomb":
        state.bot_bomb_used = True

    if winner == "user":
        state.user_score += 1
    elif winner == "bot":
        state.bot_score += 1

    state.round += 1
    return {"state": state}

TOOL_FUNCTIONS = {
    "validate_move": validate_move,
    "resolve_round": resolve_round,
    "update_game_state": update_game_state
}
