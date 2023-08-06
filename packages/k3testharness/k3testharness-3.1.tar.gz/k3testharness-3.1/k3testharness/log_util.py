'''
Created on 20 Mar 2017

@author: joachim
'''
import datetime, traceback

class Logger:
    
    DEBUG_LVL = 20
    INFO_LVL = 30
    WARN_LVL = 40
    ERROR_LVL = 50
    
    LOG_LVL_TO_STR = {DEBUG_LVL:"debug", INFO_LVL:"info", WARN_LVL:"warning", ERROR_LVL:"error"}
    
    def __init__(self, name):
        self.name = name
    
    def _log(self, logLvl, logItem):
        raise NotImplementedError("getLogger not implemented on base logger")
    
    def debug(self, logMsg):
        self._log(Logger.DEBUG_LVL, logMsg)
    
    def info(self, logMsg):
        self._log(Logger.INFO_LVL, logMsg)
    
    def warning(self, logMsg):
        self._log(Logger.WARN_LVL, logMsg)
    
    def error(self, logMsg):
        self._log(Logger.ERROR_LVL, logMsg)
    
    def getLogger(self, name):
        raise NotImplementedError("getLogger not implemented on base logger")
    
    def close(self):
        pass

class NoneLogger(Logger):
    
    def __init__(self):
        pass
    
    def _log(self, logLvl, logItem):
        pass
    
    def getLogger(self, name):
        return self
    
class LoggerWHandler(Logger):
    
    def __init__(self, name, logEntryHandlers):
        self.name = name
        self.handlers = logEntryHandlers
        
    def _log(self, logLvl, logItem):
        try:
            errLvlStr = str(logLvl) if logLvl not in Logger.LOG_LVL_TO_STR else Logger.LOG_LVL_TO_STR[logLvl]
            errLvlStr = errLvlStr.upper()
            tsStr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            if issubclass(logItem.__class__, Exception):
                for handler in self.handlers:
                    handler.logEntry(logLvl, "{} {:^25.25} {:>7}: Exception Stacktrace:".format(tsStr, self.name, errLvlStr))
                    handler.logEntry(logLvl, "".join(traceback.format_exception(None, logItem, logItem.__traceback__)))
            else:
                for handler in self.handlers:
                    handler.logEntry(logLvl, "{} {:^25.25} {:>7}:  {}".format(tsStr, self.name, errLvlStr, logItem))
        except Exception as e:
            traceback.print_exc()
            print("Exception during logging!")
            print("Log itms was: "+str(logItem))
            
    
    def getLogger(self, name):
        return LoggerWHandler(name, self.handlers)
    
    def close(self):
        for handler in self.handlers:
            if hasattr(handler, "close") and callable(handler.close):
                handler.close()
    
#######################################################
# Handlers
#######################################################
class ConsoleLogHandler:
    def logEntry(self, logLvl, logStr):
        print(logStr)

class StdLogHandler:
    
    def __init__(self, logger):
        self.logger = logger
        
    def logEntry(self, logLvl, logStr):
        getattr(self.logger, Logger.LOG_LVL_TO_STR[logLvl])(logStr)

class MuliLevelLogfileHandler:
    
    def __init__(self, logLvlToFileNmDict):
        self.logLvlToFiles = {}
        for logLvl in logLvlToFileNmDict:
            fh = open(logLvlToFileNmDict[logLvl], "x")
            self.logLvlToFiles[logLvl] = fh
            
    def logEntry(self, logLvl, logStr):
        #print(logStr)
        for fileLogLvl in self.logLvlToFiles:
            if fileLogLvl <= logLvl:
                self.logLvlToFiles[fileLogLvl].write(logStr+"\n")
                self.logLvlToFiles[fileLogLvl].flush()
    
    def close(self):
        for logLvl in self.logLvlToFiles:
            self.logLvlToFiles[logLvl].close()
    
# special loggers
    
            
#######################################################
# Factory Methods
#######################################################

def getConsoleLogger(name):
    return LoggerWHandler(name, [ConsoleLogHandler()])


def getMuliLevelLogfileLoger(name, logLvlToFileNmDict, stdLogger=None):
    return LoggerWHandler(name, [MuliLevelLogfileHandler(logLvlToFileNmDict)] + ([StdLogHandler(stdLogger)] if stdLogger else []))
    
    
    
        