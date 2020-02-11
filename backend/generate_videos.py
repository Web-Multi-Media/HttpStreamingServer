

import shutil


for season in range(1,5):
    for episode in range(1,20):
        shutil.copyfile("/usr/src/app/Videos/folder1/Matrix.mp4",
         "/usr/src/app/Videos/folder1/The.Big.Bang.Theory.S0{}E{:02d}.HDTV.x264-LOL.mp4".format(season, episode))

for season in range(1,5):
    for episode in range(1,8):
        shutil.copyfile("/usr/src/app/Videos/folder1/Matrix.mp4",
         "/usr/src/app/Videos/folder1/The Wire [{}x{:02d}].mp4".format(season, episode))

for season in range(1,6):
    for episode in range(1,8):
        shutil.copyfile("/usr/src/app/Videos/folder1/Matrix.mp4",
         "/usr/src/app/Videos/folder1/Malcolm in the Middle S0{}E{:02d}.mp4".format(season, episode))





