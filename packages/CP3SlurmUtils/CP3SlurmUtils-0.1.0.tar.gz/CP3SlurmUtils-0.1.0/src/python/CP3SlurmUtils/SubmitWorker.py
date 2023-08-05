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

import collections
import glob
import os
import re
import signal
import subprocess

import CP3SlurmUtils.Py2Py3Helpers
from CP3SlurmUtils.Configuration import loadConfiguration
from CP3SlurmUtils.Configuration import Configuration
from CP3SlurmUtils.ConfigurationUtils import validateConfigBeforeDefaults
from CP3SlurmUtils.ConfigurationUtils import fixConfigDefaults
from CP3SlurmUtils.ConfigurationUtils import setConfigDefaults
from CP3SlurmUtils.ConfigurationUtils import validateConfigAfterDefaults
from CP3SlurmUtils.ConfigurationUtils import fixConfigDirs
from CP3SlurmUtils.ConfigurationUtils import createConfigDirs
from CP3SlurmUtils.Exceptions import CP3SlurmUtilsException
from CP3SlurmUtils.InteractiveQuestion import interactiveYesNoQuestion
from CP3SlurmUtils.InteractiveQuestion import questionTimeoutHandler
from CP3SlurmUtils.InteractiveQuestion import TimeoutException
from CP3SlurmUtils.SubmitUtils import submit


class SubmitWorker:

    def __init__(self, config=None, submit=False, yes=False, summaryJobs='', debug=False, quiet=False, calledFromScript=False):
        """SubmitWorker constructor."""

        self.calledFromScript = calledFromScript

        if isinstance(debug, bool):
            self.debug = debug
        else:
            msg = "ERROR: {} argument 'debug' must be a boolean.".format(self.__class__.__name__)
            raise CP3SlurmUtilsException(msg)

        if isinstance(quiet, bool):
            self.quiet = quiet
        else:
            msg = "ERROR: {} argument 'quiet' must be a boolean.".format(self.__class__.__name__)
            raise CP3SlurmUtilsException(msg)

        if isinstance(submit, bool):
            self.submit = submit
        else:
            msg = "ERROR: {} argument 'submit' must be a boolean.".format(self.__class__.__name__)
            raise CP3SlurmUtilsException(msg)

        if isinstance(yes, bool):
            self.yes = yes
        else:
            msg = "ERROR: {} argument 'yes' must be a boolean.".format(self.__class__.__name__)
            raise CP3SlurmUtilsException(msg)

        if isinstance(summaryJobs, str):
            self.summaryJobs = []
            for v in [j for j in map(str.strip, summaryJobs.split(',')) if j]:
                if not re.match('^[1-9][0-9]*$', v):
                    if self.calledFromScript:
                        msg = "ERROR: Option --summary-jobs has an invalid value: '{value}'. It must be a comma separated list of positive integers.".format(value=v)
                    else:
                        msg = "ERROR: Argument 'summaryJobs' has an invalid value: '{value}'. It must be a comma separated list of positive integers.".format(value=v)
                    raise CP3SlurmUtilsException(msg)
                if int(v) not in self.summaryJobs:
                    self.summaryJobs.append(int(v))
            self.summaryJobs = sorted(self.summaryJobs)
        else:
            msg = "ERROR: {} argument 'summaryJobs' must be a string.".format(self.__class__.__name__)
            raise CP3SlurmUtilsException(msg)

        self.config = None
        self.configValidated = False
        if config is not None:
            self.loadConfig(config)


    def loadConfig(self, config):
        """Load and validate the configuration."""

        self.configValidated = False

        if isinstance(config, Configuration):
            self.config = config
        elif isinstance(config, str):
            if not os.path.isfile(config):
                msg = "ERROR: Could not find configuration file {file}".format(file=config)
                raise CP3SlurmUtilsException(msg)
            if not self.quiet:
                print("Using configuration file {file}".format(file=config))
            self.config = loadConfiguration(config)
            if self.debug:
                print("Configuration loaded.")
        else:
            msg = "ERROR: {} argument 'config' must be a Configuration object or a string representing a filename.".format(self.__class__.__name__)
            raise CP3SlurmUtilsException(msg)

        self.validateConfig()


    def validateConfig(self):
        """Validate the configuration."""

        validateConfigBeforeDefaults(self.config)

        if self.debug:
            print("Configuration passed first validation.")

        fixConfigDefaults(self.config)

        if self.debug:
            print("Configuration parameter defaults redefined.")

        setConfigDefaults(self.config)

        if self.debug:
            print("Configuration parameter defaults assigned.")

        validateConfigAfterDefaults(self.config)

        if self.debug:
            print("Configuration passed final validation.")

        fixConfigDirs(self.config)

        if self.debug:
            print("Directory paths in configuration completed.")

        createConfigDirs(self.config)

        if self.debug:
            print("Directories from configuration created.")

        self.configValidated = True


    def __call__(self):
        """Run all the workload for submission."""

        if self.config is None:
            msg = "ERROR: There is no configuration defined."
            raise CP3SlurmUtilsException(msg)

        if not self.quiet:
            print("Preparing the jobs ...")

        if not self.configValidated:
            self.validateConfig()

        # For commodity, put all the configuration parameters in local variables
        # and from now on the config object should not be used anymore.
        # If some parameters need to be adjusted, it should not be done on the config object, but on these variables.
        sbatch_partition            = self.config.sbatch_partition
        sbatch_qos                  = self.config.sbatch_qos
        sbatch_chdir                = self.config.sbatch_chdir
        sbatch_time                 = self.config.sbatch_time
        sbatch_memPerCPU            = self.config.sbatch_memPerCPU
        sbatch_output               = self.config.sbatch_output
        sbatch_error                = self.config.sbatch_error
        sbatch_additionalOptions    = self.config.sbatch_additionalOptions
        writeLogsOnWN               = self.config.writeLogsOnWN
        stdoutFilename              = self.config.stdoutFilename
        stderrFilename              = self.config.stderrFilename
        separateStdoutStderrLogs    = self.config.separateStdoutStderrLogs
        scratchDir                  = self.config.scratchDir
        handleScratch               = self.config.handleScratch
        environmentType             = self.config.environmentType
        cmsswDir                    = self.config.cmsswDir
        inputSandboxContent         = self.config.inputSandboxContent
        inputSandboxDir             = self.config.inputSandboxDir
        inputSandboxFilename        = self.config.inputSandboxFilename
        batchScriptsDir             = self.config.batchScriptsDir
        batchScriptsFilename        = self.config.batchScriptsFilename
        stageout                    = self.config.stageout
        stageoutDir                 = self.config.stageoutDir
        stageoutFiles               = self.config.stageoutFiles
        stageoutLogs                = self.config.stageoutLogs
        stageoutLogsDir             = self.config.stageoutLogsDir
        useJobArray                 = self.config.useJobArray
        maxRunningJobs              = self.config.maxRunningJobs
        numJobs                     = self.config.numJobs
        inputParamsNames            = self.config.inputParamsNames
        inputParams                 = self.config.inputParams
        payload                     = self.config.payload

        if writeLogsOnWN:
            sbatch_output = '/dev/null'
            sbatch_error = '/dev/null'

        environmentType = environmentType.strip().lower()
        if self.debug:
            print("The environment type is '{env}'.".format(env=environmentType))

        numJobInputParams = len(inputParamsNames)
        if numJobs is None:
            numJobs = len(inputParams)
        elif numJobs < len(inputParams):
            if self.debug:
                msg = "The 'inputParams' list in the configuration contains more parameters than necessary for {num} jobs."
                msg += " Will use only the first {num} sets of input parameters from 'inputParams'."
                msg = msg.format(num=numJobs)
                print(msg)
            inputParams = inputParams[:numJobs]

        if self.summaryJobs and numJobInputParams == 0:
            if not self.quiet:
                if self.calledFromScript:
                    print("Ignoring option --summary-jobs, because no input parameters for the job's payload were specified" + \
                          " (the job's payload input parameters are the only information that would be shown in the summary at a per job basis).")
                else:
                    print("Ignoring argument 'summaryJobs', because no input parameters for the job's payload were specified" + \
                          " (the job's payload input parameters are the only information that would be shown in the summary at a per job basis).")
            self.summaryJobs = []
        for i, v in enumerate(self.summaryJobs):
            if v > numJobs:
                if not self.quiet:
                    if self.calledFromScript:
                        msg = "Option --summary-jobs has values that are bigger than the total number of jobs ({num}): {0}."
                        msg += " Will ignore these particular values."
                        msg = msg.format(self.summaryJobs[i:], num=numJobs)
                        print(msg)
                    else:
                        msg = "Argument 'summaryJobs' has values that are bigger than the total number of jobs ({num}): {0}."
                        msg += " Will ignore these particular values."
                        msg = msg.format(self.summaryJobs[i:], num=numJobs)
                        print(msg)
                self.summaryJobs = self.summaryJobs[:i]
                break

        jobArrayTaskIds = ''
        if useJobArray:
            if maxRunningJobs is None:
                maxRunningJobs = 0
            if self.debug:
                print("Will prepare a batch script for a slurm job array of {num} jobs.".format(num=numJobs))
                if maxRunningJobs > 0:
                    print("Will limit the number of concurrently running jobs to {}.".format(maxRunningJobs))
            if numJobs == 1:
                jobArrayTaskIds = '1'
            else:
                jobArrayTaskIds = '1-{}'.format(numJobs)
                if maxRunningJobs > 0:
                    jobArrayTaskIds += '%{}'.format(maxRunningJobs)
            if self.debug:
                print("Defined job array task ids as '{ids}'.".format(ids=jobArrayTaskIds))
        else:
            if self.debug:
                print("Will prepare {num} batch scripts for {num} independent jobs.".format(num=numJobs))

        #================================================================================
        # Define lists with the job log files and with the stageout files
        #================================================================================

        logFiles = []
        if writeLogsOnWN:
            if stageoutLogs:
                logFilesWN = [stdoutFilename]
                if separateStdoutStderrLogs:
                    logFilesWN += [stderrFilename]
                for f in logFilesWN:
                    logFiles.append('{}/{}'.format(stageoutLogsDir, f))
        else:
            if sbatch_output:
                if sbatch_output != '/dev/null':
                    if os.path.isabs(sbatch_output):
                        logFiles.append(sbatch_output)
                    else:
                        logFiles.append('{}/{}'.format(sbatch_chdir, sbatch_output))
            else:
                if useJobArray:
                    logFiles.append('{}/slurm-${{SLURM_ARRAY_JOB_ID}}_${{SLURM_ARRAY_TASK_ID}}.out'.format(sbatch_chdir))
                else:
                    logFiles.append('{}/slurm-${{SLURM_JOB_ID}}.out'.format(sbatch_chdir))
            if sbatch_error:
                if sbatch_error != '/dev/null':
                    if os.path.isabs(sbatch_error):
                        logFiles.append(sbatch_error)
                    else:
                        logFiles.append('{}/{}'.format(sbatch_chdir, sbatch_error))

        stageoutFiles = [s.strip() for s in stageoutFiles if s.strip()]

        #================================================================================
        # Prepare the input sandbox
        #================================================================================

        inputSandbox = ''
        if inputSandboxContent:
            if self.debug:
                print("Creating input sandbox.")
            inputSandbox = '{}/{}'.format(inputSandboxDir, inputSandboxFilename)
            args = ['tar', '-czf', inputSandbox]
            missingFiles = []
            for isc in inputSandboxContent:
                if os.path.isabs(isc):
                    msg = "ERROR: The files to add to the input sandbox should be given with relative paths, not absolute paths."
                    if self.calledFromScript:
                        msg += " The paths should be relative to the directory from where you are running the slurm_submit command."
                    raise CP3SlurmUtilsException(msg)
                files = glob.glob(isc)
                if not files:
                    missingFiles.append(isc)
                else:
                    args += files
            if missingFiles:
                msg = "ERROR: Some of the files that were requested to be added to the input sandbox were not found: {files}.".format(files=missingFiles)
                raise CP3SlurmUtilsException(msg)
            else:
                returncode = subprocess.call(args)
            if returncode != 0:
                msg = "ERROR: Failed to create input sandbox."
                raise CP3SlurmUtilsException(msg)
            if self.debug:
                print("Input sandbox created.")
        else:
            if self.debug:
                print("No input sanbox was created.")

        #================================================================================
        # Prepare the bash code that will set the job input parameters
        #================================================================================

        # A few lines of bash code to put the job input parameters in environment variables.
        # This code will be inserted before the payload.
        # For independent jobs we have one set of lines of code per job.
        setInputParamsCode = []
        if numJobInputParams > 0:
            if self.debug:
                print("Preparing bash code for reading input parameters for job's payload.")
            if useJobArray:
                inputParamsStr = ""
                for j in range(numJobs):
                    inputParamsStr += "\n\"{}\"".format(' <sep> '.join(list(map(str, inputParams[j]))))
                    if j == numJobs - 1: inputParamsStr += "\n"
                setInputParamsCodeStr = "inputParams=({})".format(inputParamsStr)
                setInputParamsCodeStr += "\njobInputParams=\"${inputParams[${SLURM_ARRAY_TASK_ID}-1]}\""
                for i in range(numJobInputParams):
                    setInputParamsCodeStr += "\nexport {paramName}=`echo -e \"${{jobInputParams}}\" | awk -F' <sep> ' '{{print ${paramNum}}}'`".format(paramName=inputParamsNames[i], paramNum=i+1)
                    setInputParamsCodeStr += "\necho \"{paramName} = ${{{paramName}}}\"".format(paramName=inputParamsNames[i])
                setInputParamsCode.append(setInputParamsCodeStr)
            else:
                for j in range(numJobs):
                    setInputParamsCodeStr = ""
                    for i in range(numJobInputParams):
                        if i > 0:
                            setInputParamsCodeStr += "\n"
                        setInputParamsCodeStr += "export {paramName}={paramValue}".format(paramName=inputParamsNames[i], paramValue=inputParams[j][i])
                        setInputParamsCodeStr += "\necho \"{paramName} = ${{{paramName}}}\"".format(paramName=inputParamsNames[i])
                    setInputParamsCode.append(setInputParamsCodeStr)
            if self.debug:
                print("Code for reading input parameters for job's payload created.")
        else:
            setInputParamsCodeStr = "echo \"No input parameters were defined for the payload.\""
            if self.debug:
                print("No code for reading input parameters for job's payload was created.")

        #================================================================================
        # Construct the batch script template
        #================================================================================

        if self.debug:
            print("Constructing batch scripts template.")

        batchScriptTemplate = \
"""\
#!/bin/bash
#
#SBATCH --chdir=__SBATCH_CHDIR__
#SBATCH --time=__SBATCH_TIME__
#SBATCH --mem-per-cpu=__SBATCH_MEM_PER_CPU__
#SBATCH --partition=__SBATCH_PARTITION__
"""
        if sbatch_qos:
            batchScriptTemplate += \
"""\
#SBATCH --qos=__SBATCH_QOS__
"""
        if useJobArray:
            batchScriptTemplate += \
"""\
#SBATCH --array=__SBATCH_ARRAY__
"""
        if sbatch_output:
            batchScriptTemplate += \
"""\
#SBATCH --output=__SBATCH_OUTPUT__
"""
        if sbatch_error:
            batchScriptTemplate += \
"""\
#SBATCH --error=__SBATCH_ERROR__
"""
        if sbatch_additionalOptions:
            batchScriptTemplate += \
"""\
__SBATCH_ADDITIONAL_OPTIONS__
"""
        sbatchAdditionalOptionsStr = ""
        if sbatch_additionalOptions:
            for i, sbatchAddOpt in enumerate(sbatch_additionalOptions):
                sbatchAdditionalOptionsStr += "#SBATCH {}".format(sbatchAddOpt)
                if i < len(sbatch_additionalOptions)-1:
                    sbatchAdditionalOptionsStr += "\n"
        batchScriptTemplate += \
"""\

#==================================================================================

# This variable keeps the exit code with which the batch script will exit.
exitCode=0
exitCodeMeaning=""

function updateExitCode() {
    [[ ${exitCode} -ne 0 ]] || exitCode=${1}
}

startupWorkDir=`pwd`
"""
        if scratchDir:
            if handleScratch:
                batchScriptTemplate += \
"""\

#==================================================================================
# Create the job's scratch directory
#==================================================================================

if [[ ! -d __SCRATCH_DIR__ ]]
then
    mkdir -p __SCRATCH_DIR__
fi
"""
            batchScriptTemplate += \
"""\

#==================================================================================
# Change directory to the job's scratch directory
#==================================================================================

scratchDirErrorMsg=""
if [[ -d __SCRATCH_DIR__ ]]
then
    cd __SCRATCH_DIR__ || updateExitCode 100
else
    scratchDirErrorMsg="Local scratch directory __SCRATCH_DIR__ does not exist."
    updateExitCode 100
fi
"""
        batchScriptTemplate += \
"""\

#==================================================================================
# Redirect stdout and stderr to local file(s)
#==================================================================================

writeLogsOnWN=__WRITE_LOGS_ON_WN__
separateStdoutStderrLogs=__SEPARATE_STDOUT_STDERR_LOGS__
stdoutFilename="__STDOUT_FILENAME__"
stderrFilename="__STDERR_FILENAME__"

if [[ "${writeLogsOnWN}" == "true" ]]
then
    # Redirect stdout and stderr to local file(s).
    if [[ "${separateStdoutStderrLogs}" == "true" ]]
    then
        exec 1> "${stdoutFilename}" 2> "${stderrFilename}"
    else
        exec 1> "${stdoutFilename}" 2>&1
    fi
fi

#==================================================================================
# Print some info about the job
#==================================================================================

echo "======== Starting job (`date`) ========"
echo "Job id: ${SLURM_JOB_ID}"
echo "List of nodes allocated to the job: ${SLURM_JOB_NODELIST}"
echo "Batch node: ${SLURMD_NODENAME}"
"""
        if scratchDir:
            batchScriptTemplate += \
"""\
echo "Startup working directory: ${startupWorkDir}"

if [[ ${exitCode} -eq 0 ]]
then
    echo "Job working directory: `pwd`"
elif [[ "${scratchDirErrorMsg}" != "" ]]
then
    echo ${scratchDirErrorMsg}
fi
"""
        else:
            batchScriptTemplate += \
"""\
echo "Working directory: ${startupWorkDir}"
"""
        if environmentType == 'cms':
            batchScriptTemplate += \
"""\

#==================================================================================
# Set up the environment
#==================================================================================

cmsswDir="__CMSSW_DIR__"

function setupEnvironment() {
    # Set up the CMS environment
    echo "Sourcing CMS environment file /cvmfs/cms.cern.ch/cmsset_default.sh"
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    [[ $? -eq 0 ]] || return 1
    # Set up the runtime CMS environment for the given CMSSW work area
    if [[ ! -z "${cmsswDir}" ]]
    then
        echo "CMSSW work area directory: ${cmsswDir}"
        if [[ ! -d "${cmsswDir}" ]]
        then
            echo "CMSSW work area directory does not exist."
            return 1
        fi
        currentDir=`pwd`
        cd "${cmsswDir}" || return 1
        echo "Running cmsenv"
        eval `scramv1 runtime -sh`
        cd "${currentDir}"
    fi
}

if [[ ${exitCode} -eq 0 ]]
then
    echo "==== Starting setup of CMS environment (`date`) ===="
    setupEnvironment || updateExitCode 101
    echo "==== Finished setup of CMS environment (`date`) ===="
fi
"""
        if inputSandbox:
            batchScriptTemplate += \
"""\

#==================================================================================
# Stage in and unpack the input sandbox
#==================================================================================

inputSandbox="__INPUT_SANDBOX__"
inputSandboxDir="$(dirname ${inputSandbox})"

function copy_and_unpack_input_sandbox() {
    case "${inputSandbox}" in
        *\ * )
            echo "Only one input sandbox (max. size 100 MB) should be copied. Will not continue."
            return 1
            ;;
    esac
    echo "Input sandbox file: ${inputSandbox}"
    if [[ ! -f "${inputSandbox}" ]]
    then
        echo "Input sandbox does not exist."
        return 1
    fi
    # Check that input sandbox is not bigger than 100 MB.
    local inputSandboxSize=`du -m "${inputSandbox}" | awk '{print $1}'`
    if [[ ${inputSandboxSize} -gt 100 ]]
    then
        echo "Input sandbox size (${inputSandboxSize} MB) greater than 100 MB. Will not continue."
        return 1
    fi
    echo "Input sanbox contents:"
    tar -ztvf "${inputSandbox}" | awk '{$1=$2=$3=$4=$5=""; print $0}'
    if [[ ${SLURM_JOB_NUM_NODES} -gt 1 ]]
    then
        execFile="${inputSandboxDir}/stagein-ISB"
        echo "Will create executable file ${execFile} to be run via srun in order to stagein the input sandbox to all allocated worker nodes." 
        if [[ -f "${execFile}" ]]
        then
            echo "A file ${execFile} already exists. Please remove it or rename it."
            return 1
        fi
        cat > "${execFile}" <<EOF
#!/bin/bash

function run_cmd() {
    cmd=("\${@}")
    ec=0
"""
            if scratchDir:
                batchScriptTemplate += \
"""\
    tmplog=__SCRATCH_DIR__/$(basename ${execFile}).err
"""
            else:
                batchScriptTemplate += \
"""\
    tmplog=/tmp/$(basename ${execFile}).err
"""
            batchScriptTemplate += \
"""\
    "\${cmd[@]}" 2> \${tmplog} >/dev/null || ec=1
    while read line
    do
        >&2 echo "\`hostname -f\`: \$line"
    done < \${tmplog};
    rm \${tmplog}
    return \$ec
}

inputSandbox="\${1}"
echo "\`hostname -f\`: Copying and unpacking input sandbox ..."
run_cmd cp "\${inputSandbox}" .
if [[ \$? -eq 0 ]]
then
    run_cmd tar -zxf "\$(basename \${inputSandbox})"
    if [[ \$? -eq 0 ]]
    then
        echo "\`hostname -f\`: Input sandbox copied and unpacked."
    else
        echo "\`hostname -f\`: Failed to unpack input sandbox."
        exit 1
    fi
else
    echo "\`hostname -f\`: Failed to copy input sandbox."
    exit 1
fi
EOF
        chmod 0700 "${execFile}"
        if [[ -x "${execFile}" ]]
        then
            echo "Executable file ${execFile} created."
        else
            echo "Failed to create executable file ${execFile}"
            return 1
        fi
        srun --ntasks-per-node=1 "${execFile}" "${inputSandbox}"
        ec=$?
        echo "Removing previously created file ${execFile}"
        rm -f "${execFile}"
        return $ec
    else
        echo "Copying and unpacking input sandbox ..."
        cp "${inputSandbox}" .
        if [[ $? -eq 0 ]]
        then
            tar -zxf "$(basename ${inputSandbox})"
            if [[ $? -eq 0 ]]
            then
                echo "Input sandbox copied and unpacked."
            else
                echo "Failed to unpack input sandbox."
                return 1
            fi
        else
            echo "Failed to copy input sandbox."
            return 1
        fi
    fi
}

if [[ ${exitCode} -eq 0 ]]
then
    echo "==== Starting stagein of input sandbox (`date`) ===="
    if [[ -n "${inputSandbox}" ]]
    then
        copy_and_unpack_input_sandbox || updateExitCode 102
    else
        echo "No input sandbox was specified for stagein."
    fi
    echo "==== Finished stagein of input sandbox (`date`) ===="
fi
"""
        batchScriptTemplate += \
"""\

#==================================================================================
# Read the job input arguments (if any) and run the payload
#==================================================================================
"""
        if setInputParamsCode:
            batchScriptTemplate += \
"""\

if [[ ${exitCode} -eq 0 ]]
then
    echo "==== Starting read of input parameters for job's payload (`date`) ===="
    __SET_INPUT_PARAMS_CODE__
    echo "==== Finished read of input parameters for job's payload (`date`) ===="
fi
"""
        batchScriptTemplate += \
"""\

if [[ ${exitCode} -eq 0 ]]
then
    echo "==== Starting execution of payload (`date`) ===="
    echo "------------------------- Begin payload output ------------------------"
    (
__PAYLOAD__
    )
    pec=$?
    echo "--------------------------- End payload output ------------------------"
    echo "Payload exit code: ${pec}"
    if [[ ${pec} -ne 0 ]]
    then
        if [[ ${pec} -ge 100 && ${pec} -le 113 ]]
        then
            echo "Payload exit code is in range 100-113, which is reserved for batch script non-payload errors." \\
                 "Setting batch script exit code to 103."
            updateExitCode 103
        else
            if [[ ${pec} -lt 79 || ${pec} -gt 99 ]]
            then
                echo "Payload exit code is outside the recommended range for user-defined exit codes: 79-99." \\
                     "This is not a problem, but if you are interested in defining/using exit codes for your payload that would not occur outside your payload," \\
                     "please consider restricting to that range."
            fi
            updateExitCode ${pec}
            exitCodeMeaning="failure in user's payload"
        fi
    fi
    echo "==== Finished execution of payload (`date`) ===="
fi

#==================================================================================
# Stageout of user files
#==================================================================================

function stageout() {
    local filetype="${1}"
    local files=("")
    local dir=""
    if [[ "${filetype}" == "userfiles" ]]
    then
        files=("${stageoutFiles[@]}")
        dir="${stageoutDir}"
    elif [[ "${filetype}" == "logs" ]]
    then
        files=("${logFiles[@]}")
        dir="${stageoutLogsDir}"
    fi
    if [[ ! -n "${files}" ]]
    then
        echo "No files were specified for stageout."
        return 0
    fi
    if [[ ! -n "${dir}" ]]
    then
        echo "WARNING: The following files were requested for stageout:"
        echo "${files[@]}"
        echo "but no stageout directory was specified where to copy the files."
        echo "Will NOT stage out the files."
        return 0
    fi
    mkdir -p "${dir}"
    if [[ "${filetype}" == "logs" ]]
    then
        cp "${files[@]}" "${dir}/"
        return 0
    fi
    echo "Destination directory: ${dir}"
    if [[ ! -d "${dir}" ]]
    then
        echo "Destination directory does not exist and failed to create it."
        return 1
    fi
    function join_by() { local d=$1; shift; echo -n "$1"; shift; printf "%s" "${@/#/$d}"; }
    patterns=$(join_by "', '" "${files[@]}")
    echo "List of filename patterns to match against: '${patterns}'."
    if [[ ${SLURM_JOB_NUM_NODES} -gt 1 ]]
    then
        execFile="${dir}/stageout-OSB"
        echo "Will create executable file ${execFile} to be run via srun in order to stageout the user files from all allocated worker nodes." 
        if [[ -f "${execFile}" ]]
        then
            echo "A file ${execFile} already exists. Please remove it or rename it."
            return 1
        fi
        cat > "${execFile}" <<EOF
#!/bin/bash

function run_cmd() {
    cmd=("\${@}")
    ec=0
"""
        if scratchDir:
            batchScriptTemplate += \
"""\
    tmplog=__SCRATCH_DIR__/$(basename ${execFile}).err
"""
        else:
            batchScriptTemplate += \
"""\
    tmplog=/tmp/$(basename ${execFile}).err
"""
        batchScriptTemplate += \
"""\
    "\${cmd[@]}" 2> \${tmplog} >/dev/null || ec=1
    while read line
    do
        >&2 echo "\`hostname -f\`: \$line"
    done < \${tmplog};
    rm \${tmplog}
    return \$ec
}

files=("\${@}")
for pattern in "\${files[@]}"
do
    matchingFiles=()
    while IFS=  read -r -d $'\\\\0'
    do
        matchingFiles+=("\$REPLY")
    done < <(find -mindepth 1 -maxdepth 1 -name "\${pattern}" -print0)
    if [[ \${#matchingFiles[@]} -gt 0 ]]
    then
        for file in "\${matchingFiles[@]}"
        do
            echo "\`hostname -f\`: Copying file \${file/\.\//}"
            run_cmd cp -r "\${file}" "${dir}/"
            if [[ \$? -eq 0 ]]
            then
                echo "\`hostname -f\`: File copied."
            else
                echo "\`hostname -f\`: Failed to copy file."
                exit 1
            fi
        done
    else
        echo "\`hostname -f\`: No files matching pattern '\${pattern}'."
        exit 1
    fi
done
EOF
        chmod 0700 "${execFile}"
        if [[ -x "${execFile}" ]]
        then
            echo "Executable file ${execFile} created."
        else
            echo "Failed to create executable file ${execFile}"
            return 1
        fi
        srun --ntasks-per-node=1 "${execFile}" "${files[@]}"
        ec=$?
        echo "Removing previously created file ${execFile}"
        rm -f "${execFile}"
        return $ec
    else
        for pattern in "${files[@]}"
        do
            matchingFiles=()
            while IFS=  read -r -d $'\\0'
            do
                matchingFiles+=("$REPLY")
            done < <(find -mindepth 1 -maxdepth 1 -name "${pattern}" -print0)
            if [[ ${#matchingFiles[@]} -gt 0 ]]
            then
                for file in "${matchingFiles[@]}"
                do
                    echo "Copying file ${file/\.\//} ..."
                    cp -r "${file}" "${dir}/"
                    if [[ $? -eq 0 ]]
                    then
                        echo "File copied."
                    else
                        echo "Failed to copy file."
                        return 1
                    fi
                done
            else
                echo "No files matching pattern '${pattern}'."
                return 1
            fi
        done
    fi
}

stageout=__STAGEOUT__
stageoutDir="__STAGEOUT_DIR__"
stageoutFiles=("__STAGEOUT_FILES__")

if [[ ${exitCode} -eq 0 ]]
then
    echo "==== Starting stageout of user files (`date`) ===="
    if [[ "${stageout}" == "true" ]]
    then
        stageout userfiles || updateExitCode 104
    else
        echo "Stageout flag is off. Will not stage out any user file."
    fi
    echo "==== Finished stageout of user files (`date`) ===="
fi

#==================================================================================
# Print a final exit status message
#==================================================================================

echo "======== Finished job (`date`) ========"

exitMsg="Batch script exit code: ${exitCode}"
if [[ ${exitCode} -eq 100 ]]
then
    exitCodeMeaning="failure in changing directory to the job's local scratch directory"
elif [[ ${exitCode} -eq 101 ]]
then
    exitCodeMeaning="failure in environment setup"
elif [[ ${exitCode} -eq 102 ]]
then
    exitCodeMeaning="failure in stagein/unpack of input sandbox"
elif [[ ${exitCode} -eq 103 ]]
then
    exitCodeMeaning="failure in user's payload"
elif [[ ${exitCode} -eq 104 ]]
then
    exitCodeMeaning="failure in stageout of user files"
fi
if [[ -n "${exitCodeMeaning}" ]]
then
    exitMsg+=" (${exitCodeMeaning})"
fi
echo "${exitMsg}"

#==================================================================================
# Stageout the logs and exit
#==================================================================================

stageoutLogs=__STAGEOUT_LOGS__
stageoutLogsDir="__STAGEOUT_LOGS_DIR__"

if [[ "${writeLogsOnWN}" == "true" && "${stageoutLogs}" == "true" ]]
then
    echo "Will stageout the logs before exiting."
    if [[ "${separateStdoutStderrLogs}" == "true" ]]
    then
        logFiles=("${stdoutFilename}" "${stderrFilename}")
    else
        logFiles=("${stdoutFilename}")
    fi
    stageout logs
fi
"""
        if scratchDir and handleScratch:
            batchScriptTemplate += \
"""\

#==================================================================================
# Remove the job's scratch directory
#==================================================================================

if [[ -d __SCRATCH_DIR__ ]]
then
    rm -rf __SCRATCH_DIR__
fi
"""
        batchScriptTemplate += \
"""\
#==================================================================================

exit ${exitCode}
"""

        if self.debug:
            print("Batch scripts template constructed.")

        #================================================================================
        # Create the bash script(s) from the template
        #================================================================================

        if self.debug:
            print("Creating batch script(s).")

        batchScripts = []

        replaceDict = {
            '__SBATCH_PARTITION__': sbatch_partition,
            '__SBATCH_QOS__': sbatch_qos,
            '__SBATCH_CHDIR__': sbatch_chdir,
            '__SBATCH_TIME__': sbatch_time,
            '__SBATCH_MEM_PER_CPU__': sbatch_memPerCPU,
            '__SBATCH_ARRAY__': jobArrayTaskIds,
            '__SBATCH_OUTPUT__': sbatch_output,
            '__SBATCH_ERROR__': sbatch_error,
            '__SBATCH_ADDITIONAL_OPTIONS__': sbatchAdditionalOptionsStr,
            '__WRITE_LOGS_ON_WN__': str(writeLogsOnWN).lower(),
            '__SEPARATE_STDOUT_STDERR_LOGS__': str(separateStdoutStderrLogs).lower(),
            '__STDOUT_FILENAME__': stdoutFilename,
            '__STDERR_FILENAME__': stderrFilename,
            '__SCRATCH_DIR__': scratchDir,
            '__CMSSW_DIR__': cmsswDir,
            '__INPUT_SANDBOX__': inputSandbox,
            '__PAYLOAD__': payload.strip('\n'),
            '__STAGEOUT__': str(stageout).lower(),
            '__STAGEOUT_DIR__': stageoutDir,
            '__STAGEOUT_FILES__': '" "'.join(stageoutFiles),
            '__STAGEOUT_LOGS__': str(stageoutLogs).lower(),
            '__STAGEOUT_LOGS_DIR__': stageoutLogsDir,
        }

        for j in range(numJobs):
            if setInputParamsCode:
                replaceDict['__SET_INPUT_PARAMS_CODE__'] = setInputParamsCode[j].replace('\n', '\n    ')
            batchScriptText = batchScriptTemplate
            for k, v in CP3SlurmUtils.Py2Py3Helpers.iteritems(replaceDict):
                batchScriptText = batchScriptText.replace(k, v)
            if useJobArray:
                batchScript = '{}/{}'.format(batchScriptsDir, batchScriptsFilename)
            else:
                if '.' in batchScriptsFilename:
                    batchScript = '{}/{}_{}.{}'.format(batchScriptsDir, '.'.join(batchScriptsFilename.split('.')[:-1]), j+1, batchScriptsFilename.split('.')[-1])
                else:
                    batchScript = '{}/{}_{}'.format(batchScriptsDir, batchScriptsFilename, j+1)
            try:
                with open(batchScript, 'w') as fd:
                    fd.write(batchScriptText)
            except IOError as ex:
                msg = "ERROR: Failed to create batch script(s)."
                msg += "\nError follows:\n{}"
                msg = msg.format(str(ex))
                raise CP3SlurmUtilsException(msg)
            batchScripts.append(batchScript)
            if useJobArray:
                break

        if self.debug:
            print("Batch script(s) created.")

        #================================================================================
        # Print a summary of what will be submitted
        #================================================================================

        if self.debug:
            print("Creating summary text.")

        summary = "================================================================================"
        summary += "\n=============  Below there is a summary of what would be submitted  ============"
        summary += "\n================================================================================"
        if useJobArray:
            summary += "\nWould submit a job array consisting of {num} jobs.".format(num=numJobs)
        else:
            summary += "\nWould submit {num} independent jobs.".format(num=numJobs)
        if numJobInputParams > 0:
            if self.summaryJobs:
                if self.calledFromScript:
                    summary += "\nInput parameters to the job's payload for the jobs specified in the --summary-jobs option."
                else:
                    summary += "\nInput parameters to the job's payload for the jobs specified in the 'summaryJobs' argument."
            else:
                self.summaryJobs = list(range(1,min(10,numJobs)+1))
                summary += "\nInput parameters to the job's payload for the first {num} jobs:".format(num=min(10,numJobs))
            for j in self.summaryJobs:
                summary += "\nJob {}:".format(j)
                for i in range(numJobInputParams):
                    summary += "\n    {paramName} = {paramValue}".format(paramName=inputParamsNames[i], paramValue=inputParams[j-1][i])
        else:
            summary += "\nNo input parameters would be passed to the job's payload."
        if batchScripts:
            summary += "\nBatch scripts:"
            summary += "\n    {}".format(batchScripts[0])
            if not useJobArray and numJobs > 1:
                if numJobs > 2:
                    summary += "\n    ..."
                summary += "\n    {}".format(batchScripts[-1])
        if inputSandbox:
            summary += "\nInput sandbox:"
            summary += "\n    {}".format(inputSandbox)
        else:
            summary += "\nNo input sandbox would be staged in to the worker nodes."
        if stageout and stageoutFiles:
            summary += "\nStageout directory for user files:"
            summary += "\n    {}".format(stageoutDir)
        else:
            summary += "\nNo user files would be staged out from the worker nodes."
        if writeLogsOnWN:
            if stageoutLogs and stageoutLogsDir:
                summary += "\nJob's stdout/stderr log files would be written on the worker nodes and staged out at job termination."
                summary += "\nStageout directory for job's stdout/stderr log files:"
                summary += "\n    {}".format(stageoutLogsDir)
            else:
                summary += "\nJob's stdout/stderr log files would be written on the worker nodes, but NOT staged out at job termination."
        if logFiles:
            summary += "\nJob's stdout/stderr log filenames:"
            for f in logFiles:
                summary += "\n    {}".format(os.path.basename(f))
        elif not writeLogsOnWN:
            summary += "\nNo job's stdout/stderr log files would be created."
        summary += "\n================================================================================"
        summary += "\n===============================  end of summary  ==============================="
        summary += "\n================================================================================"

        if self.debug:
            print("Summary text created.")

        print(summary)

        #================================================================================
        # Submit the jobs
        #================================================================================

        if self.submit:
            if not self.yes:
                timeout = 5
                if self.calledFromScript:
                    print("You provided the --submit (-s) option, which instructs to submit the jobs.")
                else:
                    print("You have set the 'submit' argument to True, which instructs to submit the jobs.")
                if not self.quiet:
                    print("Please read first the summary given above, then answer whether you really want to submit the jobs.")
                    print("N.B.: You can always submit the jobs (i.e. batch scripts) yourself with the slurm 'sbatch' command.")
                question = "Are you sure you want to submit the jobs ? (you have {} minutes to answer)".format(timeout)
                signal.signal(signal.SIGALRM, questionTimeoutHandler)
                signal.alarm(timeout*60)
                try:
                    answer = interactiveYesNoQuestion(question, default='no')
                except TimeoutException as ex:
                    print(ex)
                    answer = False
                signal.alarm(0)
                if not answer:
                    print("Jobs were not submitted.")
                    return
            if useJobArray:
                print("Submitting job array consisting of {} jobs".format(numJobs))
                ret = submit(batchScripts[0], partition=sbatch_partition, qos=sbatch_qos, jobArray=True)
                if ret == 2:
                    msg = "Failed to submit jobs."
                    raise CP3SlurmUtilsException(msg)
            else:
                for j in range(numJobs):
                    print("Submitting job number {}".format(j+1))
                    ret = submit(batchScripts[j], partition=sbatch_partition, qos=sbatch_qos, jobArray=False)
                    if ret == 2:
                        msg = "Failed to submit jobs."
                        raise CP3SlurmUtilsException(msg)
        else:
            if self.calledFromScript:
                print("You have not provided the --submit (-s) option, so jobs were not submitted.")
            else:
                print("You have not set the 'submit' argument to True, so jobs were not submitted.")
            if not self.quiet:
                print("You can always submit the jobs (i.e. batch scripts) yourself with the slurm 'sbatch' command.")
