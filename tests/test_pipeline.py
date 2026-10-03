import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile
from types import SimpleNamespace as Args
spec=importlib.util.spec_from_file_location('pipeline',Path(__file__).resolve().parents[1]/'scripts/pipeline.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
REAL_ROOT=p.ROOT
class PipelineTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.base=Path(self.temp.name);p.ROOT=self.base/'drop';p.ROOT.mkdir();(p.ROOT/'catalog').mkdir();shutil.copy(REAL_ROOT/'pipeline.config.json',p.ROOT/'pipeline.config.json');p.write(p.ROOT/'catalog/catalog.json',{'schemaVersion':1,'assets':[]});self.project=self.base/'project';self.project.mkdir()
 def tearDown(self): p.ROOT=REAL_ROOT;self.temp.cleanup()
 def ingest(self,name='source.png',content=b'source'):
  file=self.base/name;file.write_bytes(content);p.ingest(Args(file=str(file),category='textures',name=None,tags=['test'],licence='Original test fixture',provenance='test'));return p.catalog()['assets'][0]['id']
 def promote(self,id,content=b'optimised'):
  file=self.base/'export.webp';file.write_bytes(content);p.promote(Args(id=id,file=str(file),target='game',licence=None))
 def test_ingest_deduplicates_without_removing_original(self):
  self.ingest();self.ingest('duplicate.png');self.assertEqual(len(p.catalog()['assets']),1);self.assertTrue((self.base/'source.png').exists());p.verify(None)
 def test_selected_exports_and_checksum_tampering(self):
  id=self.ingest();self.promote(id);p.sync(Args(target='game',project=str(self.project),ids=[id]));lock=p.read(self.project/'assets/assets.lock.json');self.assertEqual(len(lock['assets']),1);self.assertEqual((self.project/lock['assets'][0]['file']).read_bytes(),b'optimised');self.assertFalse((self.project/'source.png').exists());export=p.ROOT/p.catalog()['assets'][0]['exports'][0]['path'];export.write_bytes(b'changed');self.assertRaises(ValueError,p.sync,Args(target='game',project=str(self.project),ids=[id]))
 def test_no_runtime_copy_without_prepared_export(self):
  id=self.ingest();self.assertRaises(ValueError,p.sync,Args(target='game',project=str(self.project),ids=[id]));self.assertFalse((self.project/'assets').exists())
 def test_rehydrate_restores_locked_version_not_latest(self):
  id=self.ingest();self.promote(id,b'first');p.sync(Args(target='game',project=str(self.project),ids=[id]));lock=p.read(self.project/'assets/assets.lock.json');runtime=self.project/lock['assets'][0]['file'];runtime.unlink();self.promote(id,b'second');p.rehydrate(Args(target='game',project=str(self.project)));self.assertEqual(runtime.read_bytes(),b'first');self.assertEqual(p.read(self.project/'assets/assets.lock.json'),lock)
 def test_budget_rejects_before_writing(self):
  id=self.ingest();cfg=p.config();cfg['budgets']['game']['fileBytes']=2;p.write(p.ROOT/'pipeline.config.json',cfg);self.assertRaises(ValueError,self.promote,id);self.assertEqual(p.catalog()['assets'][0]['exports'],[])
 def test_zip_traversal_rejected_before_extraction(self):
  zip=self.base/'bad.zip'
  with zipfile.ZipFile(zip,'w') as z:z.writestr('good.png',b'a');z.writestr('../escape.txt',b'b')
  self.assertRaises(ValueError,p.unpack,Args(file=str(zip)));self.assertFalse((self.base/'escape.txt').exists());self.assertFalse((p.ROOT/'staging').exists())
 def test_safe_zip_preserves_mesh_dependency_paths(self):
  zip=self.base/'mesh.zip'
  with zipfile.ZipFile(zip,'w') as z:z.writestr('Model Folder/model.gltf','{}');z.writestr('Model Folder/texture.png',b'img')
  p.unpack(Args(file=str(zip)));matches=list((p.ROOT/'staging').glob('*/Model Folder/model.gltf'));self.assertEqual(len(matches),1);self.assertTrue(matches[0].with_name('texture.png').exists())
 def test_lfs_pointer_is_not_ingested_as_an_asset(self):
  f=self.base/'pointer.png';f.write_text('version https://git-lfs.github.com/spec/v1\noid sha256:abcd\nsize 10\n');self.assertRaises(ValueError,p.source_file,f)
 def test_source_and_runtime_paths_cannot_escape(self):
  self.assertRaises(ValueError,p.safe,self.project,'../escape');self.assertRaises(ValueError,p.safe,self.project,'/tmp/escape')
 def test_catalog_publish_copies_metadata_only(self):
  self.ingest();p.publish_catalog(Args(project=str(self.project)));self.assertEqual(len(p.read(self.project/'public/data/catalog.json')['assets']),1);self.assertEqual(len(list(self.project.rglob('*.*'))),1)
if __name__=='__main__':unittest.main()
