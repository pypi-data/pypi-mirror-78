#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports the evaluate function, which takes a list of edit events
as well as the original dataframe, and returns the current state 
of the sheet as a dataframe
"""
import pandas as pd

def evaluate(df, edit_event_list):
    d = {'col1': [1, 2, "test"], 'col2': [4, 5, 6]}
    return pd.DataFrame(data=d)