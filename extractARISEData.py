import hashlib
import re
import gzip
import shutil
import os


def md5(file_path):
    """Calculate MD5 checksum for a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def verify_checksum(md5_file, directory):
    """Verify each file's checksum against the md5 file."""
    with open(md5_file, "r") as f:
        mismatches = []
        for line in f:
            expected_md5, filename = line.strip().split("\t")
            file_path = f"{directory}/{filename.strip('.')}"

            try:
                calculated_md5 = md5(file_path)
                if calculated_md5 != expected_md5:
                    mismatches.append((filename, expected_md5, calculated_md5))
            except FileNotFoundError:
                print(f"File not found: {filename}")

    if mismatches:
        print("The following files do not match their checksums:")
        for filename, expected, calculated in mismatches:
            print(f"{filename}: Expected {expected}, but got {calculated}")
    else:
        print("All files match their checksums.")


def extract_and_organize(input_dir, output_dir, sample_list):
    pattern = re.compile(r"^(.*-\d+).*_(R[12])_.*\.fastq\.gz$")

    with open(sample_list, 'w') as sample_list:
        seen_samples = set()
        for filename in sorted(os.listdir(input_dir)):
            match = pattern.match(filename)
            if match:
                sample_name, orient = match.groups()

                sample_dir = os.path.join(output_dir, sample_name)
                os.makedirs(sample_dir, exist_ok=True)

                if sample_name not in seen_samples:
                    sample_list.write(f"{sample_name}\n")
                    seen_samples.add(sample_name)

                output_filename = f"{sample_name}_{'1' if orient == 'R1' else '2'}.fastq"
                output_path = os.path.join(sample_dir, output_filename)

                with gzip.open(os.path.join(input_dir, filename), 'rb') as f_in:
                    with open(output_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                print(f"Extracted {filename} to {output_path}")


def main():
    input_dir = "ARISE_data/raw_sequences"
    output_dir = "PROFUNGIS/samples"
    sample_list = "PROFUNGIS/sample_list.txt"

    print("Verifying checksums")
    verify_checksum("ARISE_data/md5sum.txt", "ARISE_data")

    extract_and_organize(input_dir, output_dir, sample_list)


if __name__ == "__main__":
    main()