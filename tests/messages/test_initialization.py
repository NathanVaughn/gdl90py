import pytest

from gdl90py.exceptions import DataTooLong
from gdl90py.messages.initialization import InitializationMessage


def test_initialization_serialize():
    i = InitializationMessage(
        audio_test=True,
        audio_inhibit=False,
        CDTI_ok=True,
        CSA_audio_disable=False,
        CSA_disable=True,
    )
    assert i.serialize(outgoing_lsb=False) == b"\x7e\x02\x41\x01\x43\x61\x7e"


def test_initialization_deserialize():
    i = InitializationMessage(
        audio_test=True,
        audio_inhibit=False,
        CDTI_ok=True,
        CSA_audio_disable=False,
        CSA_disable=True,
    )
    assert i == InitializationMessage.deserialize(b"\x7e\x02\x41\x01\x43\x61\x7e")


def test_initialization_deserialize_too_long():
    with pytest.raises(DataTooLong):
        InitializationMessage.deserialize(b"\x7e\x02\x41\x01\x00\x87\x3f\x7e")
