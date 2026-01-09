#!/usr/bin/env python3
"""
Clean up non-essential files from KiCad directories.
Removes cache files, lock files, autosaves, and other temporary files.
"""

import os
import sys
from pathlib import Path

# File patterns to delete
PATTERNS_TO_DELETE = [
    # Lock files
    '*.lck',
    '*~*.lck',
    '*_autosave-*.lck',
    
    # Cache files
    '*cache*',
    'fp-info-cache',
    
    # Backup files (workbook backups)
    '*.wbk',
    
    # System files
    '.DS_Store',
    'Thumbs.db',
    'desktop.ini',
    
    # Temporary files
    '*.tmp',
    '*.temp',
    '*~',
    '*~*',
    
    # Autosave files
    '*autosave*',
    '*~_autosave*',
    
    # KiCad backup files
    '*.kicad_sch-bak',
    '*.kicad_pcb-bak',
    
    # Log files
    '*.log',
    'replicate_layout.log',
    
    # Other
    '*.orig',
    '*.swp',
]

# Directories to delete entirely (if empty after file cleanup)
DIRS_TO_REMOVE_IF_EMPTY = [
    'fp-info-cache',
    '*cache*',
]

# Directories to skip
SKIP_DIRS = {
    'backup',
    'backups',
    '.git',
}

def matches_pattern(filename, pattern):
    """Check if filename matches a pattern (simple wildcard matching)."""
    import fnmatch
    return fnmatch.fnmatch(filename, pattern)

def should_delete_file(filepath):
    """Determine if a file should be deleted."""
    filename = filepath.name
    
    # Check against deletion patterns
    for pattern in PATTERNS_TO_DELETE:
        if matches_pattern(filename, pattern):
            return True
    
    # Check if it's a lock file by extension
    if filename.endswith('.lck'):
        return True
    
    # Check if it's a cache file
    if 'cache' in filename.lower():
        return True
    
    return False

def should_skip_directory(dirpath):
    """Check if we should skip this directory."""
    dirname = dirpath.name.lower()
    for skip in SKIP_DIRS:
        if skip.lower() in dirname:
            return True
    return False

def cleanup_directory(root_dir):
    """Clean up non-essential files from a directory tree."""
    root_path = Path(root_dir)
    
    deleted_files = []
    deleted_dirs = []
    errors = []
    
    print(f"Scanning {root_dir} for non-essential files...\n")
    
    # Walk through directory tree
    for dirpath, dirnames, filenames in os.walk(root_path):
        dir_path = Path(dirpath)
        
        # Skip certain directories
        dirnames[:] = [d for d in dirnames if not should_skip_directory(dir_path / d)]
        
        # Check files in this directory
        for filename in filenames:
            filepath = dir_path / filename
            
            if should_delete_file(filepath):
                try:
                    filepath.unlink()
                    deleted_files.append(filepath)
                    print(f"  ✓ Deleted: {filepath.relative_to(root_path)}")
                except Exception as e:
                    errors.append((filepath, str(e)))
                    print(f"  ✗ Error deleting {filepath.relative_to(root_path)}: {e}")
    
    # Remove empty directories (cache directories, etc.)
    print("\nRemoving empty directories...")
    for dirpath, dirnames, filenames in os.walk(root_path, topdown=False):
        dir_path = Path(dirpath)
        
        # Skip root and backup directories
        if dir_path == root_path or should_skip_directory(dir_path):
            continue
        
        # Check if directory name matches removal patterns
        dirname = dir_path.name.lower()
        should_remove = False
        for pattern in DIRS_TO_REMOVE_IF_EMPTY:
            if matches_pattern(dirname, pattern):
                should_remove = True
                break
        
        # Remove if empty and matches pattern
        if should_remove:
            try:
                if dir_path.exists() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    deleted_dirs.append(dir_path)
                    print(f"  ✓ Removed empty directory: {dir_path.relative_to(root_path)}")
            except Exception as e:
                errors.append((dir_path, str(e)))
                print(f"  ✗ Error removing {dir_path.relative_to(root_path)}: {e}")
    
    return deleted_files, deleted_dirs, errors

def main():
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = '/Users/tmarhguy/Documents/cpu/kicad'
    
    print("=" * 80)
    print("KiCad Directory Cleanup")
    print("=" * 80)
    print()
    
    deleted_files, deleted_dirs, errors = cleanup_directory(root_dir)
    
    print()
    print("=" * 80)
    print("Summary")
    print("=" * 80)
    print(f"Files deleted: {len(deleted_files)}")
    print(f"Directories removed: {len(deleted_dirs)}")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\nErrors encountered:")
        for item, error in errors:
            print(f"  {item}: {error}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
