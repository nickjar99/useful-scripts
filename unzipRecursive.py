from subprocess import Popen, PIPE
import os, sys, time
import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", type=str)
parser.add_argument("--here", action="store_true")
args = parser.parse_args()

pathsToSearch = [args.input]

def unzip(filename):
    print("Unzipping %s" % filename)

    newFolderName = '.'.join(filename.split('.')[:-1])
    outputDir = os.path.join(os.path.dirname(filename), newFolderName)
    
    ext = filename.split('.')[-1]
    if ext == 'rar':
        command = ['unrar', 'x', "\'%s\'" % filename, "\'%s\'" % outputDir]
    else:
        command = ['unzip', '-o', "\'%s\'" % filename, '-d', "\'%s\'/" % outputDir]

    print(' '.join(command))
    process = Popen(' '.join(command), stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = process.communicate()
    print(stdout.decode())
    print(stderr.decode())
    return outputDir

def getArchivesAtPath(path):
    result = []
    if os.path.isdir(path):
        for root, subdirs, files in os.walk(path):
            # print(root, subdirs, files)
            for file in files:
                fullPath = os.path.join(root, file)
                ext = fullPath.split('.')[-1]

                if (ext in ['rar', 'zip']):
                    result.append(fullPath)
    else:
        result = [path]
    return result


while True:
    archives = []
    for path in pathsToSearch:
        archives.extend(getArchivesAtPath(path))
    pathsToSearch = []
    for filename in archives:
        time.sleep(1)
        outputDir = unzip(filename)
        pathsToSearch.append(outputDir)
        # Deleting all sub archives but not the original one
        # if filename != args.input:
        #     os.remove(filename)
    if pathsToSearch == []:
        break

print('Done!')