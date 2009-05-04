"""DOM utilities."""
        
def get_element_text(element):
    """
    Return: the text inside the element. Example: for <mytag>blah</mytag> return
        'blah'.
    """
    return element.firstChild.nodeValue        

def create_element(document, parent, name):
    """
    Create a new element inside the `parent` element with the given `name`.
    """    
    element = document.createElement(name)
    parent.appendChild(element)
    return element
    
def create_text_element(document, parent, text):
    """
    Create a new text element inside the `parent` element with the given `text`.
    """
    parent.appendChild(document.createTextNode(text))

def create_element_with_text(document, parent, name, text):
    """
    Create a new element inside the `parent` element and create a text element
    inside it with the given `text`. 
    
    Example: create_element_with_text(document, parent, 'newelement', 'blah')
        Will create the element <newelement>blah</newelement> inside the 
        `parent` element.
    """
    
    element = create_element(document, parent, name)
    create_text_element(document, element, text)

def get_unique_element_by_tag_name(
    document,
    parent, 
    name,
    create_if_not_exist=True, 
    raise_if_not_exist=False):
    """
    Get the unique element inside `element` with the given `name`.
    
    Arguments:
    document -- A DOM Document.
    parent -- The parent element object.
    name -- The element unique name.
    create_if_not_exist -- Create the element if it does not exist.
    raise_if_not_exist -- Raise an exception if the element does not exist.
    
    Raise: ValueError if the element is not unique.
    """
    
    elements = parent.getElementsByTagName(name)
    if not elements:
        if raise_if_not_exist:
            raise ValueError('Element %s does not exist.' % name)        
        if create_if_not_exist:
            return create_element(document, parent, name)        
    
    if len(elements) != 1:
        raise ValueError('Element %s is not unique.' % name)
    
    return elements[0]     

def write_document_to_file(document, filename):
    """Write a DOM document to a file, creating it if needed."""    
    f = open(filename, 'w')
    f.write(document.toprettyxml())
    f.close()