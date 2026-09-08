import os
import re
from datetime import datetime

# Set this to the path where your PDFs are stored
folder_path = "/path/to/your/pdf/folder"  # CHANGE THIS

def extract_date_from_filename(filename):
    """Extract date from filename like '...DATED 15.04.2024.pdf'"""
    # Look for pattern: DATED DD.MM.YYYY or DATED DD-MM-YYYY
    pattern = r'DATED\s+(\d{2})[\.\-](\d{2})[\.\-](\d{4})'
    match = re.search(pattern, filename)
    
    if match:
        day, month, year = match.groups()
        # Convert to datetime object for validation and formatting
        date_obj = datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")
        return date_obj.strftime("%Y-%m-%d")  # YYYY-MM-DD format
    return None

def rename_files(folder_path):
    """Rename all PDF files to YYYY-MM-DD_91-182-364.pdf"""
    
    # Get all PDF files
    files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    
    renamed_count = 0
    skipped_count = 0
    
    for filename in files:
        date_str = extract_date_from_filename(filename)
        
        if date_str:
            # New filename format
            new_name = f"{date_str}_91-182-364.pdf"
            
            # Full paths
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            
            # Check if file already exists (handle duplicates safely)
            if os.path.exists(new_path):
                print(f"⚠️  File already exists: {new_name} (skipping {filename})")
                skipped_count += 1
                continue
            
            # Rename the file
            os.rename(old_path, new_path)
            print(f"✅ Renamed: {filename} → {new_name}")
            renamed_count += 1
        else:
            print(f"❌ Could not extract date from: {filename}")
            skipped_count += 1
    
    print(f"\n📊 Summary:")
    print(f"   Renamed: {renamed_count} files")
    print(f"   Skipped: {skipped_count} files")

if __name__ == "__main__":
    # Replace with your actual folder path
    folder_path = "./"  # CHANGE THIS!
    rename_files(folder_path)
