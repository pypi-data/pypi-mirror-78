CP3SlurmUtils
=============

CP3SlurmUtils was written with the aim to be an utility for physicists of the
[CP3 institute](https://uclouvain.be/en/research-institutes/irmp/cp3) that would
facilitate the submission (and resubmission) of jobs to their computing cluster,
which is managed by [Slurm](https://slurm.schedmd.com/documentation.html). Most
of the physicists at CP3 that would use this utility are collaborating with the
CMS experiment at CERN.

In CP3SlurmUtils, jobs are defined via a submit configuration file written in
Python similar to the type of submit configuration file used in [CRABClient](https://github.com/dmwm/CRABClient),
the tool used by CMS users to submit jobs to the Worldwide LHC Computing Grid.
The utility creates then the batch scripts to be submitted with the Slurm __sbatch__ command.
The submission can be done on-the-go by the utility itself or later-on by the user.

CP3SlurmUtils provides the following features:

- handling of job stdout/stderr
- handling of a scratch directory
- handling of job exit codes
- handling of job input and output files
- setup of the CMS environment (optional)

For the copying of files to/from the worker nodes, the __cp__ command is used,
assuming there is a filesystem shared with the submission node.

## INSTALLATION

CP3SlurmUtils can be installed via the [Python Package Installer](https://pip.pypa.io/en/stable/),
or it can simply be downloaded from the git repository:
https://gitlab.cern.ch/cp3-cms/CP3SlurmUtils.

## CONFIGURATION

An example configuration file for CP3SlurmUtils named _defaults.cfg.example_
is included in the package. In the git repository, it can be found in the
__etc__ folder. In the distribution, it can be found in a sub-directory named
__etc/CP3SlurmUtils__.

CP3SlurmUtils will try to read the _defaults.cfg_ configuration file from the
following locations, in this order:

- /etc/CP3SlurmUtils/
- $xdg_config_dir/CP3SlurmUtils/ where $xdg_config_dir is each of the paths
  defined by the environment variable $XDG_CONFIG_DIRS; if $XDG_CONFIG_DIRS is
  not defined, $xdg_config_dir defaults to /etc/xdg/
- site.USER_BASE/etc/CP3SlurmUtils/ where site.USER_BASE is the python variable
  that defines the location for a user installation
- $xdg_config_home/CP3SlurmUtils/ where $xdg_config_home is the environment
  variable $XDG_CONFIG_HOME when defined and not empty; otherwise it defaults to
  $HOME/.config
- $VIRTUAL_ENV/etc/CP3SlurmUtils/ when $VIRTUAL_ENV is defined and not empty 

There is no installation or configuration script provided with this utility;
it is left to the user to put the _defaults.cfg_ configuration file in a visible
location or appropriately point the environment variable $XDG_CONFIG_DIRS or
$XDG_CONFIG_HOME to it.

## REPORTING BUGS

To report an issue/bug or to provide suggestions for enhancement/improvement,
open an issue in the git repository: https://gitlab.cern.ch/cp3-cms/CP3SlurmUtils.
Pull requests are also welcome.
Questions can be sent to cp3-support@uclouvain.be.

## LEGAL

CP3SlurmUtils is provided "as is" and with no warranty. This software is
distributed under the GNU General Public License; please see the file LICENSE
for details.
