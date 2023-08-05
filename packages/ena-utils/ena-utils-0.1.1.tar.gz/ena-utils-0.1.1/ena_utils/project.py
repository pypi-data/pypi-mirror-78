import os
import sys
import collections
import pandas as pd
from xmltodict import unparse
from re import sub

class Project(object):
    """A project."""

    def __init__(self, alias, title, description, **kwargs):
        """Create a project."""
        self.dict = collections.OrderedDict({'PROJECT':{
            '@alias':str(alias),
            'TITLE':str(title),
            'DESCRIPTION':str(description),
            'SUBMISSION_PROJECT':{'SEQUENCING_PROJECT':{}}
        }})
        self.xml = unparse(self.dict, pretty = True)

class ProjectSet(object):
    """A project set."""

    def __init__(self, project, **kwargs):
        """Create a project set.
           Projects are added using the 'project' argument
           
           Args:
                project:    - An object of class Project
                            - A list of object of class Project
                            - The file path of a tab-delimited text table,
                              each row representing an obkect of class Project
                              with its arguments described in columns.
                              The first row must contain columns headers.
        """

        self.dict = collections.OrderedDict({'PROJECT_SET':{}})
        # If a single object of class Project is specified
        if isinstance(project, Project):
            self.project_list = [project]
        # If a list of objects of class Projects are specified
        elif isinstance(project, list) and all(isinstance(x, Project) for x in project):
            self.project_list = project
        # If a text table of projects is specified
        elif isinstance(project, str):
            try:
                # Edit default columns names if specified in kwargs
                colnames = {'alias':'alias', 'title':'title', 'description':'description'}
                for k in colnames.keys():
                    if k in kwargs.keys():
                        colnames[k] = kwargs[k]
                self.project_list = []
                for i, row in pd.read_table(project).iterrows():
                    # Retrieve the project details from table using columns names
                    args = {}
                    for key, value in colnames.items():
                        args[key] = dict(row)[value]
                    self.project_list.append(Project(**args))
            except Exception as e:
                print('Error: ' + str(e))
                raise
        else:
            raise ValueError('project is of wrong type')
        # Create a dict that follows the structure of the ENA XML file
        for i, e in enumerate(self.project_list):
            # Unlike in XML, each key must be unique
            e.dict['PROJECT_unique_key_' + str(i)] = e.dict.pop('PROJECT')
            self.dict['PROJECT_SET'].update(e.dict)
        # Convert the dict to XML
        self.xml = sub('PROJECT_unique_key_[0-9]*',
                'PROJECT',
                unparse(self.dict, pretty = True))
    
    def write_xml(self, file):
        """Write the XML file."""
        with open(file, 'w') as f:
            f.write(self.xml)

def write_table_template(file):
    """Write a template table."""

    data = {'alias': ['study01', 'study02'],
        'title': ['My study 1 title.', 'My study 2 title.'],
        'description': ['My study 1 description.', 'My study 2 description.']
        }
    pd.DataFrame(data,
        columns = ['alias', 'title', 'description']
        ).to_csv(file, sep = '\t', index =  False)
