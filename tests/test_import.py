import pytest


def test_import_package():
    import importlib
    mod = importlib.import_module('ai_content_gen')
    assert mod is not None

