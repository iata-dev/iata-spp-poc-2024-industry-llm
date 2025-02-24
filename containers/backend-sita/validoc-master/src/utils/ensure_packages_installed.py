def ensure_packages_installed(packages):
    """
    Installs the specified list of Python packages using pip in silent mode.

    Parameters:
    - packages (list): A list of package names to be installed.

    Details:
    - Uses subprocess to invoke pip for package installation.
    - Redirects stdout and stderr to os.devnull to suppress all output (silent mode).
    - Alternative:
        * You can capture the output in a log file by replacing os.devnull with a file handle.
        * To enable verbose mode, omit stdout and stderr redirection.
    - Uses `sys.executable` to ensure the correct Python interpreter is used.

    Exceptions:
    - subprocess.CalledProcessError: Raised if any package installation fails, and logs the error.
    - sys.exit(1): Terminates the program if installation fails to avoid runtime issues due to missing dependencies.
    """
    try:
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *packages], stdout=devnull, stderr=devnull)
    except subprocess.CalledProcessError as e:
        logger.error(f'Error installing packages: {e}')
        sys.exit(1)
