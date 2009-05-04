"""
Functions to work with Eclipse .project files represented as BeautifulSoup.
"""

from BeautifulSoup import Tag, NavigableString

FILE_RESOURCE_TYPE = '1'
DIR_RESOURCE_TYPE = '2'

def get_resource_type(is_dir):
    return (is_dir and DIR_RESOURCE_TYPE) or FILE_RESOURCE_TYPE

def add_linked_resources(soup, links):
    """
    Add linked resources.
    
    Arguments:
    soup -- A BeatifulSoup object.
    links -- A dict mapping from link names to (path, is_dir) tuples.
    """
    projectdescription = soup.projectdescription
    
    linkedresources = projectdescription.find(
        name='linkedresources', 
        recursive=False
    )    
    if not linkedresources:
        linkedresources = Tag(soup, 'linkedresources')
        projectdescription.insert(0, linkedresources)
    
    # Remove existing links.
    existing_links = linkedresources(name='link', recursive=False)
    for l in existing_links:
        l.extract()
    
    # Add the links.
    for (name, (path, is_dir))  in links.iteritems():
        link_tag = Tag(soup, name='link')
        
        name_tag = Tag(soup, 'name')
        name_tag.insert(0, NavigableString(name))
        
        location_tag = Tag(soup, 'location')
        location_tag.insert(0, NavigableString(path))
        
        type_tag = Tag(soup, 'type')
        type_tag.insert(0, NavigableString(get_resource_type(is_dir)))
        
        
        link_tag.insert(0, name_tag)
        link_tag.insert(1, location_tag)
        link_tag.insert(2, type_tag)
        linkedresources.insert(0, link_tag)
    
def remove_existing_linked_resources(soup):    
    """Remove all existing linked resources."""
    projectdescription = soup.projectdescription
    
    linkedresources = projectdescription.find(
        name='linkedresources', 
        recursive=False
    )    
    if not linkedresources:
        return
    
    # Remove existing links.
    existing_links = linkedresources(name='link', recursive=False)
    for l in existing_links:
        l.extract()    

def set_project_name(soup, project_name):
    """Set the project name."""
    soup.projectdescription.nameTag.contents[0].replaceWith(project_name)    