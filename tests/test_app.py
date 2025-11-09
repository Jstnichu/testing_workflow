import os
import subprocess
import time
import shutil
from pathlib import Path

import requests
import pytest


def node_available():
    return shutil.which("node") is not None


@pytest.fixture(scope="module")
def repo_root():
    # tests/ is directly under the repo root
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def server(repo_root):
    """
    Start the Node.js sample app as a subprocess and yield when it's ready.
    The fixture will stop the process after tests complete.
    """
    if not node_available():
        pytest.skip("node is required to run these tests")

    env = os.environ.copy()
    env.setdefault("NODE_ENV", "test")
    # run the server on port 8080 (default in index.js)
    proc = subprocess.Popen(["node", "index.js"], cwd=str(repo_root), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    url = "http://127.0.0.1:8080/"
    for _ in range(40):
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.25)
    else:
        proc.kill()
        stdout, stderr = proc.communicate(timeout=1)
        pytest.fail(f"Server did not start in time. stdout={stdout!r} stderr={stderr!r}")

    yield proc

    # teardown
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()


def test_root_response(server):
    r = requests.get("http://127.0.0.1:8080/")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert data.get("message") == "Hello from sample-app"
    assert "env" in data


def test_production_env(repo_root):
    """Start the server with NODE_ENV=production on a different port and assert env reflected."""
    if not node_available():
        pytest.skip("node is required to run these tests")

    env = os.environ.copy()
    env["NODE_ENV"] = "production"
    env["PORT"] = "8081"
    proc = subprocess.Popen(["node", "index.js"], cwd=str(repo_root), env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    url = "http://127.0.0.1:8081/"
    for _ in range(40):
        try:
            r = requests.get(url, timeout=1)
            if r.status_code == 200:
                break
        except Exception:
            time.sleep(0.25)
    else:
        proc.kill()
        stdout, stderr = proc.communicate(timeout=1)
        pytest.fail(f"Server (production) did not start. stdout={stdout!r} stderr={stderr!r}")

    try:
        r = requests.get(url)
        assert r.status_code == 200
        data = r.json()
        assert data.get("env") == "production"
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
