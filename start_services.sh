#!/bin/bash

PROJECT_DIR="$(pwd)"
VENV_DIR="$PROJECT_DIR/venv"
LOG_DIR="$PROJECT_DIR/logs"

mkdir -p "$LOG_DIR"

if [ ! -d "$VENV_DIR" ]; then
    echo "error: venv not found in $VENV_DIR"
    exit 1
fi

source "$VENV_DIR/bin/activate"

check_port() {
    local port="$1"
    if lsof -i :"$port" > /dev/null 2>&1; then
        echo "error: port $port is already in use"
        exit 1
    fi
}

check_port 5000
check_port 5001
check_port 5002
check_port 5003

start_service() {
    local service_dir=$1
    local service_name=$2
    local port=$3
    local script_file=$4

    echo "Starting $service_name on port $port..."
    cd "$PROJECT_DIR/$service_dir" || exit 1
    nohup python "$script_file" > "$LOG_DIR/$service_name.log" 2>&1 &
    echo "$!" > "$LOG_DIR/$service_name.pid"
    cd "$PROJECT_DIR"
}

start_service "api_gateway" "api_gateway" 5000 "app.py"
start_service "auth_service" "auth_service" 5001 "app.py"
start_service "user_service" "user_service" 5002 "app.py"
start_service "task_services" "task_services" 5003 "app.py"

echo "Todos los servicios fueron iniciados correctamente"
echo "Logs guardados en $LOG_DIR"
echo "Presiona Ctrl+C para salir (detén manualmente los procesos si es necesario)"
