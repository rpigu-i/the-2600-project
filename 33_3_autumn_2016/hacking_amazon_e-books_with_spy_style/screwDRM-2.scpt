:set shellCommand to "screencapture -R 150,0,1300,850 -T1 -m /Users/Jerome/ebooks/" & i & ".png"
do shell script shellCommand
delay 1
set shellCommand to "/usr/local/bin/tesseract /Users/Jerome/ebooks/" & i & ".png /Users/Jerome/ebooks/" & i & " -l eng"
do shell script shellCommand
delay 1

