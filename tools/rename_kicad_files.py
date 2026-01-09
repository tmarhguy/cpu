#!/usr/bin/env python3
"""
Refactor KiCad file names to match their directory names.
Ensures consistency and updates all references in .kicad_pro files.
"""

import os
import re
import json
import sys
from pathlib import Path

def get_directory_name(path):
    """Extract the directory name from a path."""
    return os.path.basename(os.path.normpath(path))

def find_kicad_files(directory):
    """Find all KiCad files in a directory."""
    kicad_extensions = ['.kicad_sch', '.kicad_pcb', '.kicad_pro', '.kicad_prl']
    files = {}
    for ext in kicad_extensions:
        pattern = f"*{ext}"
        matches = list(Path(directory).glob(pattern))
        if matches:
            # Take the first match (should only be one per type)
            files[ext] = matches[0]
    return files

def update_kicad_pro_references(file_path, old_name, new_name):
    """Update file references in a .kicad_pro file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # .kicad_pro files are JSON
        # Need to update references to schematic and PCB files
        data = json.loads(content)
        
        modified = False
        
        # Update board file reference (can be string or dict)
        if 'board' in data:
            if isinstance(data['board'], str) and old_name in data['board']:
                data['board'] = data['board'].replace(old_name, new_name)
                modified = True
            elif isinstance(data['board'], dict):
                # Recursively update dict values
                def update_dict(obj, old, new):
                    if isinstance(obj, dict):
                        return {k: update_dict(v, old, new) for k, v in obj.items()}
                    elif isinstance(obj, list):
                        return [update_dict(item, old, new) for item in obj]
                    elif isinstance(obj, str) and old in obj:
                        return obj.replace(old, new)
                    return obj
                old_board = str(data['board'])
                data['board'] = update_dict(data['board'], old_name, new_name)
                if str(data['board']) != old_board:
                    modified = True
        
        # Update schematic files list
        if 'schematic' in data:
            if isinstance(data['schematic'], list):
                for i, sch in enumerate(data['schematic']):
                    if isinstance(sch, str) and old_name in sch:
                        data['schematic'][i] = sch.replace(old_name, new_name)
                        modified = True
            elif isinstance(data['schematic'], str):
                if old_name in data['schematic']:
                    data['schematic'] = data['schematic'].replace(old_name, new_name)
                    modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        # Try simple string replacement as fallback
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            if old_name in content:
                content = content.replace(old_name, new_name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
        except Exception as e2:
            pass  # Silent fail for reference updates
    except Exception as e:
        pass  # Silent fail for reference updates
    return False

def update_sch_references(file_path, old_name, new_name):
    """Update file references in .kicad_sch files (s-expressions)."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update Sheetfile references
        pattern = rf'\(property "Sheetfile" ".*{re.escape(old_name)}[^"]*"'
        replacement = lambda m: m.group(0).replace(old_name, new_name)
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
    except Exception as e:
        print(f"  Warning: Could not update {file_path}: {e}")
    return False

def rename_kicad_files(directory):
    """Rename KiCad files in a directory to match the directory name."""
    dir_name = get_directory_name(directory)
    files = find_kicad_files(directory)
    
    if not files:
        return None
    
    # Determine the current base name from existing files
    current_name = None
    for ext, file_path in files.items():
        base = file_path.stem
        # Skip if already matches directory name
        if base == dir_name:
            continue
        if current_name is None:
            current_name = base
        elif current_name != base:
            print(f"  Warning: Multiple file base names found: {current_name}, {base}")
    
    if current_name is None or current_name == dir_name:
        return None
    
    # Rename files
    renames = []
    for ext, file_path in files.items():
        old_path = file_path
        new_path = file_path.parent / f"{dir_name}{ext}"
        
        if old_path != new_path:
            renames.append((old_path, new_path, current_name, dir_name))
    
    return renames if renames else None

def process_directory(root_dir):
    """Process all directories and rename files."""
    root_path = Path(root_dir)
    all_renames = []
    
    # Find all directories that might contain KiCad files
    for dir_path in root_path.rglob('*'):
        if not dir_path.is_dir():
            continue
        
        # Skip backup directories and hidden directories
        if 'backup' in dir_path.name.lower() or dir_path.name.startswith('.'):
            continue
        
        # Skip if directory is too shallow (root level modules only)
        if len(dir_path.relative_to(root_path).parts) < 2:
            continue
        
        renames = rename_kicad_files(str(dir_path))
        if renames:
            all_renames.extend(renames)
    
    # Sort by depth (deepest first) to avoid path issues
    all_renames.sort(key=lambda x: len(str(x[0].parent).split(os.sep)), reverse=True)
    
    return all_renames

def main():
    if len(sys.argv) > 1:
        root_dir = sys.argv[1]
    else:
        root_dir = '/Users/tmarhguy/Documents/cpu/kicad/modules'
    
    print(f"Scanning {root_dir} for KiCad files...")
    renames = process_directory(root_dir)
    
    if not renames:
        print("No files need renaming.")
        return
    
    print(f"\nFound {len(renames)} files to rename:\n")
    
    # Show what will be renamed
    for old_path, new_path, old_name, new_name in renames:
        print(f"  {old_path.name} -> {new_path.name}")
        print(f"    ({old_path.parent} -> {new_path.parent})")
    
    print(f"\nTotal: {len(renames)} files")
    
    # Auto-confirm if --yes flag is provided, otherwise ask
    auto_yes = '--yes' in sys.argv or '-y' in sys.argv
    if not auto_yes:
        try:
            confirm = input("\nProceed with renaming? (yes/no): ").strip().lower()
            if confirm not in ['yes', 'y']:
                print("Cancelled.")
                return
        except EOFError:
            print("\nNo input available. Use --yes flag to auto-confirm.")
            print("Dry-run mode: showing what would be renamed without actually renaming.")
            auto_yes = False
            # Don't proceed, just show
            return
    
    # Perform renames
    print("\nRenaming files...")
    for old_path, new_path, old_name, new_name in renames:
        try:
            # Rename the file
            old_path.rename(new_path)
            print(f"  ✓ Renamed: {old_path.name} -> {new_path.name}")
            
            # Update references in .kicad_pro files
            pro_files = list(new_path.parent.glob('*.kicad_pro'))
            for pro_file in pro_files:
                if update_kicad_pro_references(pro_file, old_name, new_name):
                    print(f"    Updated references in {pro_file.name}")
            
            # Update references in .kicad_sch files
            sch_files = list(new_path.parent.glob('*.kicad_sch'))
            for sch_file in sch_files:
                if update_sch_references(sch_file, old_name, new_name):
                    print(f"    Updated references in {sch_file.name}")
        
        except Exception as e:
            print(f"  ✗ Error renaming {old_path.name}: {e}")
    
    print("\nDone!")

if __name__ == '__main__':
    main()
