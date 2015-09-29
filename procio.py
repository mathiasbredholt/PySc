from subprocess import PIPE, STDOUT, Popen
from threading import Thread
from queue import Queue, Empty


def run(cmd):
    proc = Popen(cmd,
                 stdout=PIPE,
                 stdin=PIPE,
                 stderr=STDOUT,
                 universal_newlines=True,
                 bufsize=1)

    queue = Queue()
    thread = Thread(target=enqueue_output, args=(proc.stdout, queue))
    thread.daemon = True  # thread dies with the program
    thread.start()

    # Catch initial output
    # process_input(proc, queue, thread, 20)
    return (proc, queue, thread)


def process_input(proc, queue, thread, wait=0, single=False):
    try:
        line = queue.get(timeout=wait)  # or q.get(timeout=.1)
    except Empty:
        return ""
    else:  # got line
        if single:
            return line
        else:
            return line + process_input(proc, queue, thread, wait)


def print_input(proc, queue, thread, wait=0, single=False):
    try:
        line = queue.get(timeout=wait)  # or q.get(timeout=.1)
    except Empty:
        return ""
    else:  # got line
        print(line.strip("\n"))
        if not single:
            process_input(proc, queue, thread, wait)


def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()
