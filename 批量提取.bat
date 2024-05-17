setlocal

set "DIRECTORY=scn"

for /R "%DIRECTORY%" %%F in (*) do (
    PsbDecompile.exe -indent 4 "%%F"
)

endlocal