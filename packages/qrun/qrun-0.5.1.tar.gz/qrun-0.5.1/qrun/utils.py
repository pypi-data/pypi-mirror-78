from __future__ import print_function
from __future__ import unicode_literals
import subprocess
import os, sys, inspect, logging, shutil, re, json, hashlib, tempfile, stat, io

class workdir(object):
  '''
  A context class to temporarily change working directory.
  '''
  def __init__(self, path):
    self.old_dir = os.getcwd()
    self.new_dir = path

  def __enter__(self):
    if self.new_dir is not None:
      os.chdir(self.new_dir)

  def __exit__(self, *args):
    if self.new_dir is not None:
      os.chdir(self.old_dir)

def run(cmd,wd=None,capture_output=False,input=None):
  '''Run a command and return its exit status, standard output, and standard error.'''
  try: input = input.encode('utf-8')
  except: pass 

  stdout = None
  if capture_output:
    stdout = subprocess.PIPE

  with workdir(wd):
    c = subprocess.run( cmd, shell=True, executable="/bin/bash", input=input, stdout=stdout,stderr=subprocess.STDOUT)

  r = c.returncode
  o = c.stdout

  try:
    o = o.decode('utf-8')
  except: pass

  return r,o

def qx(cmd,wd=None):
  '''Run a command and returns its output.'''
  r,o = run(cmd,wd)
  return o

def render(text,context,opts=dict()):
  for k in context:
    text = text.replace("<%"+k+"%>",context[k])
  # remove any left over keys
  if 'remove_missing_keys' not in opts or opts['remove_missing_keys']:
    text = re.sub("<%.*%>","",text)

  return text

def generate_name(cmd_str):
  if len(cmd_str) > 20:
    return "_"+hashlib.sha1(cmd_str.encode("utf-8")).hexdigest()

  return cmd_str.replace(" ","_")

