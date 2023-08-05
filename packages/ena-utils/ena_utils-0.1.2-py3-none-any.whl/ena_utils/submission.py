import os
import sys
import collections
from xmltodict import unparse
from re import sub

class Submission(object):
    """A submission."""

    def __init__(self, type = 'ADD', **kwargs):
        """Create a submission."""
        self.dict = collections.OrderedDict({'SUBMISSION':{
            'ACTIONS':{
                'ACTION_key_1':{type.upper():{}}
            }}})
        if 'hold' in kwargs.keys():
            if kwargs['hold'] is not None:
                self.dict['SUBMISSION']['ACTIONS'].update({'ACTION_key_2':{'HOLD':{
                        '@HoldUntilDate':kwargs['hold']
                    }}})
        self.xml = sub('ACTION_key_[0-9]*',
                'ACTION',
                unparse(self.dict, pretty = True))

    def write_xml(self, file):
        """Write XML file."""
        with open(file, 'w') as f:
            f.write(self.xml)
