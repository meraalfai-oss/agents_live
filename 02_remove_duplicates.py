#!/usr/bin/env python3
"""
Phase 2: Remove Duplicate Files
Safely removes identified duplicate files after verification
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import json

class DuplicateRemover:
    def __init__(
        self,
        root_path: Path,
        dry_run: bool = True,
        backup_dir: Path = None
    ):
        """
        Args:
            root_path (Path): The root directory to operate on.
            dry_run (bool): If True, no files will be deleted.
            backup_dir (Path, optional): Directory to store backups. Defaults to 'cleanup/backups/<timestamp>' under root_path.
        """
        self.root = root_path
        self.dry_run = dry_run
        if backup_dir is None:
            backup_dir = root_path / 'cleanup' / 'backups' / datetime.now().strftime('%Y%m%d_%H%M%S')
        self.backup_dir = backup_dir
        self.removed_files = []
        
    def remove_duplicates(self):
        """Remove all identified duplicate files."""
        print("=" * 80)
        print("YMERA PHASE 2: REMOVE DUPLICATES")
        print("=" * 80)
        print(f"\nMode: {'DRY RUN (no files will be deleted)' if self.dry_run else 'LIVE (files will be deleted)'}")
        print()
        
        # Define duplicates to remove (keep the first one in each pair)
        duplicates_to_remove = [
            {
                'file': 'api_extensions.py',
                'reason': 'Exact duplicate of extensions.py',
                'keep': 'extensions.py'
            },
            {
                'file': 'api.gateway.py',
                'reason': 'Exact duplicate of gateway.py',
                'keep': 'gateway.py'
            },
            {
                'file': 'deployment_package/migrations/versions/001_add_indexes.py',
                'reason': 'Exact duplicate of migrations/versions/001_add_indexes.py',
                'keep': 'migrations/versions/001_add_indexes.py'
            },
            {
                'file': 'shared/utils/helpers.py',
                'reason': 'Empty file, no functionality',
                'keep': None
            },
        ]
        
        # Process each duplicate
        for dup in duplicates_to_remove:
            self._remove_file(dup)
        
        # Summary
        print("\n" + "=" * 80)
        print(f"✅ Phase 2 {'Simulation' if self.dry_run else 'Execution'} Complete!")
        print("=" * 80)
        print(f"\nFiles {'would be' if self.dry_run else ''} removed: {len(self.removed_files)}")
        
        if self.removed_files:
            print("\nRemoved files:")
            for f in self.removed_files:
                print(f"  - {f}")
        
        if not self.dry_run and self.removed_files:
            print(f"\nBackups saved to: {self.backup_dir}")
            self._save_manifest()
        
        if self.dry_run:
            print("\n⚠️  This was a DRY RUN. No files were actually deleted.")
            print("To execute for real, run: python3 cleanup/02_remove_duplicates.py --execute")
    
    def _remove_file(self, duplicate_info: dict):
        """Remove a single duplicate file."""
        file_path = self.root / duplicate_info['file']
        
        print(f"\n{'[DRY RUN] ' if self.dry_run else ''}Processing: {duplicate_info['file']}")
        print(f"  Reason: {duplicate_info['reason']}")
        if duplicate_info['keep']:
            print(f"  Keeping: {duplicate_info['keep']}")
        
        # Check if file exists
        if not file_path.exists():
            print(f"  ⚠️  File not found, skipping")
            return
        
        # Verify it's a file (not directory)
        if not file_path.is_file():
            print(f"  ⚠️  Not a file, skipping")
            return
        
        # Get file size for reporting
        size = file_path.stat().st_size
        print(f"  Size: {size} bytes")
        
        if self.dry_run:
            print(f"  ✅ Would remove this file")
            self.removed_files.append(duplicate_info['file'])
        else:
            # Create backup
            self._backup_file(file_path, duplicate_info['file'])
            
            # Remove the file
            try:
                file_path.unlink()
                print(f"  ✅ Removed successfully")
                self.removed_files.append(duplicate_info['file'])
            except Exception as e:
                print(f"  ❌ Error removing file: {e}")
    
    def _backup_file(self, file_path: Path, relative_path: str):
        """Backup a file before deletion."""
        backup_path = self.backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(file_path, backup_path)
            print(f"  💾 Backed up to: cleanup/backups/...")
        except Exception as e:
            print(f"  ⚠️  Backup failed: {e}")
    
    def _save_manifest(self):
        """Save a manifest of removed files."""
        manifest = {
            'timestamp': datetime.now().isoformat(),
            'removed_files': self.removed_files,
            'backup_location': str(self.backup_dir)
        }
        
        manifest_path = self.backup_dir / 'manifest.json'
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\nManifest saved: {manifest_path}")


def main():
    import sys
    
    # Check for --execute flag
    execute = '--execute' in sys.argv or '-e' in sys.argv
    dry_run = not execute
    
    if dry_run:
        print("\n⚠️  Running in DRY RUN mode (simulation only)")
        print("To execute for real, add --execute flag\n")
    else:
        print("\n⚠️  Running in EXECUTE mode (files will be deleted)")
        response = input("Are you sure you want to delete duplicate files? (yes/no): ")
        if response.lower() != 'yes':
            print("Cancelled.")
            return
        print()
    
    remover = DuplicateRemover(Path.cwd(), dry_run=dry_run)
    remover.remove_duplicates()
    
    if dry_run:
        print("\n📝 Next steps:")
        print("1. Review the files that would be removed above")
        print("2. Run with --execute flag to actually remove them")
        print("3. Run tests: pytest")
        print("4. Commit changes: git add -u && git commit -m 'Remove duplicate files'")
    else:
        print("\n📝 Next steps:")
        print("1. Run tests: pytest")
        print("2. Verify nothing broke")
        print("3. Commit changes: git add -u && git commit -m 'Remove duplicate files'")


if __name__ == "__main__":
    main()
