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