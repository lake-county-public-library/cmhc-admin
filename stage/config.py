"""Remote host configuration."""
from os import environ, path
from dotenv import load_dotenv

# Load environment variables from .env
basedir = path.abspath(path.dirname(__file__))
print(f"config: basedir = %s" %str(basedir))
load_dotenv(path.join(basedir, '.env'))

# Read environment variables
host = environ.get('REMOTE_HOST')
user = environ.get('REMOTE_USERNAME')
password = environ.get('REMOTE_PASSWORD')
ssh_key_filepath = environ.get('SSH_KEY')
wax_home = environ.get('WAX_HOME')
wax_host_ip = environ.get('WAX_HOST_IP')
local_csv_directory = environ.get('LOCAL_CSV_DIRECTORY')
local_images_directory = environ.get('LOCAL_IMAGES_DIRECTORY')
remote_csv_directory = environ.get('REMOTE_CSV_DIRECTORY')
remote_images_directory = environ.get('REMOTE_IMAGES_DIRECTORY')
