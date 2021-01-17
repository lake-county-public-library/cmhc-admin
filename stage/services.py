from paramiko import SSHClient
from scp import SCPClient
import sys
from subprocess import Popen, PIPE

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
  def stage_csv():
    remote = RemoteClient(host, user, ssh_key_filepath, remote_path)
    upload_files_to_remote(remote)
    remote.disconnect()
    return "success"

  def stage_images():
    return "success"

def upload_files_to_remote(remote):
  """Upload files to remote via SCP."""
  local_files = fetch_local_files(local_file_directory)
  remote.bulk_upload(local_files)


class Generator():
  def generate_derivatives():
    p = Popen(["ls", "-l"], stdout=PIPE, stderr=PIPE)

    l = "Generating derivatives"
    print(l)
    while p.poll() is None:
      print(l)
      l = p.stdout.readline().decode()
      
    return "Success: " + str(l)
