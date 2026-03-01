@echo off
setlocal enabledelayedexpansion
title Hot Corners — Build EXE
color 0A

echo.
echo  =========================================
echo    Hot Corners  ^|  EXE Builder
echo  =========================================
echo.

:: ── Locate Python ─────────────────────────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python not found in PATH.
    echo          Download from https://python.org and tick "Add to PATH".
    pause & exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo  [OK] %PY_VER%

:: ── Check required source files ───────────────────────────────────────────────
if not exist "hot_corners.py" (
    echo  [ERROR] hot_corners.py not found.
    echo          Put this build.bat in the same folder as hot_corners.py
    pause & exit /b 1
)
echo  [OK] hot_corners.py found

if exist "icon.ico" (
    echo  [OK] icon.ico found  ^(will be embedded^)
    set ICON_FLAG=--windows-icon-from-ico=icon.ico
    @REM set ICON_FLAG=--icon=icon.ico
) else (
    echo  [WARN] icon.ico not found  ^(no icon will be embedded^)
    set ICON_FLAG=""
)

echo.

:: ── Try Nuitka first (smallest output) ────────────────────────────────────────
python -m nuitka --version >nul 2>&1

:install_nuitka
echo.
echo  [*] Installing Nuitka...
pip install nuitka --quiet --upgrade
if errorlevel 1 (
    echo  [ERROR] Could not install Nuitka.
    echo          Try:  pip install nuitka
    pause & exit /b 1
)
echo  [OK] Nuitka ready 
goto :build_nuitka

if not errorlevel 1 (
    echo  [*] Nuitka detected — using Nuitka ^(produces smallest EXE^)
    goto :build_nuitka
)

pip show nuitka >nul 2>&1
if not errorlevel 1 (
    echo  [*] Nuitka installed — using Nuitka
    goto :build_nuitka
)

echo  [*] Nuitka not found — trying to install it...
goto :install_nuitka
echo  [*] If installation fails, PyInstaller will be used as a fallback.
goto :install_pyinstaller

:: ── Nuitka build ──────────────────────────────────────────────────────────────
:build_nuitka
echo.
echo  [*] Building with Nuitka ^(this takes 2-5 min on first run^)...
echo.

python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=disable ^
    --windows-product-name="Hot Corners" ^
    --windows-file-description="Hot Corners for Windows" ^
    --windows-product-version=4.0.0.0 ^
    %ICON_FLAG% ^
    --plugin-enable=tk-inter ^
    --assume-yes-for-downloads ^
    --output-filename=HotCorners.exe ^
    --output-dir=dist ^
    --remove-output ^
    hot_corners.py

if errorlevel 1 (
    echo.
    echo  [WARN] Nuitka build failed — falling back to PyInstaller
    goto :install_pyinstaller
)
goto :done

:: ── PyInstaller install + build ───────────────────────────────────────────────
:install_pyinstaller
echo.
echo  [*] Installing PyInstaller...
pip install pyinstaller --quiet --upgrade
if errorlevel 1 (
    echo  [ERROR] Could not install PyInstaller.
    echo          Try:  pip install pyinstaller
    pause & exit /b 1
)
echo  [OK] PyInstaller ready

:build_pyinstaller
echo.
echo  [*] Building with PyInstaller...
echo.

:: Check for UPX (optional binary compressor, cuts size ~40%)
set UPX_ARG=
where upx >nul 2>&1
if not errorlevel 1 (
    echo  [OK] UPX found — will compress output
    set UPX_ARG=--upx-dir=.
) else (
    echo  [INFO] UPX not found — skipping compression
    echo         Drop upx.exe here to compress the output
)

pyinstaller ^
    --onefile ^
    --windowed ^
    --name HotCorners ^
    --icon=icon.ico ^
    --distpath dist ^
    --workpath build_tmp ^
    --specpath . ^
    --exclude-module _bootlocale ^
    --exclude-module lib2to3 ^
    --exclude-module email ^
    --exclude-module html ^
    --exclude-module http ^
    --exclude-module unittest ^
    --exclude-module xml ^
    --exclude-module xmlrpc ^
    --exclude-module pydoc ^
    --exclude-module doctest ^
    --exclude-module difflib ^
    --exclude-module optparse ^
    --exclude-module curses ^
    --exclude-module numpy ^
    --exclude-module scipy ^
    --exclude-module pandas ^
    --exclude-module matplotlib ^
    %UPX_ARG% ^
    hot_corners.py

if errorlevel 1 (
    echo.
    echo  [ERROR] Build failed. Check the output above for details.
    pause & exit /b 1
)

:: Clean up PyInstaller temp files
if exist build_tmp  rmdir /s /q build_tmp  >nul 2>&1
if exist HotCorners.spec del HotCorners.spec >nul 2>&1

:: ── Done ──────────────────────────────────────────────────────────────────────
:done
echo.
if not exist "dist\HotCorners.exe" (
    echo  [ERROR] Expected dist\HotCorners.exe was not created.
    pause & exit /b 1
)

for %%F in (dist\HotCorners.exe) do (
    set /a SIZE_KB=%%~zF/1024
    set /a SIZE_MB=%%~zF/1048576
)

echo  =========================================
echo    BUILD COMPLETE
echo  =========================================
echo.
echo    Output : dist\HotCorners.exe
echo    Size   : ~!SIZE_MB! MB  (!SIZE_KB! KB^)
echo.
echo    To auto-start with Windows, paste a shortcut to
echo    HotCorners.exe into:
echo      %%APPDATA%%\Microsoft\Windows\Start Menu\Programs\Startup
echo.
pause