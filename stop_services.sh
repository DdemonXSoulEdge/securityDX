PROJECT_DIR="$(pwd)"
LOG_DIR="$PROJECT_DIR/logs"

stop_service() {
    local service_name=$1
    local pid_file="$LOG_DIR/$service_name.pid"

    if [ -f "$pid_file" ]; then
        local pid
        pid=$(cat "$pid_file")

        if kill -0 "$pid" > /dev/null 2>&1; then
            echo "Stopping $service_name (PID: $pid)..."
            kill "$pid"
            rm "$pid_file"
            echo "$service_name stopped."
        else
            echo "Warning: $service_name process with PID $pid not found. Removing stale PID file."
            rm "$pid_file"
        fi
    else
        echo "No PID file found for $service_name. It may not be running."
    fi
}

stop_service "api_gateway"
stop_service "auth_service"
stop_service "user_service"
stop_service "task_services"

echo "All services have been stopped (if running)."
