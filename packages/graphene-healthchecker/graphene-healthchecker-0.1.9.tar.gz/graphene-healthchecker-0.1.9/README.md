# Graphene Backend Healthchecking

## Installation

    pip3 install graphene-healthchecker

## Running Health Check

```
Usage: graphenehealth [OPTIONS] URL

Options:
  --listen INTEGER
  --help            Show this message and exit.
```

**Example**:

```
graphenehealth --listen 8080 https://__ENDPOINT__
```

## Deploy with UWSGI

To deploy with UWSGI, please copy the `config-defaults.yml` file
into your working directory and deploy with systemd.

In `backend-health.service`, replace the variables in `{{ ... }}`
and install it in your systemd directory `/etc/systemd/system`.

## Health Check

1. Check if a connection can be established to the backend node. 
   (Raise HTTP/402 if not.)
2. Check that the returned answer from the backend has status code 200.
   (Raise HTTP/402 if not.)
3. Check if the answer has a "result" key in its json representation.
   (Raise HTTP/402 if not.)
4. Obtain the time of the most recent block as well as the next
   maintenance time
5. Check that current head time is less than 60 seconds old and next
   maintenance interval is more than 10 seconds in the future.
   (Raise HTTP/402 if not.)
