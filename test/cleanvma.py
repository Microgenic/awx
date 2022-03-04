import os
import shutil

# Delete all files in /home/chexci/services/nginx/http-storage/__cache__ once
print("Files and Directories in /home/chexci/services/nginx/http-storage/__cache__")
#shell: rm -rf /home/chexci/services/nginx/http-storage/__cache__/*

# Start directory to be scanned
#path = '/var/lib/docker/volumes/jenkins_home/_data/jobs'
path = '/var/lib/docker/volumes/jenkins/_data/jobs'
combinepath = ''
threshold = 0

# List all files and diretories
# in the specified path
print("Files and Directories in '% s':" % path)
try:
  with os.scandir(path) as dirs1:
    for dir1 in dirs1 :
      if dir1.is_dir(follow_symlinks=False):
        combinepath = dir1.path + '/jobs/main/branches'
        if os.path.exists(combinepath):
          with os.scandir(combinepath) as dirs2:
            for dir2 in dirs2:
              if dir2.is_dir(follow_symlinks=False) and dir2.name != 'master':
                shutil.rmtree(dir2.path)
                #print(dir2.path)
                #print("ende1")
        combinepath = dir1.path + '/jobs/main/branches/master/builds'
        if os.path.exists(combinepath):
          #print("pfad da")
          with open(dir1.path + '/jobs/main/branches/master/nextBuildNumber') as f:
            threshold = int(f.read())-5
            #print(threshold)
          with os.scandir(combinepath) as dirs3:
            for dir3 in os.scandir(combinepath):
              #print(dir3.name)
              if dir3.is_dir(follow_symlinks=False) and dir3.name.isnumeric():
                if int(dir3.name) < threshold:
                  shutil.rmtree(dir3.path)
                  #print(dir3.path)
except:
  print("Something went wrong")
