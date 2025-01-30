import os
import shutil

from copystatic import copy_files


path_static = "./static"
path_public = "./public"

def main():
    print("Copying static files to public directory...")
    copy_files(path_static, path_public)





if __name__ == "__main__":
    main()
