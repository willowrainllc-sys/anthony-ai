@echo off
echo 🔱 WILLOW RAIN SECURITY: IGNITING INDUSTRIAL MATRIX...
start /b python -m pproxy -l socks5://0.0.0.0:8000
for /L %%p in (1080,1,1180) do (
    start /b python -m pproxy -l socks5://0.0.0.0:%%p
)
echo ✓ MATRIX ARMED (Ports 8000, 1080-1180)
