import os
import shutil

# Directory to be scanned
path = '/var/lib/docker/volumes/jenkins_home/_data/jobs'
threshold = 0
# Scan the directiory and get
# an iterator of os.DirEntry objets
# corresponding to entries in it
# using os.scandir() method
obj = os.scandir(path)

# List all files and diretories
# in the specified path
print("Files and Directories in '% s':" % path)
try:
   for entry in obj :
     if entry.is_dir(follow_symlinks=False):
       if os.path.exists(entry.path + '/jobs/main/branches'):
         for xxx in os.scandir(entry.path + '/jobs/main/branches') :
           if xxx.is_dir(follow_symlinks=False) and xxx.name != 'master':
             shutil.rmtree(xxx.path)
             #print(xxx.path)
             #print("ende1")
       if os.path.exists(entry.path + '/jobs/main/branches/master/builds'):
         #print("pfad da")
         with open(entry.path + '/jobs/main/branches/master/nextBuildNumber') as f:
           threshold = int(f.read())-5
           #print(threshold)
         for xxx in os.scandir(entry.path + '/jobs/main/branches/master/builds') :
           #print(xxx.name)
           if xxx.is_dir(follow_symlinks=False) and xxx.name.isnumeric():
             if int(xxx.name) < threshold:
               shutil.rmtree(xxx.path)
               #print(xxx.path)

finally:
  obj.close()