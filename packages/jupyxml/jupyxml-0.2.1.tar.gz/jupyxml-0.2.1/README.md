![logo](jupyxml_logo.png)

JupyXML is a small library designed to allow you to easily read an XML file and display it in Jupyter Notebooks.

If you've ever used pandas in Jupyter Notebooks, like how it prints out a nice HTML table, but have to work with an XML file, this project is for you!

Description
===========

The scope of this project is to:
- Read an XML file with `lxml`
- Display the XMl file as HTML with collapse options
- Use an interactive widget to search/filter the nodes based on some criteria.


Bugs
====

If you spot any bugs or use cases that don't work, please let me know!
This project currently lives at https://gitlab.com/robertlayton/jupyxml

If you are presenting a bug, please do the following:
- Update your version of `jupyxml` to the latest version, or create a new environment and test your code with the latest - your bug may already be fixed!
- Reduce your example code to the bare minimum, preferably one or two lines of code and a 10 line XML files at most, but this obviously depends on your bug!
- Explain clearly what you were expecting the code to do. Its not always obvious, and if the code 'runs for me', I might not see why its 'not working'
- Be patient! This is a volunteer project, by one person, who has plenty of other stuff to do.

I also *actually don't know XML that well*.
I wrote this library with the expectation that the `lxml` library *does* know XML, and to just leverage off that.
For that reason, please keep the language non-technical, especially on the XML side.
I know *of* things like SOAP, schemas and so on, but don't really do much with them.

Help wanted
===========

Please feel free to suggest improvements to the library. This doesn't need to be code!

Things that can always be improved are:
- Improving the documentation
- Adding clear, focused examples of the usage of the library
- Testing the code on different versions of python and different versions of libraries, and fixing the code to work as generally as possible.

Things that I'm not good at and could use some help
- Styling the output of the XML. It is currently blocky and wastes space.
- Parsing more advanced XML, for instance with XSD schemas, validation, etc (it would be nice if this type of thing was shown in the output)


Ultimately I'd like to keep the scope of this library small and focused.
For that reason, pull requests that drastically increase the scope of this project are likely not to be accepted.
If you do have a great reason to extend this, please bring up a feature request before you put lots of work into
integrating it.
If it is a drastic increase in scope, consider creating a new library that uses jupyxml, rather than adding your
features to jupyxml.


Features I'd like to see, that deviate from the scope listed above:
- Ability to change the XMl parsing engine. Use `lxml` by default, but be able to pass another module in and use that
- Ability to extract a specific node as a Pandas DataFrame


TODO
====

Here is the planned list of features:
- Documentation (its currently just the default)
- Add ability to "collapse/show all"
- Add ability to "collapse/show all" within a given element
- Ability to export any element as a string
- Fancy formatting of element's attributes (currently its just printing out the dict)
- Ability to set your own css
- Ability to set your own HTML template
- More minimalist view that doesn't waste as much space
- Better styling of everything
- Search / Filter boxes
- Test data as separate files, rather than embedded in the test py files
- If an elements children do not have children of their own, just show them, not as a collapsible item

Features I'm considering adding but aren't sure if I will:
- Export "tables" as pandas. i.e. if there is an element that has a bunch of similar elements in it, convert to pandas


Additional items are marked with a comment with `TODO`, throughout the code.
These are things that are nice to haves, but weren't important at the time (i.e I was working on something else).


Uploading to PyPI
=================

1. Commit all changes and tag the current commit. This must be done, as PyPI doesn't allow "dirty" or "local" versions
1. Tag the current commit with `git tag 0.3`  (replace 0.3 with the version of the software)
1. Push tags with `git push --tags`
2. Delete everything in `dist/` you don't want to upload (you could also specify just the one filename in the next step if you don't want to delete things in here).
3. Run `python setup.py sdist` and `python setup.py bdist_wheel`
4. Run `python -m twine upload dist/*`
5. Username is `__token__`
6. Password is the API key you get from PyPI

If you don't want to enter your token everytime, setup a [.pypirc file](https://packaging.python.org/guides/distributing-packages-using-setuptools/#create-an-account)


Supporting the project
======================

I'm more than happy for people to sponsor the project or send me money, however that isn't required.
If you'd rather, give the money to a local hackerspace, library or open source community.


Note
====

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
