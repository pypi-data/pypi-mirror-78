from flask import Blueprint

blueprint = Blueprint(name='api', import_name=__name__)

@blueprint.route('/issue', methods=['POST'])
def create():
    return 'Hello World'

@blueprint.route('/issue', methods=['POST'])
def update():
    return 'Hello World'

@blueprint.route('/issue', methods=['POST'])
def delete():
    return 'Hello World'