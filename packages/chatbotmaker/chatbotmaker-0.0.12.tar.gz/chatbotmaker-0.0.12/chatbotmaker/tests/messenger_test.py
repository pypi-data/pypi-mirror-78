from ..messenger import Messenger
from . import pytest


def test_send_message_should_fail():
    messenger = Messenger()
    with pytest.raises(Exception) as exception_info:
        messenger.send("user", "message")
    assert "implemented" in str(exception_info)


def test_mark_writing_on_should_do_nothing():
    messenger = Messenger()
    messenger.mark_writing("user", True)


def test_mark_writing_off_should_do_nothing():
    messenger = Messenger()
    messenger.mark_writing("user", False)


def test_mark_seen_should_do_nothing():
    messenger = Messenger()
    messenger.mark_seen("user")
