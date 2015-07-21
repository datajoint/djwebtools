from flask import Blueprint

import datajoint as dj
from .forms import DataJointFormFactory

PER_PAGE = 20
ENABLE_EDIT=True


djpage = Blueprint('djpage', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/%s' % __name__
                    )


form_factory = DataJointFormFactory()
_registered_relations = {}

from .display_tools import display
from .edit import enter


def register(for_form=False, **kwargs):
    for name, rel in kwargs.items():
        assert isinstance(rel, dj.Relation), "rel must be a subclass of dj.Relation"
        _registered_relations[name] = rel

    if for_form:
        form_factory.register(**kwargs)


djpage.add_app_template_global(ENABLE_EDIT, 'edit_enabled')
