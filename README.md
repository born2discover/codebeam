# CodeBeam
> **Requires Python 3.6+**

This is a boilerplate/demo project showcasing basic usage of the
[Sanic](https://github.com/channelcat/sanic/) framework/webserver.
In short, it's basically the backend for PasteBin-like service
implemented in \~80 LOC. Great as a quickstart or learn-by-example
guide.

### [application.py](application.py)
> Contains all of the Sanic bits and routing logic.

### [database.py](database.py)
> Contains all of the Redis database interactions.


## Running
To run any instance of the webserver you'll need to set a `REDIS_URL` environment
variable with the connection URL of a valid Redis database.

```
# SET ENV VARIABLE  (default local instance)
export REDIS_URL='redis://@localhost:6379/0'  # Bash
set -x REDIS_URL 'redis://@localhost:6379/0'  # Fish

# DEBUGGING
python -B application.py [port]

# DEPLOYING
python -m sanic application.app --host=0.0.0.0 --port=<port>
```


## Heroku/Dokku
This software is _Heroku-ready_, meaning you can host this on any
_Heroku-like_ platform, including Dokku on a private VPS. You only need to
make sure you add a Redis plugin to it and link it to the Heroku app,
making sure that it's providing a connection URL to your app on the
`REDIS_URL` variable. Setup instructions are as follows:

### From the Dokku instance
```
dokku apps:create <appname>
dokku plugin:install https://github.com/dokku/dokku-redis.git redis
dokku redis:create <dbname>
dokku redis:link <dbname> <appname>
```

### From your application's git repository
```
git remote add dokku dokku@<serveraddress>:<appname>
git push dokku master
```

To deploy another branch into production use `git push dokku <branch>:master`

To deploy this in Heroku find another database module for Redis.


## API Usage
Data should always be sent as form data on the POST request.

### Check if the service is running
```
GET /ping
yields: "pong" as "text/plain"
```

### Submit content
```
   POST /submit Accept:*/*,text/plain content="whatever"
or POST /raw/submit content="whatever"
or POST /text/submit content="whatever"
or POST /plain/submit content="whatever"
yields: <beamid> as "text/plain"
errors: # Accept header had an unsupported mimetype (only for /submit resource)
        status-code=406
        X-Error-Message="requested content type for reply is unsupported"

        # you tried to post an empty paste
        status-code=403
        X-Error-Message="beam had no content in it"

   POST /submit Accept:application/json content="whatever"
or POST /json/submit content="whatever"
yields: {
    "beamid": "<beamid>"
} as "application/json"
errors: # Accept header had an unsupported mimetype (only for /submit resource)
        status-code=406
        X-Error-Message="requested content type for reply is unsupported"

        # you tried to post an empty paste
        status-code=403
        X-Error-Message="beam had no content in it"
```

### Fetch content
```
   GET /<beamid> Accept:*/*,text/plain
or GET /raw/<beamid>
or GET /text/<beamid>
or GET /plain/<beamid>
yields: <content> as "text/plain"
errors: # Accept header had an unsupported mimetype (only for /<beamid> resource)
        status-code=406
        X-Error-Message="requested content type for reply is unsupported"

        # beamid was badly formatted
        status-code=400
        X-Error-Message="the given beamid was malformatted"

        # beam not found
        status-code=404
        X-Error-Message="the requested beamid matches no existing beams"

   GET /<beamid> Accept:application/json
or GET /json/<beamid>
yields: {
    "beamid": "<beamid>",
    "content": "<content>"
} as "application/json"
errors: # Accept header had an unsupported mimetype (only for /<beamid> resource)
        status-code=406
        X-Error-Message="requested content type for reply is unsupported"

        # beamid was badly formatted
        status-code=400
        X-Error-Message="the given beamid was malformatted"

        # beam not found
        status-code=404
        X-Error-Message="the requested beamid matches no existing beams"
```

