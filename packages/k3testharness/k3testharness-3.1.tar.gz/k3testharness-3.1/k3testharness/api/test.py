'''
Created on Mar 22, 2019

@author: Abel Carrión
'''

import sys
from abc import ABCMeta, abstractmethod

def set_parser_args(parser):
    '''Sets the arguments that the parser must analyze

    Args:
        parser (argparse.ArgumentParser): the parser instance to be configured

    Raises:

    Returns:
    
    '''
    raise NotImplemented("Test.setParserArgs has no implementation")
        
def instantiate_test(args):
    '''Creates an instance of the Test class

    Args:
        args (List of arguments): List of arguments and its corresponding values
        testDir (String): Path to the test result/working directories 

    Raises:

    Returns:
        testInstance (Test): A instance of the Test class
    
    '''
    raise NotImplemented("Test.instantiateTest has no implementation")

class Test(metaclass=ABCMeta):
    
    def test_duration_estimate(self):
        '''Gets the estimated test duration in seconds

        Args: 

        Raises:

        Returns:
            duration (integer): the estimated test duration in seconds, None if not defined
    
        '''
        return None
    
    @abstractmethod
    def run_test(self, *dependencies):
        '''Abstract method for implementing the execution of a Test

        Args:
            *dependencies (Objects): A series of dependencies needed for running the Test
            
        Raises:

        Returns:
    
        '''
        raise NotImplemented("Test.run_test has no implementation")