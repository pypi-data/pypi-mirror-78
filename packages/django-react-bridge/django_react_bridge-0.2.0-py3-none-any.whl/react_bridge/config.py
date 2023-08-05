import os
from django.conf import settings

DEFAULT_JS_CONFIG = {
    'use_yarn': True,
    'npm_command': 'yarn',
    'package_json_path': None,
    'output_path': None,
    'output_url': '/static/build/',
    'resolve': None,
    'entry': None,
}

USE_JS_DEV_SERVER = getattr(settings, 'REACT_BRIDGE_DEV', True)

JS_CONFIG = {
    **DEFAULT_JS_CONFIG,
    **getattr(settings, 'REACT_BRIDGE_JS_CONFIG', {})
}

# Set defaults from pkg path when not defined
if JS_CONFIG['package_json_path']:
    pkg_path = JS_CONFIG['package_json_path']
    if JS_CONFIG['output_path'] is None:
        JS_CONFIG['output_path'] = os.path.join(pkg_path, 'static/build')
    if JS_CONFIG['entry'] is None:
        JS_CONFIG['entry'] = os.path.join(pkg_path, 'src/index.js')