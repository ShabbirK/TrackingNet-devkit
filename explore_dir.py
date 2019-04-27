import os
import pprint

def explore_dir(dir):

    files = []
    dirs = []
    file_counts = {}

    for (dirpath, dirnames, filenames) in os.walk(dir):
        files.extend([(dirpath + '/' + fname).replace('//', '/').replace('\\', '/') for fname in filenames])
        dirs.extend([(dirpath + '/' + dname).replace('//', '/').replace('\\', '/') for dname in dirnames])
        file_counts[dirpath + '/'] = len(filenames)    

    return files, dirs, file_counts

if __name__ == '__main__':

    main_dir = 'image_data/org-resized-85/'
    files, dirs, file_counts = explore_dir(main_dir)
    pprint.pprint(files)
    pprint.pprint(dirs)
    pprint.pprint(file_counts)