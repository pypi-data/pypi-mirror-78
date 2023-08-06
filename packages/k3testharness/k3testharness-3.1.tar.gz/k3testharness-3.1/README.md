# k3testharness

## Overview
k3testharness is a command line focused test execution engine. It provides 2 APIs, for tests and test dependencies respectively. Before running a test run it instantiates a test, then it checks the dependencies of a test and instantiates them as well, and finally it proceeds to execute the test.


## Test & Dependency API

### Test API
[k3testharness/api/test.py](k3testharness/api/test.py)

A test needs to implement the set_parser_args & instantiate_test methods

```python
# within set_parser_args, arguments for a test can be added to the given argparse parser
set_parser_args(parser)

# given the parsed arguemnts, return an instance of an object that conforms to the abstract api of the k3testharness.api.test.Test class
instantiate_test(args) -> k3testharness.api.test.Test
```

Here the API defined by the abstract class k3testharness.api.test.Test:  
DependencyClass1 & DependencyClass2 are here for illustration purposes only

```python
class Test(ABC):
    @abstractmethod
    def run_test(self, depency1 : DependencyClass1, depency2 : DependencyClass2):
        raise k3testharness.api.exceptions.TestingFailedException("Some message") #If there is a testing error
        raise k3testharness.api.exceptions.TestFailedException("Some message") #If the test fails
```

### Dependency API
 
[k3testharness/api/dependency.py](k3testharness/api/dependency.py)
 
* Any external dependency that is given as a dependency to the run_test method needs to extend the Dependency abstract class  
ie. The dependency needs to implement the abstract class methods set_parser_args & instantiate_dependency.
* pre_processing and post_processing will be called before and after a test run respectively and can be used for initializing resources and saving the dependency state after a test run.

```python
class Dependency(ABC):

    @classmethod
    @abstractmethod
    def set_parser_args(cls, parser):
        pass

    @classmethod
    @abstractmethod
    def instantiate_dependency(cls, testDirectory, args):
        pass

    def pre_processing(self, testDirectory):
        pass

    def post_processing(self, testDirectory):
        pass

```

### Basic example

Let's suppose that the user implements the Test Dependency API found in [k3testharness/api/dependency.py](k3testharness/api/dependency.py), inside the python module 'my_test_dependency.py'.


```python
'''
This is an example implementation of a test dependency
'''

from k3testharness.api.dependency import Dependency

class MyTestDependency(Dependency):

    def __init__(self, args):
        self.dependencyArg1 = args.dependency_arg1

    @classmethod
    def set_parser_args(cls, parser):
        parser.add_argument("--dependency_arg1")
    
    @classmethod
    def instantiate_dependency(cls, testDirectory, args):
        return cls(args)

    def pre_processing(self, testDirectory):
        pass

    def post_processing(self, testDirectory):
        pass
    
    def dependency_function1(self):
        return self.dependencyArg1
        
```
Next, the user implements the Test API found in [k3testharness/api/test.py](k3testharness/api/test.py), inside the python module 'my_test.py'.

```python
'''
This is an example implementation of a test
'''

from k3testharness.api.test import Test
from my_test_dependency import MyTestDependency
from k3testharness.api.exceptions import TestFailedException, TestingFailedException

def set_parser_args(parser):
    parser.add_argument("--test_arg1")

def instantiate_test(testDir, args):
    return MyTest(args)

class MyTest(Test):

    def __init__(self, args):
        self.testArg1 = args.test_arg1

    def run_test(self, myTestDependency: MyTestDependency):
        dependencyArg = myTestDependency.dependency_function1()
        if !dependencyArg.is_integer():
            raise TestingFailedException("The value must be an integer")
        else if dependencyArg != self.testArg1:
            raise TestFailedException("{} is not equal to {}".format(dependencyArg, self.testArg1)) 
```

Now it is possible to perform the test by executing the following command line (assuming that the file 'my_test.py' is in the current directory and all the modules are in the PYTHON_PATH):

```
python3 k3testharness --test my_test.py --test_arg1 100 --dependency_arg1 100
```

## Installation & Setup

### Prerequisites

k3testharness requires Python 3.5+


### Installation

k3testharness should be installed with pip. It is recommended that it is installed within a virtual python environment. Any dependencies that a given test uses must be found within the python path at runtime.

Shell commands:

```
virtualenv venv
source venv/bin/activate

# install k3testharness
pip install k3testharness

# install a test dependency
pip install git+<test-dependency-url>

# run test harness with info level logging to console
# Note: the test and/or test dependencies may need further arguments
k3testharness -v --test <the-test-to-execute>
```


### Usage

```
usage: k3testharness [-h] [--test TEST] [--test_dir TEST_DIR] [-v] [-vv]

k3testharness is a framework for hosting test.

Author: Joachim Kestner <joachim.kestner@khoch3.de>
Version: 1.0

optional arguments:
  -h, --help            show this help message and exit. Note: if --test is
                        passed this help message will be extended to include
                        test and possibly dependency arguments
  --test TEST           the path to a module that implements the test API
  --test_dir TEST_DIR   path to the test result/working directories. Default: current working directory
  -v, --verbose         Enable info logging
  -vv, --extra_verbose  Enable debug logging
```