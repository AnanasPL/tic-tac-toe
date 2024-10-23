from event_handlers.shared import rooms


class SocketSetupTeardown:
    def teardown_method(self, method):
        rooms._rooms.clear()
    