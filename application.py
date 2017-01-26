from sanic import Sanic
from sanic.response import json, text
from database import Database


app = Sanic()
db = Database()


# BASELINE
##########

def abort(code):
    if code == 400:
        return text('', 400, {'X-Error-Message': 'the given beamid was malformatted'})
    elif code == 403:
        return text('', 403, {'X-Error-Message': 'beam had no content in it'})
    elif code == 404:
        return text('', 404, {'X-Error-Message': 'the requested beamid matches no existing beams'})
    elif code == 406:
        return text('', 406, {'X-Error-Message': 'requested content type for reply is unsupported'})


@app.route('/ping', methods=['GET',])
async def ping(request):
    return text('pong')


# SUBMITTING
############

@app.route('/raw/submit', methods=['POST',])
@app.route('/text/submit', methods=['POST',])
@app.route('/plain/submit', methods=['POST',])
async def submitraw(request):
    if request.form.get('content', '').strip() == '': return abort(403)
    return text(db.setkey(request.form['content']))


@app.route('/json/submit', methods=['POST',])
async def submitjson(request):
    if request.form.get('content', '').strip() == '': return abort(403)
    return json({'beamid': db.setkey(request.form['content'])})


@app.route('/submit', methods=['POST',])
async def submit(request):
    for mime in request.headers['accept'].split(','):
        if mime in ('*/*', 'text/plain'):
            return await submitraw(request)
        elif mime == 'application/json':
            return await submitjson(request)
    return abort(406)


# FETCHING
##########

@app.route('/raw/<beamid>', methods=['GET',])
@app.route('/text/<beamid>', methods=['GET',])
@app.route('/plain/<beamid>', methods=['GET',])
async def fetchraw(request, beamid):
    if not db.haskey(beamid): return abort(404)
    return text(db.getkey(beamid))


@app.route('/json/<beamid>', methods=['GET',])
async def fetchjson(request, beamid):
    if not db.haskey(beamid): return abort(404)
    return json({'beamid': beamid, 'content': db.getkey(beamid)})


@app.route('/<beamid>', methods=['GET',])
async def fetch(request, beamid):
    for mime in request.headers['accept'].split(','):
        if mime in ('*/*', 'text/plain'):
            return await fetchraw(request, beamid)
        elif mime == 'application/json':
            return await fetchjson(request, beamid)
    return abort(406)


# DEBUGGING
###########

if __name__ == '__main__':
    from sys import argv
    app.run(debug=True, port=int(argv[1]) if len(argv) > 1 else 5000)

