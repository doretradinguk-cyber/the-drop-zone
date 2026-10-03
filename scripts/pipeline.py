"""Drop Zone pipeline. Python 3.10+, standard library only. Does not execute assets."""
import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
ROOT = Path(__file__).resolve().parents[1]
ACTIVE_COLLECTION = None
EXTENSIONS = {
 'textures': '.png .jpg .jpeg .webp .tga .tif .tiff .bmp .psd .psb .dds .ktx2',
 'models': '.fbx .obj .gltf .glb .blend .bin .mtl',
 'shaders': '.gdshader .glsl .vert .frag .shader',
 'audio': '.wav .mp3 .ogg .flac .aiff .aif',
 'hdri': '.hdr .exr', 'sprites': '', 'animations': '.anim .tres .tscn',
 'backgrounds': '', 'blueprints': '.pdf', 'text': '.txt .md .json .csv .yaml .yml',
 'fonts': '.ttf .otf .woff .woff2', 'references': '.mp4 .webm .mov .avi',
 'packages': '.zip .7z .rar .tar .gz',
}
RUNTIME = {
 'dashboard': {'.png','.jpg','.jpeg','.webp','.avif','.ogg','.mp3','.wav','.mp4','.webm','.woff2'},
 'game': {'.png','.jpg','.jpeg','.webp','.ktx2','.ogg','.wav','.mp3','.glb','.ttf','.otf'},
}
def now(): return datetime.now(timezone.utc).isoformat()
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def write(path, data):
 path.parent.mkdir(parents=True,exist_ok=True)
 # Atomic manifest update; one operator at a time (no multi-writer service).
 fd,tmp=tempfile.mkstemp(prefix='catalog-',suffix='.tmp',dir=path.parent)
 try:
  with os.fdopen(fd,'w',encoding='utf-8') as f: json.dump(data,f,indent=2,ensure_ascii=False);f.write('\n')
  os.replace(tmp,path)
 finally:
  if os.path.exists(tmp): os.unlink(tmp)
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
 return h.hexdigest()
def safe(root, relative):
 p=Path(relative)
 if p.is_absolute() or '..' in p.parts: raise ValueError('Unsafe relative path')
 dest=root/p
 if dest.is_symlink() or not dest.resolve().is_relative_to(root.resolve()): raise ValueError('Path escapes its root')
 return dest

def source_file(path):
 p=Path(path).resolve()
 if not p.is_file(): raise ValueError(f'File not found: {p}')
 with p.open('rb') as f:
  if f.read(128).startswith(b'version https://git-lfs.github.com/spec/v1'): raise ValueError('This is an LFS pointer. Run git lfs pull first.')
 return p

def slug(value):
 return re.sub(r'[^a-z0-9]+','_',value.lower()).strip('_')[:70] or 'asset'
def config(): return read(ROOT/'pipeline.config.json')
def catalog(): return read(ROOT/'catalog/catalog.json')
def get_asset(data, id):
 for asset in data['assets']:
  if asset['id']==id: return asset
 raise ValueError(f'Unknown asset: {id}')
def copy_verified(src,dest,sha):
 dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists():
  if not dest.is_file() or digest(dest)!=sha: raise ValueError(f'Refusing to overwrite different content: {dest}')
  return
 # Exclusive output prevents accidental overwrite.
 try:
  with src.open('rb') as inp, dest.open('xb') as out: shutil.copyfileobj(inp,out)
  if digest(dest)!=sha: raise ValueError('Copy checksum mismatch')
 except Exception:
  if dest.is_file(): dest.unlink()
  raise

def ingest(args):
 src=source_file(args.file);data=catalog();cfg=config();ext=src.suffix.lower()
 category=args.category or next((k for k,v in EXTENSIONS.items() if ext in v.split()),None)
 if category not in cfg['categories']: raise ValueError('Unknown type: choose --category explicitly')
 sha=digest(src)
 for item in data['assets']:
  if item['sha256']==sha:
   print(f"Already archived: {item['id']} (original left untouched)");return
 name=slug(src.stem);id=f'{name}_{sha[:12]}'
 dest=safe(ROOT,str(Path(cfg['categories'][category])/id/(name+ext)))
 copy_verified(src,dest,sha)
 item={'id':id,'name':args.name or src.stem,'category':category,'tags':args.tags or [],'originalName':src.name,'source':dest.relative_to(ROOT).as_posix(),'sha256':sha,'bytes':src.stat().st_size,'licence':args.licence or 'unreviewed','provenance':args.provenance or '', 'addedAt':now(),'exports':[]}
 data['assets'].append(item);write(ROOT/'catalog/catalog.json',data)
 print(f'Archived {id}\nSource unchanged. Catalogue: catalog/catalog.json')

def unpack(args):
 src=source_file(args.file)
 if src.suffix.lower()!='.zip': raise ValueError('Safe unpack supports ZIP only. Other packages can be archived intact.')
 # Validate every entry before writing any content; preserve relative names for mesh dependencies.
 with zipfile.ZipFile(src) as z:
  infos=z.infolist();size=sum(i.file_size for i in infos)
  if len(infos)>10000 or size>2*1024**3: raise ValueError('ZIP exceeds 10,000 entries or 2 GiB expanded limit')
  names=set()
  for info in infos:
   name=info.filename;p=PurePosixPath(name)
   if '\\' in name or ':' in name or p.is_absolute() or '..' in p.parts or any(x.startswith('.') for x in p.parts): raise ValueError(f'Unsafe ZIP path: {name}')
   if any(x.endswith((' ','.')) or x.split('.')[0].upper() in {'CON','PRN','AUX','NUL',*[f'COM{i}' for i in range(1,10)],*[f'LPT{i}' for i in range(1,10)]} for x in p.parts): raise ValueError('ZIP contains a Windows-incompatible path')
   key=p.as_posix().rstrip('/').casefold()
   if key in names: raise ValueError('Duplicate or case-colliding ZIP paths')
   names.add(key)
   mode=info.external_attr>>16
   if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0,stat.S_IFREG,stat.S_IFDIR)): raise ValueError('ZIP special files are not supported')
   if info.flag_bits&1: raise ValueError('Encrypted ZIP not supported')
   if info.file_size>512*1024**2 or (info.file_size>10*1024**2 and info.file_size/max(info.compress_size,1)>200): raise ValueError('Suspicious ZIP expansion ratio or entry size')
  dest=ROOT/'staging'/f'{slug(src.stem)}_{digest(src)[:12]}'
  if dest.exists(): raise ValueError(f'Staging directory already exists: {dest}')
  dest.parent.mkdir(parents=True,exist_ok=True)
  with tempfile.TemporaryDirectory(dir=dest.parent,prefix='unpack-') as temp:
   temp=Path(temp)
   for info in infos:
    out=safe(temp,info.filename)
    if info.is_dir(): out.mkdir(parents=True,exist_ok=True);continue
    out.parent.mkdir(parents=True,exist_ok=True)
    with z.open(info) as inp,out.open('xb') as f: shutil.copyfileobj(inp,f)
   # Keep atomic final directory after extraction and CRC checks succeed.
   temp.rename(dest)
 print(f'Inspected and unpacked to {dest}\nNames preserved to protect linked mesh/material references. No code executed. Archive the ZIP separately with ingest.')

def promote(args):
 data=catalog();asset=get_asset(data,args.id);src=source_file(args.file)
 licence=args.licence or asset['licence']
 if licence.strip().lower() in ('','unknown','unreviewed'): raise ValueError('Record a reviewed licence using --licence before preparing an export')
 if src.suffix.lower() not in RUNTIME[args.target]: raise ValueError('Unsupported runtime format. Prepare a self-contained image/audio/font or GLB export first; code and source archives are not copied into apps.')
 budget=config()['budgets'][args.target]['fileBytes']
 if src.stat().st_size>budget: raise ValueError(f'Export exceeds the configured {budget} byte per-file budget')
 sha=digest(src)
 for e in asset['exports']:
  if e['target']==args.target and e['sha256']==sha: print('This export is already prepared');return
 version=1+max((e['version'] for e in asset['exports'] if e['target']==args.target),default=0)
 name=slug(src.stem)+src.suffix.lower()
 dest=safe(ROOT,f"exports/{args.target}/{asset['id']}/v{version}/{name}")
 copy_verified(src,dest,sha)
 asset['exports'].append({'target':args.target,'version':version,'path':dest.relative_to(ROOT).as_posix(),'sha256':sha,'bytes':src.stat().st_size,'licence':licence,'preparedAt':now()})
 write(ROOT/'catalog/catalog.json',data);print(f'Prepared {dest.relative_to(ROOT)}; source preserved. No automatic optimisation was performed.')

def sync(args):
 data=catalog();project=Path(args.project).resolve()
 if not project.is_dir() or project==ROOT: raise ValueError('Choose an existing dashboard or game checkout')
 manifest_rel='public/data/assets.lock.json' if args.target=='dashboard' else 'assets/assets.lock.json'
 output_rel='public/assets/runtime' if args.target=='dashboard' else 'assets/runtime'
 manifest=safe(project,manifest_rel);safe(project,output_rel)
 selected=[];total=0
 for id in dict.fromkeys(args.ids):
  asset=get_asset(data,id);versions=[e for e in asset['exports'] if e['target']==args.target]
  if not versions: raise ValueError(f'No {args.target} export prepared for {id}')
  e=max(versions,key=lambda e:e['version']);src=source_file(safe(ROOT,e['path']))
  if digest(src)!=e['sha256'] or src.stat().st_size!=e['bytes']: raise ValueError(f'Export modified since preparation: {id}')
  budget=config()['budgets'][args.target]
  if e['bytes']>budget['fileBytes']: raise ValueError(f'Export exceeds per-file budget: {id}')
  total+=e['bytes']
  filename=f"{asset['id']}_v{e['version']}_{e['sha256'][:12]}{src.suffix.lower()}"
  dest=safe(project,f'{output_rel}/{filename}')
  if dest.exists() and digest(dest)!=e['sha256']: raise ValueError('Existing runtime file was modified; refusing to overwrite it')
  selected.append((src,dest,{'id':id,'version':e['version'],'source':e['path'],'file':dest.relative_to(project).as_posix(),'sha256':e['sha256'],'bytes':e['bytes'],'licence':e['licence']}))
 if total>config()['budgets'][args.target]['totalBytes']: raise ValueError('Selection exceeds target total-byte budget')
 for src,dest,e in selected: copy_verified(src,dest,e['sha256'])
 write(manifest,{'schemaVersion':1,'collection':ACTIVE_COLLECTION,'target':args.target,'totalBytes':total,'assets':[e for _,_,e in selected]})
 print(f'Synced {len(selected)} selected exports ({total} bytes). Lock: {manifest}\nPrevious unselected cached files are retained; only the lock lists this selection.')

def rehydrate(args):
 project=Path(args.project).resolve()
 manifest=safe(project,'public/data/assets.lock.json' if args.target=='dashboard' else 'assets/assets.lock.json')
 data=read(manifest)
 if data.get('collection')!=ACTIVE_COLLECTION: raise ValueError('Lock belongs to another collection; select its matching --collection option')
 if data.get('schemaVersion')!=1 or data.get('target')!=args.target: raise ValueError('Lock version or target mismatch')
 output='public/assets/runtime/' if args.target=='dashboard' else 'assets/runtime/'
 selected=[];total=0;seen=set();cfg=config()['budgets'][args.target]
 for e in data['assets']:
  if not e['source'].startswith('exports/'+args.target+'/') or not e['file'].startswith(output): raise ValueError('Lock path outside permitted export/runtime directories')
  if e['file'] in seen: raise ValueError('Duplicate runtime destination')
  seen.add(e['file'])
  src=source_file(safe(ROOT,e['source']));dest=safe(project,e['file'])
  if src.suffix.lower() not in RUNTIME[args.target] or dest.suffix.lower()!=src.suffix.lower(): raise ValueError('Invalid runtime file format')
  if digest(src)!=e['sha256'] or src.stat().st_size!=e['bytes']: raise ValueError('Locked source checksum/size mismatch')
  if e['bytes']>cfg['fileBytes']: raise ValueError('Locked file exceeds current budget')
  if dest.exists() and digest(dest)!=e['sha256']: raise ValueError('Runtime file was modified; refusing to overwrite')
  total+=e['bytes'];selected.append((src,dest,e))
 if total>cfg['totalBytes'] or total!=data['totalBytes']: raise ValueError('Lock size or budget mismatch')
 for src,dest,e in selected: copy_verified(src,dest,e['sha256'])
 print(f'Restored {len(selected)} exact locked exports; lock unchanged')

def publish_catalog(args):
 project=Path(args.project).resolve()
 if not project.is_dir() or project==ROOT: raise ValueError('Choose the dashboard checkout')
 dest=safe(project,'public/data/catalog.json');write(dest,catalog());print(f'Copied catalogue only to {dest}')

def verify(args):
 data=catalog();ids=set()
 if data.get('schemaVersion')!=1: raise ValueError('Unsupported catalogue version')
 for a in data['assets']:
  if a['id'] in ids: raise ValueError('Duplicate asset ID')
  ids.add(a['id'])
  for e in [{'path':a['source'],'sha256':a['sha256'],'bytes':a['bytes']},*a['exports']]:
   p=source_file(safe(ROOT,e['path']))
   if digest(p)!=e['sha256'] or p.stat().st_size!=e['bytes']: raise ValueError(f"Checksum/size mismatch: {e['path']}")
 print(f"Verified {len(ids)} assets and their exports")

def main():
 global ROOT, ACTIVE_COLLECTION
 bootstrap=argparse.ArgumentParser(add_help=False)
 bootstrap.add_argument('--collection',choices=['retro-game-assets'],help='Use the dedicated retro game asset collection (place before the command)')
 selected,_=bootstrap.parse_known_args()
 if selected.collection:
  ROOT=safe(ROOT,selected.collection);ACTIVE_COLLECTION=selected.collection
 p=argparse.ArgumentParser(description=__doc__,parents=[bootstrap]);s=p.add_subparsers(dest='command',required=True)
 a=s.add_parser('ingest',help='Copy one source into archive and catalogue');a.add_argument('file');a.add_argument('--category',choices=list(config()['categories']));a.add_argument('--name');a.add_argument('--tags',nargs='*');a.add_argument('--licence');a.add_argument('--provenance');a.set_defaults(func=ingest)
 a=s.add_parser('unpack',help='Validate and extract a ZIP to ignored staging');a.add_argument('file');a.set_defaults(func=unpack)
 a=s.add_parser('promote',help='Register an already optimised runtime export');a.add_argument('id');a.add_argument('file');a.add_argument('--target',choices=RUNTIME,required=True);a.add_argument('--licence');a.set_defaults(func=promote)
 a=s.add_parser('sync',help='Copy only selected exports and write a lock manifest');a.add_argument('--target',choices=RUNTIME,required=True);a.add_argument('--project',required=True);a.add_argument('--ids',nargs='+',required=True);a.set_defaults(func=sync)
 a=s.add_parser('rehydrate',help='Restore exact versions from an existing consumer lock');a.add_argument('--target',choices=RUNTIME,required=True);a.add_argument('--project',required=True);a.set_defaults(func=rehydrate)
 a=s.add_parser('publish-catalog',help='Copy metadata to the dashboard (no binary files)');a.add_argument('--project',required=True);a.set_defaults(func=publish_catalog)
 a=s.add_parser('verify',help='Verify sources and exports against hashes');a.set_defaults(func=verify)
 args=p.parse_args()
 try: args.func(args)
 except (ValueError,OSError,KeyError,zipfile.BadZipFile,json.JSONDecodeError) as e: print(f'ERROR: {e}',file=sys.stderr);return 1
 return 0
if __name__=='__main__': sys.exit(main())
