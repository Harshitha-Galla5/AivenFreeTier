def detect_issue(log):
    message = log['message'].lower()

    if "connection refused" in message:
        return "restart_service"
    elif "disk full" in message:
        return "cleanup_storage"
    elif "timeout" in message:
        return "retry"
    else:
        return None
