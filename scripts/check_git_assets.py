"""CI/pre-push check: source binaries must be stored as LFS pointers in Git."""
import subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
records=subprocess.check_output(['git','ls-files','--stage','-z'],cwd=root).split(b'\0')
errors=[]
for record in records:
 if not record: continue
 meta,name=record.split(b'\t',1);path=name.decode();sha=meta.split()[1].decode()
 attr=subprocess.check_output(['git','check-attr','filter','--',path],cwd=root).decode().strip()
 if attr.endswith(': lfs'):
  size=int(subprocess.check_output(['git','cat-file','-s',sha],cwd=root))
  if size>1024 or not subprocess.check_output(['git','cat-file','-p',sha],cwd=root).startswith(b'version https://git-lfs.github.com/spec/v1\n'): errors.append(path)
if errors:
 print('Files staged without LFS pointers:\n'+'\n'.join(errors));sys.exit(1)
print('Git LFS pointer check passed')
