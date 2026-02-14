import os, sys

def main():
    # Remove the venv's bin from PATH so we don't recurse into .venv/bin/ruff
    venv_bin = os.path.join(sys.prefix, "bin")
    path_parts = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p and p != venv_bin]
    os.environ["PATH"] = os.pathsep.join(path_parts)

    # Now "ruff" should resolve to your Nix-provided binary on PATH.
    os.execvp("ruff", ["ruff", *sys.argv[1:]])

