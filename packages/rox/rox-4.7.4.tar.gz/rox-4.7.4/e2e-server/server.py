import os
from flask import Flask, jsonify, request

from rox.server.flags.rox_flag import RoxFlag
from rox.server.rox_server import Rox
from rox.server.rox_options import RoxOptions

class Container:
    instance = None

    def __init__(self):
        self.boolDefaultFalse = RoxFlag(False)
        self.boolDefaultTrue = RoxFlag(True)

Container.instance = Container()

class ServerLogger:
    def debug(self, message, ex=None):
        if ex is None:
            print(message)
        else:
            print('%s. Exception: %s' % (message, ex))

    def error(self, message, ex=None):
        if ex is None:
            print(message)
        else:
            print(message, ex)

    def warn(self, message, ex=None):
        if ex is None:
            print(message)
        else:
            print('%s. Exception: %s' % (message, ex))

# def rox_setup():
#     os.environ['ROLLOUT_MODE'] = 'QA'
#     options = RoxOptions(dev_mode_key='78a38345febcbfef161d8bf6')
#     Rox.register('test', con)
#     Rox.setup('58dbcdce18720f1be0624803', options).result()


con = Container()
app = Flask(__name__)
cancel_event = None

@app.route('/status-check')
def values():
    return ''


@app.route('/api/values/<id>')
def value(id):
    if con.first_flag.is_enabled():
        return jsonify('value%s' % id)
    else:
        return jsonify('Eladddddd')


@app.route('/', methods=['POST'])
def post_value():
    global cancel_event
    data = request.json
    action = data['action']
    payload = data.get('payload')
    print(data)
    if action == 'staticFlagIsEnabled':
        result = getattr(Container.instance, payload['flag']).is_enabled(payload['context'])
        return jsonify({ 'result': result })
    elif action == 'registerStaticContainers':
        Rox.register('namespace', Container.instance)
        return jsonify({ 'result': 'done' })
    elif action == 'setCustomPropertyToThrow':
        def raise_(ex):
            raise ex
        Rox.set_custom_string_property(payload['key'], lambda context: raise_(Exception('error')))
        return jsonify({ 'result': 'done' })
    elif action == 'setCustomStringProperty':
        Rox.set_custom_string_property(payload['key'], payload['value'])
        return jsonify({ 'result': 'done' })
    elif action == 'dynamicFlagValue':
        if payload.get('context'):
            for key in payload.get('context'):
                if type(payload.get('context').get(key)) is str:
                    Rox.set_custom_string_property(key, payload.get('context').get(key))
                if type(payload.get('context').get(key)) is bool:
                    Rox.set_custom_boolean_property(key, payload.get('context').get(key))
                if type(payload.get('context').get(key)) is int:
                    Rox.set_custom_int_property(key, payload.get('context').get(key))
                if type(payload.get('context').get(key)) is float:
                    Rox.set_custom_float_property(key, payload.get('context').get(key))
        result = Rox.dynamic_api().value(payload['flag'], payload['defaultValue'], [], payload.get('context'))
        return jsonify({ 'result': result })
    elif action == 'dynamicFlagIsEnabled':
        if payload.get('context'):
            for key in payload.get('context'):
                if type(payload.get('context').get(key)) is str:
                    Rox.set_custom_string_property(key, payload.get('context').get(key))
                if type(payload.get('context').get(key)) is bool:
                    Rox.set_custom_boolean_property(key, payload.get('context').get(key))
                if type(payload.get('context').get(key)) is int:
                    Rox.set_custom_int_property(key, payload.get('context').get(key))
                if type(payload.get('context').get(key)) is float:
                    Rox.set_custom_float_property(key, payload.get('context').get(key))
        result = Rox.dynamic_api().is_enabled(payload['flag'], payload['defaultValue'], payload.get('context'))
        return jsonify({ 'result': result })
    elif action == 'setupAndAwait':
        print(payload['options'])
        env = 'stam'
        if payload.get('options'):
            options = payload.get('options')
            if options.get('configuration'):
                configuration = options.get('configuration')
                env = configuration.get('env')
        if env == 'qa':
            os.environ['ROLLOUT_MODE'] = 'QA'
        options = RoxOptions(logger=ServerLogger())
        cancel_event = Rox.setup(payload['key'], options).result()
        return jsonify({ 'result': 'done' })
    elif action == 'stop':
        if cancel_event:
            cancel_event.set()
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()
        return jsonify({ 'result': 'done' })
    return ''


@app.route('/api/values/<id>', methods=['PUT'])
def put_value(id):
    return ''


@app.route('/api/values/<id>', methods=['DELETE'])
def delete_value(id):
    return ''

if __name__ == "__main__":
    app.run(host="localhost", port=os.environ['PORT'])
