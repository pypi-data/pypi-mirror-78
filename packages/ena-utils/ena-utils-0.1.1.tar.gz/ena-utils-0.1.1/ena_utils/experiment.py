import os
import sys
import collections
import pandas as pd
from xmltodict import unparse
from re import sub

class Experiment(object):
    """An experiment."""

    def __init__(self, study, sample, alias, center, title, design,
        lib_name, lib_strategy, lib_source, lib_selection, lib_length,
        lib_protocol, instrument, **kwargs):
        """Create an experiment."""
        self.dict = collections.OrderedDict({'EXPERIMENT':{
            '@alias':str(alias),
            'TITLE':str(title),
            'STUDY_REF':{'@accession':str(study)},
            'DESIGN':{
                'DESIGN_DESCRIPTION':str(design),
                'SAMPLE_DESCRIPTOR':{'@refname':str(sample)},
                'LIBRARY_DESCRIPTOR':{
                    'LIBRARY_NAME':str(lib_name),
                    'LIBRARY_STRATEGY':str(lib_strategy),
                    'LIBRARY_SOURCE':str(lib_source),
                    'LIBRARY_SELECTION':str(lib_selection),
                    'LIBRARY_LAYOUT':{'PAIRED':{'@NOMINAL_LENGTH':str(lib_length)}},
                    'LIBRARY_CONSTRUCTION_PROTOCOL':str(lib_protocol)
                }
            },
            'PLATFORM':{
                'ILLUMINA':{
                    'INSTRUMENT_MODEL':str(instrument)
                    }
            }
            }
            })
        self.xml = unparse(self.dict, pretty = True)

class ExperimentSet(object):
    """An experiment set."""

    def __init__(self, experiment, **kwargs):
        """Create an experiment set.
           Experiments are added using the 'experiment' argument
           
           Args:
                experiment: - An object of class Experiment
                            - A list of object of class Experiment
                            - The file path of a tab-delimited text table,
                              each row representing an object of class Experiment
                              with its arguments described in columns.
                              The first row must contain columns headers.
        """

        self.dict = collections.OrderedDict({'EXPERIMENT_SET':{}})
        # If a single object of class Experiment is specified
        if isinstance(experiment, Experiment):
            self.experiment_list = [experiment]
        # If a list of objects of class Experiment is specified
        elif isinstance(experiment, list) and all(isinstance(x, Experiment) for x in experiment):
            self.experiment_list = experiment
        # If a text table of experiments is specified
        elif isinstance(experiment, str):
            try:
                # Edit default columns names if specified in kwargs
                colnames = {'study':'study', 'sample':'sample', 'alias':'alias', 'center':'center',
                    'title':'title', 'design':'design', 'lib_name':'lib_name',
                    'lib_strategy':'lib_strategy', 'lib_source':'lib_source', 'lib_selection':'lib_selection',
                    'lib_length':'lib_length', 'lib_protocol':'lib_protocol', 'instrument':'instrument'}
                for k in colnames.keys():
                    if k in kwargs.keys():
                        colnames[k] = kwargs[k]
                self.experiment_list = []
                for i, row in pd.read_table(experiment).iterrows():
                    # Retrieve the experiment details from table using columns names
                    args = {}
                    for key, value in colnames.items():
                        args[key] = dict(row)[value]
                    self.experiment_list.append(Experiment(**args))
            except Exception as e:
                print('Error: ' + str(e))
                raise
        else:
            raise ValueError('experiment is of wrong type')
        # Create a dict that follows the structure of the ENA XML file
        for i, e in enumerate(self.experiment_list):
            # Unlike in XML, each key must be unique
            e.dict['EXPERIMENT_unique_key_' + str(i)] = e.dict.pop('EXPERIMENT')
            self.dict['EXPERIMENT_SET'].update(e.dict)
        # Convert the dict to XML
        self.xml = sub('EXPERIMENT_unique_key_[0-9]*',
                'EXPERIMENT',
                unparse(self.dict, pretty = True))
    
    def write_xml(self, file):
        """Write the XML file."""
        with open(file, 'w') as f:
            f.write(self.xml)

def write_table_template(file):
    """Write a template table."""

    data = {'study': ['study_accession_number (ex: PRJEB12345)', 'study_accession_number (ex: PRJEB12345)'],
        'sample': ['sample01', 'sample02'],
        'alias': ['exp01', 'exp02'],
        'center': ['My research center', 'My research center'],
        'title': ['Experiment 1 title.', 'Experiment 2 title.'],
        'design': ['Bacterial 16S rRNA gene v1-v2 region (F27-R338)', 'bacterial 16S rRNA gene v1-v2 region (F27-R338)'],
        'lib_name': ['LIB01', 'LIB02'],
        'lib_strategy': ['AMPLICON', 'AMPLICON'],
        'lib_source': ['METAGENOMIC', 'METAGENOMIC'],
        'lib_selection': ['PCR', 'PCR'],
        'lib_length': ['311', '311'],
        'lib_protocol': ['The library was constructed as described in doi: XXX.', 'The library was constructed as described in doi: XXX.'],
        'instrument': ['Illumina MiSeq', 'Illumina MiSeq']
        }
    pd.DataFrame(data,
        columns = ['study', 'sample', 'alias', 'center', 'title', 'design',
        'lib_name', 'lib_strategy', 'lib_source', 'lib_selection', 'lib_length',
        'lib_protocol', 'instrument']
        ).to_csv(file, sep = '\t', index =  False)