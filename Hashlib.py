import hashlib
import os
import json

# Hashing function
def compute_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

# Save hashes
def create_baseline(directory, output_file="hashes.json"):
    hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            hashes[path] = compute_hash(path)
    with open(output_file, "w") as f:
        json.dump(hashes, f, indent=2)
    print(f"Baseline saved to {output_file}")

# Check for changes
def verify_integrity(directory, baseline_file="hashes.json"):
    with open(baseline_file, "r") as f:
        baseline = json.load(f)
    modified = []
    missing = []
    new_files = []

    current_files = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            path = os.path.join(root, filename)
            current_files[path] = compute_hash(path)

    for path, old_hash in baseline.items():
        if path not in current_files:
            missing.append(path)
        elif old_hash != current_files[path]:
            modified.append(path)

    for path in current_files:
        if path not in baseline:
            new_files.append(path)

    print("Modified files:", modified)
    print("Missing files:", missing)
    print("New files:", new_files)

# Example usage:
# To create baseline:
# create_baseline("your_directory_path")

# To verify integrity:
# verify_integrity("your_directory_path")
