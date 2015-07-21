# djwebtools
Flask tools to write small web applications for datajoint.

**This is an alpha version**: Use with caution.

## Installation

Clone the repository and put into your shell

```sudo pip3 install -e djwebtools```

The ```-e``` will install it locally, you want to install it into the system.

## Minimal example

You need a running [datajoint](http://datajoint.github.io/) installation with a database server.

Assume you have a datajoint `Subject` in the file `myschema.py` that looks like this:

```python

import datajoint as dj
schema = dj.schema('mydbname', locals())


@schema
class Subject(dj.Manual):
    definition = """  # Basic information about animal subjects used in experiments
    subject_id   :int  #  unique subject id
    ---
    real_id            :varchar(40)  # real-world name. Omit if the same as subject_id
    species = "mouse"  :enum('mouse', 'monkey', 'human')
    date_of_birth      :date
    subject_notes      :varchar(4000)
    """

    contents = [
        [1551, '1551', 'mouse', '2015-04-01', 'genetically engineered super mouse'],
        [10, 'Curious George', 'monkey', '2008-06-30', ''],
        [1552, '1552', 'mouse', '2015-06-15', ''],
        [1553, '1553', 'mouse', '2016-07-01', '']]

    def prepare(self):
        self.insert(self.contents, ignore_errors=True)

```

The next step is to create a [Flask](http://flask.pocoo.org/) application with the following directory structure.

```
├── dj_local_conf.json
├── myserver.py
├── static
│   └── style.css
└── templates
    └── base.html

```



The file `base.html` could look like this

```html
<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>Subject Administration System</title>
    <link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
    {% block datajointhead%} {% endblock %}
</head>
<body>

<div class="main">
    {% block body%}

    {% endblock %}
</div>
</body>
</html>
```

Notice the `datajointhead` in the heading. `djwebtools` will place the custom `.css` file there. If you don't want that,
remove it. The file has to be named `base.html` since, the templates in `djwebtools` will extend it.

The file `myserver.py` could look like this

```python
from flask import Flask
import djwebtools as djw

app = Flask(__name__)
app.secret_key = # place a flask secret key here
app.register_blueprint(djw.djpage, url_prefix='/dj')



import atlab_commons
from myschema import Subject

djw.register(subject=Subject(), for_form=True)

if __name__ == '__main__':
    app.run(debug=True)

```

This file registeres the flask blueprint from `djwebtools` with your flask application. If you run it via:

```python3 myserver.py```

`djwebtools` will provide the following URLs

- http://127.0.0.1:5000/dj/display/subject
- http://127.0.0.1:5000/dj/enter/subject

It also provides a URL for editing, but that is better accessed from the display URL, since it needs a few GET parameters
to fetch the correct entry from the database.