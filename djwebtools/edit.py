from flask import request, flash, url_for, render_template
from werkzeug.utils import redirect
from . import djpage, form_factory
from . import _registered_relations
import wtforms as wtf


@djpage.route('/enter/<relname>', methods=['GET', 'POST'], defaults={'target': 'index'})
@djpage.route('/enter/<relname>/<target>', methods=['GET', 'POST'])
def enter(relname, target):
    enter_form = form_factory(relname)(request.form)
    if request.method == 'POST':
        if request.form['submit'] == 'Submit':
            if enter_form.validate():
                enter_form.insert()
                flash("Data has been entered in %s" % (enter_form._rel.__class__.__name__,))
                return redirect(url_for(target))
            return render_template('datajoint_form.html', form=enter_form)
        return redirect(url_for(target))
    else:
        for k, v in request.args.items():
            try:
                setattr(getattr(enter_form, k), 'data', v)
            except:
                pass
    return render_template('datajoint_form.html', form=enter_form,
                           target=url_for('.enter', relname=relname, target=target))


def request_args_as_key():
    key = dict(request.args.items())

    for k in list(key.keys()):
        if key[k] == 'None':
            del key[k]
            continue

        # need to do it this way, since numpy.float32 converts 4.7 into 4.69999 which
        # will cause an error in the restriction below.
        try:
            key[k] = int(key[k])
            continue
        except ValueError:
            pass

        try:
            key[k] = float(key[k])
            continue
        except ValueError:
            pass
    return key


@djpage.route('/edit/<relname>', methods=['GET', 'POST'])
def edit(relname):
    if request.method == 'POST':
        edit_form = form_factory(relname)(request.form)
        if request.form['submit'] == 'Submit':
            if edit_form.validate():
                edit_form.insert(replace=True)
                flash("Data has been replaced in %s" % (edit_form._rel.__class__.__name__,))

                return redirect(edit_form.REFERRER.data)
            return render_template('datajoint_form.html', form=edit_form)
        return redirect(edit_form.REFERRER.data)
    else:
        rel = _registered_relations[relname]
        key = request_args_as_key()
        args = (rel & key).fetch1()
        edit_form = form_factory(relname)(REFERRER=request.referrer, **args)

    return render_template('datajoint_form.html', form=edit_form,
                           target=url_for('.edit', relname=relname))


@djpage.app_template_global('get_edit_url')
def get_edit_url(key, relname):
    get_str = '?' + '&'.join(["%s=%s" % (k, str(v)) for k, v in key.items()])
    return url_for('.edit', relname=relname) + get_str
