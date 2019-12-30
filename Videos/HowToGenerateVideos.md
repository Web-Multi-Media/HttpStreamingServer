youtube-dl -o test.mp4 -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4' https://www.youtube.com/watch\?v\=rBM7z2y15uc

ffmpeg -i test.mp4 -f segment -segment_time 10 output_%03d.mp4