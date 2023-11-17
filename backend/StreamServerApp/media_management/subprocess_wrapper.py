from StreamingServer.settings import customstderr, customstdout
import subprocess


def run_subprocess(cmd):
    completed_process_instance = subprocess.run(cmd, stdout=customstdout,
                                                stderr=customstderr)
    if completed_process_instance.returncode != 0:
        print("An error occured while running ffmpeg subprocess")
        if (completed_process_instance.stderr):
            print(completed_process_instance.stderr.decode())
        if (completed_process_instance.stdout):
            print(completed_process_instance.stdout.decode())

        raise Exception('ffmpeg_error', 'error')

    return completed_process_instance.stdout
