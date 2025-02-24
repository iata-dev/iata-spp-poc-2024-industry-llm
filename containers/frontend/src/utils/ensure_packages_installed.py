import sys
import subprocess

def ensure_packages_installed(packages):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', *packages])
        print('All packages installed successfully.')
    except subprocess.CalledProcessError as e:
        print(f'Error installing packages: {e}')
        sys.exit(1)

