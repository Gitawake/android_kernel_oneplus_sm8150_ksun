"""Merge verified MindTheGapps/Gboard/KernelSU APKs into mounted offline ext4 copies.
Run as root in Linux. Stock partition sizes and existing files are retained.
"""
import argparse, hashlib, json, os, shutil, zipfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args();root=a.root.resolve()
mounts=root/'mounts';stage=root/'gapps-stage'
assert (mounts/'system/system/build.prop').is_file()
assert 'ro.build.version.sdk=37' in (mounts/'system/system/build.prop').read_text()
assert not stage.exists(), 'Use a fresh staging directory'
shutil.copytree(root/'gapps17/system',stage)
# Match MindTheGapps' non-Pixel-Tablet installation branch.
shutil.rmtree(stage/'product/priv-app/VelvetTitan',ignore_errors=True)
gboard=stage/'product/app/LatinIMEGooglePrebuilt';gboard.mkdir(parents=True,exist_ok=True)
for apk in sorted((root/'device-readonly/Gboard').glob('*.apk')):
 shutil.copy2(apk,gboard/apk.name)
assert (gboard/'base.apk').is_file()
manager=stage/'product/app/KernelSUNext';manager.mkdir(parents=True,exist_ok=True)
shutil.copy2(root/'KernelSU_Next_v3.4.2_33355-release.apk',manager/'KernelSUNext.apk')
addon=stage/'addon.d';head=(addon/'addond_head').read_text();tail=(addon/'addond_tail').read_text()
files=sorted(str(f.relative_to(stage)) for f in stage.rglob('*') if f.is_file() and not f.is_relative_to(addon))
(addon/'30-gapps.sh').write_text(head+'\n'.join(files)+'\n'+tail)
(addon/'addond_head').unlink();(addon/'addond_tail').unlink()
# Only change the offline copied product image, never the host filesystem.
shutil.rmtree(mounts/'product/app/LatinIME',ignore_errors=True)
shutil.rmtree(mounts/'product/app/LatinIMEGooglePrebuilt',ignore_errors=True)
(mounts/'product/overlay/LatinIME__lineage_hotdog__auto_generated_rro_product.apk').unlink(missing_ok=True)
provision=mounts/'system_ext/priv-app/Provision'
if (stage/'system_ext/priv-app/SetupWizard').exists() and provision.exists():shutil.rmtree(provision)
report=[]
for f in sorted(stage.rglob('*')):
 rel=f.relative_to(stage);parts=rel.parts
 if parts[0] in ('product','system_ext'):
  dest=mounts/parts[0]/Path(*parts[1:])
 else:dest=mounts/'system/system'/rel
 if f.is_dir():
  dest.mkdir(parents=True,exist_ok=True);mode=0o755
 else:
  dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest)
  mode=0o755 if f.suffix=='.sh' or not f.suffix else 0o644
 os.chown(dest,0,0);os.chmod(dest,mode)
 os.setxattr(dest,'security.selinux',b'u:object_r:system_file:s0\0')
 if f.is_file():report.append({'path':str(rel),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'mode':oct(mode),'selinux':os.getxattr(dest,'security.selinux').decode().rstrip('\0')})
(root/'integrated-files.json').write_text(json.dumps(report,indent=2)+'\n')
print('Integrated',len(report),'files; Android 17 GApps, Google-signed Gboard, official KSU manager')
