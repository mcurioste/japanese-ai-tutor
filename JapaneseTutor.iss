#define MyAppName "Japanese Tutor"
#define MyAppVersion "0.1.0"
[Setup]
AppId={{B991C506-E5C4-4A12-87B6-4F046EED8AE0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={localappdata}\Programs\JapaneseTutor
DefaultGroupName={#MyAppName}
OutputDir=installer
OutputBaseFilename=JapaneseTutor-Setup-0.1.0
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
WizardStyle=modern
[Files]
Source: "dist\JapaneseTutor\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs ignoreversion
[Icons]
Name: "{group}\Japanese Tutor"; Filename: "{app}\JapaneseTutor.exe"
Name: "{autodesktop}\Japanese Tutor"; Filename: "{app}\JapaneseTutor.exe"; Tasks: desktopicon
[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"
[Run]
Filename: "{app}\JapaneseTutor.exe"; Description: "Launch Japanese Tutor"; Flags: nowait postinstall skipifsilent
