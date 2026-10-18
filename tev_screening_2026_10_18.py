"""Apply the unchanged approved gate to Tev's native adapter in isolation."""
import importlib.util
from pathlib import Path
import subprocess
import sys
from hashlib import sha256

import tev_native_adapter_2026_10_18 as adapter

ROOT=Path(__file__).resolve().parent
CONTROL_SHA256='acba3a3b454b982946f9c121ab40770bcc522aee94e36a1b7f2771b062beb30a'
assert sha256((ROOT/'llm_screening_2026_10_18.py').read_bytes()).hexdigest()==CONTROL_SHA256
spec=importlib.util.spec_from_file_location('_tev_policy_controller_20261018',ROOT/'llm_screening_2026_10_18.py')
control=importlib.util.module_from_spec(spec)
spec.loader.exec_module(control)
control.run=adapter
# Receipts bind this wrapper; the immutable parent-controller dependency is
# additionally pinned by CONTROL_SHA256 above. No running chat process changes.
control.__file__=__file__


def invoke(model_id,*args):
    result=subprocess.run([sys.executable,str(ROOT/'tev_native_adapter_2026_10_18.py'),
                           '--model',model_id,*args],capture_output=True,text=True,cwd=ROOT)
    if result.stdout.strip():print(result.stdout.strip(),flush=True)
    if result.returncode:raise RuntimeError('Tev executor paused: '+result.stderr[-1600:])


control.invoke=invoke

if __name__=='__main__':control.main()
