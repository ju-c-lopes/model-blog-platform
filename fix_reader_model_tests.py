import glob
import re

for filepath in glob.glob("website/tests/**/*.py", recursive=True):
    with open(filepath, "r") as f:
        content = f.read()

    modified = content
    # Remove reader_name="...", access_level=2
    modified = re.sub(r',\s*reader_name=[\'"].*?[\'"]', "", modified)
    modified = re.sub(r",\s*access_level=\d+", "", modified)

    if content != modified:
        with open(filepath, "w") as f:
            f.write(modified)
        print(f"Updated {filepath}")
