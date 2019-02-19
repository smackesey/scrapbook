#!/usr/bin/env python
# -*- coding: utf-8 -*-
import mock
import pytest

import pandas as pd

from collections import OrderedDict
from IPython.display import Markdown
from pandas.util.testing import assert_frame_equal

from . import get_notebook_path
from .. import read_notebooks
from ..models import Scrap, Scraps


class AnyMarkdownWith(Markdown):
    def __eq__(self, other):
        try:
            return self.data == other.data
        except AttributeError:
            return False


@pytest.fixture
def notebook_collection():
    path = get_notebook_path("collection")
    return read_notebooks(path)


def test_assign_from_path(notebook_collection):
    notebook_collection["result_no_exec.ipynb"] = get_notebook_path(
        "result_no_exec.ipynb"
    )


def test_notebook_scraps(notebook_collection):
    assert notebook_collection.notebook_scraps == OrderedDict(
        [
            (
                "result1",
                Scraps(
                    [
                        (
                            "one",
                            Scrap(name="one", data=1, encoder="json", display=None),
                        ),
                        (
                            "number",
                            Scrap(name="number", data=1, encoder="json", display=None),
                        ),
                        (
                            "list",
                            Scrap(
                                name="list",
                                data=[1, 2, 3],
                                encoder="json",
                                display=None,
                            ),
                        ),
                        (
                            "dict",
                            Scrap(
                                name="dict",
                                data={"a": 1, "b": 2},
                                encoder="json",
                                display=None,
                            ),
                        ),
                        (
                            "output",
                            Scrap(
                                name="output",
                                data=None,
                                encoder="display",
                                display={
                                    "data": {"text/plain": "'Hello World!'"},
                                    "metadata": {"papermill": {"name": "output"}},
                                    "output_type": "display_data",
                                },
                            ),
                        ),
                        (
                            "one_only",
                            Scrap(
                                name="one_only",
                                data=None,
                                encoder="display",
                                display={
                                    "data": {"text/plain": "'Just here!'"},
                                    "metadata": {"scrapbook": {"name": "one_only"}},
                                    "output_type": "display_data",
                                },
                            ),
                        ),
                    ]
                ),
            ),
            (
                "result2",
                Scraps(
                    [
                        (
                            "two",
                            Scrap(name="two", data=2, encoder="json", display=None),
                        ),
                        (
                            "number",
                            Scrap(name="number", data=2, encoder="json", display=None),
                        ),
                        (
                            "list",
                            Scrap(
                                name="list",
                                data=[4, 5, 6],
                                encoder="json",
                                display=None,
                            ),
                        ),
                        (
                            "dict",
                            Scrap(
                                name="dict",
                                data={"a": 3, "b": 4},
                                encoder="json",
                                display=None,
                            ),
                        ),
                        (
                            "output",
                            Scrap(
                                name="output",
                                data=None,
                                encoder="display",
                                display={
                                    "data": {"text/plain": "'Hello World 2!'"},
                                    "metadata": {"papermill": {"name": "output"}},
                                    "output_type": "display_data",
                                },
                            ),
                        ),
                        (
                            "two_only",
                            Scrap(
                                name="two_only",
                                data=None,
                                encoder="display",
                                display={
                                    "data": {"text/plain": "'Just here!'"},
                                    "metadata": {"scrapbook": {"name": "two_only"}},
                                    "output_type": "display_data",
                                },
                            ),
                        ),
                    ]
                ),
            ),
        ]
    )


def test_scraps(notebook_collection):
    assert notebook_collection.scraps == Scraps(
        [
            ("one", Scrap(name="one", data=1, encoder="json", display=None)),
            ("number", Scrap(name="number", data=2, encoder="json", display=None)),
            ("list", Scrap(name="list", data=[4, 5, 6], encoder="json", display=None)),
            (
                "dict",
                Scrap(name="dict", data={"a": 3, "b": 4}, encoder="json", display=None),
            ),
            (
                "output",
                Scrap(
                    name="output",
                    data=None,
                    encoder="display",
                    display={
                        "data": {"text/plain": "'Hello World 2!'"},
                        "metadata": {"papermill": {"name": "output"}},
                        "output_type": "display_data",
                    },
                ),
            ),
            (
                "one_only",
                Scrap(
                    name="one_only",
                    data=None,
                    encoder="display",
                    display={
                        "data": {"text/plain": "'Just here!'"},
                        "metadata": {"scrapbook": {"name": "one_only"}},
                        "output_type": "display_data",
                    },
                ),
            ),
            ("two", Scrap(name="two", data=2, encoder="json", display=None)),
            (
                "two_only",
                Scrap(
                    name="two_only",
                    data=None,
                    encoder="display",
                    display={
                        "data": {"text/plain": "'Just here!'"},
                        "metadata": {"scrapbook": {"name": "two_only"}},
                        "output_type": "display_data",
                    },
                ),
            ),
        ]
    )


def test_papermill_metrics(notebook_collection):
    expected_df = pd.DataFrame(
        [
            ("result1.ipynb", "Out [1]", 0.0, "time (s)", "result1"),
            ("result1.ipynb", "Out [2]", 0.123, "time (s)", "result1"),
            ("result2.ipynb", "Out [1]", 0.0, "time (s)", "result2"),
            ("result2.ipynb", "Out [2]", 0.456, "time (s)", "result2"),
        ],
        columns=["filename", "cell", "value", "type", "key"],
    )
    assert_frame_equal(notebook_collection.papermill_metrics, expected_df)


def test_papermill_dataframe(notebook_collection):
    expected_df = pd.DataFrame(
        [
            ("bar", "hello", "parameter", "result1.ipynb", "result1"),
            ("foo", 1, "parameter", "result1.ipynb", "result1"),
            ("dict", {u"a": 1, u"b": 2}, "record", "result1.ipynb", "result1"),
            ("list", [1, 2, 3], "record", "result1.ipynb", "result1"),
            ("number", 1, "record", "result1.ipynb", "result1"),
            ("one", 1, "record", "result1.ipynb", "result1"),
            ("bar", "world", "parameter", "result2.ipynb", "result2"),
            ("foo", 2, "parameter", "result2.ipynb", "result2"),
            ("dict", {u"a": 3, u"b": 4}, "record", "result2.ipynb", "result2"),
            ("list", [4, 5, 6], "record", "result2.ipynb", "result2"),
            ("number", 2, "record", "result2.ipynb", "result2"),
            ("two", 2, "record", "result2.ipynb", "result2"),
        ],
        columns=["name", "value", "type", "filename", "key"],
    )
    assert_frame_equal(notebook_collection.papermill_dataframe, expected_df)


@mock.patch("scrapbook.models.ip_display")
def test_scraps_report(mock_display, notebook_collection):
    notebook_collection.scraps_report()
    mock_display.assert_has_calls(
        [
            mock.call(AnyMarkdownWith("### result1")),
            mock.call(AnyMarkdownWith("#### output")),
            mock.call(
                {u"text/plain": u"'Hello World!'"},
                # We re-translate the metadata from older messages
                metadata={u"scrapbook": {u"name": u"output"}},
                raw=True,
            ),
            mock.call(AnyMarkdownWith("#### one_only")),
            mock.call(
                {u"text/plain": u"'Just here!'"},
                metadata={u"scrapbook": {u"name": u"one_only"}},
                raw=True,
            ),
            mock.call(AnyMarkdownWith("<hr>")),
            mock.call(AnyMarkdownWith("### result2")),
            mock.call(AnyMarkdownWith("#### output")),
            mock.call(
                {u"text/plain": u"'Hello World 2!'"},
                # We re-translate the metadata from older messages
                metadata={u"scrapbook": {u"name": u"output"}},
                raw=True,
            ),
            mock.call(AnyMarkdownWith("#### two_only")),
            mock.call(
                {u"text/plain": u"'Just here!'"},
                metadata={u"scrapbook": {u"name": u"two_only"}},
                raw=True,
            ),
        ]
    )


@mock.patch("scrapbook.models.ip_display")
def test_scraps_report_no_header(mock_display, notebook_collection):
    notebook_collection.scraps_report(header=None)
    mock_display.assert_has_calls(
        [
            mock.call(
                {u"text/plain": u"'Hello World!'"},
                # We re-translate the metadata from older messages
                metadata={u"scrapbook": {u"name": u"output"}},
                raw=True,
            ),
            mock.call(
                {u"text/plain": u"'Just here!'"},
                metadata={"scrapbook": {"name": "one_only"}},
                raw=True,
            ),
            mock.call(
                {u"text/plain": u"'Hello World 2!'"},
                # We re-translate the metadata from older messages
                metadata={u"scrapbook": {u"name": u"output"}},
                raw=True,
            ),
            mock.call(
                {u"text/plain": u"'Just here!'"},
                metadata={u"scrapbook": {u"name": u"two_only"}},
                raw=True,
            ),
        ]
    )


@mock.patch("scrapbook.models.ip_display")
def test_scraps_report_with_scrap_list_names(mock_display, notebook_collection):
    notebook_collection.scraps_report(scrap_names=["output"])
    mock_display.assert_has_calls(
        [
            mock.call(AnyMarkdownWith("### result1")),
            mock.call(AnyMarkdownWith("#### output")),
            mock.call(
                {"text/plain": "'Hello World!'"},
                # We re-translate the metadata from older messages
                metadata={"scrapbook": {"name": "output"}},
                raw=True,
            ),
            mock.call(AnyMarkdownWith("<hr>")),
            mock.call(AnyMarkdownWith("### result2")),
            mock.call(AnyMarkdownWith("#### output")),
            mock.call(
                {"text/plain": "'Hello World 2!'"},
                # We re-translate the metadata from older messages
                metadata={"scrapbook": {"name": "output"}},
                raw=True,
            ),
        ]
    )


@mock.patch("scrapbook.models.ip_display")
def test_scraps_report_with_scrap_string_name(mock_display, notebook_collection):
    notebook_collection.scraps_report(scrap_names="one_only")
    mock_display.assert_has_calls(
        [
            mock.call(AnyMarkdownWith("### result1")),
            mock.call(AnyMarkdownWith("#### one_only")),
            mock.call(
                {"text/plain": "'Just here!'"},
                metadata={"scrapbook": {"name": "one_only"}},
                raw=True,
            ),
            mock.call(AnyMarkdownWith("<hr>")),
            mock.call(AnyMarkdownWith("### result2")),
            mock.call(AnyMarkdownWith("#### one_only")),
            mock.call("No scrap found with name 'one_only' in this notebook"),
        ]
    )


@mock.patch("scrapbook.models.ip_display")
def test_scraps_report_with_notebook_names(mock_display, notebook_collection):
    notebook_collection.scraps_report(notebook_names="result1")
    mock_display.assert_has_calls(
        [
            mock.call(AnyMarkdownWith("### result1")),
            mock.call(AnyMarkdownWith("#### output")),
            mock.call(
                {u"text/plain": u"'Hello World!'"},
                # We re-translate the metadata from older messages
                metadata={u"scrapbook": {u"name": u"output"}},
                raw=True,
            ),
            mock.call(AnyMarkdownWith("#### one_only")),
            mock.call(
                {u"text/plain": u"'Just here!'"},
                metadata={u"scrapbook": {u"name": u"one_only"}},
                raw=True,
            ),
        ]
    )


@mock.patch("scrapbook.models.ip_display")
def test_scraps_report_with_scrap_and_notebook_names(mock_display, notebook_collection):
    notebook_collection.scraps_report(
        scrap_names=["output"], notebook_names=["result1"]
    )
    mock_display.assert_has_calls(
        [
            mock.call(AnyMarkdownWith("### result1")),
            mock.call(AnyMarkdownWith("#### output")),
            mock.call(
                {u"text/plain": u"'Hello World!'"},
                # We re-translate the metadata from older messages
                metadata={u"scrapbook": {u"name": u"output"}},
                raw=True,
            ),
        ]
    )
