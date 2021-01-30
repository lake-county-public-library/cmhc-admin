"""Client to handle connections and actions executed against a remote host."""

import errno
import re
from os import system, path, strerror
from paramiko import SSHClient, AutoAddPolicy, RSAKey
from paramiko.auth_handler import AuthenticationException, SSHException
from scp import SCPClient, SCPException
from .log import logger

class RemoteClient:
  """Client to interact with a remote host via SSH & SCP."""

  def __init__(self, host, user, password, ssh_key_filepath=""):
    self.host = host
    self.user = user
    self.password = password
    self.ssh_key_filepath = ssh_key_filepath
    self.client = None
    self.scp = None
    self.conn = None

    if self.ssh_key_filepath:
      self._upload_ssh_key()

  @logger.catch   
  def _get_ssh_key(self):
    """
    Fetch locally stored SSH key.
    """
    try:
      self.ssh_key = RSAKey.from_private_key_file(self.ssh_key_filepath)
      logger.info(f'Found SSH key at self {self.ssh_key_filepath}')
    except SSHException as error:
      logger.error(error)
    return self.ssh_key


  @logger.catch   
  def _upload_ssh_key(self):
    try:
      system(f'ssh-copy-id -i {self.ssh_key_filepath} {self.user}@{self.host}>/dev/null 2>&1')
      system(f'ssh-copy-id -i {self.ssh_key_filepath}.pub {self.user}@{self.host}>/dev/null 2>&1')
      logger.info(f'{self.ssh_key_filepath} uploaded to {self.host}')
    except FileNotFoundError as error:
      logger.error(error) 


  @logger.catch   
  def _connect(self):
    """Open connection to remote host."""
    if self.conn is None:

      logger.info(f'host: {self.host}, user: {self.user}')


      try:
        self.client = SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(AutoAddPolicy())

        # If using ssh key
        if self.ssh_key_filepath:
          self.client.connect(
            self.host,
            username=self.user,
            key_filename=self.ssh_key_filepath,
            look_for_keys=True,
            timeout=5000
          )
        else:
          self.client.connect(
            self.host,
            username=self.user,
            password=self.password,
            timeout=5000
          )

        self.scp = SCPClient(self.client.get_transport())
      except AuthenticationException as error:
        logger.error(f'Authentication failed: \
          did you remember to create an SSH key? {error}')
        raise error
    return self.client

  def disconnect(self):
    """Close ssh connection."""
    if self.client:
      self.client.close()
    if self.scp:
      self.scp.close()


  def download_single_file(self, remote_file, local_file, out):
    """Download a single file from a remote directory."""
    self.conn = self._connect()
    download = None
    try:
      out.write(f'Started download from: {remote_file} to: {local_file}<br>')
      out.flush()
      self.scp.get(
        remote_file,
        local_file
      )
      download = local_file
      logger.info(f'Downloaded {remote_file} to {download}')
      out.write(f'Finished download of {remote_file}<br>')
      out.flush()
    except SCPException as error:
      logger.error(error)
      raise error
    except Exception as e:
      logger.error(e)
      raise e
    else:
      return download


  @logger.catch
  def bulk_download(self, remote_directory, local_directory, out):
    """
    Download multiple files from a remote directory.

    :param files: List of paths to remote files.
    :type files: List[str]
    """

    # Ensure valid input
    if remote_directory is None:
      print("Error: Arg 'remote_directory' is null in RemoteClient.bulk_download ")
      return

    logger.info(f'Downloading from {remote_directory} to {local_directory}')

    self.conn = self._connect()

    # Ensure Windows formatting of directory path
    windows_dir = remote_directory.replace("/", "\\")

    # Find the listing of images on the remote machine
    stdin, stdout, stderr = self.conn.exec_command(f"dir {windows_dir}")
    stdout = stdout.readlines()
    stderr = stderr.readlines()

    # Collect the image filenames (expecting '.tif')
    images = []
    for line in stdout:
      res = re.search(r"\w+.tif", line)
      if res:
        images.append(res.group(0))

    # Was there an error?
    # ..if so, stop
    outerr = ""
    for line in stderr:
      outerr = outerr + line
    if outerr != "":
      print(f"error: {outerr}")
      out.write(f"error: {outerr}")
      return

    downloads = [self.download_single_file(remote_directory + file, local_directory + file.lower(), out) for file in images]
    logger.info(f'Finished downloading {len(downloads)} files ({images}) from {remote_directory} to {local_directory} from {self.host}')
    out.write(f'<p>Finished downloading {len(downloads)} files ({images}) from {remote_directory} to {local_directory} from {self.host}</p>')

