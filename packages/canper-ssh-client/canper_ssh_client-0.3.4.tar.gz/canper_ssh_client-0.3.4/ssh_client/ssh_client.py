import re
from os import environ
from contextlib import contextmanager
import random
from ssh_client.remote_client import RemoteClient

from ssh_client.helpers import remote_bat_file, generate_inmemory_file, generate_file_data


RELATIVE_REMOTE_DIR = "bat_runner"
ABSOLUTE_REMOTE_DIR = f"C:\\Users\\CASA\\Canper\\{RELATIVE_REMOTE_DIR}"
HOST = environ.get('REMOTE_HOST')
USER = environ.get('REMOTE_USER')
PASSWORD = environ.get('REMOTE_PASSWORD')


@contextmanager
def client_manager():
    try:
        client = RemoteClient(HOST, USER, PASSWORD)
        client.connect()
        yield client
    finally:
        client.disconnect()


def _extract_rb(value):
    return f'rb{re.search(r"rb(.*?)-", value).group(1)}'


def send_connection_ovpn(conexion, conexion_id):
    rb = _extract_rb(conexion)

    with client_manager() as client:
        # Create folder for this raspberry
        client.execute_commands([
            f'cmd.exe /c "mkdir {ABSOLUTE_REMOTE_DIR}"\\{rb}'
        ])

        # setup_file_inmemory = generate_inmemory_file(ovpn_file.file.read())
        client.upload_single_file_from_url(f'ficheros/raspberries/{conexion_id}/{conexion}.ovpn', f'{RELATIVE_REMOTE_DIR}/{rb}/{conexion}.ovpn')


def delete_connection_ovpn(conexion):
    rb = _extract_rb(conexion)

    with client_manager() as client:
        client.execute_commands([
            # Remove ovpn file
            f'cmd.exe /c "del {ABSOLUTE_REMOTE_DIR}\\{rb}\\{conexion}.ovpn"',
        ])


def create_connection(conexion, password, expiry_date):
    rb = _extract_rb(conexion)
    file_name = f'setup_{rb}_{random.randint(1,1000004)}'

    with client_manager() as client:
        # Create folder for this raspberry
        client.execute_commands([
            f'cmd.exe /c "mkdir {ABSOLUTE_REMOTE_DIR}"\\{file_name}'
        ])
        # Load file template
        setup_file_template = remote_bat_file('bats/setup.bat')

        # Fullfill template with conecttion data
        setup_file_content = setup_file_template.format(
            exe_passes=password,
            ids=conexion,
            ovpn_passes='test',
            expiry_dates=expiry_date,
            expiry_times='23:59',
            folder=file_name
        )
        setup_file_inmemory = generate_inmemory_file(setup_file_content.encode())
            
        client.upload_single_file(setup_file_inmemory, f'{RELATIVE_REMOTE_DIR}/{file_name}.bat')

        client.execute_commands([
            # Run setup_XXXX.bat
            f'cmd.exe /c "{ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
        ])

        # Download generated EXE file to local
        exe_file_name = f'{conexion}.exe'
        exe_file = client.download_file_into_memory(exe_file_name, f'{RELATIVE_REMOTE_DIR}/{file_name}/{exe_file_name}')

        client.execute_commands([
            # Remove recursively folder setup_XXXX
            f'cmd.exe /c rmdir "{ABSOLUTE_REMOTE_DIR}\\{file_name}" /s /q',
            # Remove file setup_XXXX.bat
            f'cmd.exe /c "del {ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
        ])

        return exe_file


def refresh_exe_connections(connections, expiry_date):
    ids, exe_passes, ovpn_passes, expiry_dates, expiry_times = generate_file_data(connections, expiry_date)
    file_name = f'setup_{random.randint(1,1000004)}'

    with client_manager() as client:
        # Create folder for this raspberry
        client.execute_commands([
            f'cmd.exe /c "mkdir {ABSOLUTE_REMOTE_DIR}"\\{file_name}'
        ])
        setup_file_template = remote_bat_file('bats/setup.bat')
        setup_file_content = setup_file_template.format(
            exe_passes='\n'.join(exe_passes),
            ids='\n'.join(ids),
            ovpn_passes='\n'.join(ovpn_passes),
            expiry_dates='\n'.join(expiry_dates),
            expiry_times='\n'.join(expiry_times),
            folder=file_name
        )
        setup_file_inmemory = generate_inmemory_file(setup_file_content.encode())
            
        client.upload_single_file(setup_file_inmemory, f'{RELATIVE_REMOTE_DIR}/{file_name}.bat')

        client.execute_commands([
            # Run setup_XXXX.bat
            f'cmd.exe /c "{ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
        ])

        # Download generated EXE files to local
        for c in connections:
            exe_file_name = f'{c["canper_id"]}.exe'
            client.download_file(exe_file_name, f'{RELATIVE_REMOTE_DIR}/{file_name}/{exe_file_name}')

        client.execute_commands([
            # Remove recursively folder setup_XXXX
            f'cmd.exe /c rmdir "{ABSOLUTE_REMOTE_DIR}\\{file_name}" /s /q',
            # Remove file setup_XXXX.bat
            f'cmd.exe /c "del {ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
        ])
        


def check_connections(ids, ovpn_passes):
    file_name = f'check_{random.randint(1,1000004)}'

    with client_manager() as client:
        template = remote_bat_file('bats/check.bat')
        check_file = template.format(
            ids='\n'.join(ids),
            ovpn_passes='\n'.join(ovpn_passes),
            file_name=f'{file_name}'
        )
        check_file_inmemory = generate_inmemory_file(check_file.encode())

        client.upload_single_file(check_file_inmemory, f'{RELATIVE_REMOTE_DIR}/{file_name}.bat')

        client.execute_commands([
            # Run chech_XXX.bat
            f'cmd.exe /c "{ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
            # Remove chech_XXX.bat
            f'cmd.exe /c "del {ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
            # Run chech_XXX.exe. It will generate a log_XXXX.csv file
            f'cmd.exe /c "{ABSOLUTE_REMOTE_DIR}\\{file_name}.exe"',
            # Remove chech_XXX.exe
            f'cmd.exe /c "del {ABSOLUTE_REMOTE_DIR}\\{file_name}.exe"',
        ])

        # Load log_XXXX.csv into memory
        # Download generated EXE file to local
        log_file_name = f'{file_name}.csv'
        log_file = client.download_file_into_memory(log_file_name, f'{RELATIVE_REMOTE_DIR}/{log_file_name}')

        client.execute_commands([
            # Remove file log_XXXX.csv
            f'cmd.exe /c "del {ABSOLUTE_REMOTE_DIR}\\{log_file_name}"',
        ])

        return log_file
