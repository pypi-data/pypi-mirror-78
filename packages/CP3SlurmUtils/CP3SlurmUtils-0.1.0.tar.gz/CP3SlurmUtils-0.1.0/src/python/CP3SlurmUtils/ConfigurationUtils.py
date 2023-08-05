"""
Copyright (C) 2019  Universite catholique de Louvain, Belgium.

This file is part of CP3SlurmUtils.

CP3SlurmUtils is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CP3SlurmUtils is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CP3SlurmUtils.  If not, see <http://www.gnu.org/licenses/>.
"""

import ast
import collections
import datetime
import os
import random
import re
import site
import string
import subprocess

from CP3SlurmUtils import SpellChecker
from CP3SlurmUtils.Exceptions import ConfigurationException
from CP3SlurmUtils.Exceptions import CP3SlurmUtilsException

try:
    import configparser
except ImportError:
    import ConfigParser as configparser
defaultsCfg = configparser.ConfigParser()
defaultsCfg.add_section('USER_CONFIG_DEFAULTS')
defaultsCfg.set('USER_CONFIG_DEFAULTS', 'sbatch_partition', 'cp3')
defaultsCfg.set('USER_CONFIG_DEFAULTS', 'sbatch_qos', 'cp3')
defaultsCfg.set('USER_CONFIG_DEFAULTS', 'sbatch_time', '0-04:00')
defaultsCfg.set('USER_CONFIG_DEFAULTS', 'sbatch_memPerCPU', '2048')
defaultsCfg.set('USER_CONFIG_DEFAULTS', 'scratchDir', '${LOCALSCRATCH}')
defaultsCfg.add_section('USER_CONFIG_VALID_VALUES')
defaultsCfg.set('USER_CONFIG_VALID_VALUES', 'sbatch_partition', 'Def,cp3,cp3-fast,cp3-gpu')
defaultsCfg.set('USER_CONFIG_VALID_VALUES', 'sbatch_qos', 'normal,cp3,cp3-gpu')
defaultsCfg.set('USER_CONFIG_VALID_VALUES', 'environmentType', 'cms')
defaultsCfg.add_section('USER_CONFIG_PARTITIONS_FOR_QOS')
defaultsCfg.set('USER_CONFIG_PARTITIONS_FOR_QOS', 'qos_cp3', 'cp3,cp3-fast')
defaultsCfg.set('USER_CONFIG_PARTITIONS_FOR_QOS', 'qos_cp3-gpu', 'cp3-gpu')
defaultsCfg.set('USER_CONFIG_PARTITIONS_FOR_QOS', 'alternative_qos', 'normal')
xdgConfigDirsDef = os.path.join(os.path.sep, 'etc', 'xdg')
xdgConfigDirs = os.getenv('XDG_CONFIG_DIRS', xdgConfigDirsDef)
if xdgConfigDirs.strip() == '':
    xdgConfigDirs = xdgConfigDirsDef
xdgConfigHomeDef = os.path.join(os.path.expanduser('~'), '.config')
xdgConfigHome = os.getenv('XDG_CONFIG_HOME', xdgConfigHomeDef)
if xdgConfigHome.strip() == '':
    xdgConfigHome = xdgConfigHomeDef
siteUserBase = site.USER_BASE
virtualenv = os.getenv('VIRTUAL_ENV')
defaultsCfgLocations = {
    'system'     : [os.path.join(os.path.sep, 'etc', 'CP3SlurmUtils', 'defaults.cfg')] + \
                   [os.path.join(xdgConfigDir.strip(), 'CP3SlurmUtils', 'defaults.cfg') for xdgConfigDir in xdgConfigDirs.split(':') if xdgConfigDir.strip()],
    'local'      : [os.path.join(siteUserBase, 'etc', 'CP3SlurmUtils', 'defaults.cfg')],
    'user'       : [os.path.join(xdgConfigHome, 'CP3SlurmUtils', 'defaults.cfg')],
    'virtualenv' : [os.path.join(virtualenv, 'etc', 'CP3SlurmUtils', 'defaults.cfg')] if virtualenv else [],
}
defaultsCfg.read(defaultsCfgLocations['system'] + defaultsCfgLocations['local'] + defaultsCfgLocations['user'] + defaultsCfgLocations['virtualenv'])

timestamp = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f"))
randomstr = ''.join(random.choice(string.ascii_lowercase) for i in range(4))


validConfigParams = collections.OrderedDict({
    'sbatch_partition'            : {'mandatory': False, 'type': str,                        'default': defaultsCfg.get('USER_CONFIG_DEFAULTS', 'sbatch_partition'), 'sbatch_option_long': 'partition',   'sbatch_option_short': 'p'},
    'sbatch_qos'                  : {'mandatory': False, 'type': str,                        'default': defaultsCfg.get('USER_CONFIG_DEFAULTS', 'sbatch_qos'),       'sbatch_option_long': 'qos',         'sbatch_option_short': None},
    'sbatch_time'                 : {'mandatory': False, 'type': str,                        'default': defaultsCfg.get('USER_CONFIG_DEFAULTS', 'sbatch_time'),      'sbatch_option_long': 'time',        'sbatch_option_short': 't'},
    'sbatch_memPerCPU'            : {'mandatory': False, 'type': str,                        'default': defaultsCfg.get('USER_CONFIG_DEFAULTS', 'sbatch_memPerCPU'), 'sbatch_option_long': 'mem-per-cpu', 'sbatch_option_short': None},
    'sbatch_chdir'                : {'mandatory': False, 'type': str,                        'default': '.',                                                         'sbatch_option_long': 'chdir',       'sbatch_option_short': 'D'},
    'sbatch_output'               : {'mandatory': False, 'type': str,                        'default': '',                                                          'sbatch_option_long': 'output',      'sbatch_option_short': 'o'},
    'sbatch_error'                : {'mandatory': False, 'type': str,                        'default': '',                                                          'sbatch_option_long': 'error',       'sbatch_option_short': 'e'},
    'sbatch_additionalOptions'    : {'mandatory': False, 'type': list, 'element_type': str,  'default': []},
    'scratchDir'                  : {'mandatory': False, 'type': str,                        'default': defaultsCfg.get('USER_CONFIG_DEFAULTS', 'scratchDir')},
    'handleScratch'               : {'mandatory': False, 'type': bool,                       'default': False},
    'environmentType'             : {'mandatory': False, 'type': str,                        'default': ''},
    'cmsswDir'                    : {'mandatory': False, 'type': str,                        'default': ''},
    'inputSandboxContent'         : {'mandatory': False, 'type': list, 'element_type': str,  'default': []},
    'inputSandboxDir'             : {'mandatory': False, 'type': str,                        'default': '<config.sbatch_chdir>'},
    'inputSandboxFilename'        : {'mandatory': False, 'type': str,                        'default': 'input_sandbox_{}_{}.tar.gz'.format(timestamp, randomstr)},
    'batchScriptsDir'             : {'mandatory': False, 'type': str,                        'default': '<config.sbatch_chdir>'},
    'batchScriptsFilename'        : {'mandatory': False, 'type': str,                        'default': 'slurm_batch_script_{}_{}.sh'.format(timestamp, randomstr)},
    'stageout'                    : {'mandatory': False, 'type': bool,                       'default': True},
    'stageoutFiles'               : {'mandatory': False, 'type': list, 'element_type': str,  'default': []},
    'stageoutDir'                 : {'mandatory': False, 'type': str,                        'default': '<config.sbatch_chdir>'},
    'writeLogsOnWN'               : {'mandatory': False, 'type': bool,                       'default': True},
    'separateStdoutStderrLogs'    : {'mandatory': False, 'type': bool,                       'default': False},
    'stdoutFilename'              : {'mandatory': False, 'type': str,                        'default': ''},
    'stderrFilename'              : {'mandatory': False, 'type': str,                        'default': ''},
    'stageoutLogs'                : {'mandatory': False, 'type': bool,                       'default': True},
    'stageoutLogsDir'             : {'mandatory': False, 'type': str,                        'default': '<config.stageoutDir>/logs'},
    'useJobArray'                 : {'mandatory': False, 'type': bool,                       'default': True},
    'maxRunningJobs'              : {'mandatory': False, 'type': int,                        'default': None},
    'numJobs'                     : {'mandatory': False, 'type': int,                        'default': None},
    'inputParamsNames'            : {'mandatory': False, 'type': list, 'element_type': str,  'default': []},
    'inputParams'                 : {'mandatory': False, 'type': list, 'element_type': list, 'default': []},
    'payload'                     : {'mandatory': True,  'type': str,                        'default': None},
})

renamedParams = [
]

deprecatedParams = [
]

invalidConfigMsg = "ERROR: Invalid Configuration:"


def strip(string, separator=''):
    if separator:
        return separator.join([s.strip() for s in string.split(separator) if s.strip()])
    else:
        return string.strip()


def fixConfigDefaults(config):
    """_fixConfigDefaults_
    Change the default values of some configuration parameters
    depending on the actual values of other configuration parameters.
    """
    if getattr(config, 'writeLogsOnWN', validConfigParams['writeLogsOnWN']['default']):
        validConfigParams['sbatch_output']['default'] = "/dev/null"
        validConfigParams['sbatch_error']['default'] = "/dev/null"
    if getattr(config, 'useJobArray', validConfigParams['useJobArray']['default']): 
        validConfigParams['stdoutFilename']['default'] = "slurm-${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.out"
        validConfigParams['stderrFilename']['default'] = "slurm-${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.err"
    else:
        validConfigParams['stdoutFilename']['default'] = "slurm-${SLURM_JOB_ID}.out"
        validConfigParams['stderrFilename']['default'] = "slurm-${SLURM_JOB_ID}.err"


def setConfigDefaults(config):
    """_setConfigDefaults_
    Apply the default values to the optional attributes that are not
    already set.
    """
    for paramName, paramSpecs in list(validConfigParams.items()):
        if paramSpecs['mandatory']:
            continue
        if getattr(config, paramName, None) is None or (paramSpecs['type'] == str and getattr(config, paramName) == ''):
            refParamName = paramName
            refParamSpecs = paramSpecs
            n = 0
            while (getattr(config, refParamName, None) is None or (refParamSpecs['type'] == str and getattr(config, refParamName) == '')) and \
                  (isinstance(refParamSpecs['default'], str) and '<' in refParamSpecs['default'] and '>' in refParamSpecs['default']):
                refParamName, postStr = refParamSpecs['default'].split('<config.')[1].split('>')
                preStr = refParamSpecs['default'].split('<config.')[0]
                if refParamName not in validConfigParams:
                    msg = "ERROR: Default value for parameter '{param}' is referencing an invalid parameter '{reference_param}'."
                    msg = msg.format(param=paramName, reference_param=refParamName)
                    raise CP3SlurmUtilsException(msg)
                refParamSpecs = validConfigParams[refParamName]
                n += 1
                if n > len(validConfigParams):
                    msg = "ERROR: Seems parameter '{param}' will not be able to get a default value."
                    msg += "\nLooped already {0} times, which is more than the number of available configuration parameters ({1})."
                    msg = msg.format(n, len(validConfigParams), param=paramName)
                    raise CP3SlurmUtilsException(msg)
            if refParamName != paramName:
                if isinstance(getattr(config, refParamName, refParamSpecs['default']), str):
                    setattr(config, paramName, preStr + getattr(config, refParamName, refParamSpecs['default']) + postStr)
                else:
                    setattr(config, paramName, getattr(config, refParamName, refParamSpecs['default']))
            else:
                setattr(config, paramName, paramSpecs['default'])


def validateConfigBeforeDefaults(config):
    """_validateConfigBeforeDefaults_
    Do a validation of a Configuration before any defauls are appield.
    """
    validateConfigBasic(config)
    validateConfigDirs(config)


def checkType(attr, requiredType):
    """_checkType_
    Check the type of an attribute.
    """
    if isinstance(attr, bool) and requiredType == int:
        return False
    return isinstance(attr, requiredType)


def validateConfigBasic(config):
    """_validateConfigBasic_
    Do a basic validation of a Configuration.
    """
    # Some parameters may have been renamed. Check if there is an old
    # parameter and tell the user what is the new parameter name.
    for renamedParam in renamedParams:
        if hasattr(config, renamedParam['oldName']):
            msg = invalidConfigMsg
            msg += "\nParameter '{param}' has been renamed to '{new_param}'. Please change your configuration file accordingly."
            msg = msg.format(param=renamedParam['oldName'], new_param=renamedParam['newName'])
            raise ConfigurationException(msg)
    # Check if there is a deprecated parameter.
    for deprecatedParam in deprecatedParams:
        if hasattr(config, deprecatedParam['name']):
            msg = invalidConfigMsg
            msg += "\nParameter '{param}' has been deprecated in version {version}."
            if deprecatedParam['msg']:
                msg += "\n{message}"
            msg = msg.format(param=deprecatedParam['name'], version=deprecatedParam['version'], message=deprecatedParam['msg'])
            raise ConfigurationException(msg)
    # Check the type of the existing parameters.
    for paramName, paramSpecs in list(validConfigParams.items()):
        if getattr(config, paramName, None) is None:
            continue
        attr = getattr(config, paramName)
        if not checkType(attr, paramSpecs['type']):
            msg = invalidConfigMsg
            msg += "\nParameter '{param}' is not of type '{type}'."
            msg = msg.format(param=paramName, type=paramSpecs['type'])
            raise ConfigurationException(msg)
        # Remove leading and trailing spaces in configuration parameters that are strings.
        if paramSpecs['type'] == str:
            if paramName == 'sbatch_partition':
                setattr(config, paramName, strip(attr, ','))
            else:
                setattr(config, paramName, strip(attr))
        if paramSpecs['type'] == list:
            for i, el in enumerate(attr):
                if not checkType(el, paramSpecs['element_type']):
                    msg = invalidConfigMsg
                    msg += "\nList element {0} in parameter '{param}' is not of type '{type}'."
                    msg = msg.format(i, param=paramName, type=paramSpecs['element_type'])
                    raise ConfigurationException(msg)
            # Remove leading and trailing spaces in configuration parameters that are lists of strings.
            # Remove also empty strings.
            if paramSpecs['element_type'] == str:
                setattr(config, paramName, [s for s in list(map(str.strip, attr)) if s])
    # Check if there is an unknown parameter and try to suggest the correct parameter name.
    SpellChecker.DICTIONARY = SpellChecker.train(list(validConfigParams.keys()))
    for param in config.getConfigAttrs_():
        if not SpellChecker.is_correct(param):
            msg = invalidConfigMsg
            msg += "\nParameter '{param}' is not known."
            if SpellChecker.correct(param) != param:
                msg += " Maybe you mean '{suggested_param}'?"
            msg = msg.format(param=param, suggested_param=SpellChecker.correct(param))
            raise ConfigurationException(msg)
    checkMandatoryConfigParams(config)


def checkMandatoryConfigParams(config, params=None):
    """_checkMandatoryConfigParams_
    Check the mandatory parameters of a Configuration.
    params: a sublist of parameters to check.
    """
    # Mandatory parameters should be there and can not have an empty value.
    for paramName, paramSpecs in list(validConfigParams.items()):
        if params and paramName not in params:
            continue
        if paramSpecs['mandatory']:
            if not hasattr(config, paramName):
                msg = invalidConfigMsg
                msg += "\nParameter '{param}' is mandatory."
                msg = msg.format(param=paramName)
                raise ConfigurationException(msg)
            elif getattr(config, paramName) in [None, [], {}] or (paramSpecs['type'] == str and getattr(config, paramName) == ''):
                msg = invalidConfigMsg
                msg += "\nParameter '{param}' is mandatory (and can not be defined as None or an empty string/list/dict)."
                msg = msg.format(param=paramName)
                raise ConfigurationException(msg)


def validateConfigDirs(config):
    """_validateConfigDirs_
    Validate the directories of a Configuration checking that they
    do not point to an existing file.
    """
    for paramName, paramSpecs in list(validConfigParams.items()):
        if not paramName.endswith('Dir'):
            continue
        if getattr(config, paramName, None) is None:
            continue
        dirName = getattr(config, paramName)
        if os.path.isfile(dirName):
            msg = invalidConfigMsg
            msg += "\nThe directory provided in parameter '{param}' is already an existing file: {value}"
            msg = msg.format(param=paramName, value=dirName)
            raise ConfigurationException(msg)


def validateConfigAfterDefaults(config):
    """_validateConfigAfterDefaults_
    Do a basic validation of a Configuration assuming defaults were applied.
    """
    paramNotDefinedMsg = invalidConfigMsg+"\nParameter '{param}' is not defined."
    paramInvalidValueMsg = invalidConfigMsg+"\nParameter '{param}' has an invalid value: '{value}'."
    paramInvalidValueMsgSuggest = paramInvalidValueMsg+"\nValid values are: '{valid}'."
    # Check that there are no sbatch options specified in 'sbatch_additionalOptions'
    # for which we already have a configuration parameter available.
    for paramName, paramSpecs in list(validConfigParams.items()):
        if paramName.startswith('sbatch_') and paramName != 'sbatch_additionalOptions':
            sbatchOptLong = paramSpecs['sbatch_option_long']
            sbatchOptShort = paramSpecs['sbatch_option_short']
            sbatchAddOpts = [opt.split('=')[0].strip() for opt in config.sbatch_additionalOptions]
            if ('--{}'.format(sbatchOptLong) in sbatchAddOpts):
                msg = invalidConfigMsg
                msg += "\nPlease use the configuration parameter '{param}'"
                msg += " instead of setting the --{long_option} sbatch option in 'sbatch_additionalOptions'."
                msg = msg.format(param=paramName, long_option=sbatchOptLong)
                raise ConfigurationException(msg)
            if sbatchOptShort and ('-{}'.format(sbatchOptShort) in sbatchAddOpts):
                msg = invalidConfigMsg
                msg += "\nPlease use the configuration parameter '{param}'"
                msg += " instead of setting the -{short_option} sbatch option in 'sbatch_additionalOptions'."
                msg = msg.format(param=paramName, short_option=sbatchOptShort)
                raise ConfigurationException(msg)
    # Check that time, memory and partition are defined.
    # We do not make these parameters mandatory in validConfigParams,
    # because in principle there are default values for them.
    # But since the default values can be omitted in defaults.cfg,
    # we have to make sure that these parameters are defined.
    if not config.sbatch_time:
        msg = paramNotDefinedMsg.format(param='sbatch_time')
        raise ConfigurationException(msg)
    if not config.sbatch_memPerCPU:
        msg = paramNotDefinedMsg.format(param='sbatch_memPerCPU')
        raise ConfigurationException(msg)
    if not config.sbatch_partition:
        msg = paramNotDefinedMsg.format(param='sbatch_partition')
        raise ConfigurationException(msg)
    # Check the partition.
    validPartitions = [ x for x in strip(defaultsCfg.get('USER_CONFIG_VALID_VALUES', 'sbatch_partition'), ',').split(',') if x ]
    if validPartitions:
        for partition in config.sbatch_partition.split(','):
            if partition not in validPartitions:
                msg = paramInvalidValueMsg
                msg += "\nIt should be a string of comma separated cluster partitions. Acceptable partitions are: '{valid}'."
                msg = msg.format(param='sbatch_partition', value=config.sbatch_partition, valid="', '".join(validPartitions))
                raise ConfigurationException(msg)
    # Check the qos.
    if config.sbatch_qos:
        validQOSs = [ x for x in strip(defaultsCfg.get('USER_CONFIG_VALID_VALUES', 'sbatch_qos'), ',').split(',') if x ]
        if validQOSs:
            if config.sbatch_qos not in validQOSs:
                msg = paramInvalidValueMsgSuggest.format(param='sbatch_qos', value=config.sbatch_qos, valid="', '".join(validQOSs))
                raise ConfigurationException(msg)
        # Check the compatibility between qos and partition.
        if defaultsCfg.has_option('USER_CONFIG_PARTITIONS_FOR_QOS', 'qos_'+config.sbatch_qos):
            partitionsForQOS = [ x for x in strip(defaultsCfg.get('USER_CONFIG_PARTITIONS_FOR_QOS', 'qos_'+config.sbatch_qos), ',').split(',') if x ]
            if partitionsForQOS:
                for partition in config.sbatch_partition.split(','):
                    if partition not in partitionsForQOS:
                        msg = invalidConfigMsg
                        msg += "\nParameters 'sbatch_partition' and 'sbatch_qos' have incompatible values:"
                        msg += "\nsbatch_partition: '{partition}'"
                        msg += "\nsbatch_qos: '{qos}'"
                        msg += "\nQuality of service '{qos}' is forbidden on cluster partitions other than '{partitions_for_qos}' (jobs would be accepted anyway, but would never start running)."
                        alternativeQOS = defaultsCfg.get('USER_CONFIG_PARTITIONS_FOR_QOS', 'alternative_qos')
                        if alternativeQOS:
                            msg += "\nThus, when submitting jobs to a cluster partition that is not in the above list, the quality of service should be set to '{alternative_qos}'."
                        msg = msg.format(partition=config.sbatch_partition, qos=config.sbatch_qos, partitions_for_qos="', '".join(partitionsForQOS), alternative_qos=alternativeQOS)
                        raise ConfigurationException(msg)
    # Check the environmentType.
    if config.environmentType:
        validEnvTypes = [ x for x in strip(defaultsCfg.get('USER_CONFIG_VALID_VALUES', 'environmentType'), ',').split(',') if x ]
        if validEnvTypes:
            if config.environmentType.lower() not in validEnvTypes:
                msg = paramInvalidValueMsg
                msg += "\nValid values are (apart from the empty string or None): '{valid}'."
                msg = msg.format(param='environmentType', value=config.environmentType, valid="', '".join(validEnvTypes))
                raise ConfigurationException(msg)
        # For CMS jobs, check that a CMSSW work area was given, that it exists and is a directory.
        if config.environmentType.lower() == 'cms':
            if not config.cmsswDir:
                msg = invalidConfigMsg
                msg += "\nParameter 'environmentType' is set to 'cms', but parameter 'cmsswDir' was not specified."
                msg += "\nTo setup the CMS environment, a CMSSW work area has to be specified where to run the cmsenv command."
                msg += "\nIf you don't need to setup the CMS environment, set 'environmentType' to an empty string or None."
                raise ConfigurationException(msg)
            if not os.path.isdir(config.cmsswDir):
                msg = invalidConfigMsg
                msg += "\nParameter '{param}' does not correspond to an existing directory: '{value}'."
                msg = msg.format(param='cmsswDir', value=config.cmsswDir)
                raise ConfigurationException(msg)
    # Check that at least one of 'numJobs' or 'inputParams' was specified.
    if config.numJobs is None and len(config.inputParams) == 0:
        msg = invalidConfigMsg
        msg += "\nAt least one of 'numJobs' or 'inputParams' must be specified (with a sensitive value)."
        raise ConfigurationException(msg)
    # Check that 'numJobs' is either None or a positive integer.
    # If positive, and if there are input parameters for the jobs,
    # check that there are enough input parameters for all jobs.
    if config.numJobs is not None:
        if config.numJobs <= 0:
            msg = invalidConfigMsg
            msg += "\nParameter 'numJobs' must be a positive integer (or None)."
            raise ConfigurationException(msg)
        if 0 < len(config.inputParams) and len(config.inputParams) < config.numJobs:
            msg = invalidConfigMsg
            msg += "\nThe length of the 'inputParams' list ({0}) is smaller than 'numJobs' ({1})."
            msg = msg.format(len(config.inputParams), config.numJobs)
            raise ConfigurationException(msg)
    # Check that 'maxRunningJobs' is either None or a non-negative integer.
    if config.maxRunningJobs is not None:
        if config.maxRunningJobs < 0:
            msg = invalidConfigMsg
            msg += "\nParameter 'maxRunningJobs' must be a non-negative integer (or None)."
            raise ConfigurationException(msg)
    # Check the consistency in length between the lists 'inputParamsNames' and 'inputParams'.
    if config.inputParamsNames and not config.inputParams:
        msg = invalidConfigMsg
        msg += "\nInconsistency between 'inputParamsNames' and 'inputParams'."
        msg += "\nYou provided 'inputParamsNames', but not 'inputParams'."
        msg += "\nEither both of them have to be provided or none of them."
        raise ConfigurationException(msg)
    if not config.inputParamsNames and config.inputParams:
        msg = invalidConfigMsg
        msg += "\nInconsistency between 'inputParamsNames' and 'inputParams'."
        msg += "\nYou provided 'inputParams', but not 'inputParamsNames'."
        msg += "\nEither both of them have to be provided or none of them."
        raise ConfigurationException(msg)
    numJobInputParams = len(config.inputParamsNames)
    if numJobInputParams > 0:
        for i, jobInputParams in enumerate(config.inputParams):
            if len(jobInputParams) != numJobInputParams:
                msg = invalidConfigMsg
                msg += "\nInconsistency between 'inputParamsNames' and 'inputParams'."
                msg += "\nThe list element {0} of the 'inputParams' list contains {1} parameters"
                msg += " while according to the list 'inputParamsNames' there should be {2} parameters per job."
                msg = msg.format(i, len(jobInputParams), numJobInputParams)
                raise ConfigurationException(msg)
    # If 'stageout' is True, and if there are user files to stageout,
    # then 'stageoutDir' must be specified.
    if config.stageout and config.stageoutFiles and not config.stageoutDir:
        msg = invalidConfigMsg
        msg += "\nParameter 'stageout' is True, but parameter 'stageoutDir' was not specified (while there are -a priori- files to stageout)."
        raise ConfigurationException(msg)
    # If 'writeLogsOnWN' is True, there should be no sbatch --output or --error option specified.
    if config.writeLogsOnWN:
        if config.sbatch_output != '/dev/null' or config.sbatch_error != '/dev/null': 
            msg = invalidConfigMsg
            msg += "\nParameters 'writeLogsOnWN' and 'sbatch_output'/'sbatch_error' are mutually exclusive."
            msg += "\nNote: You either write the logs on the WN (and eventually stage them out)"
            msg += " or you use the 'sbatch_output'/'sbatch_error' options (eventually leaving them empty so to use slurm defaults)"
            msg += " to let the logs be created outside the WN."
            raise ConfigurationException(msg)
    # Make a sanity check of the input sandbox, batch script and logs filenames.
    paramInvalidRegexMsg = paramInvalidValueMsg + "\nIt should contain only the following characters: a-zA-Z0-9${{}}._-"
    if config.inputSandboxFilename:
        if not re.match("^[a-zA-Z0-9${}._-]+$", config.inputSandboxFilename):
            msg = paramInvalidRegexMsg.format(param='inputSandboxFilename', value=config.inputSandboxFilename)
            raise ConfigurationException(msg)
    if config.batchScriptsFilename:
        if not re.match("^[a-zA-Z0-9${}._-]+$", config.batchScriptsFilename):
            msg = paramInvalidRegexMsg.format(param='batchScriptsFilename', value=config.batchScriptsFilename)
            raise ConfigurationException(msg)
    if config.stdoutFilename:
        if not re.match("^[a-zA-Z0-9${}._-]+$", config.stdoutFilename):
            msg = paramInvalidRegexMsg.format(param='stdoutFilename', value=config.stdoutFilename)
            raise ConfigurationException(msg)
    if config.stderrFilename:
        if not re.match("^[a-zA-Z0-9${}._-]+$", config.stderrFilename):
            msg = paramInvalidRegexMsg.format(param='stderrFilename', value=config.stderrFilename)
            raise ConfigurationException(msg)
    # If 'stageoutLogs' is True, then 'writeLogsOnWN' must also be True.
    if config.stageoutLogs and not config.writeLogsOnWN:
        msg = invalidConfigMsg
        msg += "\nParameter 'stageoutLogs' is True, but parameter 'writeLogsOnWN' is False."
        raise ConfigurationException(msg)
    # If 'stageoutLogs' is True, then 'stageoutLogsDir' must be specified.
    if config.stageoutLogs and not config.stageoutLogsDir:
        msg = invalidConfigMsg
        msg += "\nParameter 'stageoutLogs' is True, but parameter 'stageoutLogsDir' was not specified."
        raise ConfigurationException(msg)


def fixConfigDirs(config):
    """_fixConfigDirs_
    Replace relative paths by absolute paths in a Configuration.
    Expand ~.
    """
    for paramName, paramSpecs in list(validConfigParams.items()):
        if not paramName.endswith('Dir'):
            continue
        if getattr(config, paramName, None) is None:
            continue
        dirName = getattr(config, paramName)
        if dirName and not dirName.startswith('$'):
            dirName = os.path.expanduser(dirName)
            dirName = os.path.abspath(dirName)
        setattr(config, paramName, dirName)


def createConfigDirs(config):
    """_createConfigDirs_
    Create the directories of a Configuration.
    """
    for paramName, paramSpecs in list(validConfigParams.items()):
        if paramName not in ['inputSandboxDir', 'batchScriptsDir']:
            continue
        if not getattr(config, paramName, None):
            continue
        returncode = subprocess.call(['mkdir', '-p', getattr(config, paramName)])
        if returncode != 0:
            msg = "ERROR: Failed to create directory {}".format(getattr(config, paramName))
            raise CP3SlurmUtilsException(msg)
