import hashlib
import logging
from pathlib import Path
import argparse
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_file_hash(file_path, algorithm='sha256'):
    """
    Calculate the hash of a file using the specified algorithm.
    """
    try:
        # The algorithm name goes to hashlib unchecked. An unknown name raises
        # here and a weak one, md5 or sha1, is accepted without a word: the
        # caller picks the algorithm, and this tool's job is the comparison,
        # not judging what the caller compares with.
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as file:
            # The file is hashed in 4096 byte chunks through the iter sentinel
            # idiom, so the size of the file does not decide the memory used. The
            # chunk size changes nothing about the digest, only about how many
            # update calls stand behind it.
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
    Returns 0 when the calculated hash matches the expected hash, and 1
    when it does not match, the path is not a file, or hashing fails.
    The expected hash comparison is case-insensitive, because hex digests
    are commonly copied in either upper or lower case.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    file_path = Path(args.file_path)
    # The expected value is stripped as well as lowered. Hashes get copied
    # out of terminals and documents with stray spaces attached, and a
    # mismatch caused by paste formatting would read as a modified file.
    expected_hash = args.expected_hash.strip().lower()
    algorithm = args.algorithm

    # is_file is checked before any hashing, so a directory or a missing
    # path returns the same exit 1 as a genuine mismatch. Scripts see one
    # failure code for every way this check can fail; the log line is what
    # separates them.
    if not file_path.is_file():
        logging.error(f"The specified path is not a file: {file_path}")
        return 1

    try:
        calculated_hash = calculate_file_hash(file_path, algorithm)
        if calculated_hash.lower() == expected_hash:
            logging.info("File integrity verified. The file has not been modified.")
            return 0
        else:
            logging.warning("File integrity check failed. The file has been modified.")
            logging.warning(f"Expected: {expected_hash}")
            logging.warning(f"Calculated: {calculated_hash}")
            return 1
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

# Usage example:
# python main.py <file_path> <expected_hash> --algorithm sha256