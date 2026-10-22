"""Apply the unchanged approved gate to Tev's native adapter in isolation."""
from repo_layout import source_file
import importlib.util
from pathlib import Path
import subprocess
import sys
from hashlib import sha256

import tev_native_adapter_2026_10_18 as adapter

ROOT=Path(__file__).resolve().parents[1]
CONTROL_SHA256='d73699f919d8816cde38c53a9edc6ee67eeaaee924a627b860eaba0bae0b5bc4'
assert sha256(source_file(ROOT/'llm_screening_2026_10_18.py').read_bytes()).hexdigest()==CONTROL_SHA256
spec=importlib.util.spec_from_file_location('_tev_policy_controller_20261018',source_file(ROOT/'llm_screening_2026_10_18.py'))
control=importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)
control.run=adapter
# Receipts bind this wrapper; the relocated parent controller is also pinned
# above. Historical receipt checks use its exact pre-layout snapshot separately.
control.__file__=__file__


def invoke(model_id,*args):
    result=subprocess.run([sys.executable,str(source_file(ROOT/'tev_native_adapter_2026_10_18.py')),
                           '--model',model_id,*args],capture_output=True,text=True,cwd=ROOT)
    if result.stdout.strip():print(result.stdout.strip(),flush=True)
    if result.returncode:raise RuntimeError('Tev executor paused: '+result.stderr[-1600:])


control.invoke=invoke

if __name__=='__main__':control.main()
