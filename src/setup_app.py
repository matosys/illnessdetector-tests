import balder
from selenium.webdriver.firefox.options import Options

from lib import setup_features, pages
import balderhub.selenium.lib.setup_features


class SeleniumFeature(balderhub.selenium.lib.setup_features.SeleniumRemoteWebdriverFeature):
    command_executor = "http://seleniumfirefox:4444"
    selenium_options = Options()


class SetupApp(balder.Setup):

    class InternDevice(balder.Device):
        pass

    @balder.connect('InternDevice', over_connection=balder.Connection)
    class DatabaseSpy(balder.Device):
        retriever = setup_features.MultipleDatabaseReceiver()

    @balder.connect('InternDevice', over_connection=balder.Connection)
    class ClientBrowser(balder.Device):
        selenium = SeleniumFeature()
        page = pages.AppWebPage()
        creator = setup_features.SingleQuestionCreator()
        example = setup_features.ExampleQuestionProvider()

    @balder.connect('InternDevice', over_connection=balder.Connection)
    class ClientRest(balder.Device):
        creator = setup_features.SingleQuestionCreatorOverRest()
        example = setup_features.ExampleQuestionProvider()

    @balder.fixture('session')
    def resources(self):
        self.ClientBrowser.selenium.create()
        yield
        self.DatabaseSpy.retriever.close_db()
        self.ClientBrowser.selenium.quit()

    @balder.fixture('testcase')
    def press_restart(self):
        yield
        if self.ClientBrowser.page.btn_restart.is_visible():
            self.ClientBrowser.page.btn_restart.click()
