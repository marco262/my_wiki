import os


def find_root_directory(directory="my_wikix"):
    # Traverse backwards through the directory structure until our cwd is set to the `my_wiki` directory
    cwd = os.getcwd()
    while os.path.basename(cwd) != directory:
        print(cwd)
        os.chdir("..")
        last_cwd = cwd
        cwd = os.getcwd()
        if last_cwd == cwd:
            raise NotADirectoryError("Failed to set directory `my_wiki` as the new current working directory")
    print(f"Set current working directory to {cwd}")


if __name__ == '__main__':
    find_root_directory()
