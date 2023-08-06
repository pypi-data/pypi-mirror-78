import grpc
import px.px_pb2 as px
from px.px_pb2_grpc import BrowserStub
from px_server.server import Server
import logging

logging.getLogger().setLevel(logging.INFO)

class Client:

    channel = None

    stub = None

    debug = False

    server = None

    url = None

    def __init__(self, url=None, debug=False):
        if url is None:
            self.server = Server()
            url = 'localhost:{}'.format(self.server.port)

        self.url = url
        self.channel = grpc.insecure_channel(self.url)
        grpc.channel_ready_future(self.channel).result(timeout=300)
        self.stub = BrowserStub(self.channel)
        self.debug = debug

    def __del__(self):
        if self.channel is not None:
            self.channel.close()
            logging.info('Channel closed')

    def do_request(self, actions):
        request = px.DoRequest(actions=[actions])
        response = self.stub.Do(request)
        if response.status == 1:
            raise Exception(response.error)
        else:
            return response.result

    def clear_and_type(self, selector, text):
        actions = px.Action(clearAndTypeAction=px.ClearAndTypeAction(selector=selector, text=text))
        self.do_request(actions)

    def click(self, selector, option=None):
        actions = px.Action(clickAction=px.ClickAction(selector=selector, option=option))
        self.do_request(actions)

    def clickAndWaitForNavigation(self, selector, option=None, waitOption=None):
        actions = px.Action(clickAndWaitForNavigationAction=px.ClickAndWaitForNavigationAction(selector=selector, option=option, waitOption=waitOption))
        self.do_request(actions)

    def close(self):
        actions = px.Action(closeAction=px.CloseAction())
        self.do_request(actions)

    def cookies(self):
        actions = px.Action(cookiesAction=px.CookiesAction())
        self.do_request(actions)

    def delete_cookies(self):
        actions = px.Action(deleteCookiesAction=px.DeleteCookiesAction())
        self.do_request(actions)

    def get_text(self, selector):
        actions = px.Action(getInnerTextAction=px.GetInnerTextAction(selector=selector))
        return self.do_request(actions)

    def goto(self, url):
        actions = px.Action(gotoAction=px.GotoAction(url=url))
        self.do_request(actions)

    def launch(self, headless=None, defaultViewport=None):
        actions = px.Action(launchAction=px.LaunchAction(headless=headless, defaultViewport=defaultViewport))
        self.do_request(actions)

    def select(self, selector, values):
        actions = px.Action(selectAction=px.SelectAction(selector=selector, values=values))
        self.do_request(actions)

    def screenshot(self, path, fullPage):
        actions = px.Action(screenshotAction=px.ScreenshotAction(path=path, fullPage=fullPage))
        self.do_request(actions)

    def reload(self):
        actions = px.Action(reloadAction=px.ReloadAction())
        self.do_request(actions)

    def type(self, selector, text):
        actions = px.Action(typeAction=px.TypeAction(selector=selector, text=text))
        self.do_request(actions)

    def wait(self, time):
        actions = px.Action(waitAction=px.WaitAction(time=time))
        self.do_request(actions)

    def waitFor(self, selector):
        actions = px.Action(waitForAction=px.WaitForAction(selector=selector))
        return self.do_request(actions)
