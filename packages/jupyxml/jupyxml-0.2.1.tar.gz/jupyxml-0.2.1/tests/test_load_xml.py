import os

from testfixtures import tempdir

# TODO: It would be nice if these templates were extra datafiles
simple_xml_file = """<?xml version="1.0" encoding="utf-8" ?>
<a>
    <b>Child 0</b>
    <b>Child 1</b>
    <b>
        Child 3
        <c>Grandchild 3.0</c>
    </b>
</a>
"""


@tempdir()
def test_load_xml_file(dir):
    temp_filename = "simple_test.xml"
    dir.write(temp_filename, simple_xml_file.encode())
    from jupyxml import JupyXML

    representation_obj = JupyXML(os.path.join(dir.path, temp_filename))
    representation = representation_obj._repr_html_()
    assert isinstance(representation, str)
