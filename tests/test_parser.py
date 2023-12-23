import pytest

from gdl90py.exceptions import UnkownMessageID
from gdl90py.messages.initialization import InitializationMessage
from gdl90py.parser import parse_message, parse_messages


def test_parse_message_known():
    i = InitializationMessage(
        audio_test=True,
        audio_inhibit=False,
        CDTI_ok=True,
        CSA_audio_disable=False,
        CSA_disable=True,
    )
    assert parse_message(b"\x7e\x02\x41\x01\x43\x61\x7e") == i


def test_parse_message_unknown():
    with pytest.raises(UnkownMessageID):
        parse_message(b"\x7e\x55\x00\x00\x50\x0a\x7e")


def test_parse_message_ignore():
    # make sure nothing is raised
    parse_message(b"\x7e\x55\x00\x00\x50\x0a\x7e", ignore_unknown=True)


def test_parse_messages_known():
    i = InitializationMessage(
        audio_test=True,
        audio_inhibit=False,
        CDTI_ok=True,
        CSA_audio_disable=False,
        CSA_disable=True,
    )
    assert parse_messages(b"\x7e\x02\x41\x01\x43\x61\x7e") == [i]


def test_parse_messages_unknown():
    with pytest.raises(UnkownMessageID):
        parse_messages(b"\x7e\x55\x00\x00\x50\x0a\x7e")


def test_parse_messages_ignore1():
    # make sure nothing is raised
    parse_messages(b"\x7e\x55\x00\x00\x50\x0a\x7e", ignore_unknown=True)


def test_parse_messages_ignore2():
    i = InitializationMessage(
        audio_test=True,
        audio_inhibit=False,
        CDTI_ok=True,
        CSA_audio_disable=False,
        CSA_disable=True,
    )
    assert parse_messages(
        b"\x7e\x55\x00\x00\x50\x0a\x7e\x7e\x02\x41\x01\x43\x61\x7e", ignore_unknown=True
    ) == [i]
