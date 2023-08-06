from io import BytesIO
from os import path
import secrets
import string
from datetime import date


def remote_bat_file(filename):
    script_dir = path.dirname(__file__)
    abs_file_path = path.join(script_dir, filename)
    with open(abs_file_path, 'r') as file:
        return file.read()

def generate_inmemory_file(file_content):
    fl = BytesIO()
    fl.write(file_content)
    fl.seek(0)
    return fl

def _generate_random_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(12))


def generate_file_data(connections, expiry_date):
    ids = []
    exe_passes = []
    ovpn_passes = []
    expiry_dates = []
    expiry_times = []

    for c in connections:
        ids.append(c['canper_id'])
        exe_passes.append(c['exe_contraseña'])
        ovpn_passes.append(c['raspberry']['ovpn_contraseña'])
        expiry_dates.append(expiry_date.strftime('%d-%m-%Y'))
        expiry_times.append('23:59')

    return ids, exe_passes, ovpn_passes, expiry_dates, expiry_times
