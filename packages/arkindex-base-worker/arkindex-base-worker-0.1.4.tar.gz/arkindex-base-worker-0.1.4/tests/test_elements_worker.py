# -*- coding: utf-8 -*-
import json
import os
import sys
import tempfile
from argparse import Namespace
from uuid import UUID

import pytest
from apistar.exceptions import ErrorResponse

from arkindex_worker.models import Element
from arkindex_worker.worker import ElementsWorker, EntityType, TranscriptionType

TRANSCRIPTIONS_SAMPLE = [
    {
        "polygon": [[100, 150], [700, 150], [700, 200], [100, 200]],
        "score": 0.5,
        "text": "The",
    },
    {
        "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
        "score": 0.75,
        "text": "first",
    },
    {
        "polygon": [[1000, 300], [1200, 300], [1200, 500], [1000, 500]],
        "score": 0.9,
        "text": "line",
    },
]


def test_cli_default(monkeypatch, mock_worker_version_api):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump(
            [
                {"id": "volumeid", "type": "volume"},
                {"id": "pageid", "type": "page"},
                {"id": "actid", "type": "act"},
                {"id": "surfaceid", "type": "surface"},
            ],
            f,
        )

    monkeypatch.setenv("TASK_ELEMENTS", path)
    monkeypatch.setattr(sys, "argv", ["worker"])
    worker = ElementsWorker()
    worker.configure()

    assert worker.args.elements_list.name == path
    assert not worker.args.element
    os.unlink(path)


def test_cli_arg_elements_list_given(mocker, mock_worker_version_api):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump(
            [
                {"id": "volumeid", "type": "volume"},
                {"id": "pageid", "type": "page"},
                {"id": "actid", "type": "act"},
                {"id": "surfaceid", "type": "surface"},
            ],
            f,
        )

    mocker.patch.object(sys, "argv", ["worker", "--elements-list", path])
    worker = ElementsWorker()
    worker.configure()

    assert worker.args.elements_list.name == path
    assert not worker.args.element
    os.unlink(path)


def test_cli_arg_element_one_given_not_uuid(mocker, mock_elements_worker):
    mocker.patch.object(sys, "argv", ["worker", "--element", "1234"])
    worker = ElementsWorker()
    with pytest.raises(SystemExit):
        worker.configure()


def test_cli_arg_element_one_given(mocker, mock_elements_worker):
    mocker.patch.object(
        sys, "argv", ["worker", "--element", "12341234-1234-1234-1234-123412341234"]
    )
    worker = ElementsWorker()
    worker.configure()

    assert worker.args.element == [UUID("12341234-1234-1234-1234-123412341234")]
    # elements_list is None because TASK_ELEMENTS environment variable isn't set
    assert not worker.args.elements_list


def test_cli_arg_element_many_given(mocker, mock_elements_worker):
    mocker.patch.object(
        sys,
        "argv",
        [
            "worker",
            "--element",
            "12341234-1234-1234-1234-123412341234",
            "43214321-4321-4321-4321-432143214321",
        ],
    )
    worker = ElementsWorker()
    worker.configure()

    assert worker.args.element == [
        UUID("12341234-1234-1234-1234-123412341234"),
        UUID("43214321-4321-4321-4321-432143214321"),
    ]
    # elements_list is None because TASK_ELEMENTS environment variable isn't set
    assert not worker.args.elements_list


def test_list_elements_elements_list_arg_wrong_type(monkeypatch, mock_elements_worker):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump({}, f)

    monkeypatch.setenv("TASK_ELEMENTS", path)
    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    with pytest.raises(AssertionError) as e:
        worker.list_elements()
    assert str(e.value) == "Elements list must be a list"


def test_list_elements_elements_list_arg_empty_list(monkeypatch, mock_elements_worker):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump([], f)

    monkeypatch.setenv("TASK_ELEMENTS", path)
    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    with pytest.raises(AssertionError) as e:
        worker.list_elements()
    assert str(e.value) == "No elements in elements list"


def test_list_elements_elements_list_arg_missing_id(monkeypatch, mock_elements_worker):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump([{"type": "volume"}], f)

    monkeypatch.setenv("TASK_ELEMENTS", path)
    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    elt_list = worker.list_elements()

    assert elt_list == []


def test_list_elements_elements_list_arg(monkeypatch, mock_elements_worker):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump(
            [
                {"id": "volumeid", "type": "volume"},
                {"id": "pageid", "type": "page"},
                {"id": "actid", "type": "act"},
                {"id": "surfaceid", "type": "surface"},
            ],
            f,
        )

    monkeypatch.setenv("TASK_ELEMENTS", path)
    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    elt_list = worker.list_elements()

    assert elt_list == ["volumeid", "pageid", "actid", "surfaceid"]


def test_list_elements_element_arg(mocker, mock_elements_worker):
    mocker.patch(
        "arkindex_worker.worker.argparse.ArgumentParser.parse_args",
        return_value=Namespace(
            element=["volumeid", "pageid"], verbose=False, elements_list=None
        ),
    )

    worker = ElementsWorker()
    worker.configure()

    elt_list = worker.list_elements()

    assert elt_list == ["volumeid", "pageid"]


def test_list_elements_both_args_error(mocker, mock_elements_worker):
    _, path = tempfile.mkstemp()
    with open(path, "w") as f:
        json.dump(
            [
                {"id": "volumeid", "type": "volume"},
                {"id": "pageid", "type": "page"},
                {"id": "actid", "type": "act"},
                {"id": "surfaceid", "type": "surface"},
            ],
            f,
        )
    mocker.patch(
        "arkindex_worker.worker.argparse.ArgumentParser.parse_args",
        return_value=Namespace(
            element=["anotherid", "againanotherid"],
            verbose=False,
            elements_list=open(path),
        ),
    )

    worker = ElementsWorker()
    worker.configure()
    os.unlink(path)

    with pytest.raises(AssertionError) as e:
        worker.list_elements()
    assert str(e.value) == "elements-list and element CLI args shouldn't be both set"


def test_load_corpus_classes_api_error(responses, mock_elements_worker):
    corpus_id = "12341234-1234-1234-1234-123412341234"
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/corpus/{corpus_id}/classes/",
        status=500,
    )

    assert not mock_elements_worker.classes
    with pytest.raises(ErrorResponse):
        mock_elements_worker.load_corpus_classes(corpus_id)

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        f"http://testserver/api/v1/corpus/{corpus_id}/classes/",
    ]
    assert not mock_elements_worker.classes


def test_load_corpus_classes(responses, mock_elements_worker):
    corpus_id = "12341234-1234-1234-1234-123412341234"
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/corpus/{corpus_id}/classes/",
        status=200,
        json={
            "results": [
                {
                    "id": "0000",
                    "name": "good",
                    "nb_best": 0,
                },
                {
                    "id": "1111",
                    "name": "average",
                    "nb_best": 0,
                },
                {
                    "id": "2222",
                    "name": "bad",
                    "nb_best": 0,
                },
            ]
        },
    )

    assert not mock_elements_worker.classes
    mock_elements_worker.load_corpus_classes(corpus_id)

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        f"http://testserver/api/v1/corpus/{corpus_id}/classes/",
    ]
    assert mock_elements_worker.classes == {
        "12341234-1234-1234-1234-123412341234": {
            "good": "0000",
            "average": "1111",
            "bad": "2222",
        }
    }


def test_get_ml_class_id_load_classes(responses, mock_elements_worker):
    corpus_id = "12341234-1234-1234-1234-123412341234"
    responses.add(
        responses.GET,
        f"http://testserver/api/v1/corpus/{corpus_id}/classes/",
        status=200,
        json={
            "results": [
                {
                    "id": "0000",
                    "name": "good",
                    "nb_best": 0,
                }
            ]
        },
    )

    assert not mock_elements_worker.classes
    ml_class_id = mock_elements_worker.get_ml_class_id(corpus_id, "good")

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        f"http://testserver/api/v1/corpus/{corpus_id}/classes/",
    ]
    assert mock_elements_worker.classes == {
        "12341234-1234-1234-1234-123412341234": {"good": "0000"}
    }
    assert ml_class_id == "0000"


def test_get_ml_class_id_inexistant_class(mock_elements_worker):
    corpus_id = "12341234-1234-1234-1234-123412341234"
    mock_elements_worker.classes = {
        "12341234-1234-1234-1234-123412341234": {"good": "0000"}
    }

    assert mock_elements_worker.classes == {
        "12341234-1234-1234-1234-123412341234": {"good": "0000"}
    }
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.get_ml_class_id(corpus_id, "bad")
    assert str(e.value) == f"ml_class 'bad' doesn't exist on corpus {corpus_id}"


def test_get_ml_class_id(mock_elements_worker):
    corpus_id = "12341234-1234-1234-1234-123412341234"
    mock_elements_worker.classes = {
        "12341234-1234-1234-1234-123412341234": {"good": "0000"}
    }

    ml_class_id = mock_elements_worker.get_ml_class_id(corpus_id, "good")
    assert ml_class_id == "0000"


def test_create_sub_element_wrong_element(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=None,
            type="something",
            name="0",
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element="not element type",
            type="something",
            name="0",
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"


def test_create_sub_element_wrong_type(mock_elements_worker):
    elt = Element({"zone": None})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type=None,
            name="0",
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "type shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type=1234,
            name="0",
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "type shouldn't be null and should be of type str"


def test_create_sub_element_wrong_name(mock_elements_worker):
    elt = Element({"zone": None})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type="something",
            name=None,
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "name shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type="something",
            name=1234,
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "name shouldn't be null and should be of type str"


def test_create_sub_element_wrong_polygon(mock_elements_worker):
    elt = Element({"zone": None})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type="something",
            name="0",
            polygon=None,
        )
    assert str(e.value) == "polygon shouldn't be null and should be of type list"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type="something",
            name="O",
            polygon="not a polygon",
        )
    assert str(e.value) == "polygon shouldn't be null and should be of type list"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type="something",
            name="O",
            polygon=[[1, 1], [2, 2]],
        )
    assert str(e.value) == "polygon should have at least three points"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type="something",
            name="O",
            polygon=[[1, 1, 1], [2, 2, 1], [2, 1, 1], [1, 2, 1]],
        )
    assert str(e.value) == "polygon points should be lists of two items"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type="something",
            name="O",
            polygon=[[1], [2], [2], [1]],
        )
    assert str(e.value) == "polygon points should be lists of two items"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_sub_element(
            element=elt,
            type="something",
            name="O",
            polygon=[["not a coord", 1], [2, 2], [2, 1], [1, 2]],
        )
    assert str(e.value) == "polygon points should be lists of two numbers"


def test_create_sub_element_api_error(responses, mock_elements_worker):
    elt = Element(
        {
            "id": "12341234-1234-1234-1234-123412341234",
            "corpus": {"id": "11111111-1111-1111-1111-111111111111"},
            "zone": {"image": {"id": "22222222-2222-2222-2222-222222222222"}},
        }
    )
    responses.add(
        responses.POST,
        "http://testserver/api/v1/elements/create/",
        status=500,
    )

    with pytest.raises(ErrorResponse):
        mock_elements_worker.create_sub_element(
            element=elt,
            type="something",
            name="0",
            polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
        )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        "http://testserver/api/v1/elements/create/",
    ]


def test_create_sub_element(responses, mock_elements_worker):
    elt = Element(
        {
            "id": "12341234-1234-1234-1234-123412341234",
            "corpus": {"id": "11111111-1111-1111-1111-111111111111"},
            "zone": {"image": {"id": "22222222-2222-2222-2222-222222222222"}},
        }
    )
    responses.add(
        responses.POST,
        "http://testserver/api/v1/elements/create/",
        status=200,
        json={"id": "12345678-1234-1234-1234-123456789123"},
    )

    sub_element_id = mock_elements_worker.create_sub_element(
        element=elt,
        type="something",
        name="0",
        polygon=[[1, 1], [2, 2], [2, 1], [1, 2]],
    )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        "http://testserver/api/v1/elements/create/",
    ]
    assert json.loads(responses.calls[1].request.body) == {
        "type": "something",
        "name": "0",
        "image": "22222222-2222-2222-2222-222222222222",
        "corpus": "11111111-1111-1111-1111-111111111111",
        "polygon": [[1, 1], [2, 2], [2, 1], [1, 2]],
        "parent": "12341234-1234-1234-1234-123412341234",
        "worker_version": "12341234-1234-1234-1234-123412341234",
    }
    assert sub_element_id == "12345678-1234-1234-1234-123456789123"


def test_create_transcription_wrong_element(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=None,
            text="i am a line",
            type=TranscriptionType.Line,
            score=0.42,
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element="not element type",
            text="i am a line",
            type=TranscriptionType.Line,
            score=0.42,
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"


def test_create_transcription_wrong_type(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=elt,
            text="i am a line",
            type=None,
            score=0.42,
        )
    assert (
        str(e.value) == "type shouldn't be null and should be of type TranscriptionType"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=elt,
            text="i am a line",
            type=1234,
            score=0.42,
        )
    assert (
        str(e.value) == "type shouldn't be null and should be of type TranscriptionType"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=elt,
            text="i am a line",
            type="not_a_transcription_type",
            score=0.42,
        )
    assert (
        str(e.value) == "type shouldn't be null and should be of type TranscriptionType"
    )


def test_create_transcription_wrong_text(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=elt,
            text=None,
            type=TranscriptionType.Line,
            score=0.42,
        )
    assert str(e.value) == "text shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=elt,
            text=1234,
            type=TranscriptionType.Line,
            score=0.42,
        )
    assert str(e.value) == "text shouldn't be null and should be of type str"


def test_create_transcription_wrong_score(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=elt,
            text="i am a line",
            type=TranscriptionType.Line,
            score=None,
        )
    assert (
        str(e.value) == "score shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=elt,
            text="i am a line",
            type=TranscriptionType.Line,
            score="wrong score",
        )
    assert (
        str(e.value) == "score shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=elt,
            text="i am a line",
            type=TranscriptionType.Line,
            score=0,
        )
    assert (
        str(e.value) == "score shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_transcription(
            element=elt,
            text="i am a line",
            type=TranscriptionType.Line,
            score=2.00,
        )
    assert (
        str(e.value) == "score shouldn't be null and should be a float in [0..1] range"
    )


def test_create_transcription_api_error(responses, mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})
    responses.add(
        responses.POST,
        f"http://testserver/api/v1/element/{elt.id}/transcription/",
        status=500,
    )

    with pytest.raises(ErrorResponse):
        mock_elements_worker.create_transcription(
            element=elt,
            text="i am a line",
            type=TranscriptionType.Line,
            score=0.42,
        )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        f"http://testserver/api/v1/element/{elt.id}/transcription/",
    ]


def test_create_transcription(responses, mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})
    responses.add(
        responses.POST,
        f"http://testserver/api/v1/element/{elt.id}/transcription/",
        status=200,
    )

    mock_elements_worker.create_transcription(
        element=elt,
        text="i am a line",
        type=TranscriptionType.Line,
        score=0.42,
    )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        f"http://testserver/api/v1/element/{elt.id}/transcription/",
    ]

    assert json.loads(responses.calls[1].request.body) == {
        "text": "i am a line",
        "type": "line",
        "worker_version": "12341234-1234-1234-1234-123412341234",
        "score": 0.42,
    }


def test_create_classification_wrong_element(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=None,
            ml_class="a_class",
            confidence=0.42,
            high_confidence=True,
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element="not element type",
            ml_class="a_class",
            confidence=0.42,
            high_confidence=True,
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"


def test_create_classification_wrong_ml_class(mock_elements_worker):
    elt = Element(
        {
            "id": "12341234-1234-1234-1234-123412341234",
            "corpus": {"id": "11111111-1111-1111-1111-111111111111"},
        }
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=elt,
            ml_class=None,
            confidence=0.42,
            high_confidence=True,
        )
    assert str(e.value) == "ml_class shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=elt,
            ml_class=1234,
            confidence=0.42,
            high_confidence=True,
        )
    assert str(e.value) == "ml_class shouldn't be null and should be of type str"

    mock_elements_worker.classes = {
        "11111111-1111-1111-1111-111111111111": {"another_class": "0000"}
    }
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=elt,
            ml_class="a_class",
            confidence=0.42,
            high_confidence=True,
        )
    assert (
        str(e.value)
        == "ml_class 'a_class' doesn't exist on corpus 11111111-1111-1111-1111-111111111111"
    )


def test_create_classification_wrong_confidence(mock_elements_worker):
    mock_elements_worker.classes = {
        "11111111-1111-1111-1111-111111111111": {"a_class": "0000"}
    }
    elt = Element(
        {
            "id": "12341234-1234-1234-1234-123412341234",
            "corpus": {"id": "11111111-1111-1111-1111-111111111111"},
        }
    )
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=elt,
            ml_class="a_class",
            confidence=None,
            high_confidence=True,
        )
    assert (
        str(e.value)
        == "confidence shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=elt,
            ml_class="a_class",
            confidence="wrong confidence",
            high_confidence=True,
        )
    assert (
        str(e.value)
        == "confidence shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=elt,
            ml_class="a_class",
            confidence=0,
            high_confidence=True,
        )
    assert (
        str(e.value)
        == "confidence shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=elt,
            ml_class="a_class",
            confidence=2.00,
            high_confidence=True,
        )
    assert (
        str(e.value)
        == "confidence shouldn't be null and should be a float in [0..1] range"
    )


def test_create_classification_wrong_high_confidence(mock_elements_worker):
    mock_elements_worker.classes = {
        "11111111-1111-1111-1111-111111111111": {"a_class": "0000"}
    }
    elt = Element(
        {
            "id": "12341234-1234-1234-1234-123412341234",
            "corpus": {"id": "11111111-1111-1111-1111-111111111111"},
        }
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=elt,
            ml_class="a_class",
            confidence=0.42,
            high_confidence=None,
        )
    assert (
        str(e.value) == "high_confidence shouldn't be null and should be of type bool"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_classification(
            element=elt,
            ml_class="a_class",
            confidence=0.42,
            high_confidence="wrong high_confidence",
        )
    assert (
        str(e.value) == "high_confidence shouldn't be null and should be of type bool"
    )


def test_create_classification_api_error(responses, mock_elements_worker):
    mock_elements_worker.classes = {
        "11111111-1111-1111-1111-111111111111": {"a_class": "0000"}
    }
    elt = Element(
        {
            "id": "12341234-1234-1234-1234-123412341234",
            "corpus": {"id": "11111111-1111-1111-1111-111111111111"},
        }
    )
    responses.add(
        responses.POST,
        "http://testserver/api/v1/classifications/",
        status=500,
    )

    with pytest.raises(ErrorResponse):
        mock_elements_worker.create_classification(
            element=elt,
            ml_class="a_class",
            confidence=0.42,
            high_confidence=True,
        )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        "http://testserver/api/v1/classifications/",
    ]


def test_create_classification(responses, mock_elements_worker):
    mock_elements_worker.classes = {
        "11111111-1111-1111-1111-111111111111": {"a_class": "0000"}
    }
    elt = Element(
        {
            "id": "12341234-1234-1234-1234-123412341234",
            "corpus": {"id": "11111111-1111-1111-1111-111111111111"},
        }
    )
    responses.add(
        responses.POST,
        "http://testserver/api/v1/classifications/",
        status=200,
    )

    mock_elements_worker.create_classification(
        element=elt,
        ml_class="a_class",
        confidence=0.42,
        high_confidence=True,
    )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        "http://testserver/api/v1/classifications/",
    ]

    assert json.loads(responses.calls[1].request.body) == {
        "element": "12341234-1234-1234-1234-123412341234",
        "ml_class": "0000",
        "worker_version": "12341234-1234-1234-1234-123412341234",
        "confidence": 0.42,
        "high_confidence": True,
    }


def test_create_entity_wrong_element(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element="not element type",
            name="Bob Bob",
            type=EntityType.Person,
            corpus="12341234-1234-1234-1234-123412341234",
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element="not element type",
            name="Bob Bob",
            type=EntityType.Person,
            corpus="12341234-1234-1234-1234-123412341234",
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"


def test_create_entity_wrong_name(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name=None,
            type=EntityType.Person,
            corpus="12341234-1234-1234-1234-123412341234",
        )
    assert str(e.value) == "name shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name=1234,
            type=EntityType.Person,
            corpus="12341234-1234-1234-1234-123412341234",
        )
    assert str(e.value) == "name shouldn't be null and should be of type str"


def test_create_entity_wrong_type(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=None,
            corpus="12341234-1234-1234-1234-123412341234",
        )
    assert str(e.value) == "type shouldn't be null and should be of type EntityType"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=1234,
            corpus="12341234-1234-1234-1234-123412341234",
        )
    assert str(e.value) == "type shouldn't be null and should be of type EntityType"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type="not_an_entity_type",
            corpus="12341234-1234-1234-1234-123412341234",
        )
    assert str(e.value) == "type shouldn't be null and should be of type EntityType"


def test_create_entity_wrong_corpus(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=EntityType.Person,
            corpus=None,
        )
    assert str(e.value) == "corpus shouldn't be null and should be of type str"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=EntityType.Person,
            corpus=1234,
        )
    assert str(e.value) == "corpus shouldn't be null and should be of type str"


def test_create_entity_wrong_metas(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=EntityType.Person,
            corpus="12341234-1234-1234-1234-123412341234",
            metas="wrong metas",
        )
    assert str(e.value) == "metas should be of type dict"


def test_create_entity_wrong_validated(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=EntityType.Person,
            corpus="12341234-1234-1234-1234-123412341234",
            validated="wrong validated",
        )
    assert str(e.value) == "validated should be of type bool"


def test_create_entity_api_error(responses, mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})
    responses.add(
        responses.POST,
        "http://testserver/api/v1/entity/",
        status=500,
    )

    with pytest.raises(ErrorResponse):
        mock_elements_worker.create_entity(
            element=elt,
            name="Bob Bob",
            type=EntityType.Person,
            corpus="12341234-1234-1234-1234-123412341234",
        )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        "http://testserver/api/v1/entity/",
    ]


def test_create_entity(responses, mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})
    responses.add(
        responses.POST,
        "http://testserver/api/v1/entity/",
        status=200,
        json={"id": "12345678-1234-1234-1234-123456789123"},
    )

    entity_id = mock_elements_worker.create_entity(
        element=elt,
        name="Bob Bob",
        type=EntityType.Person,
        corpus="12341234-1234-1234-1234-123412341234",
    )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        "http://testserver/api/v1/entity/",
    ]
    assert json.loads(responses.calls[1].request.body) == {
        "name": "Bob Bob",
        "type": "person",
        "metas": None,
        "validated": None,
        "corpus": "12341234-1234-1234-1234-123412341234",
        "worker_version": "12341234-1234-1234-1234-123412341234",
    }
    assert entity_id == "12345678-1234-1234-1234-123456789123"


def test_create_element_transcriptions_wrong_element(mock_elements_worker):
    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=None,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=TRANSCRIPTIONS_SAMPLE,
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element="not element type",
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=TRANSCRIPTIONS_SAMPLE,
        )
    assert str(e.value) == "element shouldn't be null and should be of type Element"


def test_create_element_transcriptions_wrong_sub_element_type(mock_elements_worker):
    elt = Element({"zone": None})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type=None,
            transcription_type=TranscriptionType.Word,
            transcriptions=TRANSCRIPTIONS_SAMPLE,
        )
    assert (
        str(e.value) == "sub_element_type shouldn't be null and should be of type str"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type=1234,
            transcription_type=TranscriptionType.Word,
            transcriptions=TRANSCRIPTIONS_SAMPLE,
        )
    assert (
        str(e.value) == "sub_element_type shouldn't be null and should be of type str"
    )


def test_create_element_transcriptions_wrong_transcription_type(mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=None,
            transcriptions=TRANSCRIPTIONS_SAMPLE,
        )
    assert (
        str(e.value)
        == "transcription_type shouldn't be null and should be of type TranscriptionType"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=1234,
            transcriptions=TRANSCRIPTIONS_SAMPLE,
        )
    assert (
        str(e.value)
        == "transcription_type shouldn't be null and should be of type TranscriptionType"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type="not_a_transcription_type",
            transcriptions=TRANSCRIPTIONS_SAMPLE,
        )
    assert (
        str(e.value)
        == "transcription_type shouldn't be null and should be of type TranscriptionType"
    )


def test_create_element_transcriptions_wrong_transcriptions(mock_elements_worker):
    elt = Element({"zone": None})

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=None,
        )
    assert str(e.value) == "transcriptions shouldn't be null and should be of type list"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=1234,
        )
    assert str(e.value) == "transcriptions shouldn't be null and should be of type list"

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [[100, 150], [700, 150], [700, 200], [100, 200]],
                    "score": 0.5,
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: text shouldn't be null and should be of type str"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [[100, 150], [700, 150], [700, 200], [100, 200]],
                    "score": 0.5,
                    "text": None,
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: text shouldn't be null and should be of type str"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [[100, 150], [700, 150], [700, 200], [100, 200]],
                    "score": 0.5,
                    "text": 1234,
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: text shouldn't be null and should be of type str"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [[100, 150], [700, 150], [700, 200], [100, 200]],
                    "text": "word",
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: score shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [[100, 150], [700, 150], [700, 200], [100, 200]],
                    "score": None,
                    "text": "word",
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: score shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [[100, 150], [700, 150], [700, 200], [100, 200]],
                    "score": "a wrong score",
                    "text": "word",
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: score shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [[100, 150], [700, 150], [700, 200], [100, 200]],
                    "score": 0,
                    "text": "word",
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: score shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [[100, 150], [700, 150], [700, 200], [100, 200]],
                    "score": 2.00,
                    "text": "word",
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: score shouldn't be null and should be a float in [0..1] range"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {"score": 0.5, "text": "word"},
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: polygon shouldn't be null and should be of type list"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {"polygon": None, "score": 0.5, "text": "word"},
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: polygon shouldn't be null and should be of type list"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {"polygon": "not a polygon", "score": 0.5, "text": "word"},
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: polygon shouldn't be null and should be of type list"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {"polygon": [[1, 1], [2, 2]], "score": 0.5, "text": "word"},
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: polygon should have at least three points"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [[1, 1, 1], [2, 2, 1], [2, 1, 1], [1, 2, 1]],
                    "score": 0.5,
                    "text": "word",
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: polygon points should be lists of two items"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {"polygon": [[1], [2], [2], [1]], "score": 0.5, "text": "word"},
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: polygon points should be lists of two items"
    )

    with pytest.raises(AssertionError) as e:
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=[
                {
                    "polygon": [[0, 0], [2000, 0], [2000, 3000], [0, 3000]],
                    "score": 0.75,
                    "text": "The",
                },
                {
                    "polygon": [["not a coord", 1], [2, 2], [2, 1], [1, 2]],
                    "score": 0.5,
                    "text": "word",
                },
            ],
        )
    assert (
        str(e.value)
        == "Transcription at index 1 in transcriptions: polygon points should be lists of two numbers"
    )


def test_create_element_transcriptions_api_error(responses, mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})
    responses.add(
        responses.POST,
        f"http://testserver/api/v1/element/{elt.id}/transcriptions/bulk/",
        status=500,
    )

    with pytest.raises(ErrorResponse):
        mock_elements_worker.create_element_transcriptions(
            element=elt,
            sub_element_type="page",
            transcription_type=TranscriptionType.Word,
            transcriptions=TRANSCRIPTIONS_SAMPLE,
        )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        f"http://testserver/api/v1/element/{elt.id}/transcriptions/bulk/",
    ]


def test_create_element_transcriptions(responses, mock_elements_worker):
    elt = Element({"id": "12341234-1234-1234-1234-123412341234"})
    responses.add(
        responses.POST,
        f"http://testserver/api/v1/element/{elt.id}/transcriptions/bulk/",
        status=200,
        json=[
            {"id": "word1_1_1", "created": False},
            {"id": "word1_1_2", "created": False},
            {"id": "word1_1_3", "created": False},
        ],
    )

    annotations = mock_elements_worker.create_element_transcriptions(
        element=elt,
        sub_element_type="page",
        transcription_type=TranscriptionType.Word,
        transcriptions=TRANSCRIPTIONS_SAMPLE,
    )

    assert len(responses.calls) == 2
    assert [call.request.url for call in responses.calls] == [
        "http://testserver/api/v1/workers/versions/12341234-1234-1234-1234-123412341234/",
        f"http://testserver/api/v1/element/{elt.id}/transcriptions/bulk/",
    ]

    assert json.loads(responses.calls[1].request.body) == {
        "element_type": "page",
        "transcription_type": "word",
        "worker_version": "12341234-1234-1234-1234-123412341234",
        "transcriptions": TRANSCRIPTIONS_SAMPLE,
        "return_elements": True,
    }
    assert annotations == [
        {"id": "word1_1_1", "created": False},
        {"id": "word1_1_2", "created": False},
        {"id": "word1_1_3", "created": False},
    ]
