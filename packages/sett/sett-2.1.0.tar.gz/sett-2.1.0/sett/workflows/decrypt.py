import os
import json

from typing import List, Optional

from . import workflow
from ..core.error import UserError
from ..core.archive import check_tar, unpack, extract, \
    METADATA_FILE, DATA_ARCHIVE, DATA_FILE_ENCRYPTED, \
    CHECKSUM_FILE
from ..core.crypt import decrypt as core_decrypt, extract_pub_key_ids, \
    validated_keys_by_ids, fingerprint2keyid, verify_metadata_signature
from ..core.filesystem import delete_files
from ..core.checksum import verify_checksums, compute_checksum_sha256, read_checksum_file
from ..core.metadata import MetaData
from ..utils.log import create_logger
from ..utils.progress import ProgressInterface, with_progress, progress_file_iter
from ..utils.config import Config


logger = create_logger(__name__)


@workflow(logger, (UserError, FileNotFoundError))
def decrypt(files: List[str],
            *,
            passphrase: Optional[str] = None,
            output_dir: str,
            config: Config,
            decrypt_only: bool = False,
            dry_run: bool = False,
            progress: ProgressInterface = None):
    """ Decrypt and decompress an input .tar file."""

    logger.info("""Input summary:
    file(s) to decrypt: %s
    output_dir: %s
    dry_run: %s
""", "\n\t".join(files), output_dir, dry_run)

    with logger.log_task("Input data check"):
        for tar_name in files:
            check_tar(tar_name)

    if dry_run:
        logger.info("Dry run completed successfully")
        return

    for tar_file in files:
        verify_metadata_signature(
            tar_file, config.gpg_store,
            config.key_validation_authority_keyid,
            config.keyserver_url)

    decrypted_tars = []
    for tar in progress_file_iter(files, progress=progress, mode='rb'):
        logger.info("Untar file %s", tar.name)

        # To avoid overwriting files, each tarball is untarred in a directory
        # that has the same name as the tar file minus the .tar extension.
        out_dir = os.path.splitext(os.path.join(
            output_dir, os.path.basename(tar.name)))[0]
        decrypted_file = os.path.join(out_dir, DATA_ARCHIVE)
        with extract(tar, METADATA_FILE, DATA_FILE_ENCRYPTED) as (f_metadata, f_data):
            metadata = MetaData.from_dict(json.load(f_metadata))
            keys = validated_keys_by_ids(extract_pub_key_ids(f_data),
                                         config.gpg_store,
                                         config.key_validation_authority_keyid,
                                         config.keyserver_url)
            logger.info("Data encrypted for:\n%s",
                        "\n".join(f"User ID    : {key.uids[0]}\n"
                                  f"Fingerprint: {key.fingerprint}"
                                  for key in keys))
            with logger.log_task("Verifying checksums..."):
                if metadata.checksum.lower() != compute_checksum_sha256(f_data):
                    raise UserError(f"Checksum mismatch for {f_data.name}")
            with logger.log_task("Decrypting data..."):
                os.makedirs(out_dir, exist_ok=True)
                sender_fprs = core_decrypt(f_data, decrypted_file,
                                           gpg_store=config.gpg_store,
                                           passphrase=passphrase)
                decrypted_tars.append(decrypted_file)
            sender_sig_keys = validated_keys_by_ids(
                map(fingerprint2keyid, sender_fprs),
                config.gpg_store,
                config.key_validation_authority_keyid,
                config.keyserver_url)
            logger.info("Data signed by:\n%s",
                        "\n".join(f"User ID    : {key.uids[0]}\n"
                                  f"Fingerprint: {key.fingerprint}"
                                  for key in sender_sig_keys))

    if decrypt_only:
        logger.info("Data decryption completed successfully")
        return

    for tar_name in decrypted_tars:
        with logger.log_task(f"Untar file '{tar_name}'"):
            with extract(open(tar_name, 'rb'), CHECKSUM_FILE) as f_checksum:
                sha_checks = list(read_checksum_file(f_checksum))
            output_dir = os.path.dirname(tar_name)
            unpacked = unpack(
                with_progress(open(tar_name, 'rb'), progress), output_dir)
            log_files(unpacked)

        with logger.log_task("Checksum verification of uncompressed data..."):
            verify_checksums(sha_checks, output_dir)

        delete_files(tar_name)

    logger.info("Data decryption completed successfully.")


def log_files(files: List[str]):
    max_files_to_list = 50
    d_n = len(files) - max_files_to_list
    logger.info("List of extracted files: \n\t%s%s",
                "\n\t".join(files[:max_files_to_list]),
                ((f"\n\t and {d_n} more files "
                  "- not listing them all.") if d_n > 0 else ""))
