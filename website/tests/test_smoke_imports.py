import importlib
import os


def test_import_website_modules():
    root = os.path.dirname(os.path.dirname(__file__))
    imported = 0
    errors = {}
    for dirpath, dirnames, filenames in os.walk(root):
        # skip tests and migrations folders
        if "tests" in dirpath.split(os.sep) or "migrations" in dirpath.split(os.sep):
            continue
        for fn in filenames:
            if not fn.endswith(".py"):
                continue
            if fn == "__init__.py":
                # import package
                mod_path = os.path.relpath(dirpath, root).replace(os.sep, ".")
                if mod_path == ".":
                    module_name = "website"
                else:
                    module_name = f"website.{mod_path}"
            else:
                mod_rel = os.path.relpath(os.path.join(dirpath, fn), root)[:-3]
                module_name = "website." + mod_rel.replace(os.sep, ".")

            # skip obvious heavy or test-only files
            if any(
                x in module_name for x in (".tests", ".migrations", "tests.", "test_")
            ):
                continue

            try:
                importlib.import_module(module_name)
                imported += 1
            except Exception as e:
                errors[module_name] = str(e)

    # sanity check: we should have imported at least some modules
    assert (
        imported > 10
    ), f"Imported too few modules: {imported}; errors: {list(errors.keys())[:5]}"
