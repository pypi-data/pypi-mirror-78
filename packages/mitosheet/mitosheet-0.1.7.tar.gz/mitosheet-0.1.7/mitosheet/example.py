#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget
from traitlets import Unicode, List
from ._frontend import module_name, module_version
from .evaluate import evaluate
from .transpile import transpile
import json

def sheet(df=None):
    return ExampleWidget(df=df)

def df_to_json(df=None):
    if df is None:
        return '{}'
    return df.to_json(orient="split")


class ExampleWidget(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('ExampleModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('ExampleView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    value = Unicode('Hello World').tag(sync=True)
    sheet_json = Unicode('').tag(sync=True)
    code_json = Unicode('').tag(sync=True)
    edit_event_list = List()

    def __init__(self, *args, **kwargs):
        # Call the DOMWidget constructor to set up the widget properly
        super(ExampleWidget, self).__init__(*args, **kwargs)
        self.df = kwargs['df']
        self.sheet_json = df_to_json(kwargs['df'])
        self.code_json = json.dumps({
            "data": "This is code"
        })
        self.code_change = 1
        self.on_msg(self.receive_message)

    def receive_message(self, widget, content, buffers=None):
        self.edit_event_list.append(content)

        # First, we send this new edit to the evaluator
        # TODO
        new_sheet = evaluate(self.df, self.edit_event_list)
        self.send({
            "type": "update_sheet"
        })

        # Then, we send these edits to the transpiler
        new_code = transpile(self.edit_event_list)
        # update the code 
        self.code_json = json.dumps({
            "code": new_code
        })
        # tell the front-end to render the new code
        self.send({
            "type": "update_code"
        })

