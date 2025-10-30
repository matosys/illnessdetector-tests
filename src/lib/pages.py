from typing import Union, List

from balderhub.html.lib.scenario_features import HtmlPage
import balderhub.html.lib.utils.components as html
from balderhub.html.lib.utils import Selector
from balderhub.url.lib.utils import Url


class AppWebPage(HtmlPage):

    @property
    def applicable_on_url_schema(self) -> Union[Url, List[Url]]:
        return Url('http://webserver:5000')

    def open(self):
        self.guicontrol.driver.navigate_to(self.applicable_on_url_schema)

    @property
    def span_question(self):
        return html.HtmlSpanElement.by_selector(self.driver, Selector.by_id('question'))

    @property
    def span_diagnosis(self):
        return html.HtmlSpanElement.by_selector(self.driver, Selector.by_id('result'))

    def btn_by_name(self, name: str):
        return html.HtmlButtonElement.by_selector(self.driver, Selector.by_xpath(f'.//div[contains(text(),"{name}")]'))

    @property
    def btn_yes(self):
        return self.btn_by_name('Yes')

    @property
    def btn_no(self):
        return self.btn_by_name('No')

    @property
    def btn_restart(self):
        return html.HtmlButtonElement.by_selector(self.driver, Selector.by_xpath('.//button[contains(text(),"Restart")]'))
