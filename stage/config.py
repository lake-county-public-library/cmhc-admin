"""Remote host configuration."""
from os import environ, path
from dotenv import load_dotenv

# Load environment variables from .env
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# Read environment variables
host = environ.get('REMOTE_HOST')
user = environ.get('REMOTE_USERNAME')
ssh_key_filepath = environ.get('SSH_KEY')
remote_path = environ.get('REMOTE_PATH')
remote_images_path = environ.get('REMOTE_IMAGES_PATH')
wax_home = environ.get('WAX_HOME')
wax_host_ip = environ.get('WAX_HOST_IP')

local_file_directory = 'data'
local_images_directory = 'data/images'
