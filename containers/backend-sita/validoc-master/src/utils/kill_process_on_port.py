def kill_process_on_port(port):
    try:
        current_pid = os.getpid()
        parent_pid = psutil.Process(current_pid).ppid()
        result = subprocess.run(['lsof', '-i', f':{port}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            lines = result.stdout.splitlines()
            pids = set((int(line.split()[1]) for line in lines[1:] if line.strip()))
            pids_to_kill = {pid for pid in pids if pid not in {current_pid, parent_pid}}
            for pid in pids_to_kill:
                try:
                    os.kill(pid, signal.SIGKILL)
                    logger.info(f'Killed process with PID: {pid}')
                except ProcessLookupError:
                    logger.info(f'Process with PID {pid} already terminated.')
        else:
            logger.info(f'No processes found on port {port}')
    except Exception as e:
        logger.error(f'Error: {e}')
def kill_process_on_port(port):
    try:
        current_pid = os.getpid()
        parent_pid = psutil.Process(current_pid).ppid()
        result = subprocess.run(['lsof', '-i', f':{port}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout:
            lines = result.stdout.splitlines()
            pids = set((int(line.split()[1]) for line in lines[1:] if line.strip()))
            pids_to_kill = {pid for pid in pids if pid not in {current_pid, parent_pid}}
            logger.info(f'Processes to kill on port {port}: {pids_to_kill}')
            for pid in pids_to_kill:
                try:
                    os.kill(pid, signal.SIGKILL)
                    logger.info(f'Killed process with PID: {pid}')
                except ProcessLookupError:
                    logger.error(f'Process with PID {pid} already terminated.')
        else:
            logger.info(f'No processes found on port {port}')
    except Exception as e:
        logger.error(f'Error: {e}')
