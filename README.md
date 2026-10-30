## File Integrity Tool

### Project Description

This tool verifies the integrity of a single file by computing its hash and comparing it with an expected hash value you supply. If the hashes match, the file is reported as unmodified. If they differ, the tool reports that the file has been modified and prints both hashes. It checks one file per run; it does not monitor directories, watch for changes, or analyze file operations.

### Requirements and Installation

1. Ensure you have Python 3.8 or later installed.
2. Clone the repository: `git clone https://github.com/ShadowGuardAI/file-integrity.git`
3. No third party dependencies are needed. The tool uses only the Python standard library, and this repository has no `requirements.txt`.

### Usage

```
python3 main.py <file_path> <expected_hash> [--algorithm ALGORITHM]
```

Both arguments are positional; there is no `--file-path` option.

- `file_path`: Path to the file to verify (relative or absolute).
- `expected_hash`: The expected hex digest of the file. The comparison is case-insensitive.
- `--algorithm`: Any hashing algorithm name accepted by Python `hashlib` (default: `sha256`). Examples: `md5`, `sha1`, `sha512`.

The file is read in 4096 byte chunks, so large files do not need to fit in memory.

Exit codes, so the tool can be used in scripts:

- `0`: The calculated hash matches the expected hash.
- `1`: The hash does not match, the path is not a file, or hashing failed (for example an unknown `--algorithm` value).
- `2`: Command line usage error, reported by argparse (for example a missing argument).

### Examples

Get a file's expected SHA-256 hash, then verify it:

```
sha256sum report.pdf
python3 main.py report.pdf c2bdffafce05ba3a71c0957039c6dba3427f649428dfe38f7cb7215ff7fd68fe
```

Verified output for a matching file:

```
INFO - File integrity verified. The file has not been modified.
```

Verified output for a file whose contents changed after the expected hash was taken:

```
WARNING - File integrity check failed. The file has been modified.
WARNING - Expected: c2bdffafce05ba3a71c0957039c6dba3427f649428dfe38f7cb7215ff7fd68fe
WARNING - Calculated: b102047f2d7beaabec4b287691c5b42461db3de847b81443163987503d228e6a
```

Verify with a different algorithm:

```
python3 main.py report.pdf <expected_md5_hex> --algorithm md5
```

### Security Warnings

This tool is designed to assist in maintaining the integrity of your files. However, it is important to note that no security measure is foolproof: a hash comparison only proves a file matches the expected digest you supply, so the expected digest itself must come from a trusted source. It is recommended to use this tool in conjunction with other security best practices, such as encryption and regular backups.

### License

This tool is licensed under the GNU General Public License v3.0; see the `LICENSE` file in this repository. The software is provided "as is" without warranty of any kind.
