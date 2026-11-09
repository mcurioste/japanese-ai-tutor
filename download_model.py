from pathlib import Path
from urllib.request import urlopen, Request
import hashlib

NAME = 'Qwen2.5-0.5B-Instruct-Q4_K_M.gguf'
URL = 'https://huggingface.co/bartowski/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/' + NAME
SHA256 = '6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653'
TARGET = Path(__file__).resolve().parent / 'models' / NAME
TEMP = TARGET.with_suffix('.gguf.part')

TARGET.parent.mkdir(exist_ok=True)
if TARGET.exists():
    h = hashlib.sha256(TARGET.read_bytes()).hexdigest()
    if h == SHA256:
        print('Model already downloaded and verified:', TARGET)
        raise SystemExit(0)
    print('Existing file has unexpected checksum. Downloading replacement.')

print('Downloading ~398 MB model into models/ ...')
try:
    with urlopen(Request(URL, headers={'User-Agent': 'JapaneseTutorDemo/1.0'}), timeout=60) as response, open(TEMP, 'wb') as dest:
        digest = hashlib.sha256()
        count = 0
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            dest.write(block)
            digest.update(block)
            count += len(block)
            if count % (25 * 1024 * 1024) < len(block):
                print(f'{count // (1024 * 1024)} MiB downloaded')
    if digest.hexdigest() != SHA256:
        raise RuntimeError('Checksum mismatch; download was not saved. Check the model page for updated hash.')
    TEMP.replace(TARGET)
    print('Done:', TARGET)
except Exception:
    TEMP.unlink(missing_ok=True)
    raise
