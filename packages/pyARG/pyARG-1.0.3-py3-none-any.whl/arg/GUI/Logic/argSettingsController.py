#HEADER
#                     arg/GUI/Logic/argSettingsController.py
#               Automatic Report Generator (ARG) v. 1.0
#
# Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
# (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
# Government retains certain rights in this software.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Questions? Visit gitlab.com/AutomaticReportGenerator/arg
#
#HEADER

import os
import sys

from PySide2.QtCore import QObject

from arg.GUI.Logic.argUserSettingsReader import argUserSettingsReader
from arg.GUI.Logic.argUserSettingsWriter import argUserSettingsWriter


class argSettingsController(QObject):
    """A controller class to handle settings
    """

    def __init__(self, parent=None):
        super(argSettingsController, self).__init__(parent)
        self.label = 0
        self.mandatory = 1
        self.commentary = 2
        self.settings = {}
        self.confSettingsFileName = "ARG-GUI-config.yml"
        self.confSettingsFilePath = 'Logic/'
        self.scriptDirectory = os.path.dirname(os.path.realpath(__file__))
        self.scriptDirectoryConfigFilePath = os.path.join(self.scriptDirectory, self.confSettingsFileName)
        self.homePath = os.environ["APPDATA"] if "APPDATA" in os.environ else os.environ["HOME"]
        self.userHomeConfigFilePath = os.path.join(os.path.join(self.homePath, "ARG"), self.confSettingsFileName)
        self.userSettingsReader = argUserSettingsReader(self.scriptDirectoryConfigFilePath, self.userHomeConfigFilePath)
        self.userSettingsWriter = argUserSettingsWriter()
        self.argPythonExePath = None
        self.argPythonSitePackagePath = None
        self.argScriptPath = None
        self.argLatexProcessorPath = None

    def initialize(self):

        # Initialize user settings from config file
        missingSettings = self.initializeUserSettings()

        # Current file opened
        self.currentParameterFile = ""

        # Current file run
        self.currentParameterFileRun = ""

        # Report information
        self.settings[self.backendTypeKey()] = ["Backend", True]
        self.settings[self.reportTypeKey()] = ["Report Type", True]
        self.settings[self.classificationKey()] = ["Classification", True]
        self.settings[self.fileNameKey()] = ["File Name", False]
        self.settings[self.mutablesFileKey()] = ["Mutables File", False]
        self.settings[self.structureFileKey()] = ["Structure File", False]
        self.settings[self.structureEndFileKey()] = ["Analyst Authored Results Section", False]
        self.settings[self.artifactFileKey()] = ["Artifact File", False]
        self.settings[self.outputFolderKey()] = ["Output Folder", True]
        self.settings[self.verbosityKey()] = ["Verbosity", False]

        # General Options
        self.settings[self.titleKey()] = ["Title", False]
        self.settings[self.numberKey()] = ["Number", False]
        self.settings[self.issueKey()] = ["Issue", False]
        self.settings[self.versionsKey()] = ["Versions", False]
        self.settings[self.authorsKey()] = ["Authors", False]
        self.settings[self.organizationsKey()] = ["Organizations", False]
        self.settings[self.locationKey()] = ["Location", False]
        self.settings[self.yearKey()] = ["Year", False]
        self.settings[self.monthKey()] = ["Month", False]
        self.settings[self.abstractFileKey()] = ["Abstract File", False]
        self.settings[self.prefaceKey()] = ["Preface", False]
        self.settings[self.thanksKey()] = ["Thanks", False]
        self.settings[self.executiveSummaryKey()] = ["Executive Summary", False]
        self.settings[self.nomenclatureKey()] = ["Nomenclature", False]
        self.settings[self.finalKey()] = ["Final", False]
        self.settings[self.keySeparatorKey()] = ["Key Separator", False]

        # Data
        self.settings[self.dataFolderKey()] = ["Model Directory", False]
        self.settings[self.inputDeckKey()] = ["Input Deck", False]
        self.settings[self.geometryRootKey()] = ["Geometry Root", False]
        self.settings[self.reportedCadMetaDataKey()] = ["Reported CAD Metadata", False]
        self.settings[self.logFileKey()] = ["Log File", False]
        self.settings[self.ignoredBlocksKey()] = ["Ignored Blocks", False]
        self.settings[self.bijectiveMappingsKey()] = ["Bijective Mapping", False]
        self.settings[self.cadToFemKey()] = ["CAD to FEM", False]
        self.settings[self.femToCadKey()] = ["FEM to CAD", False]

        # Return list of missing settings
        return missingSettings

    def initializeUserSettings(self):

        # Read settings
        missingAdmin, missingSettings = self.userSettingsReader.read()

        # Exit early if ADMIN level config file is missing
        if missingAdmin:
            print("** ERROR: No complete config file at ADMIN level \'{}\'. Exiting. ".format(
                self.scriptDirectoryConfigFilePath))
            sys.exit(1)
        elif missingSettings:
            return missingSettings

        # Python executable
        self.argPythonExePath = self.userSettingsReader.getPythonExecutable().replace('\\', '/')
        print("\t{} = {}".format(self.getArgPythonExePathUserSettingsKey(), self.argPythonExePath))

        # Python packages
        self.argPythonSitePackagePath = self.userSettingsReader.getPythonSitePackage().replace('\\', '/')
        print("\t{} = {}".format(self.getArgPythonSitePackagePathUserSettingsKey(), self.argPythonSitePackagePath))

        # ARG.py script
        self.argScriptPath = self.userSettingsReader.getArgScript().replace('\\', '/')
        print("\t{} = {}".format(self.getArgScriptPathUserSettingsKey(), self.argScriptPath))

        # LaTeX processor
        self.argLatexProcessorPath = self.userSettingsReader.getLatexProcessor().replace('\\', '/')
        print("\t{} = {}".format(self.getArgLatexProcessorPathUserSettingsKey(), self.argLatexProcessorPath))

    def saveSettings(self, data):

        # Write current set of settings to config file at script directory location
        if self.userSettingsWriter.write(self.userHomeConfigFilePath, data):

            # Save current set of settings as RunTime paths
            self.setArgPythonExePath(data[self.getArgPythonExePathUserSettingsKey()])
            self.setArgPythonSitePackagePath(data[self.getArgPythonSitePackagePathUserSettingsKey()])
            self.setArgScriptPath(data[self.getArgScriptPathUserSettingsKey()])
            self.setArgLatexProcessorPath(data[self.getArgLatexProcessorPathUserSettingsKey()])

        else:
            print("*  WARNING: Current set of settings could not be saved:\n\t{}".format(data))

    def getCompanyName(self):
        return "ARG"

    def getToolName(self):
        return "ARG-GUI"

    def getRecentMenuSettings(self):
        return "Recent Menu"

    def getSaveBeforeRunSettings(self):
        return "SaveBeforeRunEnabled"

    def getConfigArgPythonExePath(self):
        return self.userSettingsReader.getPythonExecutable()

    def readConfigArgPythonExePath(self):
        return self.userSettingsReader.readPythonExecutable(self.userSettingsReader.usrLvlPath)

    def getArgPythonExePath(self):
        return self.argPythonExePath

    def getArgPythonExePathLabel(self):
        return "Python executable"

    def getArgPythonExePathKey(self):
        return "argPythonExePath"

    def getArgPythonExePathUserSettingsKey(self):
        return "python_executable"

    def getArgPythonExePathToolTip(self):
        return "Fill the line edit with the complete path of the Python executable to be used to run ARG."

    def setArgPythonExePath(self, pythonExePath):
        self.argPythonExePath = pythonExePath

    def getConfigArgPythonSitePackagePath(self):
        return self.userSettingsReader.getPythonSitePackage()

    def readConfigArgPythonSitePackagePath(self):
        return self.userSettingsReader.readPythonSitePackage(self.userSettingsReader.usrLvlPath)

    def getArgPythonSitePackagePath(self):
        return self.argPythonSitePackagePath

    def getArgPythonSitePackagePathLabel(self):
        return "Python site-packages folder"

    def getArgPythonSitePackagePathKey(self):
        return "argPythonSitePackagePath"

    def getArgPythonSitePackagePathUserSettingsKey(self):
        return "python_site_package"

    def getArgPythonSitePackagePathToolTip(self):
        return "Fill the line edit with the complete path to the site-packages directory required by Python. <br><br>" \
               "(e.g: '<code>.../Python.framework/Versions/3.7/lib/python3.7/site-packages</code>')"

    def setArgPythonSitePackagePath(self, pythonSitePackagePath):
        self.argPythonSitePackagePath = pythonSitePackagePath

    def getConfigArgScriptPath(self):
        return self.userSettingsReader.getArgScript()

    def readConfigArgScriptPath(self):
        return self.userSettingsReader.readArgScript(self.userSettingsReader.usrLvlPath)

    def getArgScriptPathLabel(self):
        return "ARG.py script"

    def getArgScriptPathKey(self):
        return "argScriptPath"

    def getArgScriptPathUserSettingsKey(self):
        return "arg_script"

    def getArgScriptPathToolTip(self):
        return "Fill the line edit with the complete path to '<code>ARG.py</code>' script."

    def getArgScriptPath(self):
        return self.argScriptPath

    def setArgScriptPath(self, scriptPath):
        self.argScriptPath = scriptPath

    def getConfigArgLatexProcessorPath(self):
        return self.userSettingsReader.getLatexProcessor()

    def readConfigArgLatexProcessorPath(self):
        return self.userSettingsReader.readLatexProcessor(self.userSettingsReader.usrLvlPath)

    def getArgLatexProcessorPath(self):
        return self.argLatexProcessorPath

    def getArgLatexProcessorPathLabel(self):
        return "Latexmk processor"

    def getArgLatexProcessorPathKey(self):
        return "argLatexProcessorPath"

    def getArgLatexProcessorPathUserSettingsKey(self):
        return "latex_processor"

    def getArgLatexProcessorPathToolTip(self):
        return "Fill the line edit with the complete path to Latexmk processor executable.<br><br>\
                (e.g: '<code>.../bin/latexmk</code>')<br><br><br>\
                <i><u>Note</u>: The <code>Latexmk</code> processor is not part of ARG, the ability to call it from ARG is provided as a convenience.</i>"

    def setArgLatexProcessorPath(self, latexProcessorPath):
        self.argLatexProcessorPath = latexProcessorPath

    def getCurrentParameterFile(self):
        return self.currentParameterFile

    def setCurrentParameterFile(self, filePath):
        self.currentParameterFile = filePath

    def getCurrentParameterFileRun(self):
        return self.currentParameterFileRun

    def setCurrentParameterFileRun(self, filePath):
        self.currentParameterFileRun = filePath

    def settingsValue(self, keyFunction, keyValue):
        app = 'ARG-GUI'
        if keyValue == None:
            return self.settings.get(keyFunction())
        elif keyValue < 3:
            return self.settings.get(keyFunction())[keyValue]
        else:
            print("[{}] Could not find value for parameter \'{}\'.".format(app, keyFunction))
            return ""

    # ARG execution option
    def eOption(self):
        return "-e"

    def gOption(self):
        return "-g"

    # Report information
    def backendTypeKey(self):
        return "BackendType"

    def backendTypeParameterFileKey(self):
        return "backend_type"

    def backendTypeValue(self, keyValue=None):
        return self.settingsValue(self.backendTypeKey, keyValue)

    def backendTypeKeyWord(self):
        return "Word"

    def backendTypeKeyLatex(self):
        return "LaTeX"

    def reportTypeKeyReport(self):
        return "Report"

    def reportTypeKey(self):
        return "ReportType"

    def reportTypeParameterFileKey(self):
        return "report_type"

    def reportTypeValue(self, keyValue=None):
        return self.settingsValue(self.reportTypeKey, keyValue)

    def classificationKey(self):
        return "Classification"

    def classificationParameterFileKey(self):
        return "classification"

    def classificationKeyGeneric(self):
        return "Generic"

    def classificationValue(self, keyValue=None):
        return self.settingsValue(self.classificationKey, keyValue)

    def fileNameKey(self):
        return "File Name"

    def fileNameParameterFileKey(self):
        return "file_name"

    def fileNameValue(self, keyValue=None):
        return self.settingsValue(self.fileNameKey, keyValue)

    def mutablesFileKey(self):
        return "Mutables"

    def mutablesFileParameterFileKey(self):
        return "mutables"

    def mutablesFileValue(self, keyValue=None):
        return self.settingsValue(self.mutablesFileKey, keyValue)

    def structureFileKey(self):
        return "StructureFile"

    def structureFileParameterFileKey(self):
        return "structure"

    def structureFileValue(self, keyValue=None):
        return self.settingsValue(self.structureFileKey, keyValue)

    def structureEndFileKey(self):
        return "StructureEnd"

    def structureEndFileParameterFileKey(self):
        return "structure_end"

    def structureEndFileValue(self, keyValue=None):
        return self.settingsValue(self.structureEndFileKey, keyValue)

    def artifactFileKey(self):
        return "ArtifactFile"

    def artifactFileParameterFileKey(self):
        return "artifact"

    def artifactFileValue(self, keyValue=None):
        return self.settingsValue(self.artifactFileKey, keyValue)

    def outputFolderKey(self):
        return "OutputDir"

    def outputFolderParameterFileKey(self):
        return "output"

    def outputFolderValue(self, keyValue=None):
        return self.settingsValue(self.outputFolderKey, keyValue)

    def verbosityKey(self):
        return "Verbosity"

    def verbosityParameterFileKey(self):
        return "verbosity"

    def verbosityKeyTerse(self):
        return "Terse"

    def verbosityKeyTerseAsInt(self):
        return -1

    def verbosityKeyDefault(self):
        return "Default"

    def verbosityKeyDefaultAsInt(self):
        return 0

    def verbosityKeyVerbose(self):
        return "Verbose"

    def verbosityKeyVerboseAsInt(self):
        return 1

    def verbosityValue(self, keyValue=None):
        return self.settingsValue(self.verbosityKey, keyValue)

    # General Options
    def titleKey(self):
        return "Title"

    def titleValue(self, keyValue=None):
        return self.settingsValue(self.titleKey, keyValue)

    def titleParameterFileKey(self):
        return "title"

    def numberKey(self):
        return "Number"

    def numberValue(self, keyValue=None):
        return self.settingsValue(self.numberKey, keyValue)

    def numberParameterFileKey(self):
        return "number"

    def issueKey(self):
        return "Issue"

    def issueValue(self, keyValue=None):
        return self.settingsValue(self.issueKey, keyValue)

    def issueParameterFileKey(self):
        return "issue"

    def versionsKey(self):
        return "Versions"

    def versionsValue(self, keyValue=None):
        return self.settingsValue(self.versionsKey, keyValue)

    def versionParameterFileKey(self):
        return "version"

    def authorsKey(self):
        return "Authors"

    def authorsValue(self, keyValue=None):
        return self.settingsValue(self.authorsKey, keyValue)

    def authorParameterFileKey(self):
        return "author"

    def organizationsKey(self):
        return "Organizations"

    def organizationsValue(self, keyValue=None):
        return self.settingsValue(self.organizationsKey, keyValue)

    def organizationParameterFileKey(self):
        return "organization"

    def locationKey(self):
        return "Location"

    def locationValue(self, keyValue=None):
        return self.settingsValue(self.locationKey, keyValue)

    def locationParameterFileKey(self):
        return "location"

    def yearKey(self):
        return "Year"

    def yearValue(self, keyValue=None):
        return self.settingsValue(self.yearKey, keyValue)

    def yearParameterFileKey(self):
        return "year"

    def monthKey(self):
        return "Month"

    def monthValue(self, keyValue=None):
        return self.settingsValue(self.monthKey, keyValue)

    def monthParameterFileKey(self):
        return "month"

    def abstractFileKey(self):
        return "AbstractFile"

    def abstractFileValue(self, keyValue=None):
        return self.settingsValue(self.abstractFileKey, keyValue)

    def abstractFileParameterFileKey(self):
        return "abstract"

    def prefaceKey(self):
        return "Preface"

    def prefaceValue(self, keyValue=None):
        return self.settingsValue(self.prefaceKey, keyValue)

    def prefaceParameterFileKey(self):
        return "preface"

    def thanksKey(self):
        return "Thanks"

    def thanksValue(self, keyValue=None):
        return self.settingsValue(self.thanksKey, keyValue)

    def thanksParameterFileKey(self):
        return "thanks"

    def executiveSummaryKey(self):
        return "ExecutiveSummary"

    def executiveSummaryValue(self, keyValue=None):
        return self.settingsValue(self.executiveSummaryKey, keyValue)

    def executiveSummaryParameterFileKey(self):
        return "executive_summary"

    def nomenclatureKey(self):
        return "Nomenclature"

    def nomenclatureValue(self, keyValue=None):
        return self.settingsValue(self.nomenclatureKey, keyValue)

    def nomenclatureParameterFileKey(self):
        return "nomenclature"

    def finalKey(self):
        return "Final"

    def finalValue(self, keyValue=None):
        return self.settingsValue(self.finalKey, keyValue)

    def finalParameterFileKey(self):
        return "final"

    def keySeparatorKey(self):
        return "KeySeparator"

    def keySeparatorDefault(self):
        return ";"

    def keySeparatorValue(self, keyValue=None):
        return self.settingsValue(self.keySeparatorKey, keyValue)

    def keySeparatorParameterFileKey(self):
        return "key_separator"

    # Data
    def dataFolderKey(self):
        return "DataDirectory"

    def dataFolderParameterFileKey(self):
        return "data"

    def dataFolderDefault(self):
        return '.'

    def dataFolderValue(self, keyValue=None):
        return self.settingsValue(self.dataFolderKey, keyValue)

    def solutionCasesKey(self):
        return "SolutionCases"

    def solutionCasesParameterFileKey(self):
        return "solution_cases"

    def solutionCasesValue(self, keyValue=None):
        return self.settingsValue(self.solutionCasesKey, keyValue)

    def solutionCasesLabelsList(self):
        return ["Type", "Ignored Blocks", "Mode minimum value", "Mode maximum value"]

    def solutionCasesAddKey(self):
        return "Add solution case"

    def solutionCasesRemoveKey(self):
        return "Remove solution case"

    def solutionCasesTypeKey(self):
        return "type"

    def solutionCasesTypeValues(self):
        return ["eigen"]

    def solutionCasesIgnoredBlocksKey(self):
        return "ignored_blocks"

    def solutionCasesModeKey(self):
        return "modes"

    def cadParametersSectionKey(self):
        return "CAD Parameters"

    def geometryRootKey(self):
        return "GeometryRoot"

    def geometryRootParameterFileKey(self):
        return "geometry_root"

    def geometryRootValue(self, keyValue=None):
        return self.settingsValue(self.geometryRootKey, keyValue)

    def reportedCadMetaDataKey(self):
        return "ReportedCadMetaData"

    def reportedCadMetaDataParameterFileKey(self):
        return "reported_cad_metadata"

    def reportedCadMetaDataValue(self, keyValue=None):
        return self.settingsValue(self.reportedCadMetaDataKey, keyValue)

    def femParametersSectionKey(self):
        return "FEM Parameters"

    def inputDeckKey(self):
        return "DeckRoot"

    def inputDeckParameterFileKey(self):
        return "input_deck"

    def inputDeckValue(self, keyValue=None):
        return self.settingsValue(self.inputDeckKey, keyValue)

    def logFileKey(self):
        return "LogFile"

    def logFileParameterFileKey(self):
        return "log_file"

    def logFileValue(self, keyValue=None):
        return self.settingsValue(self.logFileKey, keyValue)

    def ignoredBlocksKey(self):
        return "IgnoredBlockKeys"

    def ignoredBlocksParameterFileKey(self):
        return "ignored_blocks"

    def ignoredBlocksValue(self, keyValue=None):
        return self.settingsValue(self.ignoredBlocksKey, keyValue)

    def mappingsSectionKey(self):
        return "Mappings"

    def bijectiveMappingsKey(self):
        return "Mappings"

    def bijectiveMappingsValue(self, keyValue=None):
        return self.settingsValue(self.bijectiveMappingsKey, keyValue)

    def bijectiveMappingsParameterFileKey(self):
        return "mappings"

    def cadToFemKey(self):
        return "CAD_to_FEM"

    def cadToFemValue(self, keyValue=None):
        return self.settingsValue(self.cadToFemKey, keyValue)

    def cadToFemAddKey(self):
        return "Add CAD to FEM"

    def cadToFemRemoveKey(self):
        return "Remove CAD to FEM"

    def cadToFemHeaderLabelsList(self):
        return ["CAD parts", "FEM blocks ", "Factors"]

    def femToCadKey(self):
        return "FEM_to_CAD"

    def femToCadValue(self, keyValue=None):
        return self.settingsValue(self.femToCadKey, keyValue)

    def femToCadAddKey(self):
        return "Add FEM to CAD"

    def femToCadRemoveKey(self):
        return "Remove FEM to CAD"

    def femToCadHeaderLabelsList(self):
        return ["FEM blocks ", "CAD parts", "Factors"]

    def elementsKey(self):
        return "elements"

    def factorsKey(self):
        return "factors"

    # Inserts
    def insertionKey(self):
        return "Insert"

    def insertionParameterFileKey(self):
        return "insert_in"

    def insertionValue(self, keyValue=None):
        return self.settingsValue(self.insertionKey(), keyValue)

    def insertionLocationKey(self):
        return "location"

    def insertionTypeTextKey(self):
        return "string"

    def insertionTypeImageKey(self):
        return "image"

    def insertionAddKey(self):
        return "Add insert"

    def insertionRemoveKey(self):
        return "Remove insert"

    def insertHeaderLabelsList(self):
        return ["Location", "Type", "Text / Image Path"]

    def textParameterFileKey(self):
        return "string"

    def textValue(self, keyValue=None):
        return self.settingsValue(self.textKey, keyValue)

    def imageParameterFileKey(self):
        return "image"

    def imageValue(self, keyValue=None):
        return self.settingsValue(self.imageKey, keyValue)
