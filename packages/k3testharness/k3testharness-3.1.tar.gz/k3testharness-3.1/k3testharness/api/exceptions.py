'''
Created on 20 Mar 2017

@author: joachim
'''

class TestFrameworkBaseException(Exception):
    pass

class TestFailedException(TestFrameworkBaseException):
    pass

class TestingFailedException(TestFrameworkBaseException):
    pass

class TestFrameworkException(TestFrameworkBaseException):
    pass

class FrameworkSupportModuleException(TestFrameworkException):
    pass