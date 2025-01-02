import hashlib
import logging
from pathlib import Path
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_file_hash(file_path, algorithm='sha256'):
    """
    Calculate the hash of a file using the specified algorithm.
    """
    try:
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except PermissionError:
        logging.error(f"Permission denied for file: {file_path}")
        raise
    except Exception as e:
        logging.error(f"An error occurred while processing the file {file_path}: {e}")
        raise

def setup_argparse():
    """
    Setup command-line argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="Verify file integrity and detect modifications."
    )
    parser.add_argument(
        "file_path", type=str, help="Path to the file to verify."
    )
    parser.add_argument(
        "expected_hash", type=str, help="Expected hash value of the file."
    )
    parser.add_argument(
        "--algorithm", type=str, default="sha256", 
        help="Hashing algorithm to use (default: sha256)."
    )
    return parser

def main():
    """
    Main function to verify file integrity.
    """
    parser = setup_argparse()
    args = parser.parse_args()
    
    file_path = Path(args.file_path)
    expected_hash = args.expected_hash
    algorithm = args.algorithm

    if not file_path.is_file():
        logging.error(f"The specified path is not a file: {file_path}")
        return

    try:
        calculated_hash = calculate_file_hash(file_path, algorithm)
        if calculated_hash == expected_hash:
            logging.info("File integrity verified. The file has not been modified.")
        else:
            logging.warning("File integrity check failed. The file has been modified.")
            logging.warning(f"Expected: {expected_hash}")
            logging.warning(f"Calculated: {calculated_hash}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# Usage example:
# python main.py <file_path> <expected_hash> --algorithm sha256