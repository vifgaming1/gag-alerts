import os
import subprocess
import tempfile

# Files to package
files = ["alert.mp3", "icon.png", "main.ps1", "main.py"]
output_exe = "package.exe"
cmd_to_run = "powershell.exe -ExecutionPolicy Bypass -File main.ps1"

# Create the SED config
sed_content = f"""
[Version]
Class=IEXPRESS
SEDVersion=3
[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=1
HideExtractAnimation=0
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSigning=0
RebootMode=I
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetName={output_exe}
FriendlyName=Seed Alert Package
AppLaunched={cmd_to_run}
PostInstallCmd=
AdminQuietInstCmd=
UserQuietInstCmd=
SourceFiles=SourceFiles

[SourceFiles]
SourceFiles0={os.getcwd()}

[SourceFiles0]
"""

# Append files to the config
for file in files:
    sed_content += f'{file}=\n'

# Save the SED file temporarily
with tempfile.NamedTemporaryFile("w", suffix=".sed", delete=False) as sed_file:
    sed_file.write(sed_content)
    sed_path = sed_file.name

# Run IExpress
print(f"Running IExpress with config: {sed_path}")
subprocess.run(["iexpress", "/N", sed_path], shell=True)

# Optionally delete the sed file
# os.remove(sed_path)
