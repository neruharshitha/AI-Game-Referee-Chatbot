from pydantic import BaseModel

class GameState(BaseModel):
    user_score: int = 0
    bot_score: int = 0
    round: int = 1
    user_bomb_used: bool = False
    bot_bomb_used: bool = False

    def to_dict(self):
        return self.model_dump()
