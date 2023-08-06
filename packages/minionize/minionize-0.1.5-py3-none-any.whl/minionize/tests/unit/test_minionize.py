import unittest
import unittest.mock as mock


from minionize import EntryPoint, ProcessCallback

class TestException(Exception):
    pass


class TestEntryPointGeneral(unittest.TestCase):
    def setUp(self):
        engine = mock.Mock()
        engine.next = mock.Mock(side_effect=["test", None])
        engine.ack = mock.Mock()
        engine.nack = mock.Mock()
        callback = mock.Mock()
        callback.setup = mock.Mock()
        callback.process = mock.Mock()
        callback.teardown = mock.Mock()
        self.engine = engine
        self.callback = callback

    def test_normal_operations(self):
        entrypoint = EntryPoint(self.callback, self.engine)
        entrypoint.run()

        self.assertEqual(2, self.engine.next.call_count)
        self.assertEqual(1, self.callback.setup.call_count)
        self.assertEqual(1, self.callback.process.call_count)
        self.assertEqual(1, self.callback.teardown.call_count)

    def test_operations_one_exception(self):
        exception = TestException("test_exception")
        self.callback.process = mock.Mock(side_effect=[exception, None])
        entrypoint = EntryPoint(self.callback, self.engine)
        entrypoint.run()

        self.assertEqual(2, self.engine.next.call_count)
        self.assertEqual(1, self.callback.setup.call_count)
        self.assertEqual(1, self.callback.process.call_count)
        self.assertEqual(1, self.callback.teardown.call_count)
        # check parameters
        self.callback.teardown.assert_called_with("test", self.engine, exception)

class TestEntryPointWithProcessCallback(unittest.TestCase):
    def setUp(self):
        engine = mock.Mock()
        engine.next = mock.Mock(side_effect=["test", None])
        engine.ack = mock.Mock()
        engine.nack = mock.Mock()
        callback = ProcessCallback()
        self.engine = engine
        self.callback = callback

    def test_normal_operations(self):
        entrypoint = EntryPoint(self.callback, self.engine)
        entrypoint.run()

        self.assertEqual(2, self.engine.next.call_count)
        self.assertEqual(1, self.engine.ack.call_count)
        self.assertEqual(0, self.engine.nack.call_count)
        self.engine.ack.assert_called_with("test")

    def test_operations_one_exception(self):

        class CustomCallback(ProcessCallback):
            def to_cmd(self):
                return "exit 1"
        entrypoint = EntryPoint(CustomCallback(), self.engine)
        entrypoint.run()

        self.assertEqual(2, self.engine.next.call_count)
        self.assertEqual(0, self.engine.ack.call_count)
        self.assertEqual(1, self.engine.nack.call_count)