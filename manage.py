import os
import sys
import argparse


def manage(module_name: str, with_tests: bool = False):
    os.makedirs(module_name, exist_ok=True)
    module_path = os.path.join(os.getcwd(), module_name)

    files_content = {
        "__init__.py": "# __init__.py\n",
        "models.py": "# models.py\n",
        "schemas.py": "# schemas.py\n",
        "utils.py": "# utils.py\n",
        "views.py": "# views.py\n",
    }

    for filename, content in files_content.items():
        filepath = os.path.join(module_path, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    if with_tests:
        tests_dir = os.path.join(module_path, "tests")
        os.makedirs(tests_dir, exist_ok=True)

        test_files = {
            "__init__.py": "# tests/__init__.py\n",
            "conftest.py": "# conftest.py\n",
            "test_api.py": "# test_api.py\n",
        }

        for filename, content in test_files.items():
            filepath = os.path.join(tests_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)

        print(f"Test directory: {tests_dir}")

    print(f"Module '{module_name}' created: {module_path}")


def main():
    """
    python manage.py chat -t  -> Создать директирию с тестами.
    python manage.py chat  -> Создать директирию без тестов.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("module_name", help="Module name")
    parser.add_argument(
        "--with-tests", "-t", action="store_true", help="Add test folder"
    )

    args = parser.parse_args()

    if not args.module_name.isidentifier():
        print("Error")
        sys.exit(1)

    manage(args.module_name, with_tests=args.with_tests)


if __name__ == "__main__":
    main()