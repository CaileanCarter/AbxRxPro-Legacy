@ECHO OFF
TITLE Antibiotic Resistance Profiles for Clinical Isolates

CD C:\Users\carterc\OneDrive - Norwich BioScience Institutes\Python scripts\Antibiotic_data\Antibiotic_data\

SET /P input="Would you like to run RGI Pipeline too? (y/n): "

IF %input%==y (
    CALL :RunPipeline
    ) ELSE (
        CALL :LaunchFigure
    )

SET /P secondInput="Display all antibiotics detected and plotted? (y/n): "

IF %secondInput%==y CALL :LaunchTables

EXIT /B 0


:RunPipeline
    ECHO Running RGI Pipeline...
    RGI_pipeline.py
    ECHO RGI Pipeline completed.
    CALL :LaunchFigure
GOTO :EOF


:LaunchFigure
    ECHO Loading figure...
    Antibiotic_resistance_profiles.py
    ECHO Figure loaded.
GOTO :EOF


:LaunchTables
    ECHO Loading tables...
    Launch_antibiotics_table.py
    ECHO Tables loaded.
EXIT /B 0