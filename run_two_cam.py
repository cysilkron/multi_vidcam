import subprocess

subprocess.Popen(f'python queue_read_frame.py --src 0 --save --save_dir "./frames/src_0"')
subprocess.Popen(f'python queue_read_frame.py --src 1 --save --save_dir "./frames/src_1"')
