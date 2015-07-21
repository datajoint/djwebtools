from . import djpage, _registered_relations, PER_PAGE
from flask import render_template, request, url_for
from .forms import Restriction
from .relationtable import RelationTable


@djpage.route('/display/<relname>', methods=['GET', 'POST'])
def display(relname):
    form = Restriction(request.form)
    error_msg = None

    args = dict(request.args)
    sortby = args.pop('sortby', None)
    sortdir = int(args.pop('sortdir', ['0'])[0])
    page = int(args.pop('page', ['1'])[0])
    restr = args.pop('restr', None)

    if request.method == 'POST':
        if request.form['submit'] == 'apply restriction':
            if form.validate():
                restriction = form.restriction.data.strip()
                if len(restriction) > 0:
                    if restr is not None:
                        restr.append(restriction)
                    else:
                        restr = [restriction]


    reltab = RelationTable(relname, per_page=PER_PAGE, restrictions=restr, descending=sortdir, sortby=sortby, page=page)
    return render_template('display_table.html', reltab=reltab, form=form, error_msg=error_msg)




