from paramiko import SSHClient
from scp import SCPClient
import sys
import time
from subprocess import Popen, PIPE, STDOUT

from .files import fetch_local_files
from .client import RemoteClient

"""Perform tasks against a remote host."""
from .config import (
  host,
  user,
  ssh_key_filepath,
  local_file_directory,
  remote_path
)

class Stager():
  def stage_csv(filename):
    local_file = local_file_directory + "/" + filename
    remote = RemoteClient(host, user, ssh_key_filepath, remote_path)

    try:
      upload_single_file_to_remote(remote, local_file)
    except FileNotFoundError as error:
      raise error
    except Exception as e:
      raise e
    finally:
      remote.disconnect()

  def stage_images():
    return "success"

def upload_single_file_to_remote(remote, local_file):
  """Upload single file to remote via SCP."""
  remote.upload_single_file(local_file)
    

def upload_files_to_remote(remote):
  """Upload files to remote via SCP."""
  local_files = fetch_local_files(local_file_directory)
  remote.bulk_upload(local_files)


class Generator():

  def generate_derivatives(f):
    out = open(f, 'w')

    p = Popen(["ls", "-l"], stdout=out, stderr=STDOUT, bufsize=0)

    print("Generated derivatives")
     
    out.close()
    return "Success"

class LogFinder():
  
  def find(f):
    data = []
    with open(f, 'r') as log:
      lines = log.readlines()
      for line in lines:
        data.append(line)
        data.append("<br>")
    return "".join(data)

