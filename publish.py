import shutil
import os
from pathlib import Path
import subprocess
import datetime


def format_kdb(tmp, _posts):

    ref = set(str(tmp).split("/"))
    ref.add("kdb")

    dest = _posts

    if dest.exists():
        shutil.rmtree(str(dest.resolve()))
    mds = list(tmp.glob("**/*.md"))

    dest.mkdir()

    for md in mds:
        name = "-".join(d for d in str(md).split("/") if d not in ref)

        is_main_readme = "-" not in name

        categories = "  - " + name.split("-")[0]
        _set = name.split("-")[0]

        date = datetime.datetime.fromtimestamp(int(os.path.getmtime(str(md))))
        new_name = "{}-{}-{}-{}".format(date.year, date.month, "01", name)

        new_file = dest / new_name
        with md.open("r") as f:
            lines = f.readlines()

        # fields = "title, categories, description, set"

        title = "error"
        for i, l in enumerate(lines):
            if l.startswith("# "):
                title = '"{}"'.format(
                    l.split("# ")[1]
                    .strip()
                    .encode("unicode-escape")
                    .decode("utf-8")
                    .replace('"', "'")
                )
                # lines[i] = ""
                if not is_main_readme:
                    break
            if is_main_readme and "<img" in l:
                lines[i] = ""
                break

        if is_main_readme:
            frontmatter = "---\nmain: true\n---"
        else:
            frontmatter = "---\ntitle: {}\ncategories:\n{}\nset: {}\n---\n\n".format(
                title, categories, _set
            )

        new_lines = [frontmatter] + lines

        with new_file.open("w") as f:
            f.writelines(new_lines)


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
    os.system("cd {} && git clone {}".format(str(tmp), repo))
    print("ok.")

    shutil.rmtree(_posts)
    _posts.mkdir()
    format_kdb(tmp, _posts)
    shutil.rmtree(tmp)

    os.system("rake publish")

    print("\nDone updating.")
