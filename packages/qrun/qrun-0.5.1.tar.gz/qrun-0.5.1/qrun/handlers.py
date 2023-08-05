from __future__ import print_function
from __future__ import unicode_literals
from .utils import *

handler_priority = [
    'slurm',
    'xjobs',
    'gnuparallel',
  ]

class Handler(object):
  '''
  Base class for handlers. New handlers should subclass this class and provide the following methods:

  REQUIRED:
    test() - return true if the handle can handle.
    template() - return a template string for generating submit scripts.
    run() - a method that can run all of the scripts in stored in self.submit_scripts member.
  OPTIONAL:
    default_context() - return a dict containing context entries for template file rendering.
  '''
  def __init__(self,opts):
    self.opts = opts
    self.submit_scripts = list()
    self.tmpdir = None


  @staticmethod
  def test():
    return False

  def default_context(self):
    return dict()

  def generate_scripts(self,commands):

    # get user-supplied context
    user_context = dict()
    if self.opts.context_file:
      with open(self.opts.context_file,'r') as f:
        user_context.update(json.load(f))
    user_context.update(json.loads(self.opts.context))


    currdir = os.getcwd()
    self.tmpdir = tempfile.mkdtemp(prefix='run-')
    logging.info("using %s for temporary storage"%self.tmpdir)
    # create submission scripts. one for each command.
    for command in commands:
      context = self.default_context()
      try:
        context['CMD'],context['ARGS'] = command.strip().split(maxsplit=1)
      except:
        context['CMD'] = command
        context['ARGS'] = ""
      context['WORKDIR'] = currdir
      context['NAME'] = generate_name(command)

      context.update(user_context)

      # use template file if provided by user, otherwise use template provided by the handler.
      if self.opts.template:
        with open(self.opts.template,'r') as f:
          template = f.read()
      else:
        template = self.template()

      if self.opts.print_template:
        print(template)
        sys.exit(0)

      submit_script_text = render(template,context)

      submit_script = "run-submit_script.%d"%len(self.submit_scripts)
      with workdir(self.tmpdir):
        with open(submit_script,'w') as f:
          f.write(submit_script_text)
        st = os.stat(submit_script)
        os.chmod(submit_script, st.st_mode | stat.S_IEXEC)
        self.submit_scripts.append( os.path.abspath( submit_script ) )
      
  def cleanup(self):
    if self.opts.leave_tempdir:
      print("Temporary directory '%s' left behind."%self.tmpdir)
    else:
      shutil.rmtree(self.tmpdir)
  



class SerialHandler(Handler):
  @staticmethod
  def test():
    # we can always run jobs in serial
    return True

  def template(self):
    return '''#! <%INTERPRETER%>

cd <%WORKDIR%>
echo "CMD: <%CMD%>"
echo "ARGS: <%ARGS%>"
echo -n "BEGIN: "
date +"%Y%m%d %H:%M:%S"
<%CMD%> <%ARGS%>
echo -n "END:   "
date +%"Y%m%d %H:%M:%S"
'''

  def default_context(self):
    context = dict()
    context['INTERPRETER'] = shutil.which("bash")

    return context


  def run(self):
    for file in self.submit_scripts:
      print("Running %s"%(file))
      run(file)



class xJobsHandler(SerialHandler):
  @staticmethod
  def test():
    return shutil.which("xjobs") is not None

  def run(self):
    run("xjobs", input="\n".join(self.submit_scripts))


class GnuParallelHandler(SerialHandler):
  @staticmethod
  def test():
    return shutil.which("parallel") is not None

  def run(self):
    run("parallel ::: "+" ".join(self.submit_scripts))

class SlurmHandler(SerialHandler):
  @staticmethod
  def test():
    return shutil.which("sbatch") is not None

  def run(self):
    for file in self.submit_scripts:
      run("sbatch %s"%file)

  def default_context(self):
    context = dict()
    context['INTERPRETER'] = shutil.which("bash")

    return context


  def template(self):
    serial_script = re.sub("#!.*","",super().template())

    return '''#! <%INTERPRETER%>

#SBATCH --job-name=<%NAME%>
#SBATCH --output=<%NAME%>.out
#SBATCH --time=0-01:00:00
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
##SBATCH --mem-per-cpu=1G

{SERIAL}

'''.format(SERIAL=serial_script)
