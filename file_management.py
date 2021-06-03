import logging

def strip_extension(filename):
    if "." in filename:
        return ".".join(filename.split('.')[0:-1])
    else:
        return filename

def remove_leading_lines(filename, number):
    stripped = None
    with open(filename, "r") as f:
        stripped = f.read().split('\n')[number:]
    with open(filename, "w") as f:
        f.write("\n".join(stripped))

def remove_empty_lines(filename):
    stripped = []
    with open(filename, "r") as f:
        for line in f.read().split('\n'):
            if line != "": stripped.append(line)
    with open(filename, "w") as f:
        f.write("\n".join(stripped))
