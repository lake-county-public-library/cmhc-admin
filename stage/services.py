from paramiko import SSHClient
from scp import SCPClient
import sys
import time
from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
from os import path
import threading

from .files import fetch_local_files
from .client import RemoteClient

"""Perform tasks against a remote host."""
from .config import (
  host,
  user,
  password,
  ssh_key_filepath,
  local_csv_directory,
  local_images_directory,
  remote_csv_directory,
  remote_images_directory,
  wax_home,
  wax_host_ip,
)

class Stager():

  def stage_csv(filename, logfile):
    """
    """
    remote_file = remote_csv_directory + "/" + filename
    local_file = local_csv_directory + "/" + filename
    remote = RemoteClient(host, user, password, ssh_key_filepath)

    try:
      out = open(logfile, 'w')
      download_single_file_from_remote(remote, remote_file, local_file, out)
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

    remote = RemoteClient(host, user, password, ssh_key_filepath)
    try:
      download_files_from_remote(remote, remote_images_directory, local_images_directory, out)
    except FileNotFoundError as error:
      raise error
    except Exception as e:
      raise e
    finally:
      remote.disconnect()
      out.close()


def download_single_file_from_remote(remote, remote_file, local_file, out):
  """Download single file from remote via SCP."""
  remote.download_single_file(remote_file, local_file, out)
    
def download_files_from_remote(remote, remote_directory, local_directory, out):
  """Download files from remote via SCP."""
  remote.bulk_download(remote_directory, local_directory, out)




def upload_single_file_to_remote(remote, local_file, out):
  """Upload single file to remote via SCP."""
  remote.upload_single_file(local_file, remote_file, out)
    

def upload_files_to_remote(remote, local_directory, remote_directory, out):
  """Upload files to remote via SCP."""
  local_files = fetch_local_files(local_directory)
  remote.bulk_upload(local_files, remote_directory, out)


class WaxHelper():

  p = None

  def generate_derivatives(logfile):
    print("Generating derivatives")
    
    out = open(logfile, 'w')
    p = Popen(["bundle", "exec", "rake", "wax:derivatives:iiif", "cmhc"],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)
     
    out.close()


  def stop_on_failure(process, out):
    # Wait up to 5 minutes
    try:
      process.wait(timeout=300)
    except TimeoutExpired as e:
      process.kill()
      out.write(f"Error: Process timed-out! %s" %process.args)
      raise e
      return

    rc = process.returncode
    if rc == None:
      # Should never happen
      out.write(f"Error: Should never happen! %s" %process.args)
      raise TimeoutExpired()
    elif rc != 0:
      out.write(f"Error: Process exited with failure! %s %d" %(process.args, rc))
      raise ValueError(f"Error: Process exited with failure! %s %d" %(process.args, rc))
    else:
      out.write(f"Process exited successfully: %s <br>" %process.args)


  def generate_pages(logfile, keep_log_open=False):
    print("Generating pages")
    out = open(logfile, 'w')
    p = Popen(["bundle", "exec", "rake", "wax:pages", "cmhc"],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)
    WaxHelper.stop_on_failure(p, out)

    if not keep_log_open:
      out.close()


  def generate_index(logfile, keep_log_open=False):
    print("Generating index")
    out = open(logfile, 'w')
    p = Popen(["bundle", "exec", "rake", "wax:search", "main"],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)
    WaxHelper.stop_on_failure(p, out)

    if not keep_log_open:
      out.close()


  def run_local(logfile):
    print("Running local site")
    out = open(logfile, 'w')
    WaxHelper.p = Popen(["bundle", "exec", "jekyll", "serve", "--host", wax_host_ip],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)

    out.write("When complete, site will be available at:<br>")
    out.write(f"<a href='http://%s:4000/cmhc/' target='_blank'>http://%s:4000/cmhc/</a><br><br>" %(wax_host_ip, wax_host_ip))
    out.write("Please wait, processing...<br>")

    out.close()


  def kill_local():
    print("Stopping local site")
    WaxHelper.p.kill()


  def deploy(logfile):
    print("Deploying to AWS")
    out = open(logfile, 'w')

    # Clean the local environment
    print(f"cwd: %s" %wax_home)
    p = Popen(["rm", "-f", "_cmhc/*"], cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)
    WaxHelper.stop_on_failure(p, out)

    p = Popen(["rm", "-f", "search/index.json"], cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)
    WaxHelper.stop_on_failure(p, out)

    p = Popen(["bundle", "exec", "jekyll", "clean"],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)
    WaxHelper.stop_on_failure(p, out)

    # Re-generate pages and index
    WaxHelper.generate_pages(logfile, True)
    WaxHelper.generate_index(logfile, True)

    # Re-generate production site
    p = Popen(["bundle", "exec", "jekyll", "build"],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)
    WaxHelper.stop_on_failure(p, out)

    # Publish to AWS
    p = Popen(["s3_website", "push"],
              cwd=wax_home,
              stdout=out, stderr=STDOUT, bufsize=0)
    WaxHelper.stop_on_failure(p, out)

    out.close()


class LogFinder():
  def find(f, unwanted='not-used'):
    data = []
    with open(f, 'r') as log:
      lines = log.readlines()
      for line in lines:
        if unwanted not in line:
          data.append(line)
          data.append("<br>")
    return "".join(data)

