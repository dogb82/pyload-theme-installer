#!/usr/bin/python
from inspect import currentframe, getframeinfo
import time
from enum import Enum
#import logging

PRINT_DEBUG_MSG = True

class LogColor(object):
    BLUE = '\033[94m'
    CYAN  = "\033[1;36m"
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    HEADER = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DEFAULT = ''

class Level(Enum):
	LOG = 'LOG'
	DEBUG = 'DEBUG'
	SUCCESS = 'SUCCESS'
	INFO = 'INFO'
	WARN = 'WARN'
	ERROR = 'ERROR'

def log(text, color = LogColor.DEFAULT, level = Level.LOG):
	if color in LogColor.__dict__.values():
		isInLogColor = True
	else: 
		isInLogColor = False

	dati = time.strftime("[%Y-%m-%d %H:%M:%S]")
	strLevel = stringFormat('(' + level.value + ')', 10)
	
	result = ""
	if not isInLogColor:
		result = text
	else:
		result = color + dati + " " + strLevel + " - " + text + LogColor.ENDC

	print(result)

def error(text):
    log(text, LogColor.RED, Level.ERROR)

def success(text):
	log(text, LogColor.GREEN, Level.SUCCESS)

def warn(text):
	log(text, LogColor.YELLOW, Level.WARN)

def info(text):
	log(text, LogColor.CYAN, Level.INFO)

def header(text):
	log(text, LogColor.HEADER)

def underline(text):
	log(text, LogColor.UNDERLINE)

def bold(text):
	log(text, LogColor.BOLD)

def debug(filename, text):
	if PRINT_DEBUG_MSG:
		frameinfo = getframeinfo(currentframe())
		#filenameAndLineNumber = "[" + filename + " | " +frameinfo.filename + " (" + str(frameinfo.lineno) + ")]"
		dati = time.strftime("[%Y-%m-%d %H:%M:%S]")

		log(filename + ": " + text, LogColor.BLUE, Level.DEBUG)

def stringFormat(text, places):
	res = '%-10s' % (text)
	return res
#def debugLog(filename, text):
#	logging.
# log("hello", LogColor.OKGREEN)

