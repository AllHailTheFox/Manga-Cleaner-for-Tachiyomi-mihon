# Manga-Cleaner-for-Tachiyomi-mihon

A Python script that processes manga folders by converting chapter folders into `.cbz` comic book archives, ensuring compatibility with comic book reader applications. It also converts the first image in the first chapter to `.jpg` format if necessary and handles image transparency issues.

---

## 📁 Directory Structure (Expected Input)

Each manga folder should contain chapter subfolders, with images inside each chapter:

- `Folder/`
  - `Manga1/`
    - `Chapter 01/`
      - `page1.png`
      - `page2.png`
    - `Chapter 02/`
      - `page1.jpg`
      - `page2.jpg`
  - `Manga2/`
    - `Chapter 01/`
      - `page1.png`
      - `page2.png`
  - `Manga3.zip/`

---

## ✅ Features

- ✅ Converts the **first image in the first chapter** to `.jpg` if not already.
- ✅ Converts chapter folders into `.cbz` (ZIP archives with `.cbz` extension).
- ✅ Fixes transparency in images (e.g., `.png` with alpha channel).
- ✅ Deletes original chapter folders after conversion.
- ✅ Renames leftover `.zip` files to `.cbz`.

---


## 📦 Output Example
After running the script:
- `Folder/`
  - `Manga1/`
      - `Chapter 01.cbz`
      - `Chapter 02.cbz`
  - `Manga2/`
    - `Chapter 01/`
      - `Chapter 01.cbz`
      - `Chapter 02.cbz`
  - `Manga3/`
    - `Chapter 01.cbz`




## 🧰 Requirements

- Python 3.x
- [Pillow](https://pypi.org/project/Pillow/): install with  
  ```bash
  pip install Pillow
