:tell application "Kindle" to activate
repeat with i from 1 to 999
	tell application "System Events"
		key code 124
		set shellCommand to "screencapture -R 150,0,1300,850 -T1 -m /Users/Jerome/ebooks/" & i & ".png"
		do shell script shellCommand
		delay 1
		set shellCommand to "/usr/local/bin/tesseract /Users/Jerome/ebooks/" & i & ".png /Users/Jerome/ebooks/" & i & " -l eng"
		do shell script shellCommand
		delay 1
		try
			do shell script "diff -q /Users/Jerome/ebooks/" & i & ".png /Users/Jerome/ebooks/" & (i - 1) & ".png"
			exit repeat
		on error
			# last images are different so continue
		end try
	end tell
end repeat

