

def test_basic_parsing_string_input():
    from jupyxml import JupyXML

    obj = JupyXML("<b>Hello world</b>")

    html = obj._repr_html_()
    assert isinstance(html, str)
