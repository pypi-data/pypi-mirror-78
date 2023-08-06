from lxml import etree

accordion_element = """
<div class="card">
    <div class="card-header" id="{heading_identifier}">
        <button class="btn btn-link" data-toggle="collapse" data-target="#{collapse_identifier}" 
            aria-expanded="true" aria-controls="{collapse_identifier}">
          <h3>
              {heading}
          </h3>
        </button>
    </div>
    
    <div id="{collapse_identifier}" class="collapse {do_show}" aria-labelledby="{heading_identifier}" >
      <div class="card-body">
        {contents}
      </div>
    </div>
</div>
"""

flat_element = """
<div class="leaf_node">
    <h3>{heading}</h3>
    {contents}
</div>
"""


def create_recursive_accordian_html(current_node: etree.ElementTree, root_identifier: str, max_depth: int = 10,
                                    current_depth: int = 0, show_expanded: bool = False, text_limit: int = 500) -> str:
    """ Converts the current node to HTML, including recursively calling itself for each child node.
    
    Args:
        current_node: etree.ElementTree
            The element to be converted into html
        root_identifier: str
            a globally unique identifier for this element. Children will be identified by this + "_" + child's ID
        max_depth: int, default 10
            The maximum depth of children that we will traverse, from the root node
        current_depth: int, default 0
            The current depth of this element.
        show_expanded: bool, default False
            If True, the accordion element is shown. If False (default) it is collapsed
        text_limit:
            The maximum number of characters to show for the text of a given element

    Returns:
        A string containing HTML that represents the current_node.

    """
    heading_identifier = f"heading_{root_identifier}"
    collapse_identifier = f"collapse_{root_identifier}"
    heading = f"Item: {current_node.tag}"
    do_show = show_expanded

    contents = ""
    if len(current_node.attrib):
        contents += f"Attributes: {current_node.attrib}<br>"
    contents += f"Text: {current_node.text[:text_limit]}"
    # TODO There is no test for when we reach the max depth
    # TODO There is no test that the text limit works, or that it is applied to child nodes
    # TODO There is no tests that the show_expanded option actually does anything
    if current_depth <= max_depth:
        contents += str.join("\n",
                             [create_recursive_accordian_html(child, root_identifier=f"{root_identifier}_{child_id}",
                                                              max_depth=max_depth, current_depth=current_depth + 1,
                                                              show_expanded=(child_id == 0),
                                                              text_limit=text_limit)
                              for child_id, child in enumerate(current_node)])
    if len(current_node):
        return accordion_element.format(**locals())
    else:
        return flat_element.format(**locals())
