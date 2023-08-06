py3adf
======

`py3adf` is a port of David Boddie's `ADF2INF` ADFS image reading tool and its
supporting `ADFSlib` library module. The original versions can be found,
alongside many other nice things, in the [Acorn-Format-Tools][] repository.

The primary goal of this fork is to provide a version of `ADF2INF` that runs on
Python 3.

Additional goals include:

 - Minor enhancements for `ADF2INF`.
 - `pip` packaging, with support for running `py3adf.py` easily on Windows.
 - Tasteful use of new language features.
 - Increased type safety with type hints and explicit casts (where essential).
 - Automated acceptance tests.

[Acorn-Format-Tools]: https://github.com/dboddie/Acorn-Format-Tools

Installing
----------
```
pip install py3adf
```

Running
-------
The pip package installs `py3adf.py` as a runnable script, so just:
```
py3adf.py
```

Authors
-------

* David Boddie <david@boddie.org.uk>
* Toby McLaughlin <toby@jarpy.net>

License
-------

py3adf is licensed under the GNU General Public License version 3 or later:

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.