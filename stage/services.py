from paramiko import SSHClient
from scp import SCPClient
import sys
import time
from subprocess import Popen, PIPE, STDOUT
from os import path
import threading

from .files import fetch_local_files
from .client import RemoteClient

"""Perform tasks against a remote host."""
from .config import (
  host,
  user,
  ssh_key_filepath,
  local_file_directory,
  local_images_directory,
  remote_path,
  remote_images_path,
  wax_home,
  wax_host_ip,
)

class Stager():

  def stage_csv(filename, logfile):
    """
    """
    local_file = local_file_directory + "/" + filename
    remote = RemoteClient(host, user, ssh_key_filepath, remote_path)

    try:
      out = open(logfile, 'w')
      upload_single_file_to_remote(remote, local_file, out)
    except FileNotFoundError as error:
      raise error
    except Exception as e:
      raise e
    finally:
      remote.disconnect()
      out.close()

  def stage_images(logfile):
    """
    """
    out = open(logfile, 'w')
    print("Staging images")

    # Verify inputs
    if not path.isdir(local_images_directory):
      out.write(f"Error: %s is not a valid directory!" %local_images_directory)  
      return

    remote = RemoteClient(host, user, ssh_key_filepath, remote_images_path)
    try:
      upload_files_to_remote(remote, local_images_directory, out)
    except FileNotFoundError as error:
      raise error
    except Exception as e:
      raise e
    finally:
      remote.disconnect()
      out.close()



def upload_single_file_to_remote(remote, local_file, out):
  """Upload single file to remote via SCP."""
  remote.upload_single_file(local_file, out)
    

def upload_files_to_remote(remote, local_directory, out):
  """Upload files to remote via SCP."""
  local_files = fetch_local_files(local_directory)
  remote.bulk_upload(local_files, out)


class WaxHelper():

  p = None

  def generate_derivatives(logfile):
    print("Generating derivatives")
    
    out = open(logfile, 'w')
    p = Popen(["bundle", "exec", "rake", "wax:derivatives:iiif", "cmhc"],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)
     
    out.close()


  def generate_pages(logfile):
    print("Generating pages")
    out = open(logfile, 'w')
    p = Popen(["bundle", "exec", "rake", "wax:pages", "cmhc"],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)

    out.close()


  def generate_index(logfile):
    print("Generating index")
    out = open(logfile, 'w')
    p = Popen(["bundle", "exec", "rake", "wax:search", "main"],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)

    out.close()


  def run_local(logfile):
    print("Running local site")
    out = open(logfile, 'w')
    WaxHelper.p = Popen(["bundle", "exec", "jekyll", "serve", "--host", wax_host_ip],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)

    out.write(f"<a href='http://%s:4000/cmhc/'>Site</a><br><br>" %wax_host_ip)

    out.close()


  def kill_local():
    print("Stopping local site")
    WaxHelper.p.kill()


class WaxHelperThread(threading.Thread, WaxHelper):
  def __init__(self):
    super(WaxHelperThread, self).__init__()

  def run(self, logfile):
    self.run_local(logfile)    
    



class LogFinder():
  
  def find(f):
    data = []
    with open(f, 'r') as log:
      lines = log.readlines()
      for line in lines:
        data.append(line)
        data.append("<br>")
    return "".join(data)

