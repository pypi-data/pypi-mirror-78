# flake8: noqa
import moban_jinja2_github.issues
from moban_jinja2_github._version import __author__, __version__
from moban.plugins.jinja2.extensions import jinja_global
from moban_jinja2_github.contributors import get_contributors

jinja_global("moban_jinja2_contributors", get_contributors)
