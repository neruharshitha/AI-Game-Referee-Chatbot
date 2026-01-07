# AI-Game-Referee-Chatbot
##  State Model

The game state is stored using a **Pydantic `GameState` model**, which lives fully in memory (no database).  
It tracks:

- Round number (max 3)
- Scores for user and bot
- Bomb usage per player (only once allowed)

This ensures persistent state across rounds while satisfying the constraint of **no external storage**.

##  Agent & Tool Design

The project follows the **Google ADK architecture mindset**:

- The **Agent brain** manages the game loop, understands input, and formats responses.
- **Tools are user-defined Python functions** (`validate_move`, `resolve_round`, `update_game_state`) that handle game logic and return structured **JSON/dict outputs**.
- The bot’s move decision is generated using **Gemini (`gemini-2.5-flash`)**, acting as the intelligent decision engine while respecting bomb-once rule.

Workflow:
User input → Agent brain → Tool validation → Gemini decides bot move → Tool resolves winner → Tool updates state → Agent prints response

##  Tradeoffs

- The real `google_adk` SDK is not publicly available via pip or student-accessible GitHub.
- The closest allowed Google AI SDK (**`google-generativeai`**) was used for model integration.
- No external APIs, databases, UI frameworks, or servers are used.

##  What I’d improve with more time

- Add detailed **reasoning explanations per round**.
- Improve **intent parsing** and typo tolerance.
- Simulate **tool call logs** for better evaluation clarity.
- Enhance UX messages (CLI-only, still minimal).


###  Summary

- Game logic is unchanged
- Tools are Python user-defined logic
- State is in-memory
- Bot decisions use Gemini
- Architecture reflects ADK separation
- No DB, UI, or servers

