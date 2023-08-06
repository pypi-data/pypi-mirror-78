'''
Created on Mar 25, 2019

@author: Abel Carrión
'''

from abc import abstractmethod, ABCMeta

class Dependency(metaclass=ABCMeta):
    '''
    The Dependency class used as base for implementing test dependencies

    Args:

    Attributes:
    
    '''
    def __init__(self):
        pass
    
    @classmethod
    @abstractmethod
    def set_parser_args(cls, parser):
        '''Sets the arguments that the parser must analyze

        Args:
            parser (argparse.ArgumentParser): the parser instance to be configured

        Raises:

        Returns:
    
        '''
        raise NotImplementedError("Dependency.set_parser_args has no implementation")
    
    @classmethod
    @abstractmethod      
    def instantiate_dependency(cls, testDirectory, args):
        ''''Creates an instance of the Dependency class

        Args:
            args (List of arguments): List of arguments and its corresponding values 
            
        Raises:

        Returns:
            testInstance (Test): A instance of the Test class
    
        '''
        raise NotImplementedError("Dependency.instantiate_dependency has no implementation")
    
    def pre_processing(self, testDir):
        '''Tasks that should be performed BEFORE running the test

        Args: 
            testDir (String): Path to the test result/working directories
            
        Raises:

        Returns:
    
        '''
        pass
    
    def post_processing(self, testDir):
        '''Tasks that should be performed AFTER running the test

        Args: 
            testDir (String): Path to the test result/working directories
            
        Raises:

        Returns:
    
        '''
        pass