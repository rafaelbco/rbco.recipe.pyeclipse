"""
Functions to work with Pydev .pydevproject files represented a BeautifulSoup.
"""

from BeautifulSoup import Tag, NavigableString

def get_pydev_pathproperty_tag_name_attr(is_external):
    return (
        (is_external and 'org.python.pydev.PROJECT_EXTERNAL_SOURCE_PATH')
        or 'org.python.pydev.PROJECT_SOURCE_PATH'
    )
    

def get_pydev_pathproperty_tag(pydev_project_tag, is_external=False):        
    return pydev_project_tag.find(
        name='pydev_pathproperty', 
        attrs={'name': get_pydev_pathproperty_tag_name_attr(is_external)},
        recursive=False
    )    

def add_pythonpath_resources(soup, paths, is_external=False):
    """
    Add paths to the PYTHONPATH.
    
    Arguments:
    soup -- A BeatifulSoup object.
    paths -- A sequence of paths.
    """
    pydev_project = soup.pydev_project
    pydev_pathproperty = get_pydev_pathproperty_tag(pydev_project, is_external)

    if not pydev_pathproperty:
        pydev_pathproperty = Tag(soup, 'pydev_pathproperty')
        pydev_pathproperty['name'] = \
            get_pydev_pathproperty_tag_name_attr(is_external)
        pydev_project.insert(0, pydev_pathproperty)    
                                
    # Add new links.
    for p in paths:
        path_tag = Tag(soup, 'path')
        path_tag.insert(0, p)
        pydev_pathproperty.insert(0, path_tag)

def remove_existing_pythonpath_resources(soup, is_external=False):
    """Remove all existing paths from the PYTHONPATH."""

    pydev_project = soup.pydev_project
    pydev_pathproperty = get_pydev_pathproperty_tag(pydev_project, is_external)
    if not pydev_pathproperty:
        return
    
    paths = pydev_pathproperty.findAll(name='path')
    for p in paths:
        p.extract()

def get_property_tag(pydev_project_tag, property_name):
    return pydev_project_tag.find(
        'pydev_property', 
        attrs={'name': property_name}
    )    

def set_property_tag(pydev_project_tag, property_name, value):
    tag = get_property_tag(pydev_project_tag, property_name)
    tag.contents[0].replaceWith(value)
        
def set_project_properties(soup, python_version=None, python_interpreter=None):
    pydev_project_tag = soup.pydev_project
    
    if python_version:
        set_property_tag(
            pydev_project_tag, 
            'org.python.pydev.PYTHON_PROJECT_VERSION', 
            'python ' + python_version
        )

    if python_interpreter:
        set_property_tag(
            pydev_project_tag, 
            'org.python.pydev.PYTHON_PROJECT_INTERPRETER', 
            python_interpreter
        )
