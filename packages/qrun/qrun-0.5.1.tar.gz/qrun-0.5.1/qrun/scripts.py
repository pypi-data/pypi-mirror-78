from __future__ import print_function
from __future__ import unicode_literals
from .utils import *
from .handlers import *
from argparse import ArgumentParser

def qrun():
  """
  # NAME
  qrun - Quickly queue and run jobs from the command line.

  # VERSION: 0.4.0

  Note: Before version 0.4.0, `run` was a Perl script. For version 0.4.0, `run` was completely rewritten in Python.

  # DESCRIPTION

    `run` is a perl script that will run a set of commands.
    It is primarily useful for running commands that are expected to run for a long
    time, such as physics simulations.  `run` uses "handlers" to actually run the
    commands, and tries to automatically select the best handler to use to complete
    the runs as quickly as possible. For example, if you are working on a cluster
    and the `qsub` command exists, `run` will create submission scripts and submit
    them to the scheduler.  If the `qsub` command does not exist, then other handlers
    are checked. For example, if the `parallel` (gnu parallel) or `xjobs` commands
    are found, they can be used to run all commands in parallel.

    If all other handlers fail, `run` will fall back to just running each command
    in serial, one after the other.  This turns out to still be useful, because if
    you have a set of simulations that you need to perform, you can use `run` to
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


    Note that `run` does not do load balancing. Each handler is given the list of commands to run, and they are responsible
    for managing the system workload.

  # EXAMPLES

    run 3 scripts

        > run script1.sh : script2.sh : script3.sh

    run 3 BTEC runs

        > run -C BTECthermal config1.btec : BTECthermal config2.btec : BTECthermal config3.btec

    run BTEC for all config files in the current directory

        > run -C BTECthermal -d' ' config*.btec

    run 3 scripts using the gnuparallel handler

        > run -H gnuparallel script1.sh : script2.sh : script3.sh

    get a list of all handlers

        > run -l

  # INSTALLATION

    `run` is a single python script that uses only standard library modules.
    To install it, just place it somewhere in your PATH.


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
  """

  clsmembers = [ cls for cls in inspect.getmembers(sys.modules[__name__], inspect.isclass) if cls[0].lower() != "handler" and cls[0].lower().endswith("handler") ]
  handlers = { k.lower().replace("handler",""):v for (k,v) in clsmembers}


  parser = ArgumentParser(description="Quickly queue and run jobs from the command-line.")

  # old options
  # "block|B" => \$opt_block,
  # "args-are-run-scripts|F" => \$opt_args_are_run_scripts,
  # "leave-run-scripts|f" => \$opt_leave_run_scripts,
  # "handler_options|O=s" => \$opt_handler_options,
  # "list-handlers|l" => \$opt_list_handlers,
  # "output|o" => \$opt_output,
  # "readme|R" => \$opt_readme,
  # "verbose|v+" => \$opt_verbose,

  parser.add_argument("arguments",
                      action="store",
                      nargs='*',
                      default=list(),
                      help="A colon-delimited list of commands to run. Note that the delimiter character can be specified with the --delimiter option." )

  parser.add_argument("-m", "--manual",
                      action="store_true",
                      help="Print manual and exit." )

  parser.add_argument("-d", "--delimiter",
                      action="store",
                      default=":",
                      help="Use DELIMITER to delimiter commands." )

  parser.add_argument("-H", "--handler",
                      action="store",
                      help="Use HANDLER to submit jobs." )

  parser.add_argument("-t", "--template",
                      action="store",
                      help="Use TEMPLATE for submission script template." )

  parser.add_argument("-l","--list-handlers",
                      action="store_true",
                      default=False,
                      help="List supported handlers and exit." )

  parser.add_argument("--debug",
                      action="store_true",
                      default=False,
                      help="Turn on debugging output." )

  parser.add_argument("--print-template",
                      action="store_true",
                      default=False,
                      help="Print template submit script that will be used and exit." )

  parser.add_argument("--leave-tempdir",
                      action="store_true",
                      default=False,
                      help="Leave the temperary directory used to write submit scripts." )

  parser.add_argument("-n", "--dry-run",
                      action="store_true",
                      default=False,
                      help="Dry run. Don't actuall run submit scripts." )

  parser.add_argument("-C", "--command",
                      action="store",
                      default="",
                      help="Prepend COMMAND to all commands before running." )

  parser.add_argument("--context",
                      action="store",
                      default="{}",
                      help="A JSON formatted string containing key=value pairs that will be added to the context when rendering the submit script." )

  parser.add_argument("--context-file",
                      action="store",
                      help="A JSON file containing key=value pairs that will be added to the context when rendering the submit script." )


  args = parser.parse_args()

  if args.manual:
    print(__doc__)
    sys.exit()

  if args.list_handlers:
    print("{:15}{:15}".format("Handler","Available"))
    print("{:=<30}".format(""))
    for h in handlers:
      print("{:15}{:15}".format(h,"yes" if handlers[h].test() else "no" ))
    sys.exit()


  if args.debug:
    logging.basicConfig(level=logging.DEBUG)

  commands = [ (args.command+" "+cmd.strip()).strip() for cmd in " ".join(args.arguments).split(args.delimiter) ]


  if args.handler:
    handler = args.handler
  else:
    # detect handlers
    candidates = dict()
    for h in handlers:
      if handlers[h].test():
        logging.info("detected %s handler"%h)
        p = 1000
        if h in handler_priority:
          p = handler_priority.index(h)
        candidates[p] = h

    if len(candidates) < 1:
      raise RuntimeError("No candidates found to handle jub submission")
    
    # take handler with the highest priotity
    handler = [ candidates[h] for h in sorted(candidates) ][0]

  if handler not in handlers:
    raise RuntimeError("Handler '%s' is not supported. Did you spell the name correctly?")

  logging.info("using %s handler"%handler)

  handler = handlers[handler](args)
  handler.generate_scripts(commands)
  if not args.dry_run:
    handler.run()
  handler.cleanup()

def cmd_time(arguments):
  parser = ArgumentParser(description="A tool to perform various tasks related to running jobs.")

  parser.add_argument("file",
                      action="store",
                      nargs="*",
                      help="Files to report time information on." )

  args = parser.parse_args(arguments)

  class parser:
    begin = pp.Literal("BEGIN:")+pp.Word(pp.nums)('date')+pp.Word(pp.nums+':')('time')
    end   = pp.Literal("END:")  +pp.Word(pp.nums)('date')+pp.Word(pp.nums+':')('time')
    cmd   = pp.Literal("CMD:")  +pp.Word(pp.printables)('command')
    args  = pp.Literal("ARGS:") +pp.Word(pp.printables)('arguments')

  for file in args.file:
    print("file:",file)
    with open(file,'r') as f:
      text = f.read()

    begin = parser.begin.searchString(text)
    end   = parser.end.searchString(text)
    cmd   = parser.cmd.searchString(text)
    args  = parser.args.searchString(text)

    for i in range(len(cmd)):
      print("\tcmd:",cmd[i]["command"])
      print("\targ:"," ".join([ args[i]["arguments"] for i in range(len(args)) ]))
      if(len(begin) < 1):
        print("\tHas not started yet")
      else:
        begin_datetime = datetime.strptime('{} {}'.format(begin[i]["date"],begin[i]["time"]), '%Y%m%d %H:%M:%S')
        if(len(end) < 1):
          print("\tHas not finished yet")
        else:
          end_datetime = datetime.strptime('{} {}'.format(end[i]["date"],end[i]["time"]), '%Y%m%d %H:%M:%S')
          duration = end_datetime-begin_datetime
          print("\tduration:",duration)
                      



def qrun_util():
  funcmembers = [ func for func in inspect.getmembers(sys.modules[__name__], inspect.isfunction) if func[0].lower().startswith("cmd_") ]
  commands = { k.lower().replace("cmd_",""):v for (k,v) in funcmembers}

  parser = ArgumentParser(description="A tool to perform various tasks related to running jobs.")

  parser.add_argument("command",
                      action="store",
                      help="sub-command." )

  parser.add_argument("command_args",
                      action="store",
                      nargs="*",
                      help="sub-command arguments/options." )

  parser.add_argument("-m", "--manual",
                      action="store_true",
                      help="Print manual and exit." )

  parser.add_argument("-l","--list-commands",
                      action="store_true",
                      default=False,
                      help="List supported handlers and exit." )

  parser.add_argument("--debug",
                      action="store_true",
                      default=False,
                      help="Turn on debugging output." )


  command_index = None
  try: command_index = sys.argv.index( next( x for x in sys.argv[1:] if not x.startswith('-') ) )
  except: pass
  main_args = sys.argv[:command_index]
  cmd_args = sys.argv[command_index:]
  args = parser.parse_args(main_args)

  if args.manual:
    print(__doc__)
    sys.exit()

  if args.list_commands:
    print("Commands:")
    for c in commands:
      print("  ",c)
    sys.exit()

  if args.debug:
    logging.basicConfig(level=logging.DEBUG)

  if not cmd_args[0] in commands:
    raise RuntimeError("Unknown command '{cmd}'. Use the '-l' option to see a list of supported commands.".format(cmd=cmd_args[0]))

  commands[cmd_args[0]]( cmd_args[1:] )

