import shutil
from os import listdir, rmdir
from os.path import join

def _copy_directories(src, dst):
    try:
        for filename in listdir(src):
            shutil.move(join(src, filename), join(dst, filename))
        rmdir(src)
    except PermissionError:
        print(f"Could not copy files from {src} to {dst}, permission error")


if __name__ == "__main__":
    _copy_directories("cv", ".")
    print("All done")
