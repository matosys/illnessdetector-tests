from dataclasses import dataclass

from balderhub.data.lib.utils import SingleDataItem


@dataclass
class QuestionResultDataItem(SingleDataItem):
    session: str
    questions_and_answers: list[tuple[str, str]]
    illness_result: str
    score: float

    def get_unique_identification(self):
        return self.session
