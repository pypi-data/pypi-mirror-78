import os
import subprocess


def ensure_dir(f):
    folder = os.path.dirname(f)
    if folder != '' and not os.path.isdir(folder):
        os.makedirs(folder)


def touch(f):
    if os.path.isfile(f):
        os.utime(f, None)
    else:
        open(f, 'w').close()


def touch_mkdir(f):
    ensure_dir(f)
    touch(f)


def touch_mkdir_many(filenames):
    for filename in filenames:
        touch_mkdir(filename)


def no_err_run(args):
    assert type(args) == list
    subprocess.call(args)

