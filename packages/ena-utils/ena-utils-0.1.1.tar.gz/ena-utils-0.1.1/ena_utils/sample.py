import os
import sys
import collections
import pandas as pd
from xmltodict import unparse
from re import sub

class Sample(object):
    """A sample."""

    def __init__(self, alias, title, taxon_id,
        scientific_name, common_name, **kwargs):
        """Create a sample."""
        self.dict = collections.OrderedDict({'SAMPLE':
        {
            '@alias':str(alias),
            'TITLE':str(title),
            'SAMPLE_NAME':{
                'TAXON_ID':str(taxon_id),
                'SCIENTIFIC_NAME':str(scientific_name),
                'COMMON_NAME':str(common_name)
            },
            'SAMPLE_ATTRIBUTES':{}
        }})
        i = 0
        for key, value in kwargs.items():
            self.dict['SAMPLE']['SAMPLE_ATTRIBUTES'].update({
               'SAMPLE_ATTRIBUTE_unique_key_' + str(i):{
                   'TAG':str(key),
                   'VALUE':str(value)
               }
            })
            i = i+1
        self.xml = sub('SAMPLE_ATTRIBUTE_unique_key_[0-9]*',
                'SAMPLE_ATTRIBUTE',
                unparse(self.dict, pretty = True))

class SampleSet(object):
    """A sample set."""

    def __init__(self, sample, **kwargs):
        """Create a sample set.
           Samples are added using the 'sample' argument
           
           Args:
                sample: - An object of class Sample
                            - A list of object of class Sample
                            - The file path of a tab-delimited text table,
                              each row representing an object of class Sample
                              with its arguments described in columns.
                              The first row must contain columns headers.
        """

        self.dict = collections.OrderedDict({'SAMPLE_SET':{}})
        # If a single object of class Sample is specified
        if isinstance(sample, Sample):
            self.sample_list = [sample]
        # If a list of objects of class Sample is specified
        elif isinstance(sample, list) and all(isinstance(x, Sample) for x in sample):
            self.sample_list = sample
        # If a text table of samples is specified
        elif isinstance(sample, str):
            try:
                # Edit default columns names if specified in kwargs
                colnames = {'alias':'alias', 'title':'title',
                 'taxon_id':'taxon_id', 'scientific_name':'scientific_name',
                    'common_name':'common_name'}
                for k in colnames.keys():
                    if k in kwargs.keys():
                        colnames[k] = kwargs[k]
                self.sample_list = []
                for i, row in pd.read_table(sample).iterrows():
                    # Retrieve the sample details from table using columns names
                    args = {}
                    for key, value in dict(row).items():
                        # Replace row headers that match colnames
                        if key in colnames.values():
                            args[key] = value
                        else:
                            args[key] = value
                    self.sample_list.append(Sample(**args))
            except Exception as e:
                print('Error: ' + str(e))
                raise
        else:
            raise ValueError('sample is of wrong type')
        # Create a dict that follows the structure of the ENA XML file
        for i, e in enumerate(self.sample_list):
            # Unlike in XML, each key must be unique
            e.dict['SAMPLE_unique_key_' + str(i)] = e.dict.pop('SAMPLE')
            self.dict['SAMPLE_SET'].update(e.dict)
        # Convert the dict to XML
        self.xml = sub('SAMPLE_ATTRIBUTE_unique_key_[0-9]*',
                'SAMPLE_ATTRIBUTE',
                sub('SAMPLE_unique_key_[0-9]*',
                    'SAMPLE',
                    unparse(self.dict, pretty = True)
                )
            )

    def write_xml(self, file):
        """Write the XML file."""
        with open(file, 'w') as f:
            f.write(self.xml)

def write_table_template(file):
    """Write a template table."""

    data = {'alias': ['sample01', 'sample02'],
        'title': ['sample 1 title.', 'sample 2 title.'],
        'taxon_id': ['10090', '10090'],
        'scientific_name': ['Mus musculus', 'Mus musculus'],
        'common_name': ['house mouse', 'house mouse'],
        'additional_arg': ['an_additional_arg', 'an_additional_arg']
        }
    pd.DataFrame(data,
        columns = ['alias', 'title', 'taxon_id', 'scientific_name',
            'common_name', 'additional_arg']
        ).to_csv(file, sep = '\t', index =  False)