# week8-branch

This repository provides the starting point for Week 9: Reverse Proxy, Application Logging, Nginx Logging, and Basic OS-Level Observation.

Students are not expected to build a backend application from scratch in this lab. The purpose of this setup is to let students focus on:

- reverse proxy behavior
- the difference between Nginx logs and application logs
- the difference between live log observation and log searching
- 502-style upstream failures
- basic OS network evidence with `ss`

## Learning goal

By the end of this week, students should be able to explain how a request moves through a reverse proxy stack, identify which layer recorded what happened, and use multiple sources of evidence to diagnose a failure.

## Repository structure

```text
week9-branch/
  README.md
  app/
    app.py
    requirements.txt
    logs/
      .gitkeep
  nginx/
    site.conf
  systemd/
    app.service
```

## What this environment demonstrates

This repository creates a simple three-layer observable system:

1. **Application layer**
   - Flask app listening on `127.0.0.1:5000`
   - Writes to `app/logs/app.log`

2. **Web server layer**
   - Nginx listens on port `80`
   - Proxies requests to the Flask app
   - Writes to `/var/log/nginx/access.log` and `/var/log/nginx/error.log`

3. **OS / network layer**
   - Ubuntu can show listening ports and active connections with `ss`
   - Optional system log entries can be written with `logger`

## Application behavior

The Flask app provides three useful endpoints:

- `GET /hello`
  - returns a simple success response
  - writes an informational log entry

- `GET /headers`
  - returns selected request headers as JSON
  - helps students see what Nginx forwarded upstream

- `GET /error`
  - intentionally raises an exception
  - useful for observing failure behavior and comparing logs

## Requirements

- Ubuntu
- Python 3
- Nginx
- `python3-venv`
- `python3-pip`

## Suggested setup

### 1. Install system packages

```bash
sudo apt update
sudo apt install -y nginx python3 python3-venv python3-pip
```

### 2. Create a virtual environment

```bash
cd app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the backend application

```bash
python3 app.py
```

The backend should listen on `127.0.0.1:5000`.

### 4. Install the Nginx site configuration

Copy the provided site file into your Nginx configuration path. One common approach is:

```bash
sudo cp nginx/site.conf /etc/nginx/sites-available/week9-app
sudo ln -s /etc/nginx/sites-available/week9-app /etc/nginx/sites-enabled/week9-app
sudo rm -f /etc/nginx/sites-enabled/default
```

### 5. Test and reload Nginx

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 6. Verify behavior

Direct to app:

```bash
curl http://127.0.0.1:5000/hello
```

Through Nginx:

```bash
curl http://localhost/hello
```

## Observing logs

### Live observation

Nginx access log:

```bash
sudo tail -f /var/log/nginx/access.log
```

Nginx error log:

```bash
sudo tail -f /var/log/nginx/error.log
```

Application log:

```bash
tail -f app/logs/app.log
```

### Searching logs

Search for requests to `/hello`:

```bash
grep "/hello" /var/log/nginx/access.log
```

Search for upstream failures:

```bash
grep "502" /var/log/nginx/access.log
```

Search for application events:

```bash
grep "Request received" app/logs/app.log
```

Filter live access logs for `/hello`:

```bash
sudo tail -f /var/log/nginx/access.log | grep "/hello"
```

## Observing OS network state

Show listeners and bound processes:

```bash
sudo ss -tulnp
```

Show active TCP connections:

```bash
ss -tn
```

Refresh active TCP connections continuously:

```bash
watch -n 1 ss -tn
```

## Optional Ubuntu log activity beyond defaults

Ubuntu already records system activity in logs such as `/var/log/syslog`. For class purposes, a simple way to demonstrate OS-level logging beyond the application and Nginx is to create a manual system log entry:

```bash
logger "week9 lab test entry"
```

Then search for it:

```bash
grep "week9 lab test entry" /var/log/syslog
```

This is useful for helping students distinguish between:

- application-generated logs
- web server-generated logs
- operating system log records

## 502 failure demonstration

1. Start the app and verify `/hello` works.
2. Stop the app with `Ctrl+C`.
3. Request `/hello` through Nginx.
4. Observe:
   - `502` in Nginx access log
   - upstream connection error in Nginx error log
   - no corresponding application log entry
   - no listener on port `5000` when checked with `ss`



## 500 failure demonstration

This scenario contrasts with the 502 case. In a 500 error, Nginx can still reach the backend application, but the application fails while handling the request.

### Recreate the 500 error

1. Start the app and verify `/hello` works.
2. Request `/error` directly against the app or through Nginx.
3. Observe:
   - `500` in the Nginx access log when requested through Nginx
   - little or no useful information in the Nginx error log, because proxying still worked
   - corresponding error and exception details in `app/logs/app.log`
   - port `5000` is still listening when checked with `ss`

### Example commands

Direct to app:

```bash
curl http://127.0.0.1:5000/error
```

Through Nginx:

```bash
curl http://localhost/error
```

Search for the failed request in Nginx:

```bash
grep "500" /var/log/nginx/access.log
```

Search for the application-side failure:

```bash
grep "Unhandled exception" app/logs/app.log
```

### Key takeaway

A 500 Internal Server Error means:

> The request reached the application, but the application failed while trying to handle it.

This is different from a 502 Bad Gateway:

- **500** = application failure after the request arrived
- **502** = reverse proxy failure before the application handled the request

## Optional systemd service

A sample systemd unit file is provided in `systemd/app.service`.
This is optional and can be used later if you want the app to run as a managed service instead of from a foreground terminal.

## Instructor notes

This repository is intentionally simple.
It is designed to support reasoning about evidence across layers rather than production completeness.

Not included yet:

- log rotation
- structured JSON logs
- centralized logging
- advanced rsyslog or journald configuration

Those topics can be added later after students become comfortable with basic observation and investigation.
