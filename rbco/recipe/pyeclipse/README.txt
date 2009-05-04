rbco.recipe.pyeclipse
=====================

.. contents::

Overview
--------

This recipe creates a Pydev_ project for Eclipse. The goal is to automate
the following strategy:

1. Create a Pydev project. The project directory is separated from the
   source code directories. In other words, the source code will not reside
   inside the project directory.
2. Create links to the source code directories. This is done by right-clicking 
   the project in the Pydev Package Explorer and selection New->Folder. Then
   click Advanced and choose "Link to folder in the filesystem."
3. Add the linked directories to the PYTHONPATH of the project.   

This approach works very well when working with Zope/Plone, specially if
combined with `collective.recipe.omelette`_, as pointed in `this article`__
by Martin Aspeli.

__ `Eclipse, PyDev and Buildout`_

However it should be flexible enough to allow other strategies.


Supported options
-----------------

The recipe supports the following options:

project-name
    The project name.

python-version
    The Python version for syntatical analysis, sucha as 2.4 or 2.5.
    
python-interpreter
    Optional. The path to the Python interpreter. Defaults to the default
    interpreter configured in Eclipse.
    
project-directory
    The directory where the project configuration files will be stored.
    
source-resources
    A set of paths separated by space or newline. These will be added as
    linked directories (or files) and will be in the PYTHONPATH.
    
extra-linked-resources
    A set of paths separated by space or newline. These will be added as
    linked directories (or files) only.
                
extra-pythonpath-resources
    A set of paths separated by space or newline. These will be added only
    to the PYTHONPATH.

.. TODO: write about replace policy.

Example usage
-------------

Setup::

    >>> from os.path import join
    >>> egg_zip_filename = 'some.egg.zip'
    >>> src_dirname = 'my.python.package'       
    >>>
    >>> test_dir = tmpdir('testdir')
    >>>      
    >>> mkdir(test_dir, src_dirname)  
    >>> src_dir = join(test_dir, src_dirname)
    >>>
    >>> write(test_dir, egg_zip_filename, 'foo')    
    >>> egg_zip_file = join(test_dir, egg_zip_filename)

We'll start by creating a typical buildout that uses the recipe::

    >>> write('buildout.cfg',
    ... """
    ... [buildout]
    ... parts = eclipse_project
    ...
    ... [eclipse_project]
    ... recipe = rbco.recipe.pyeclipse
    ... project-name = TestProject
    ... python-version = 2.4
    ... project-directory = ${buildout:directory}/testproject 
    ... source-resources = 
    ...     %(src_dir)s
    ...     %(egg_zip_file)s
    ... """ % locals())
    
    >>> #cat('buildout.cfg')
    
Note that we added two source resources: a directory and a zipped egg.    
    
Running the buildout gives us::

    >>> print 'start', system(buildout)    
    start...
    Installing eclipse_project.
    <BLANKLINE>

The project directory is created if it does not exist and so happens to the
.project and .pydevproject files. The .project file will look like this::

    >>> cat(join(sample_buildout, 'testproject', '.project'))
    <?xml version='1.0' encoding='utf-8'?>
    <projectDescription>
     <name>
      TestProject
     </name>
     ...
     <buildspec>
      <buildcommand>
       <name>
        org.python.pydev.PyDevBuilder
       </name>
       <arguments>
       </arguments>
      </buildcommand>
     </buildspec>
     <natures>
      <nature>
       org.python.pydev.pythonNature
      </nature>
     </natures>
     <linkedResources>
     ...
     </linkedResources>     
    </projectDescription>

Let's look into the ``<linkedResources>`` tag. The paths listed in the 
``source-resources`` section must be listed there::

    >>> cat(join(sample_buildout, 'testproject', '.project'))
    <?xml...
    <linkedResources>...
      <link>
        <name>...my.python.package...</name>
        <location>...testdir/my.python.package...</location>      
        <type>... 2 ...</type>
      </link>...      
    </linkedResources>...
    
The egg zip file is present too::

    >>> cat(join(sample_buildout, 'testproject', '.project'))
    <?xml...
    <linkedResources>...
      <link>
        <name>...some.egg.zip...</name>
        <location>...testdir/some.egg.zip...</location>      
        <type>... 1 ...</type>
      </link>...      
    </linkedResources>...
    
References
----------

.. _Pydev: http://pydev.sourceforge.net/
.. _Eclipse, PyDev and Buildout: http://www.martinaspeli.net/articles/eclipse-pydev-and-buildout
.. _collective.recipe.omelette: http://pypi.python.org/pypi/collective.recipe.omelette

.. target-notes:: 
