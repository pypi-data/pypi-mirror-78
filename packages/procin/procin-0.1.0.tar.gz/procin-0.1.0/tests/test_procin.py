#!/usr/bin/env python

"""Tests for `procin` package."""

import pytest
import procin
import json

wierd_string = 'ä'
def test_filename():
    c = procin.Command()
    command = [wierd_string]
    s = c.command_to_filename(command)
    assert c.filename_to_command(s) == command
    command = ["echo", "-n", "[]"]
    s = c.command_to_filename(command)
    print(s)
    assert s == "echo^n-n^n^l^r^n"
    assert c.filename_to_command(s) == command
    print(command)

def test_array():
    c = procin.Command()
    ab = c.run_json(["echo", "-n", "[]"])
    assert ab == []
    ab = c.run_json(["echo", "[]"])
    assert ab == []
    ab = c.run_json(["/bin/echo", f'{{"v": "{wierd_string}"}}'])
    assert ab["v"] == wierd_string

def test_cache(tmpdir):
    c = procin.Command(cache=True, cache_dir=tmpdir)
    command = ["/bin/echo", "-n", '{"h": "hello"}']
    assert c.in_cache(command) == None
    j = c.run_json(command)
    assert j["h"] == "hello"
    s = c.in_cache(command)
    js = json.loads(s)
    assert j == js
    assert j == c.run_json(command)

def test_array2():
    c = procin.Command()