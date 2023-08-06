#!/usr/bin/env python3
'''
k3testharness is a framework for hosting test.
'''

import argparse
import importlib.util
import sys
import os
import inspect
import logging
import json
import datetime

import k3testharness.api.exceptions
from k3testharness import api

TEST_OK = 0
TEST_FAILED = 1
TESTING_FAILED = 2

logger = logging.getLogger(__name__)

__version__ = '2.0'
__author__ = 'Joachim Kestner <joachim.kestner@khoch3.de>'



# #########################
# NEW LOGGING

def setLogArgs(parser):
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable info logging to console")
    parser.add_argument("-vv", "--extra_verbose", action="store_true", help="Enable debug logging to console")
    #parser.add_argument("--log_file", default=datetime.datetime.now().strftime("%Y%m%dT%H%M%S")+"_"+logFileSuffix, help="Log file with debug logging. Default: <Datetime>_"+logFileSuffix)

def evalLogArgsAInitLogging(args, outputDir):
    fileDebugLogH = logging.FileHandler(os.path.join(outputDir, "debug.log"))
    fileInfoLogH = logging.FileHandler(os.path.join(outputDir, "info.log"))
    fileInfoLogH.setLevel(logging.INFO)
    streamLogH = logging.StreamHandler(sys.stdout)
    if args.verbose:
        streamLogH.setLevel(logging.INFO)
    elif args.extra_verbose:
        streamLogH.setLevel(logging.DEBUG)
    else:
        streamLogH.setLevel(logging.WARN)
    
    fmtStrDebug = "%(asctime)s %(levelname)7s [%(name)28s]: %(message)s [%(threadName)s]"
    fmtStrinfo = "%(asctime)s %(levelname)7s: %(message)s"
    rl = logging.getLogger()
    rl.setLevel(logging.DEBUG)
    
    fileDebugLogH.setFormatter(logging.Formatter(fmtStrDebug))
    fileInfoLogH.setFormatter(logging.Formatter(fmtStrinfo))
    streamLogH.setFormatter(logging.Formatter(fmtStrinfo))
    
    rl.addHandler(fileDebugLogH)
    rl.addHandler(fileInfoLogH)
    rl.addHandler(streamLogH)
     
#     rl.setLevel(logging.DEBUG)
#     rl.addHandler(fileDebugLogH)
#     rl.addHandler(fileInfoLogH)
#     rl.addHandler(streamLogH)

    #logging.basicConfig(level=logging.DEBUG, msgFormat="%(asctime)s %(levelname)s:  %(message)s", handlers=[fileDebugLogH, fileInfoLogH, streamLogH])
    #logging.basicConfig(level=logging.DEBUG, format=fmtStr, handlers=handlers)
        
def parse_known_args_w_help(parser, lastArgs=None):
    '''
    Parse known arguments but show the help message if the parsing fails and the --help or -h was one of the last known arguments 
    :param parser: argparse.ArgumentParser  
    :param lastArgs: the group of arguments known so far 
    '''
    try:
        return parser.parse_known_args()
    except SystemExit:
        if lastArgs != None and lastArgs.help:
            parser.print_help()
            sys.exit(0)
        raise
    


def main():
    defaultResDir = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+"_results"

    
    # Creates the parser with the main arguments 
    parser = argparse.ArgumentParser(description=__doc__+"\n\n\n\nAuthor: {}\nVersion: {}".format(__author__,__version__), formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False)
    parser.add_argument("-h", "--help", action='store_true', help='show this help message and exit. Note: if --test is passed this help message will be extended to include test and possibly dependency arguments')
    parser.add_argument("--test", help="the path to a module that implements the test API")
    #parser.add_argument("--test_dependencies", help="the path to the dir that contains the implementation of the test dependencies")
    parser.add_argument("--test_dir", default=defaultResDir, help="path to the test result/working directory. Default: {}".format(defaultResDir))
    setLogArgs(parser)

    args, remaining_argv = parser.parse_known_args() # We parse the known arguments so far
    
    if not args.test:   # --test is a mandatory argument
        if args.help:   # if -h or --help are included in the known arguments so far, print the parser help and exit
            parser.print_help()
            sys.exit(0)
        parser.print_usage()    # else print the usage message and highlight the error, i.e. the argument --test is missing
        print("k3testharness: error: the following arguments are required: --test")
        sys.exit(1)
    
    if not os.path.isfile(args.test):   # if the path of the test file passed does not exist, abort
        logger.error("Given test '{}' with the --test argument does not exist!".format(args.test))
        sys.exit(1)

    #if args.test_dependencies:
    #    if not os.path.isdir(args.test_dependencies):
    #        logger.error("Given test dependency directory '{}' does not exist!".format(args.test_dependencies))
    #        sys.exit(1)
    #    sys.path.append(os.path.abspath(args.test_dependencies))
        
    if not os.path.isdir(args.test_dir) and not args.help:  # if the path to the test result/working directory does not exist, create it 
        os.makedirs(args.test_dir, exist_ok=True)
        
    evalLogArgsAInitLogging(args, args.test_dir) # evaluate the known args and configure the logger
     
    testName = os.path.basename(os.path.splitext(args.test)[0]) # extract the test name from the test filename
    
    try:
        
        # Dynamically imports the module that corresponds to the test
        logger.debug("Instantiating test")
        spec = importlib.util.spec_from_file_location(testName, args.test)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    
        # Add a group for test arguments, calling the set_parser_args method defined in the test module
        logger.debug("Get test argparse arguments")
        module.set_parser_args(parser.add_argument_group('test arguments'))
        
        # Parse the known arguments so far (the main arguments and the ones that belong to the test
        args, remaining_argv = parse_known_args_w_help(parser, lastArgs=args)
        
        # Instantiates the test calling the instantiate_test method define in the test module
        testInstance = module.instantiate_test(args.test_dir, args)
        logger.info("Instantiating test successful")
        
    
        # Gets the list of test dependency classes required by the method run_test of the test class in the test module
        testInstanceSignature = inspect.signature(testInstance.run_test)
        testDependencyClasses = [v.annotation for v in testInstanceSignature.parameters.values()]
        logger.info("Test dependencies: "+ ", ".join([c.__name__ for c in testDependencyClasses]))
    
        
        # Adds a group of test dependency arguments for each test dependency class, calling the set_parser_args method defined in each class 
        for dependencyClass in testDependencyClasses:
            if dependencyClass == api.WorkingDirectory:
                continue
            logger.debug("Setting argparse args for dependency {}".format(dependencyClass.__name__))
            dependencyClass.set_parser_args(parser.add_argument_group(dependencyClass.__name__+" arguments"))
        
        # Parse the known arguments so far (the k3testharness arguments, the test arguments and the test dependencies arguments)
        args, remaining_argv = parse_known_args_w_help(parser, lastArgs=args)
        if args.help:
            parser.print_help()
            sys.exit(0)
        
        # If there are still arguments in the remaining_argv group, then they are invalid arguments
        if len(remaining_argv) > 0: #There are unrecognized remaining parameters
            parser.parse_args() # parser_args will exit the program when passing invalid arguments
        
        logger.debug("Parsed argparse arguments '{}'".format(args))
        

        # Gets an instance for all the test dependency classes of the test    
        dependencyInstances = []
        for dependencyClass in testDependencyClasses:
            if dependencyClass == api.WorkingDirectory:
                dependencyInstances.append(str(args.test_dir))
            else:
                logger.debug("Instantiating dependency '{}'".format(dependencyClass.__name__))
                dependencyInstances.append(dependencyClass.instantiate_dependency(args.test_dir, args))
                logger.info("Instantiating dependency '{}' successful".format(dependencyClass.__name__))
    
        logger.info("Instantiating dependencies done")
        
        startDate = datetime.datetime.now()
    
        # For each test dependency, run its corresponding pre_processing methods (sets the dependency state before actually running the test)
        for dependencyInstance in dependencyInstances:
            if hasattr(dependencyInstance, "pre_processing"):
                logger.debug("Dependency {} pre_processing".format(dependencyInstance.__class__.__name__))
                try:
                    dependencyInstance.pre_processing(args.test_dir)
                except:
                    logger.warn("Error while doing pre processing on dependency {}".format(dependencyInstance.__class__.__name__))
                    raise
                logger.info("Dependency {} pre_processing done".format(dependencyInstance.__class__.__name__))
        logger.info("All dependency pre_processing done")
        
        # Performs the actual execution of the test
        try:
            logger.info("Starting Test {} =================================================================".format(testName))
            testInstance.run_test(*dependencyInstances)
        except k3testharness.api.exceptions.TestFailedException as tfe:
            logger.info("Test {}  FAILED =================================================================".format(testName))
            logger.info("EXIT STATUS: NOT OK. TEST FAILED because: {}".format(str(tfe)))
            logger.info("Caught TestFailedException", exc_info=True)
            exitCode = TEST_FAILED
        except Exception as e:
            logger.info("Testing {} FAILED ===============================================================".format(testName))
            logger.info("EXIT STATUS: NOT OK. TESTING FAILED because: {}".format(str(e)))
            logger.info("Caught TestFailedException", exc_info=True)
            exitCode = TESTING_FAILED
        else:
            logger.info("Test {} OK ======================================================================".format(testName))
            logger.info("EXIT STATUS: OK")
            exitCode = TEST_OK
    
        # For each test dependency, run its corresponding post_processing methods
        for dependencyInstance in dependencyInstances:
            if hasattr(dependencyInstance, "post_processing"):
                logger.debug("Dependency {} post_processing".format(dependencyInstance.__class__.__name__))
                try:
                    dependencyInstance.post_processing(args.test_dir)
                except:
                    logger.warn("Error while doing post processing on dependency {}".format(dependencyInstance.__class__.__name__))
                    raise
                logger.info("Dependency {} post_processing done".format(dependencyInstance.__class__.__name__))
        logger.info("All dependency post_processing done")
    
        endDate = datetime.datetime.now()
    
        # Produces a JSON file with test result info
        info = {
            "testName": testName,
            "startDate": str(startDate),
            "endDate": str(endDate),
            "exitStatus": exitCode
        }
        resultFileName = os.path.join(args.test_dir,testName+"_"+datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".json")
        with open(resultFileName, 'w') as resultFile:
            resultFile.write(json.dumps(info))
            logger.info("Result file written to: "+resultFileName)
    except Exception as e:
        logger.error("Exception in testharness main. Exiting", exc_info=True)
        exitCode = TESTING_FAILED
    logger.info("Test harness exit code: "+str(exitCode))
    os._exit(exitCode)

if __name__ == '__main__':
    r = main()
    sys.exit(r)
    
    