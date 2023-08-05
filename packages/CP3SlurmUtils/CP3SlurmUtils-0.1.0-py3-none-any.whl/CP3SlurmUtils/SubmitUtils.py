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

import datetime
import os
import subprocess


def submit(batchScript, partition=None, qos=None, wckey=None, jobArray=False, bookkeep=True):
    timestamp = str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S%f"))
    submitOpts = ""
    if partition:
        submitOpts += " --partition={}".format(partition)
    if qos:
        submitOpts += " --qos={}".format(qos)
    if wckey:
        submitOpts += " --wckey={}".format(wckey)
    submitCmd = "sbatch{} {}".format(submitOpts, batchScript)
    print("Submission command:\n    {}".format(submitCmd))
    process = subprocess.Popen(submitCmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')
    returncode = process.returncode
    if returncode != 0:
        msg = "ERROR: Failed to submit."
        if stdout:
            msg += "\nStdout:\n\t{}".format(str(stdout).replace('\n', '\n\t'))
        if stderr:
            msg += "\nStderr:\n\t{}".format(str(stderr).replace('\n', '\n\t'))
        print(msg)
        return 2
    stdout = stdout.replace('\n', '')
    print(stdout)
    if not bookkeep:
        return 0
    jobId = ''
    if stdout.startswith('Submitted batch job '):
        jobId = stdout.replace('Submitted batch job ', '')
    if not jobId:
        msg = "WARNING: Failed to parse the sbatch stdout to retrieve the job id."
        msg += " Will not write the job to the user's slurm_jobs file."
        print(msg)
        return 1
    filename = os.path.expanduser('~/.slurm_jobs')
    try:
        with open(filename, 'a+') as fd:
            fd.write('{} {} {} jobarray={}\n'.format(timestamp, jobId, batchScript, 'T' if jobArray else 'F'))
    except IOError as ex:
        msg = "WARNING: Failed to write job to user's slurm_jobs file {file}"
        msg += "\nError follows:\n{error}"
        msg = msg.format(file=filename, error=str(ex))
        print(msg)
        return 1
    try:
        newFileContent = ""
        with open(filename, 'r') as fd:
            for line in fd:
                date, time = line.split()[0].split('-')
                year, month, day = date[:4], date[4:6], date[6:8]
                hour, minute, second, microsecond = time[:2], time[2:4], time[4:6], time[6:12]
                lineDateTime = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second), int(microsecond))
                now = datetime.datetime.now()
                if (now - lineDateTime).days < 30:
                    newFileContent += line
        with open(filename, 'w') as fd:
            fd.write(newFileContent)
    except Exception as ex:
        msg = "WARNING: Failed to clean user's slurm_jobs file {file}"
        msg += "\nError follows:\n{error}"
        msg = msg.format(file=filename, error=str(ex))
        print(msg)
        return 1
    return 0
