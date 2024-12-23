@echo off
REM Change to the directory where the Python script is located
cd "%USERPROFILE%\OneDrive - University of Wollongong\Home\Code\File organisation"

REM Activate the Anaconda environment
CALL "%USERPROFILE%\anaconda3\Scripts\activate.bat" base

REM Run the python script
python file_organizer.py