# Description: This script backs up files from a source directory to a destination directory, logging the process.
# Tags: Lab, Python, File Backup, Logging

import os
import shutil
import argparse
import logging
from datetime import datetime

log_filename = f"backup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def backup_files(src_dir, dest_dir, file_types):
    if not os.path.exists(src_dir):
        logging.error(f"Source directory does not exist: {src_dir}")
        return

    if not os.path.exists(dest_dir):
        try:
            os.makedirs(dest_dir)
            logging.info(f"Created destination directory: {dest_dir}")
        except Exception as e:
            logging.error(
                f"Failed to create destination directory: {dest_dir} - {e}")
            return

    for root, _, files in os.walk(src_dir):
        for file in files:
            if any(file.endswith(ext) for ext in file_types):
                src_file = os.path.join(root, file)
                dest_file = os.path.join(
                    dest_dir, os.path.relpath(src_file, src_dir))
                dest_file_dir = os.path.dirname(dest_file)

                if not os.path.exists(dest_file_dir):
                    try:
                        os.makedirs(dest_file_dir)
                        logging.info(f"Created directory: {dest_file_dir}")
                    except Exception as e:
                        logging.error(
                            f"Failed to create directory: {dest_file_dir} - {e}")
                        continue

                try:
                    shutil.copy2(src_file, dest_file)
                    logging.info(f"Copied: {src_file} to {dest_file}")
                except Exception as e:
                    logging.error(
                        f"Failed to copy: {src_file} to {dest_file} - {e}")


def main():
    parser = argparse.ArgumentParser(
        description="File Backup System for MacOS")
    parser.add_argument("src_dir", help="Source directory to backup")
    parser.add_argument("dest_dir", help="Destination directory for backup")
    parser.add_argument("file_types", nargs='+',
                        help="File types to backup (e.g., .txt .jpg)")

    args = parser.parse_args()

    backup_files(args.src_dir, args.dest_dir, args.file_types)


if __name__ == "__main__":
    main()
