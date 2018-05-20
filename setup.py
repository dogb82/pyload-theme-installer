#!/usr/bin/python

import datetime
import time
import shlex, subprocess
import getpass
import glob, os
import logger

try:
	import setup_config
except ImportError:
	logger.error("Config-File \"setup_config.py\" not found!")
	pass

logger.info("This Pyload-Theme-Installer is in Beta.")

installerPath = os.path.dirname(os.path.realpath(__file__))
#print(datetime.datetime.now())
stopPyloadCmd = "sudo service pyload stop"
startPyloadCmd = "sudo service pyload start"
startPyloadCmdWithPython = "{}pyLoadCore.py --daemon"
testCmd = "date"
WEBINTERFACE_FILE = "webinterface.py"
DELETE_COMPILED_WEBINTERFACE_FILE_CMD = "sudo rm -rf webinterface.pyc"
TEST_WEBINTERFACE_FILE = "inserted_webinterface.py"
SEARCH_STRING = "FileSystemLoader(join(PROJECT_DIR, \"templates\", \"default\")),"
INSERT_STRING = '"PyPlex": FileSystemLoader(join(PROJECT_DIR, "templates", "PyPlex")),'
USER_INTERACTION_INSTRUCTION = 'Login into the PyLoad webinterface, \nnavigate to the Config page, \nGeneral Tab and click on "Webinterface". \nEnter the name of the new theme: "e.g. PyPlex" \nin the template field and hit "Submit"'
copyTemplateDirCmd = 'cp -iR \"' + installerPath + '/templates/\"* \"{}\"'
copyMediaDirCmd = 'cp -iR \"' + installerPath + '/media/\"* \"{}\"'
createFoldersIfNotExist = 'mkdir -p \"{}\"'
webinterfaceSubPathInPyload = "module/web"
mkdirScript = 'bin/mkdir_helper.sh {}'
cpScript = 'bin/cp_helper.sh {0} {1}'
# get os user
osUser = getpass.getuser()
logger.debug(__file__, "OsUser: " + osUser)

possibleInstallationPath = ["/usr/share/pyload/", "/home/" + osUser + "/.pyload"]
installationPath = ""

#print(globals())
try:
	if hasattr(setup_config, 'PYLOAD_MODULE_PATH'):
		if setup_config.PYLOAD_MODULE_PATH != "":
			possibleInstallationPath = []
			possibleInstallationPath.append(setup_config.PYLOAD_MODULE_PATH)
			installationPath = PYLOAD_MODULE_PATH
		else:
			logger.warn("You have to enter the path of your pyload module.")
	else:
		logger.warn("setup_config.py corrupt!")
except NameError:
	logger.error("NameError")
	pass

logger.log(time.strftime("%Y-%m-%d %H:%M:%S"))

def file_get_contents(filename):
    try:
        with open(filename) as f:
            return f.read()
    except (IOError):
        return -1

def stopPyload():
	# stop pyload
	logger.log("Stopping PyLoad")
	logger.debug(__file__, "Stopping PyLoad: " + stopPyloadCmd)
	#subprocess.check_call(stopPyloadCmd.split())
	process = subprocess.Popen(stopPyloadCmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	returncode = process.wait()

	if returncode > 0:
		logger.error("Pyload.service not found.")
	else:
		logger.info("Pyload.service stopped")

	logger.debug(__file__, "Command \"" + stopPyloadCmd + "\" returned: " + process.stdout.read())

	# stopping hard pyload by pid
	if returncode > 0:
		logger.log("Trying to stop pyload on hard way...")
		pidFile = installationPath
		if not pidFile.endswith("/"):
			pidFile += "/"
		pidFile += "pyload.pid"
		logger.log("pyload-PID: " + pidFile)
		#showPidCmd = 'cat ' + pidFile
		#pidFileCatProcess = subprocess.Popen(showPidCmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		#getPidReturncode = pidFileCatProcess.wait()
		#logger.debug(__file__, showPidCmd + " returned code : " + str(getPidReturncode))
		pidCode = file_get_contents(pidFile)
		if pidCode < 0:
			logger.warn("No pid file/code. Maybe pyload not running")
			return
		logger.debug(__file__, "Content of \"" + pidFile + "\" " + pidCode)

		stopHardPyloadCmd = "kill -9 " + str(pidCode)
		logger.debug(__file__, "Stopping-Pyload-hard-command: " + stopHardPyloadCmd)
		killByPidProcess = subprocess.Popen(stopHardPyloadCmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		killByPidReturncode = killByPidProcess.wait()
		logger.debug(__file__, stopHardPyloadCmd + " returned code : " + str(killByPidReturncode))
		if killByPidReturncode > 0:
			logger.error("Killing pyload by pid failed. Maybe pyload not running.")
			logger.error("System-return-message: ")
		else:
			logger.log("Stopped pyload-process by process-id " + pidCode)
		
		logger.log(killByPidProcess.stdout.read())
		#stopHardPyloadCmd = "kill -9 \"$(cat " + installationPath + ")\""

def startPyload():
	# start pyload
	logger.log("Starting PyLoad")
	startPyloadProc = subprocess.Popen(startPyloadCmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	startPyloadReturnCode = startPyloadProc.wait()
	if startPyloadReturnCode > 0:
		logger.error("Could not start pyload with command: {}".format(startPyloadCmd))
	else:
		logger.success("Pyload started.")

	startPyCmd = startPyloadCmdWithPython.format(installationPath)
	logger.log("Trying to start pyload directly with python: {}".format(startPyCmd))
	os.system(startPyCmd)

def executeShellCommand( command ):
	logger.debug(__file__, "shell-command: " + command)
	args = shlex.split(command)
	proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = proc.communicate()
	logger.debug(__file__, "out: " + str(out) + "; err: " + str(err))

# search for webinterface.py
logger.log(osUser)

# insert "PyPlex" Loader to webinterface.py
for i in possibleInstallationPath:
	logger.log("looking for \"" + WEBINTERFACE_FILE + "\" in directory \"" + i + "\"")
	try:
		currentPath = i
		if not i.endswith("/"):
			currentPath += "/"
		currentPath += webinterfaceSubPathInPyload
		logger.debug(__file__, "searching " + WEBINTERFACE_FILE + " path: " + currentPath)
		os.chdir(currentPath)
		insertSuccess = False
		for file in glob.glob(WEBINTERFACE_FILE):
			logger.success("Found file \"" + file + "\" in \"" + currentPath + "\"")
			insertSuccess = False
			installationPath = i
			stopPyload()
			logger.debug(__file__, "Printing file-content: " + file + " and installationPath: " + installationPath)
			if SEARCH_STRING in open(file).read():
				logger.debug(__file__, "Found " + SEARCH_STRING + " in " + file)
				f = open(file, "r")
				contents = f.readlines()
				newContents = []
				f.close()
				index = 0
				foundLine = False
				for line in contents:
					logger.debug(__file__, "\t" + line)
					if foundLine:
						newContents.append(INSERT_STRING + "\n")
						foundLine = False
					newContents.append(line)
					# print ("{}. {}".format(index, line))
					index += 1
					if SEARCH_STRING not in line:
						continue
					else:
						insertSuccess = True
						foundLine = True
				#for index in count(contents):
				#	print(index + ". " + contents)
				f = open(WEBINTERFACE_FILE, "w")
				contents = "".join(newContents)
				f.write(contents)
				f.close()
			if insertSuccess:
				logger.success("Successfully inserted \"" + INSERT_STRING + "\"")
				break
		if not insertSuccess:
			logger.warn(WEBINTERFACE_FILE + " is not prepard. Something went wrong.")
	except OSError:
		# no directory there
		logger.error("File \"" + WEBINTERFACE_FILE + "\" not found in this directory")
		pass

# Delete compiled python "webinterface.pyc" file for refreshing
logger.log("Deleting compiled file")
subprocess.check_call(DELETE_COMPILED_WEBINTERFACE_FILE_CMD.split())

raw_input("Press Enter to continue...")

os.chdir(installerPath)

pathSeparator = "/"
if installationPath.endswith("/"):
	pathSeparator = ""

# prepare "template"
templatePath = installationPath + pathSeparator + webinterfaceSubPathInPyload + "/templates/"
logger.log("Copying content of \"templates\" folder to \"" + templatePath + "\"")

# create "templates" folder
mkdirScriptCall = 'bash ' + mkdirScript.format(templatePath)
executeShellCommand(mkdirScriptCall)

# copy "templates" content to pyload "templates"
cpScriptCall = 'bash ' + cpScript.format(installerPath + '/templates/*', templatePath)
executeShellCommand(cpScriptCall)

raw_input("Templates folders/files created. Press Enter to continue...")

# prepare "media" 
mediaPath = installationPath + pathSeparator + webinterfaceSubPathInPyload + "/media/"
logger.log("Copying content of \"media\" folder to \"" + mediaPath + "\"")

# create "media" folder
mkdirScriptCall = 'bash ' + mkdirScript.format(mediaPath)
executeShellCommand(mkdirScriptCall)

# copy "media" content to pyload "media"
mediaFolderContentList = os.listdir(installerPath + '/media/')
logger.debug(__file__, 'os.listdir: ' + str(mediaFolderContentList))

for i in mediaFolderContentList:
	cpScriptCall = 'bash ' + cpScript.format(installerPath + '/media/' + i, mediaPath)
	executeShellCommand(cpScriptCall)

raw_input("Media folders/files created. Press Enter to continue...")

# restart pyload
logger.log("Restarting pyload")
startPyload()

# user interaction is needed to activate this theme 
logger.info("")
logger.info("\n\n##########################################################\n" + USER_INTERACTION_INSTRUCTION + "\n##########################################################\n")
logger.info("enjoy! ;)")