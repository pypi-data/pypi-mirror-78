import urllib.request
import zipfile
import os, stat, errno, subprocess, socket, platform
import logging
from pathlib import Path

logging.getLogger().setLevel(logging.INFO)

px_server_package_download_root_url = 'https://ckpx.s3.amazonaws.com/px-server'

windows_px_server_package_download_url_template = px_server_package_download_root_url + '/{version}/px-windows.zip'

mac_px_server_package_download_url_template = px_server_package_download_root_url + '/{version}/px-mac.zip'

linux_px_server_package_download_url_template = px_server_package_download_root_url + '/{version}/px-linux.zip'

px_home_dir = os.path.join(Path.home(), '.px')

default_px_server_package_path = os.path.join(px_home_dir, 'px-server')

default_os_name = platform.system()

default_px_server_version = '0.0.1'

def download_and_extract_px_server_package(os_name=None, version=None, px_server_package_path=None):
    if os_name is None:
        os_name = default_os_name

    if version is None:
        version = default_px_server_version

    px_server_package_download_url = get_px_server_package_download_url(os_name=os_name, version=version)

    if px_server_package_path is None:
        px_server_package_path = default_px_server_package_path

    px_server_package_path = os.path.join(px_server_package_path, '{os}-{version}'.format(os=os_name, version=version))

    if os_name == 'Windows':
        px_server_executable_file_name = 'px.exe'
    else:
        px_server_executable_file_name = 'px'
    px_server_executable_file_path = os.path.join(px_server_package_path, px_server_executable_file_name)
    grpc_file_path = os.path.join(px_server_package_path, 'grpc_node.node')

    if not os.path.exists(px_server_executable_file_path) or not os.path.exists(grpc_file_path):
        try:
            os.remove(grpc_file_path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        try:
            os.remove(px_server_executable_file_path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

        logging.info('Download px server package from {}'.format(px_server_package_download_url))
        file_name, header = urllib.request.urlretrieve(px_server_package_download_url)

        logging.info('Extracting px server package from {} to {}'.format(file_name, px_server_package_path))
        with zipfile.ZipFile(file_name, 'r') as zip_ref:
            zip_ref.extractall(px_server_package_path)

        try:
            logging.info('Delete px server package {}'.format(file_name))
            os.remove(file_name)
        except OSError:
            pass

    os.chmod(grpc_file_path, 0o755)
    os.chmod(px_server_executable_file_path, 0o755)

    return px_server_executable_file_path

def get_px_server_package_download_url(os_name=None, version=None):
    if os_name is None:
        os_name = default_os_name

    if version is None:
        version = default_px_server_version

    if os_name == 'Windows':
        px_server_package_download_url_template = windows_px_server_package_download_url_template
    elif os_name == 'Linux':
        px_server_package_download_url_template = linux_px_server_package_download_url_template
    elif os_name == 'Darwin':
        px_server_package_download_url_template = mac_px_server_package_download_url_template
    else:
        raise Exception('Unsupported OS: {}'.format(os_name))

    return px_server_package_download_url_template.format(version=version)
