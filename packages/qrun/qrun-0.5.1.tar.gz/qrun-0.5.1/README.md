
# NAME
qrun - Quickly queue and run jobs from the command line.

# VERSION: 0.4.0

Note: Before version 0.4.0, `qrun` was a Perl script. For version 0.4.0, `qrun` was completely rewritten in Python.

# DESCRIPTION

  `qrun` is a perl script that will run a set of commands.
  It is primarily useful for running commands that are expected to run for a long
  time, such as physics simulations.  `qrun` uses "handlers" to actually run the
  commands, and tries to automatically select the best handler to use to complete
  the runs as quickly as possible. For example, if you are working on a cluster
  and the `qsub` command exists, `qrun` will create submission scripts and submit
  them to the scheduler.  If the `qsub` command does not exist, then other handlers
  are checked. For example, if the `parallel` (gnu parallel) or `xjobs` commands
  are found, they can be used to run all commands in parallel.

  If all other handlers fail, `qrun` will fall back to just running each command
  in serial, one after the other.  This turns out to still be useful, because if
  you have a set of simulations that you need to perform, you can use `qrun` to
  automatically run each simulation after one has completed.

  All handlers will first create a script wrapper for each command to run and
  then run this script.  This is done so that extra information can be embedded
  in the command output, such as a time stamp for timing data.


  Current Handlers

  `slurm`

  This handler uses the `sbatch` command. `sbatch` is used to submit jobs to
  an HPC cluster using the Slurm workload manager, which is become popular
  in recent years. The `sbatch` handler will automatically
  create a submission script for each job and subit the scripts to the scheduler.
  This is handy if you want to just quickly submit a basic job that does not
  require a complex submission script.


  `gnuparallel`

  This handler uses the `parallel` command, from the gnuparallel project. `parallel` is a
  perl script that runs multiple jobs in parallel and even supports running jobs on remote computers
  (not supported by run). It attempts to work as a parallel version of `xargs`.

  `xjobs`

  This handler uses the `xjobs` command. `xjobs` is a small C program written by Thomas Maier-Komer that
  that a command multiple times with different arguments in parallel.
  It strives to be a parallel version of `xargs`.

  `serial`

  This handler just runs each job directly, one after the other.


  Possible Future Handlers

  - `pexec` another tool for running jobs in parallel on a workstation.
  - `pbs` a common (maybe the most common) scheduler interface used on clusters.


  Note that `qrun` does not do load balancing. Each handler is given the list of commands to run, and they are responsible
  for managing the system workload.

# EXAMPLES

  run 3 scripts

      > qrun script1.sh : script2.sh : script3.sh

  run 3 BTEC runs

      > qrun -C BTECthermal config1.btec : BTECthermal config2.btec : BTECthermal config3.btec

  run BTEC for all config files in the current directory

      > qrun -C BTECthermal -d' ' config*.btec

  run 3 scripts using the gnuparallel handler

      > qrun -H gnuparallel script1.sh : script2.sh : script3.sh

  get a list of all handlers

      > qrun -l

# INSTALLATION

  `qrun` is available on PyPi
  ```
  $ pip install qrun
  ```


# LICENSE

  The MIT License (MIT)

  Copyright (c) 2015-present CD Clark III

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.

