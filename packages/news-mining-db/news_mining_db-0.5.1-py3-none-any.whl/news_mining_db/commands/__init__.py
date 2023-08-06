def init_db():
    f = open('db_config.json', 'w')

    template = '{' + ', '.join([f'"{config_key}": null' for config_key in _config_keys]) + '}'

    f.write(template)

    f.close()


def upgrade_db():
    import os
    import json
    from alembic.config import Config
    from alembic.command import upgrade

    with open('db_config.json') as config_file:
        config_data = json.load(config_file)

        config = {}
        for key in _config_keys:
            if key in config_data and config_data[key]:
                config[key] = config_data[key]

    if 'db_uri' not in config.keys():
        print('no db_uri supported.')
        return

    base_path = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
    ini_file_path = os.path.join(base_path, 'alembic.ini')
    config_object = Config(ini_file_path)
    config_object.set_main_option('sqlalchemy.url', config['db_uri'])
    config_object.set_main_option('version_locations', os.path.join(base_path, 'migrations'))

    upgrade(config_object, 'head')


_config_keys = [
    'db_uri',
]
