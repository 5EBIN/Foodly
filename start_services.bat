@echo off
echo Starting CN Project Services...

echo.
echo Starting Redis (make sure Redis is installed and running)
echo You can start Redis with: redis-server

echo.
echo Starting G-Value Service on port 5001...
start "G-Value Service" cmd /k "cd g-value-service && .\venv\Scripts\Activate.ps1 && python app/main.py"

echo.
echo Waiting 5 seconds for G-Value Service to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting Backend API on port 8000...
start "Backend API" cmd /k "cd backend && .\venv\Scripts\Activate.ps1 && python app/main.py"

echo.
echo Waiting 5 seconds for Backend API to start...
timeout /t 5 /nobreak > nul

echo.
echo Starting React Native App...
start "React Native App" cmd /k "cd frontend\worker-app && npm start"

echo.
echo All services started!
echo.
echo Services:
echo - G-Value Service: http://localhost:5001
echo - Backend API: http://localhost:8000
echo - React Native App: Expo Dev Tools
echo.
echo Press any key to exit...
pause > nul
