# -*- coding: utf-8 -*-

__author__ = "Robert Layton"
__copyright__ = "Robert Layton"
__license__ = "mit"


def test_import():
    """Simple test that the library actually imports at all"""
    import src.jupyxml
    assert src.jupyxml.__version__

    from src.jupyxml.visualiser import JupyXML
    from src.jupyxml import JupyXML
