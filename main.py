import random
from dotenv import load_dotenv
import os
from state import GameState
from tools import TOOL_FUNCTIONS

import google.generativeai as genai

# Load API key from your file
load_dotenv("apikey.env")
api_key = os.getenv("GOOGLE_ADK_API_KEY")
print("API Key Loaded ✔\n")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize game state in memory
state = GameState()

# Print rules (5 lines max)
print("Rules: Best of 3 rounds.")
print("Moves: rock, paper, scissors, bomb (once).")
print("Bomb beats all. Bomb vs Bomb = draw.")
print("Invalid input wastes round.")
print("Game auto ends after 3 rounds.\n")

# Game loop (max 3 rounds)
while state.round <= 3:
    user_move = input(f"Round {state.round} — Your move: ").strip().lower()

    # Validate move using your tool logic
    validation = TOOL_FUNCTIONS["validate_move"]({"move": user_move}, state)
    if not validation["valid"]:
        print(f"You: {user_move} | Bot: wasted")
        print("Result: Bot wins this round (invalid input wasted)\n")
        state.bot_score += 1
        state.round += 1
        continue

    # Bot move decision using Gemini model (bomb only once)
    bot_prompt = f"Round {state.round}. Choose one move from: rock, paper, scissors, bomb. Bomb only once. You already used bomb: {state.bot_bomb_used}. Respond in 1 word."
    response = model.generate_content(bot_prompt)
    bot_move = response.text.strip().lower()

    # Resolve winner using your tool logic
    result = TOOL_FUNCTIONS["resolve_round"]({"user_move": user_move, "bot_move": bot_move}, state)
    winner = result["winner"]

    # Update state using your tool logic
    state = TOOL_FUNCTIONS["update_game_state"]({"user_move": user_move, "bot_move": bot_move, "winner": winner}, state)["state"]

    # Print round feedback
    print(f"You: {user_move} | Bot: {bot_move}")
    if winner == "draw":
        print("Result: Draw!\n")
    elif winner == "user":
        print("Result: You win this round!\n")
    else:
        print("Result: Bot wins this round!\n")

    print(f"Score → You:{state.user_score} Bot:{state.bot_score}\n")

# End game automatically
print("Game Over!\n")
if state.user_score > state.bot_score:
    print("Final Result: You win the game!")
elif state.bot_score > state.user_score:
    print("Final Result: Bot wins the game!")
else:
    print("Final Result: The game is a Draw!")
