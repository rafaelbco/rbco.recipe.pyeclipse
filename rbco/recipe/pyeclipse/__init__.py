"""Recipe pyeclipse"""
import os
from data import DEFAULT_DOT_PROJECT_XML, DEFAULT_DOT_PYDEVPROJECT_XML
from fileutil import create_dir_if_not_exist, create_file_if_not_exist
import eclipseproj
import pydevproj
from BeautifulSoup import BeautifulSoup
import re

# Do not generate link tags as <link /> ... In fact we're not dealing with HTML,
# we are using XML.
BeautifulSoup.SELF_CLOSING_TAGS = {}

def format_tag(match):
    return '<%(tag)s>%(content)s</%(tag)s>' % match.groupdict()
    
def format_xml(xml):
    pattern = r'<(?P<tag>\S+)>\s*(?P<content>[A-z0-9/_\-\.]+)\s*</(?P=tag)>'
    return re.sub(pattern, format_tag, xml)


def modify_xml(filename, modifier):
    """
    Open a file, parse it generating a DOM document object, call 
    `modifier(dom)` and write `dom` back to the file.
    """
    f = open(filename)
    soup = BeautifulSoup(f)
    f.close()
        
    modifier(soup)
    xml = format_xml(soup.prettify())
    xml = (xml
        .replace('projectdescription', 'projectDescription')
        .replace('linkedresources', 'linkedResources')
    )
    
    f = open(filename, 'w')
    f.write(xml)
    f.close()


def create_or_modify_xml(filename, modifier, initial_xml):
    """
    Same as `modify_xml()` but create the file if it does not exist. 
    The contents of the newly created file is given in `initial_xml`. This
    content is written to the file before modifying the file with `modifier`.
    
    `initial_xml` is an string containing the initial XML to be inserted
    into the file, before modifying it.
    """    
    create_file_if_not_exist(filename, initial_xml)
    modify_xml(filename, modifier)

def build_path_dict(paths_str):
    """
    Given an string containing paths separated by space chars return a dict
    link this: {basename(p): (p, isdir(p))} for each path p in the string. 
    """
    return dict(
        (os.path.basename(path), (path, os.path.isdir(path)))
        for path in paths_str.split()
    )
    

class Recipe(object):
    """zc.buildout recipe"""

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name        
        
        self.project_name = options['project-name']
        self.python_version = options['python-version']
        self.python_interpreter = options.get('python-interpreter', 'Default')
        
        self.project_directory_path = options['project-directory']
        self.dot_project_path = os.path.join(
            self.project_directory_path, 
            '.project'
        )
        self.dot_pydevproject_path = os.path.join(
            self.project_directory_path, 
            '.pydevproject'            
        ) 
        
        source_resources = build_path_dict(
            options.get('source-resources', '')
        )                
        extra_linked_resources = build_path_dict(
            options.get('extra-linked-resources', '')
        )
        
        self.linked_resources = {}
        self.linked_resources.update(source_resources)
        self.linked_resources.update(extra_linked_resources)
        
        self.pythonpath_resources = [
            os.path.join('/', self.project_name, name) 
            for name in source_resources.iterkeys()
        ] 
                
        self.external_pythonpath_resources = \
            options.get('extra-pythonpath-resources', '').split()
    
    def install(self):
        """Installer"""
        create_dir_if_not_exist(self.project_directory_path)

        create_or_modify_xml(
            self.dot_project_path, 
            self.setup_eclipse_project,
            DEFAULT_DOT_PROJECT_XML
        )        
        
        create_or_modify_xml(
            self.dot_pydevproject_path, 
            self.setup_pydev_project,
            DEFAULT_DOT_PYDEVPROJECT_XML
        )         
        
        # We don't want to buildout to remove any files, so we return an empty 
        # sequence.
        return tuple()
    
    def setup_eclipse_project(self, soup):
        """Modify a BeautifulSoup representing a .project file."""        
        eclipseproj.set_project_name(soup, self.project_name)
             
        eclipseproj.remove_existing_linked_resources(soup)
        eclipseproj.add_linked_resources(soup, self.linked_resources)
        
            
    def setup_pydev_project(self, soup):
        """Modify a BeautifulSoup representing a .pydevproject file"""
        pydevproj.set_project_properties(
            soup, 
            python_version=self.python_version, 
            python_interpreter=self.python_interpreter
        )
                  
        pydevproj.remove_existing_pythonpath_resources(soup, False)
        pydevproj.add_pythonpath_resources(
            soup, 
            self.pythonpath_resources, 
            False
        )

        pydevproj.remove_existing_pythonpath_resources(soup, True)
        pydevproj.add_pythonpath_resources(
            soup, 
            self.external_pythonpath_resources,
            True
        )

                    
    update = install
