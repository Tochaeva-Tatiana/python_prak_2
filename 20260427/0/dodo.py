from pathlib import Path
from zipfile import ZipFile

DOIT_CONFIG = {"default_tasks": ['docs']}

def task_docs():
    """ Create docimentation"""

    rstpy = list(Path(".").glob("**/*.py")) + list(Path(".").glob("**/*.rst"))
    ext = {"html": "html", "text": "txt"}
    for i in ("html", "text"):
        yield {
            "name": f"{i} doc",
            "actions": [f"cd doc && sphinx-build -M {i} . _build"],
            "targets": [f"doc/_build/{i}/index.{ext[i]}"],
            "file_dep": rstpy,
        }


def task_erase():
    """Cleann all junk"""

    return {
        "actions" : ["rm -rf doc/_build"],
    }

def task_zip():
    """Create ZIP archive of docs"""

    def create_zip(fn, files):
        with ZipFile(fn, "w") as zf:
            for f in files:
                zf.write(f)


    files = list(Path("doc/_build/html").glob("**"))

    return {
        "actions" : [(create_zip, ["docs.zip", files])],
        "task_dep" : ["docs"],
    }

