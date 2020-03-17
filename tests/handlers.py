

def track_errors(view, error, response):
    # Send the error to an application
    # monitoring service, e.g., Sentry
    response.error_tracked = True
