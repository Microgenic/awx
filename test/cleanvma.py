import os
import shutil
# This file must be copied into docker container where ansible is running path is /home
# sudo docker cp cleanvma.py 4ce51e72ed76:/home/cleanvma.py

#NGINX path
nginxpath = '/home/chexci/services/nginx/storage/__cache__'

if os.path.exists(nginxpath):
  print("Delete folder '% s':" % nginxpath)
  shutil.rmtree(nginxpath)

# Directory to be scanned
path = '/var/lib/docker/volumes/jenkins/_data/jobs'
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
         for fold1 in os.scandir(entry.path + '/jobs/main/branches') :
           if fold1.is_dir(follow_symlinks=False) and fold1.name != 'master' and os.path.exists(fold1.path + '/nextBuildNumber'):
             with open(fold1.path + '/nextBuildNumber') as f:
               threshold = int(f.read())-2
               print(fold1.path)
               print(threshold)
             for fold2 in os.scandir(fold1.path + '/builds') :
               if fold2.is_dir(follow_symlinks=False) and fold2.name.isnumeric():
                 if int(fold2.name) < threshold:
                   #shutil.rmtree(fold2.path)
                   print(fold2.path)
       if os.path.exists(entry.path + '/jobs/main/branches/master/builds'):
         #print("pfad da")
         with open(entry.path + '/jobs/main/branches/master/nextBuildNumber') as f:
           threshold = int(f.read())-5
           #print(threshold)
         for fold1 in os.scandir(entry.path + '/jobs/main/branches/master/builds') :
           #print(fold1.name)
           if fold1.is_dir(follow_symlinks=False) and fold1.name.isnumeric():
             if int(fold1.name) < threshold:
               #shutil.rmtree(fold1.path)
               print(fold1.path)

finally:
  obj.close()
