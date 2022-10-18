from genericpath import isdir
import os

def directory_check(title):
    if os.path.isdir(title):
        return True
    else:
        return False

def directory_gen(title):
    if os.path.exists(title):
        return False
    else:
        os.makedirs(title)
        return True

def file_gen(title,filename,contents):
    if os.path.isdir(title):
        filepath = os.path.join(title,filename)
        if not os.path.exists(filepath):
            fileout = open(filepath, "w")
            fileout.write(str(contents)+"\n")
            fileout.close()
            return True
        else:
            return False
    else:
        return False

def file_delete(title,filename):
    if os.path.isdir(title):
        filepath = os.path.join(title,filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
            return True
        else:
            return False
    else:
        return False

def directory_delete(title):
    if os.path.isdir(title):
        files = os.listdir(title)
        for i in files:
            os.remove(os.path.join(title,i))
        os.rmdir(title)
        return True
    else:
        return False