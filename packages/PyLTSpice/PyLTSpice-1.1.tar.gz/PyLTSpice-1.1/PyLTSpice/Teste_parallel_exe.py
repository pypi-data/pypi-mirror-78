import subprocess
import threading
from queue import Queue
from time import sleep
info_back = Queue()


def launch_simulation(no, command):
    result = subprocess.run(command)


threads = []
commands = (
    [r"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe"],
    [r"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe"],
    [r"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe"]
)

# Launch our function in a thread
print("Launching")
for i, command in enumerate(commands):
    t = threading.Thread(target=launch_simulation, args=(i, command,), name="LTSPICE_SIM{}".format(i))
    threads.append(t)
    t.start()


# Joining all
print("Joining")

still_running = True
while still_running:
    still_running = False
    alive = 0
    for one_thread in threads:
        if one_thread.is_alive():
            alive += 1
            still_running = True
    print("Threads alive ", alive)
    sleep(0.5)

