#!/usr/bin/env python3
"""Restore the uploaded pre-repair source without touching user data/history."""
from __future__ import annotations
import argparse
from pathlib import Path
from zipfile import ZipFile

p=argparse.ArgumentParser()
p.add_argument('--project-root',default='.')
p.add_argument('--backup-zip',default='delivery_crcef_sv_20260627/ROLLBACK_ORIGINAL_FILES_20260627.zip')
p.add_argument('--new-files-list',default='delivery_crcef_sv_20260627/ROLLBACK_NEW_FILES_TO_REMOVE.txt')
a=p.parse_args()
root=Path(a.project_root).resolve()
backup=(root/a.backup_zip).resolve() if not Path(a.backup_zip).is_absolute() else Path(a.backup_zip)
remove=(root/a.new_files_list).resolve() if not Path(a.new_files_list).is_absolute() else Path(a.new_files_list)
if not backup.exists() or not remove.exists():
    raise SystemExit('Rollback evidence files are missing.')
for line in remove.read_text(encoding='utf-8').splitlines():
    rel=line.strip()
    if not rel: continue
    target=(root/rel).resolve()
    if root not in target.parents:
        raise SystemExit(f'Unsafe rollback path: {target}')
    if target.is_file() or target.is_symlink(): target.unlink()
with ZipFile(backup) as z:
    for member in z.infolist():
        target=(root/member.filename).resolve()
        if root not in target.parents:
            raise SystemExit(f'Unsafe archive member: {member.filename}')
    z.extractall(root)
print('Rollback complete. Original modified source restored; original data/history was never changed in the package.')
