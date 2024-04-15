from typing import List, Dict


class WorkspaceQuizGroup:
    def __init__(self, item: dict) -> None:
        self._id: str
        self.className: str
        self.quizList: List[Dict]
        self.totalScore: float
        self.name: str
        self.owner: Dict
        self.parent: Dict

        for k, v in item.items():
            if k in ["quizList"]:
                setattr(self, k, [{"collection": q.collection, "_id": q.id} for q in v])
            if k in ["owner", "parent"]:
                setattr(self, k, {"collection": v.collection, "_id": v.id})
            if k in ["_id", "className", "totalScore", "name"]:
                setattr(self, k, v)

    def dict(self) -> Dict:
        return vars(self)
