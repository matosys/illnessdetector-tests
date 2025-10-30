from __future__ import annotations

from typing import List
import balderhub.data

from balderhub.data.lib.scenario_features import ExampleDataProviderFeature
from balderhub.data.lib.utils import NOT_DEFINABLE, ResponseMessageList, ResponseMessage

from lib.utils import QuestionResultDataItem


@balderhub.data.register_for_data_item(QuestionResultDataItem)
class ExampleQuestionProvider(ExampleDataProviderFeature):

    # TODO create function that automates the example generation

    def get_valid_examples(self) -> List[ExampleDataProviderFeature.NamedExample]:

        return [
            ExampleDataProviderFeature.NamedExample(
                name='Yes-Yes-Yes',
                data=QuestionResultDataItem(
                    session=NOT_DEFINABLE,
                    questions_and_answers=[
                        ('Do you have a fever (temperature above 100°F / 38°C)?', 'Yes'),
                        ('Is the fever accompanied by chills or sweating?', 'Yes'),
                        ('Do you have a sore throat or body aches?', 'Yes')
                    ],
                    illness_result="Possible diagnosis: Flu. Recommend rest, fluids, and over-the-counter meds.",
                    score=1.5
                ),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage('Possible diagnosis: Flu. Recommend rest, fluids, and over-the-counter meds.')])

            ),
            ExampleDataProviderFeature.NamedExample(
                name='No-No-No-No',
                data=QuestionResultDataItem(
                    session=NOT_DEFINABLE,
                    questions_and_answers=[
                        ('Do you have a fever (temperature above 100°F / 38°C)?', 'No'),
                        ('Do you have any respiratory symptoms, like coughing or sneezing?', 'No'),
                        ('Do you have stomach-related issues, like nausea, vomiting, or diarrhea?', 'No'),
                        ('Do you have headaches, fatigue, or muscle aches without other symptoms?', 'No')
                    ],
                    illness_result="No clear illness detected. Maybe it's just a bad day - try again with more details!",
                    score=1.5
                ),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage("No clear illness detected. Maybe it's just a bad day - try again with more details!")])

            ),
            ExampleDataProviderFeature.NamedExample(
                name='No-Yes-Wet',
                data=QuestionResultDataItem(
                    session=NOT_DEFINABLE,
                    questions_and_answers=[
                        ('Do you have a fever (temperature above 100°F / 38°C)?', 'No'),
                        ('Do you have any respiratory symptoms, like coughing or sneezing?', 'Yes'),
                        ('Is your cough dry (no mucus) or wet (with phlegm)?', 'Wet'),
                    ],
                    illness_result="Possible diagnosis: Bronchitis or chest cold. Suggest cough syrup and rest.",
                    score=1.5
                ),
                expected_response_messages=ResponseMessageList(
                    [ResponseMessage(
                        "Possible diagnosis: Bronchitis or chest cold. Suggest cough syrup and rest.")])

            ),
        ]

    def get_invalid_examples(self) -> List[ExampleDataProviderFeature.NamedExample]:
        return [
            # TODO
        ]
