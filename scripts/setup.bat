@echo off
echo ========================================
echo AI-DOS Setup Script
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    exit /b 1
)

echo [1/5] Docker found
echo.

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker Compose is not installed
    exit /b 1
)

echo [2/5] Docker Compose found
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo [3/5] Creating .env file...
    (
        echo JWT_SECRET=change-this-in-production-%RANDOM%
        echo POSTGRES_USER=aidos
        echo POSTGRES_PASSWORD=aidos_dev_password
        echo POSTGRES_DB=aidos
        echo MINIO_ROOT_USER=aidos
        echo MINIO_ROOT_PASSWORD=aidos_dev_password
        echo RABBITMQ_DEFAULT_USER=aidos
        echo RABBITMQ_DEFAULT_PASS=aidos_dev_password
        echo STRIPE_API_KEY=sk_test_dummy
    ) > .env
    echo .env file created
) else (
    echo [3/5] .env file already exists
)
echo.

REM Create necessary directories
echo [4/5] Creating directories...
if not exist infrastructure\prometheus mkdir infrastructure\prometheus
echo Directories created
echo.

REM Create Prometheus configuration
echo [5/5] Creating Prometheus configuration...
(
    echo global:
    echo   scrape_interval: 15s
    echo   evaluation_interval: 15s
    echo.
    echo scrape_configs:
    echo   - job_name: 'api-gateway'
    echo     static_configs:
    echo       - targets: ['api-gateway:8000']
    echo.
    echo   - job_name: 'dataforge'
    echo     static_configs:
    echo       - targets: ['dataforge:8000']
    echo.
    echo   - job_name: 'modelhub'
    echo     static_configs:
    echo       - targets: ['modelhub:8000']
) > infrastructure\prometheus\prometheus.yml
echo Prometheus configuration created
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start AI-DOS, run:
echo   docker-compose up -d
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop AI-DOS:
echo   docker-compose down
echo.
echo Access points:
echo   - API Gateway: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Grafana: http://localhost:3000 (admin/admin)
echo   - MinIO Console: http://localhost:9001 (aidos/aidos_dev_password)
echo   - RabbitMQ: http://localhost:15672 (aidos/aidos_dev_password)
echo.
echo ========================================
