from pathlib import Path
from sys import exit
import tempfile

from invoke import call, task


# TODO tasks.py may not be in cwd
SRCDIR = Path(__file__).resolve().parent
BUILDDIR = SRCDIR.joinpath("build")


@task
def dirs(c):
    SRCDIR.joinpath("images", "logos").mkdir(parents=True, exist_ok=True)
    BUILDDIR.mkdir(parents=True, exist_ok=True)


@task(dirs)
def logo(c):
    logodir = SRCDIR.joinpath("images", "logos")

    if logodir.joinpath("MIT-logo-red-gray.eps").exists():
        return

    print(
        "Use your browser to download the zip file into ./images/logos (MIT certificate required)"
    )
    logourl = (
        "https://web.mit.edu/graphicidentity/download/logo-sets/MIT-logos-print.zip"
    )
    print("\t" + logourl)  # TODO try to download ourselves

    from invocations.console import confirm

    if not confirm("Have you downloaded the zip file?"):
        exit(1)

    zippath = logodir.joinpath("MIT-logos-print.zip")

    if not logodir.joinpath("MIT-logos-print.zip").exists():
        print("You failed to download the zip file")
        exit(1)

    with tempfile.TemporaryDirectory() as d:
        c.run(f"unzip -q {zippath} -d {d}")
        c.run(f"mv {d}/MIT-logos-print/*.eps {logodir}")

    c.run(f"rm {zippath}")


@task(dirs)
def compile(c, name):
    c.run(f"latexmk {name}.tex", env={"LOCALPAPERBUILD": "1"})


@task(logo, call(compile, "poster"))
def poster(c):
    """Compile poster.pdf"""
    pass


@task(call(compile, "main"))
def main(c):
    """Compile main.pdf"""
    pass


@task(main)
def arxiv(c):
    """Prepare arXiv submission tarball"""
    c.run("rm -rf arxiv")
    c.run("mkdir arxiv")
    c.run("./arxiv.py")
    with c.cd("arxiv"):
        c.run("make main")
        c.run("make clean")
    c.run("tar -c -z -f submission.tar.gz -C arxiv .")
    c.run("mv submission.tar.gz arxiv")


@task(main, poster)
def examples(c):
    """Compile example documents"""
    d = SRCDIR.joinpath("examples")
    if not d.exists():
        d.mkdir()

    for name in ("main", "poster"):
        p = BUILDDIR.joinpath(name + ".pdf")
        c.run(f"cp {p} {d}")


@task
def clean(c):
    """Clean LaTeX build files"""
    c.run(f"rm -rf {BUILDDIR}")


@task
def push(c):
    """Push to remote"""
    c.run("git push origin master")


@task
def pull(c):
    """Pull from remote"""
    c.run("git pull origin master")
