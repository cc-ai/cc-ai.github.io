import shutil
import os
from pathlib import Path
import subprocess

if __name__ == "__main__":
    p = Path()

    repo = "git@github.com:cc-ai/kdb.git"

    assert all(
        f in [d.name for d in p.iterdir() if d.is_dir()] for f in {"_site", "_posts"}
    )

    branches = subprocess.check_output(["git", "branch"]).strip().decode("utf-8")
    current = [b for b in branches.split("\n") if "*" in b][0]
    assert "source" in current

    tmp = p / "tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    _posts = p / "_posts"

    print("Fetching files...", end="")
    os.system("cd {} && git clone {} && python format.py".format(str(tmp), repo))
    print("ok.")

    shutil.rmtree(_posts)
    shutil.move(tmp, _posts)

    os.system("rake publish")

    print("\nDone updating.")
