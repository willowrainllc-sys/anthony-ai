@echo off
echo Setting JAVA_HOME to Android Studio bundled JDK...
setx JAVA_HOME "C:\Program Files\Android\Android Studio\jbr" /M

echo Updating Path to include Java bin...
:: Note: This adds to the System path. /M requires Administrator privileges.
setx PATH "%PATH%;%%JAVA_HOME%%\bin" /M

echo.
echo Java fix applied globally.
echo IMPORTANT: You MUST restart Android Studio for these changes to take effect.
pause
