#!/usr/bin/env python3
"""
Test setup script for lerobotlab CLI testing.

Creates test directories and JSON files for testing download and conversion functionality.
Supports multiple test cases for different scenarios.
"""

import json
import os
from pathlib import Path


# Test selections
SINGLE_DATASET = {
    "metadata": {
        "saved_at": "2025-08-02T23:46:33.501Z",
        "total_datasets": 1,
        "total_episodes": 3,
        "total_frames": 1997
    },
    "datasets": [
        {
            "repo_id": "marioblz/eval_act_so101_test14",
            "selected_videos": [
                "observation.images.webcam1",
                "observation.images.webcam2"
            ]
        }
    ]
}

MULTI_DATASETS = {
    "metadata": {
        "saved_at": "2025-08-02T21:45:02.190Z",
        "total_datasets": 4,
        "total_episodes": 1387,
        "total_frames": 696391
    },
    "datasets": [
        {
            "repo_id": "1lyz123576/so101_test",
            "selected_videos": [
                "observation.images.phone"
            ]
        },
        {
            "repo_id": "smanni/train_so100_all",
            "selected_videos": [
                "observation.images.intel_realsense"
            ]
        },
        {
            "repo_id": "bjb7/so101_pen_touch_test_1",
            "selected_videos": [
                "observation.images.camera_4"
            ]
        },
        {
            "repo_id": "shreyasgite/so100_base_env",
            "selected_videos": [
                "observation.images.laptop"
            ]
        }
    ]
}

# Test cases: 2 selections × 3 commands = 6 test cases
TEST_CASES = [
    "download_single_dataset",
    "download_multi_datasets", 
    "convert_vjepa2ac_single_dataset",
    "convert_vjepa2ac_multi_datasets",
    "convert_droid_single_dataset",
    "convert_droid_multi_datasets"
]


def create_test_structure():
    """Create test folder structure and JSON files."""
    
    # Define test folder and subfolders
    test_folder = Path("test_env")
    download_folder = test_folder / "download"
    vjepa2_ac_folder = test_folder / "vjepa2_ac"
    droid_folder = test_folder / "droid"
    
    # Create directories
    print("Creating test directory structure...")
    test_folder.mkdir(exist_ok=True)
    download_folder.mkdir(exist_ok=True)
    vjepa2_ac_folder.mkdir(exist_ok=True)
    droid_folder.mkdir(exist_ok=True)
    
    print(f"✓ Created: {test_folder}")
    print(f"✓ Created: {download_folder}")
    print(f"✓ Created: {vjepa2_ac_folder}")
    print(f"✓ Created: {droid_folder}")
    
    # Create JSON files
    single_json = test_folder / "single_dataset.json"
    multi_json = test_folder / "multi_datasets.json"
    
    with open(single_json, 'w', encoding='utf-8') as f:
        json.dump(SINGLE_DATASET, f, indent=2)
    
    with open(multi_json, 'w', encoding='utf-8') as f:
        json.dump(MULTI_DATASETS, f, indent=2)
    
    print(f"✓ Created: {single_json}")
    print(f"✓ Created: {multi_json}")
    
    return test_folder, single_json, multi_json


def run_test_case(test_case, test_folder, single_json, multi_json):
    """Run a specific test case."""
    
    if test_case not in TEST_CASES:
        print(f"Error: Unknown test case '{test_case}'")
        print(f"Available test cases: {', '.join(TEST_CASES)}")
        return
    
    print(f"\n{'='*60}")
    print(f"RUNNING TEST CASE: {test_case.upper()}")
    print("="*60)
    
    # Determine which JSON file to use
    if "single_dataset" in test_case:
        json_file = single_json
        print("Using: single_dataset.json (1 dataset, 3 episodes)")
    else:
        json_file = multi_json  
        print("Using: multi_datasets.json (4 datasets, 1,387 episodes)")
    
    # Run the appropriate command
    if test_case.startswith("download_"):
        cmd = f"lerobotlab download {json_file} --download-path {test_folder}/download --verbose"
        print(f"\nCommand: {cmd}")
        
    elif test_case.startswith("convert_vjepa2ac_"):
        cmd = f"lerobotlab convert {json_file} --output-path {test_folder}/vjepa2_ac --format vjepa2-ac --verbose"
        print(f"\nCommand: {cmd}")
        
    elif test_case.startswith("convert_droid_"):
        cmd = f"lerobotlab convert {json_file} --output-path {test_folder}/droid --format droid --verbose"
        print(f"\nCommand: {cmd}")
    
    print("\nTo run this test case manually:")
    print(f"  {cmd}")
    print("="*60)


def list_test_cases():
    """List all available test cases."""
    print("Available test cases:")
    print("-" * 40)
    
    print("\nDownload tests:")
    print("  download_single_dataset    - Download 1 dataset")
    print("  download_multi_datasets    - Download 4 datasets")
    
    print("\nV-JEPA2-AC conversion tests:")
    print("  convert_vjepa2ac_single_dataset  - Convert 1 dataset to V-JEPA2-AC")  
    print("  convert_vjepa2ac_multi_datasets  - Convert 4 datasets to V-JEPA2-AC")
    
    print("\nDROID conversion tests:")
    print("  convert_droid_single_dataset     - Convert 1 dataset to DROID")
    print("  convert_droid_multi_datasets     - Convert 4 datasets to DROID")
    
    print(f"\nTotal: {len(TEST_CASES)} test cases")


def cleanup_test_env():
    """Clean up test environment."""
    import shutil
    test_folder = Path("test_env")
    if test_folder.exists():
        shutil.rmtree(test_folder)
        print(f"✓ Cleaned up: {test_folder}")


def main():
    """Main function - setup test environment."""
    print("Setting up test environment for lerobotlab CLI...")
    print("-" * 50)
    
    # Create test structure
    test_folder, single_json, multi_json = create_test_structure()
    
    print("\nTest environment ready! 🚀")
    print(f"Test folder: {test_folder.absolute()}")
    print(f"Single dataset JSON: {single_json.absolute()}")
    print(f"Multi datasets JSON: {multi_json.absolute()}")
    
    print(f"\nUse 'python test_setup.py list' to see all {len(TEST_CASES)} test cases")
    print("Use 'python test_setup.py <test_case>' to run a specific test")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        cleanup_test_env()
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        list_test_cases()
    elif len(sys.argv) > 1 and sys.argv[1] in TEST_CASES:
        # Setup environment first if needed
        test_folder = Path("test_env")
        if not test_folder.exists():
            test_folder, single_json, multi_json = create_test_structure()
        else:
            single_json = test_folder / "single_dataset.json"
            multi_json = test_folder / "multi_datasets.json"
        
        run_test_case(sys.argv[1], test_folder, single_json, multi_json)
    elif len(sys.argv) > 1:
        print(f"Error: Unknown test case '{sys.argv[1]}'")
        print("\nUsage:")
        print("  python test_setup.py [test_case]")
        print("  python test_setup.py list") 
        print("  python test_setup.py cleanup")
        print()
        list_test_cases()
    else:
        main() 