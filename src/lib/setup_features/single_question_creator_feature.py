from typing import List, Dict, Any

import balder

import balderhub.data
from balderhub.crud.lib.utils.item_mapping.base_itemmapping_callback import CallbackElementObjectT

from balderhub.data.lib.utils import ResponseMessage, ResponseMessageList

from balderhub.crud.lib.setup_features import SingleDataCreatorFeature
from balderhub.crud.lib.utils.item_mapping import FillItemmappingCallback


from lib import pages
from lib.utils import QuestionResultDataItem


class ProvideAnswersCallback(FillItemmappingCallback):

    def __init__(self, html_page: pages.AppWebPage):
        super().__init__(html_page)
        self._html_page = html_page

    def execute(self, feature: balder.Feature, field: str, element_object: CallbackElementObjectT, data_to_fill) -> Any:

        val = data_to_fill.get_field_value(field)


        for cur_expected_question, cur_answer in val:
            assert self._html_page.span_question.wait_to_be_clickable_for(3).text == cur_expected_question
            self._html_page.btn_by_name(cur_answer).wait_to_be_clickable_for(1).click()
        return val


@balderhub.data.register_for_data_item(QuestionResultDataItem)
class SingleQuestionCreator(SingleDataCreatorFeature):
    page = pages.AppWebPage()

    def load(self):
        self.page.open()

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
        return self.page

    def item_mapping(self) -> Dict[str, FillItemmappingCallback]:
        return {
            'questions_and_answers': ProvideAnswersCallback(self.page),
        }

    def save(self):
        # nothing to do because result comes directly after answering the last question
        pass

    def get_active_success_messages(self) -> ResponseMessageList:
        if self.page.span_diagnosis.is_visible():
            return ResponseMessageList([
                ResponseMessage(self.page.span_diagnosis.wait_to_exist_for(3).text)
            ])
        else:
            return ResponseMessageList([])

    def get_active_error_messages(self) -> ResponseMessageList:
        return ResponseMessageList()
