import glob

replacements = {
    "from website.models.AuthorModel import": "from website.models.author.AuthorModel import",
    "from website.models.AuthorSocialMediaModel import": "from website.models.author.AuthorSocialMediaModel import",
    "from website.models.PostModel import": "from website.models.post.PostModel import",
    "from website.models.ReaderModel import": "from website.models.user.ReaderModel import",
    "from website.models.GraduationsModel import": "from website.models.author.GraduationsModel import",
    "from website.models.JobsModel import": "from website.models.author.JobsModel import",
    "from website.models.UserModel import": "from website.models.user.UserModel import",
    "from website.views.AuthorEditView import": "from website.views.author.AuthorEditView import",
}

for filepath in glob.glob("website/tests/**/*.py", recursive=True):
    with open(filepath, "r") as f:
        content = f.read()

    modified = content
    for old, new in replacements.items():
        modified = modified.replace(old, new)

    if content != modified:
        with open(filepath, "w") as f:
            f.write(modified)
        print(f"Updated {filepath}")
