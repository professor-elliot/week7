# week7-base

This repository provides the starting point for Week 7: Virtual Hosts and Multi-Site Hosting.

Students are not expected to build website content from scratch in this lab. The purpose of this setup is to let students focus on:

- virtual hosts
- server_name
- multi-site hosting on one Nginx server
- the difference between static content and proxied application content
- verification with curl, browser testing, and nginx -t

## Learning goal

By the end of this week, students should be able to explain how one Nginx server can answer for multiple sites and how a request may be served either from local files or from a backend application.

## Repository structure

week7/
  static-site/
    index.html
  app-site/
    app.py
    requirements.txt
  nginx/
    sites-available/
      static-site.conf
      app-site.conf
  systemd/
    app-site.service

## Intended architecture

This base release is designed for two servers:

Web server:
- Runs Nginx
- Hosts multiple virtual sites
- Serves one static site directly
- Proxies one site to a backend app

Backend server:
- Runs a small Python application
- Responds to HTTP requests
- Can later be used for reverse proxy, logging, health checks, and failover labs

## Suggested hostnames

Use /etc/hosts in the classroom environment.

Example:

192.168.56.10 site1.local
192.168.56.10 app1.local
192.168.56.20 backend1.local

Adjust addresses to match your environment.

## Static site

The static site is intended to be served directly by Nginx from a document root.

Example mapping:
site1.local -> local files on the web server

## Backend app

The Python app is intentionally simple. It returns request information so students can clearly see when the response came from the backend instead of a static file.

Example mapping:
app1.local -> Nginx reverse proxy -> Python backend

## Deploying Servers

### Backend server

cd app-site

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Run for testing:

python3 app.py

Optional (recommended):

sudo cp systemd/app-site.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start app-site
sudo systemctl enable app-site

### Configure Nginx (web server)

sudo cp nginx/sites-available/*.conf /etc/nginx/sites-available/

sudo ln -s /etc/nginx/sites-available/static-site.conf /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/app-site.conf /etc/nginx/sites-enabled/

sudo rm /etc/nginx/sites-enabled/default

sudo nginx -t
sudo systemctl reload nginx

## Verification (run in order)

1. Verify backend app directly

curl http://BACKEND_SERVER_IP:5000/

Expected:
- JSON response

This proves the app works before Nginx is involved.

2. Verify static site

curl -H "Host: site1.local" http://WEB_SERVER_IP/

Expected:
- HTML content

This proves Nginx is serving local files and matching server_name.

3. Verify proxied app

curl -H "Host: app1.local" http://WEB_SERVER_IP/

Expected:
- JSON response from backend

This proves proxy_pass is working.

4. Verify identity without DNS

curl -H "Host: site1.local" http://WEB_SERVER_IP/
curl -H "Host: app1.local" http://WEB_SERVER_IP/

This proves one server can return different responses based on Host header.

5. Test failure behavior

sudo systemctl stop app-site

curl -H "Host: app1.local" http://WEB_SERVER_IP/

Expected:
- 502 Bad Gateway

This proves Nginx is working but the backend is not.

## Key Concepts

- server_name determines which site answers
- root serves local files
- proxy_pass forwards to an application
- one server can behave differently based on request identity
- Nginx can be working even if the backend is down

## Common Issues

- 502 error: backend not running or wrong port
- same site for both hosts: default config still enabled or server_name mismatch
- hostnames not resolving: /etc/hosts incorrect
- nginx fails to reload: run nginx -t