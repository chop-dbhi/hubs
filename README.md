# Hubs

Hub for storing streams of data via a URL, path, or file copies.

## Install

```bash
pip install hubs
```

## Quickstart

Hubs provides a basic CLI for initializing a local hub and puttings things into it.

```bash
# Initialize the hub..
hubs init

# ..put something in it
hubs put https://github.com/timeline.json
```

## Distributed Hub

There are two ways to accomplish a _distributed_ hub. Put the default database (SQLite) on a shared filesystem accessible by all machines that act as storage for the hub or use an alternate database backend.

Hubs is built on top of Django which supports PostgreSQL, MySQL, and Oracle and natively supported. There are also community supported [third-party backends](https://docs.djangoproject.com/en/1.5/ref/databases/#using-a-3rd-party-database-backend) as well.

## Future

- HTTP endpoints for using the HUB
    - Token-based authentication
- Support for queuing pull-based tasks
- Support for authentication
    - Web
    - SSH
- Standalone server for trivial setup and use
    - Similiar to Sentry
- Drop hard dependency on Django
    - Turn into a backend
