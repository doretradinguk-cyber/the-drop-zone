"""CLI collection isolation and consumer lock regression."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
REPO=Path(__file__).resolve().parents[1]
class CollectionTests(unittest.TestCase):
 def test_collection_ingest_sync_and_wrong_root_rejected(self):
  with tempfile.TemporaryDirectory() as temp:
   root=Path(temp)/'drop';(root/'scripts').mkdir(parents=True)
   shutil.copy(REPO/'scripts/pipeline.py',root/'scripts/pipeline.py')
   for prefix in ['', 'retro-game-assets']:
    dest=root/prefix;dest.mkdir(parents=True,exist_ok=True)
    shutil.copy(REPO/prefix/'pipeline.config.json',dest/'pipeline.config.json')
    (dest/'catalog').mkdir();(dest/'catalog/catalog.json').write_text('{"schemaVersion":1,"assets":[]}')
   source=root/'test.png';source.write_bytes(b'fixture-only');project=Path(temp)/'consumer';project.mkdir()
   def cli(*args,collection=True):
    result=subprocess.run([sys.executable,str(root/'scripts/pipeline.py'),*(['--collection','retro-game-assets'] if collection else []),*map(str,args)],cwd=root,text=True,capture_output=True)
    return result
   result=cli('ingest',source,'--category','dashboard-ui','--licence','Original fixture');self.assertEqual(result.returncode,0,result.stderr)
   catalog=json.loads((root/'retro-game-assets/catalog/catalog.json').read_text());asset=catalog['assets'][0]
   self.assertTrue(asset['source'].startswith('sources/dashboard/ui/'))
   self.assertEqual(json.loads((root/'catalog/catalog.json').read_text())['assets'],[])
   self.assertEqual(cli('promote',asset['id'],source,'--target','dashboard').returncode,0)
   result=cli('sync','--target','dashboard','--project',project,'--ids',asset['id']);self.assertEqual(result.returncode,0,result.stderr)
   lock=json.loads((project/'public/data/assets.lock.json').read_text());self.assertEqual(lock['collection'],'retro-game-assets')
   result=cli('rehydrate','--target','dashboard','--project',project,collection=False);self.assertNotEqual(result.returncode,0);self.assertIn('another collection',result.stderr)
   result=cli('rehydrate','--target','dashboard','--project',project);self.assertEqual(result.returncode,0,result.stderr)
if __name__=='__main__':unittest.main()
