import os
import sys
import collections
import hashlib
import pandas as pd
from xmltodict import unparse
from re import sub

class Run(object):
    """A run."""

    def __init__(self, experiment, alias, center, filename, filetype, **kwargs):
        """Create a run."""
        self.dict = collections.OrderedDict({'RUN':{
            '@alias':str(alias),
            'EXPERIMENT_REF':{'@refname':str(experiment)},
            'DATA_BLOCK':{
                'FILES':{}
            }
        }})
        for i, fn in enumerate(filename.split(',')):
            with open(fn, 'rb') as f:
                checksum = hashlib.md5(f.read()).hexdigest()
            self.dict['RUN']['DATA_BLOCK']['FILES'].update(
                {'FILE_unique_key_' + str(i):{
                    '@filename':os.path.basename(fn),
                    '@filetype':filetype.split(',')[i],
                    '@checksum_method':"MD5",
                    '@checksum':checksum
                }})
        self.xml = sub('FILE_unique_key_[0-9]*',
                'FILE',
                unparse(self.dict, pretty = True))

class RunSet(object):
    """A run set."""

    def __init__(self, run, **kwargs):
        """Create a run set.
           Runs are added using the 'run' argument
           
           Args:
                run:        - An object of class Run
                            - A list of object of class Run
                            - The file path of a tab-delimited text table,
                              each row representing an object of class Run
                              with its arguments described in columns.
                              The first row must contain columns headers.
        """

        self.dict = collections.OrderedDict({'RUN_SET':{}})
        # If a single object of class Run is specified
        if isinstance(run, Run):
            self.run_list = [run]
        # If a list of objects of class Run is specified
        elif isinstance(run, list) and all(isinstance(x, Run) for x in run):
            self.run_list = run
        # If a text table of run is specified
        elif isinstance(run, str):
            try:
                # Edit default columns names if specified in kwargs
                colnames = {'experiment':'experiment', 'alias':'alias',
                    'center':'center', 'filename':'filename', 'filetype':'filetype'}
                for k in colnames.keys():
                    if k in kwargs.keys():
                        colnames[k] = kwargs[k]
                self.run_list = []
                for i, row in pd.read_table(run, dtype = 'str').iterrows():
                    # Retrieve the run details from table using columns names
                    args = {}
                    for key, value in colnames.items():
                        args[key] = dict(row)[value]
                    self.run_list.append(Run(**args))
            except Exception as e:
                print('Error: ' + str(e))
                raise
        else:
            raise ValueError('run is of wrong type')
        # Create a dict that follows the structure of the ENA XML file
        for i, e in enumerate(self.run_list):
            # Unlike in XML, each key must be unique
            e.dict['RUN_unique_key_' + str(i)] = e.dict.pop('RUN')
            self.dict['RUN_SET'].update(e.dict)
        # Convert the dict to XML
        self.xml = sub('FILE_unique_key_[0-9]*',
            'FILE',
            sub('RUN_unique_key_[0-9]*',
                'RUN',
                unparse(self.dict, pretty = True)
            )
        )
    
    def write_xml(self, file):
        """Write the XML file."""
        with open(file, 'w') as f:
            f.write(self.xml)

def write_table_template(file):
    """Write a template table."""

    data = {'experiment': ['exp01', 'exp02'],
        'alias': ['run01', 'run02'],
        'center': ['My research center', 'My research center'],
        'filename': ['tmp/seq_01_R1.fastq.gz,tmp/seq_01_R2.fastq.gz', 'tmp/seq_02_R1.fastq.gz,tmp/seq_02_R2.fastq.gz'],
        'filetype': ['fastq,fastq', 'fastq,fastq']
        }
    pd.DataFrame(data,
        columns = ['experiment', 'alias', 'center', 'filename', 'filetype']
        ).to_csv(file, sep = '\t', index =  False)