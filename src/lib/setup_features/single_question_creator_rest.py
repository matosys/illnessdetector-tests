from typing import List, Dict, Any

import balder
import requests

import balderhub.data
from balderhub.data.lib.utils import ResponseMessageList

from balderhub.crud.lib.setup_features import SingleDataCreatorFeature
from balderhub.crud.lib.utils.item_mapping import FillItemmappingCallback

from lib.utils import QuestionResultDataItem


class RestSession:
    url = 'http://webserver:5000'

    def __init__(self):
        self._last_response = requests.get(self.url + '/api/start').json()

    @property
    def current_question(self):
        return self._last_response.get('question')

    @property
    def current_options(self):
        return self._last_response.get('options')

    @property
    def result(self):
        return self._last_response.get('result')

    def answer_question_with(self, answer: str):
        selection_idx = self.current_options.index(answer)

        self._last_response = requests.get(self.url + '/api/answer', params={
            'session_id': self._last_response['session_id'],
            'choice': selection_idx
        }).json()


class ProvideAnswersCallback(FillItemmappingCallback):

    def execute(self, feature: balder.Feature, field: str, element_object: RestSession, data_to_fill) -> Any:
        val = data_to_fill.get_field_value(field)

        for cur_expected_question, my_answer in val:
            assert element_object.current_question == cur_expected_question
            element_object.answer_question_with(my_answer)
        return val


@balderhub.data.register_for_data_item(QuestionResultDataItem)
class SingleQuestionCreatorOverRest(SingleDataCreatorFeature):
    url = 'http://localhost:5000'
    current_container = None

    def load(self):
        self.current_container = None

    def get_non_fillable_fields(self) -> List[str]:
        return [
            'session',
            'illness_result',
            'score'
        ]

    def resolved_mandatory_fields(self) -> list[str]:
        # TODO done to disable mandatory-field test
        return []

    def get_optional_fields(self) -> List[str]:
        return []

    def get_element_container(self):
        self.current_container = RestSession()
        return self.current_container

    def item_mapping(self) -> Dict[str, FillItemmappingCallback]:
        return {
            'questions_and_answers': ProvideAnswersCallback(),
        }

    def save(self):
        # nothing to do because result comes directly after answering the last question
        pass

    def get_active_success_messages(self) -> ResponseMessageList:
        return ResponseMessageList([self.current_container.result] if self.current_container.result else [])

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList()
