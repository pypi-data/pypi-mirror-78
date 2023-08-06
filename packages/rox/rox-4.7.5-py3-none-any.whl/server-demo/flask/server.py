import os
from flask import Flask, jsonify

from rox.server.flags.rox_flag import RoxFlag
from rox.server.rox_server import Rox
from rox.server.rox_options import RoxOptions

class Container:
    def __init__(self):
        self.first_flag = RoxFlag()


def rox_setup():
    os.environ['ROLLOUT_MODE'] = 'QA'
    options = RoxOptions(dev_mode_key='78a38345febcbfef161d8bf6')
    Rox.register('test', con)
    Rox.setup('58dbcdce18720f1be0624803', options).result()


con = Container()
rox_setup()
app = Flask(__name__)

Rox.set_custom_string_property('whoo', '5000')

@app.route('/api/values')
def values():
    return jsonify(['value1', 'value2'])


@app.route('/api/values/<id>')
def value(id):
    if con.first_flag.is_enabled():
        return jsonify('value%s' % id)
    else:
        return jsonify('Eladddddd')


@app.route('/api/values', methods=['POST'])
def post_value():
    return ''


@app.route('/api/values/<id>', methods=['PUT'])
def put_value(id):
    return ''


@app.route('/api/values/<id>', methods=['DELETE'])
def delete_value(id):
    return ''

if __name__ == "__main__":
    app.run()
