import os
import tempfile
from subprocess import call


def content_from_editor(action, initial):
    return os.linesep.join(lines_from_editor(action, initial))

def lines_from_editor(action, initial=None):
    if "EDITOR" not in os.environ:
        print(f"Environment variable EDITOR is not defined. Cannot run an editor to {action}.")
        exit(1)

    tf = tempfile.NamedTemporaryFile(suffix=".tmp", delete=False)
    if initial is not None:
        with tf as f:
            f.write(initial.encode('utf-8'))

    call([os.environ["EDITOR"], f.name])

    with open(tf.name, 'r') as f:
        edited = f.read()

    try:
        os.unlink(tf.name)
    except:
        pass

    lines = edited.splitlines()
    return [line for line in lines if not line.startswith('#')]


def open_in_browser(url):
    if "BROWSER" in os.environ:
        call([os.environ["BROWSER"], url])
    else:
        print(f'Cannot open {url} in a browser')


def not_implemented():
    print("Not yet implemented")
    exit(2)
