from typing import List
import sqlite3

import balderhub.data
from balderhub.data.lib.utils import SingleDataItemCollection

from balderhub.crud.lib.scenario_features import MultipleDataReaderFeature

from lib.utils import QuestionResultDataItem


@balderhub.data.register_for_data_item(QuestionResultDataItem)
class MultipleDatabaseReceiver(MultipleDataReaderFeature):
    DATABASE_FILE = '/app/databases/sessions.db'
    database = None

    def create_db(self):
        self.database = sqlite3.connect(self.DATABASE_FILE)

    def close_db(self):
        if self.database:
            self.database.close()
            self.database = None

    def get_non_collectable_fields(self) -> List[str]:
        return []

    def load(self):
        self.create_db()

    def collect(self) -> SingleDataItemCollection:
        all_items = []
        c = self.database.cursor()
        c.execute('SELECT session_id, result, score FROM sessions')
        while True:
            row = c.fetchone()
            if row is None:
                break
            session_id, result, score = row
            answer_cursor = self.database.cursor()
            answer_cursor.execute('SELECT question, answer_text FROM answers WHERE session_id=? ORDER BY created_at', (session_id,))
            all_items.append(
                QuestionResultDataItem(
                    session=session_id,
                    questions_and_answers=answer_cursor.fetchall(),
                    illness_result=result,
                    score=score,
            ))
        return SingleDataItemCollection(all_items)
