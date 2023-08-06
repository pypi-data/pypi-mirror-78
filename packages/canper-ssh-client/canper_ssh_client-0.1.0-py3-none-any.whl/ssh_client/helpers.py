from io import BytesIO
from os import path
import secrets
import string
from datetime import date
from dateutil.relativedelta import relativedelta


def remote_bat_file(filename):
    script_dir = path.dirname(__file__)
    abs_file_path = path.join(script_dir, filename)
    with open(abs_file_path, 'r') as file:
        return file.read()

def generate_inmemory_file(file_content):
    fl = BytesIO()
    fl.write(file_content.encode())
    fl.seek(0)
    return fl

def _generate_random_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(12))


def generate_file_data(n, raspberry, ovpn_pass):
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
