
from contextlib import contextmanager
import random
from ssh_client.remote_client import RemoteClient

from ssh_client.helpers import remote_bat_file, generate_inmemory_file, generate_file_data


RELATIVE_REMOTE_DIR = "bat_runner"
ABSOLUTE_REMOTE_DIR = f"C:\\Users\\CASA\\Canper\\{RELATIVE_REMOTE_DIR}"


@contextmanager
def client_manager():
    try:
        client = RemoteClient('82.223.115.66', 'canper', '1234')
        client.connect()
        yield client
    finally:
        client.disconnect()

def create_connection(connection):
    file_name = f'setup_{connection.raspberry}_{random.randint(1,1000004)}'

    with client_manager() as client:
        # Create folder for this raspberry
        client.execute_commands([
            f'cmd.exe /c "mkdir {ABSOLUTE_REMOTE_DIR}"\\{connection.raspberry}'
        ])
        setup_file_template = remote_bat_file('bats/setup.bat')
        setup_file_content = setup_file_template.format(
            exe_passes=connection.exe_contraseña,
            ids=connection.canper_id,
            ovpn_passes='test',
            expiry_dates='25/03/2021',
            expiry_times='23:59',
            folder=file_name
        )
        setup_file_inmemory = generate_inmemory_file(setup_file_content)
            
        client.upload_single_file(setup_file_inmemory, f'{RELATIVE_REMOTE_DIR}/{file_name}.bat')

        client.execute_commands([
            # Run setup_XXXX.bat
            f'cmd.exe /c "{ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
        ])

        # Download generated EXE files to local
        for i in range(1, number_connections + 1):
            exe_file_name = f'{raspberry}-{i}.exe'
            client.download_file(exe_file_name, f'{RELATIVE_REMOTE_DIR}/{file_name}/{exe_file_name}')

        client.execute_commands([
            # Remove recursively folder setup_XXXX
            f'cmd.exe /c rmdir "{ABSOLUTE_REMOTE_DIR}\\{file_name}" /s /q',
            # Remove file setup_XXXX.bat
            f'cmd.exe /c "del {ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
        ])


def create_exe_connections(number_connections, raspberry, ovpn_passes):
    ids, exe_passes, ovpn_passes, expiry_dates, expiry_times = generate_file_data(number_connections, raspberry, ovpn_passes)
    file_name = f'setup_{raspberry}_{random.randint(1,1000004)}'

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
        setup_file_inmemory = generate_inmemory_file(setup_file_content)
            
        client.upload_single_file(setup_file_inmemory, f'{RELATIVE_REMOTE_DIR}/{file_name}.bat')

        client.execute_commands([
            # Run setup_XXXX.bat
            f'cmd.exe /c "{ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
        ])

        # Download generated EXE files to local
        for i in range(1, number_connections + 1):
            exe_file_name = f'{raspberry}-{i}.exe'
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
        check_file_inmemory = generate_inmemory_file(check_file)

        client.upload_single_file(check_file_inmemory, f'{RELATIVE_REMOTE_DIR}/{file_name}.bat')

        client.execute_commands([
            # Run chech_XXX.bat
            f'cmd.exe /c "{ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
            # Remove chech_XXX.bat
            f'cmd.exe /c "del {ABSOLUTE_REMOTE_DIR}\\{file_name}.bat"',
            # Run chech_XXX.exe
            f'cmd.exe /c "{ABSOLUTE_REMOTE_DIR}\\{file_name}.exe"',
            # Remove chech_XXX.exe
            f'cmd.exe /c "del {ABSOLUTE_REMOTE_DIR}\\{file_name}.exe"',
        ])

# create_exe_connections(2, 'RB0202', '1234')
# check_connections(['rb0202-1', 'rb0202-2'], ['11111', '11111'])