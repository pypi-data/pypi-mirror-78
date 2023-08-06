__version__ = "0.1.0"
import os

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(_BASE_DIR, 'resources')
SWAGGER_SPEC_PATH = os.path.join(RESOURCES_DIR, 'swagger', 'swaggerSpec.yml')
STATIC_DIR = os.path.join(RESOURCES_DIR, 'static')
TEMPLATES_DIR = os.path.join(RESOURCES_DIR, 'templates')
SQL_DIR = os.path.join(RESOURCES_DIR, 'sql')
MIGRATIONS_DIR = os.path.join(SQL_DIR, 'migrations')
