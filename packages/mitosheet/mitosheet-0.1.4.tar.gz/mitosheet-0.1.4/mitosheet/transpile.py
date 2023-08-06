#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Exports the transpile function, which takes a list of edit events
make to a Mito sheet and generates a resulting code string. 
"""

def transpile(edit_event_list):
    return f"Code string {len(edit_event_list)}"