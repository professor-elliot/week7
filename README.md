# week7-base

This repository provides the starting point for Week 7: Virtual Hosts and Multi-Site Hosting.

Students are not expected to build website content from scratch in this lab. The purpose of this setup is to let students focus on:

- virtual hosts
- `server_name`
- multi-site hosting on one Nginx server
- the difference between static content and proxied application content
- verification with `curl`, browser testing, and `nginx -t`

## Learning goal

By the end of this week, students should be able to explain how one Nginx server can answer for multiple sites and how a request may be served either from local files or from a backend application.

## Repository structure

```text
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
```

## Intended architecture

This base release is designed for two servers:

### Web server
- Runs Nginx
- Hosts multiple virtual sites
- Serves one static site directly
- Proxies one site to a backend app

### Backend server
- Runs a small Python application
- Responds to HTTP requests
- Can later be used for reverse proxy, logging, health checks, and failover labs

## Suggested hostnames

Use `/etc/hosts` in the classroom environment.

Example:

```text
192.168.56.10 site1.local
192.168.56.10 app1.local
192.168.56.20 backend1.local
```

Adjust addresses to match your environment.

## Static site

The static site is intended to be served directly by Nginx from a document root.

Example future mapping:
- `site1.local` -> local files on the web server

## Backend app

The Python app is intentionally simple. It returns request information so students can clearly see when the response came from the backend instead of a static file.

Example future mapping:
- `app1.local` -> Nginx reverse proxy -> Python backend

## Typical deployment idea

### On the backend server

Copy `app-site/` to a working directory such as:

```bash
/opt/week7/app-site
```

Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run for testing:

```bash
python3 app.py
```

Later, enable it as a service using the included systemd unit.

### On the web server

Copy the static site into a document root such as:

```bash
/var/www/site1
```

Copy the Nginx server block examples from `nginx/sites-available/` into your server.

Then:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## Verification ideas

### Static site

```bash
curl -H "Host: site1.local" http://WEB_SERVER_IP/
```

### Backend app directly

```bash
curl http://BACKEND_SERVER_IP:5000/
```

### Future proxied app through Nginx

```bash
curl -H "Host: app1.local" http://WEB_SERVER_IP/
```

## Instructor note

This is the `week7-base` starting point. It is intentionally minimal so it can be extended in later tags and releases.
