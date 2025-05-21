import os
import shutil
from PIL import Image
import zipfile
import tempfile
import traceback

base_dir = r"C:\Users\Ervyn\Downloads\Testing"

def convert_image_to_jpg(image_path):
    try:
        image = Image.open(image_path)
        rgb_image = image.convert('RGB')
        new_path = os.path.splitext(image_path)[0] + '.jpg'
        rgb_image.save(new_path, 'JPEG')
        os.remove(image_path)
        return new_path
    except Exception as e:
        print(f"Error converting {image_path}: {e}")
        return None

def process_chapter_folder(chapter_path, is_first_chapter=False):
    # Convert first image if this is the first chapter folder
    image_files = sorted([
        f for f in os.listdir(chapter_path)
        if os.path.isfile(os.path.join(chapter_path, f))
    ])

    if not image_files:
        return

    if is_first_chapter:
        first_image_path = os.path.join(chapter_path, image_files[0])
        ext = os.path.splitext(first_image_path)[1].lower()
        if ext not in ['.jpg', '.jpeg']:
            new_first = convert_image_to_jpg(first_image_path)
            if new_first:
                print(f"🖼️ Converted first image in first chapter folder: {chapter_path}")

    # Create CBZ archive
    cbz_name = os.path.basename(chapter_path) + '.cbz'
    cbz_path = os.path.join(os.path.dirname(chapter_path), cbz_name)
    shutil.make_archive(cbz_path.replace('.cbz', ''), 'zip', chapter_path)
    os.rename(cbz_path.replace('.cbz', '') + '.zip', cbz_path)

    # Remove original folder
    try:
        shutil.rmtree(chapter_path)
    except Exception as e:
        print(f"Error removing folder {chapter_path}: {e}")

def fix_first_image_in_zip(zip_path):
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(tmpdir)

            extracted_files = sorted([
                f for f in os.listdir(tmpdir)
                if os.path.isfile(os.path.join(tmpdir, f))
            ])

            if not extracted_files:
                return False

            first_image_path = os.path.join(tmpdir, extracted_files[0])
            ext = os.path.splitext(first_image_path)[1].lower()

            if ext not in ['.jpg', '.jpeg']:
                try:
                    image = Image.open(first_image_path)
                    image.load()

                    # Handle transparency
                    if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        background.paste(image, mask=image.split()[-1])
                        image = background
                    else:
                        image = image.convert('RGB')

                    new_image_path = os.path.splitext(first_image_path)[0] + '.jpg'
                    image.save(new_image_path, 'JPEG')
                    os.remove(first_image_path)
                except Exception as e:
                    print(f"❌ Error converting image in {zip_path}: {e}")
                    traceback.print_exc()
                    return False

                # Rezip files
                temp_zip_path = os.path.splitext(zip_path)[0] + '_fixed.zip'
                with zipfile.ZipFile(temp_zip_path, 'w') as zip_out:
                    for f in sorted(os.listdir(tmpdir)):
                        zip_out.write(os.path.join(tmpdir, f), arcname=f)

                os.remove(zip_path)
                os.rename(temp_zip_path, zip_path)
                return True

            return False
        except Exception as e:
            print(f"❌ Error processing {zip_path}: {e}")
            traceback.print_exc()
            return False

def rename_zip_to_cbz(zip_path):
    cbz_path = os.path.splitext(zip_path)[0] + '.cbz'
    try:
        os.rename(zip_path, cbz_path)
        print(f"✅ Renamed: {zip_path} -> {cbz_path}")
    except Exception as e:
        print(f"❌ Error renaming {zip_path}: {e}")

def main():
    for manga in os.listdir(base_dir):
        manga_path = os.path.join(base_dir, manga)
        if not os.path.isdir(manga_path):
            continue

        # Step 1: Process chapter folders (convert to CBZ, convert first image if first chapter folder)
        chapter_folders = sorted([
            d for d in os.listdir(manga_path)
            if os.path.isdir(os.path.join(manga_path, d))
        ])

        for idx, chapter in enumerate(chapter_folders):
            chapter_path = os.path.join(manga_path, chapter)
            is_first_chapter = (idx == 0)
            process_chapter_folder(chapter_path, is_first_chapter)

        # Step 2: After all chapter folders are processed to CBZ,
        # find all ZIP or CBZ files (some might still be ZIP)
        archive_files = []
        for root, dirs, files in os.walk(manga_path):
            for f in files:
                if f.lower().endswith(('.zip', '.cbz')):
                    archive_files.append(os.path.join(root, f))
        archive_files.sort()

        # Step 3: Fix first image inside the first archive (ZIP or CBZ)
        if archive_files:
            first_archive = archive_files[0]

            # If .cbz, treat as zip internally for processing
            temp_path = first_archive
            if first_archive.lower().endswith('.cbz'):
                # Temporarily rename to .zip to work with zipfile module
                temp_path = os.path.splitext(first_archive)[0] + '_temp.zip'
                os.rename(first_archive, temp_path)

            fixed = fix_first_image_in_zip(temp_path)

            # Rename back to .cbz if renamed before
            if first_archive.lower().endswith('.cbz'):
                os.rename(temp_path, first_archive)

        # Step 4: Rename all remaining .zip files to .cbz
        for archive in archive_files:
            if archive.lower().endswith('.zip'):
                rename_zip_to_cbz(archive)

if __name__ == '__main__':
    main()
