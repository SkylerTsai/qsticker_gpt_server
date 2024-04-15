from enum import Enum
from typing import List, Dict, Set, Optional


class Difficulty(Enum):
    UN_LABEL = "unlabel"
    VERY_EASY = "very easy"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    VERY_HARD = "very hard"


class Quiz:
    def __init__(self, item: dict) -> None:
        self._id: str
        self.difficulty: Difficulty
        self.score: int
        self.multipleSelect: Optional[bool] = False
        self.answerSet: Set[str]
        self.enableSolution: Optional[bool] = False
        self.solution: Optional[str] = ""
        self.isBlankFill: Optional[bool] = False
        self.clickAreas: List[ClickArea]

        for k, v in item.items():
            if k in ["clickAreas"]:
                setattr(self, k, [ClickArea(ca) for ca in v])
            if k in [
                "_id",
                "difficulty",
                "score",
                "multipleSelect",
                "answerSet",
                "enableSolution",
                "solution",
                "isBlankFill",
            ]:
                setattr(self, k, v)

    def dict(self) -> dict:
        ret = {}
        for k, v in vars(self).items():
            if k == "clickAreas":
                ret[k] = [ca.dict() for ca in v]
            else:
                ret[k] = v
        return ret


class ClickArea:
    def __init__(self, item: dict) -> None:
        self.label: str
        self.content: Dict[str:Dict]

        for k, v in item.items():
            if k == "label":
                setattr(self, k, v)
            if k == "content":
                temp = {}
                temp["imageField"] = {
                    "enabled": v["imageField"]["enabled"],
                    "url": v["imageField"]["url"],
                }
                temp["textField"] = {
                    "enabled": v["textField"]["enabled"],
                    "text": v["textField"]["text"],
                }
                setattr(self, k, temp)

    def dict(self) -> dict:
        return vars(self)

    def get_image(self) -> str:
        if not self.content["imageField"]["enabled"]:
            return None
        return self.content["imageField"]["url"]

    def get_text(self) -> str:
        if not self.content["textField"]["enabled"]:
            return None
        return self.content["textField"]["text"]
