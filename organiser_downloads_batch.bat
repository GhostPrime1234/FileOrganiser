@echo off
REM Change to the directory where the Python script is located
cd "C:\Users\Michael\OneDrive - University of Wollongong\Home\Code\File organisation"

REM Activate the Anaconda environment
CALL "C:\Users\Michael\anaconda3\Scripts\activate.bat" base

REM Run the python script
python organise_downloads.py