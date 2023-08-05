from io import BytesIO
from os import path
import secrets
import string
from datetime import date
from dateutil.relativedelta import relativedelta

from remote_client import RemoteClient

RASPBERRY = 'rb0202'

# RELATIVE_REMOTE_DIR = f"bat_runner"
RELATIVE_REMOTE_DIR = f"bat_runner\\{RASPBERRY}"
RELATIVE_REMOTE_DIR_2 = RELATIVE_REMOTE_DIR.replace('\\', '/')
ABSOLUTE_REMOTE_DIR = f"C:\\Users\\CASA\\Canper\\{RELATIVE_REMOTE_DIR}"

client = RemoteClient('82.223.115.66', 'canper', '1234')

# client.download_file()
def _remote_bat_file(filename):
    script_dir = path.dirname(__file__)
    abs_file_path = path.join(script_dir, filename)
    with open(abs_file_path, 'r') as file:
        return file.read()

def _generate_inmemory_file(file_content):
    fl = BytesIO()
    fl.write(file_content.encode())
    fl.seek(0)
    return fl

def _generate_random_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(12))


def _generate_file_data(n, raspberry, ovpn_pass):
    ids = []
    exe_passes = []
    ovpn_passes = []
    expiry_dates = []
    expiry_times = []
    expiry_date = date.today() + relativedelta(months=+6)

    for i in range(1, n+1):
        ids.append(f'{raspberry}-{i}')
        exe_passes.append(_generate_random_password())
        ovpn_passes.append(ovpn_pass)
        expiry_dates.append(expiry_date.strftime('%d-%m-%Y'))
        expiry_times.append('23:59')

    return ids, exe_passes, ovpn_passes, expiry_dates, expiry_times


def generate_exe_files(number_connections, raspberry, ovpn_passes):
    ids, exe_passes, ovpn_passes, expiry_dates, expiry_times = _generate_file_data(number_connections, raspberry, ovpn_passes)

    try:
        client.connect()
        # Create tmp folder for this raspberry
        client.execute_commands([
            f'cmd.exe /c "mkdir {ABSOLUTE_REMOTE_DIR}"'
        ])
        setup_file_template = _remote_bat_file('bats/setup.bat')
        setup_file_content = setup_file_template.format(
            exe_passes='\n'.join(exe_passes),
            ids='\n'.join(ids),
            ovpn_passes='\n'.join(ovpn_passes),
            expiry_dates='\n'.join(expiry_dates),
            expiry_times='\n'.join(expiry_times)
        )
        setup_file_inmemory = _generate_inmemory_file(setup_file_content)
            
        client.upload_single_file(setup_file_inmemory, f'{RELATIVE_REMOTE_DIR_2}/setup.bat')

        client.execute_commands([
            f'cmd.exe /c "{ABSOLUTE_REMOTE_DIR}\\setup.bat"',
        ])
        client.download_file('RB0202-1.EXE', f'{RELATIVE_REMOTE_DIR_2}/RB0202-1.EXE')
        # Remove tmp directory
        client.execute_commands([
            f'cmd.exe /c "rmdir {ABSOLUTE_REMOTE_DIR}" /s /q'
        ])
    finally:
        client.disconnect()

generate_exe_files(3, 'RB0202', 'ovpn_pass')