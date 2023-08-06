# Contributing to JupyXML

You can contribute to JupyXML! 
Even if you can't code that well, improvements can be made to lots of areas.

## Help wanted

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


## TODO List

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


## Supporting the project

I'm more than happy for people to sponsor the project or send me money, however that isn't required.
If you'd rather, give the money to a local hackerspace, library or open source community.
