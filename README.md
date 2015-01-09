##Query for a package/binary across Linux distros

* Needs docker up and running on the host

  On Fedora 20/21:

  ```
  # yum install docker-io
  # systemctl enable docker
  # systemctl start docker
  ```

* Uses docker-py

  On Fedora 20/21:

  ```
  # yum install python-docker-py
  ```

Examples:

```
$ python findpkg.py fedora:21 --package flask

============================== N/S matched: flask ==============================
python-flask-assets.noarch : Asset management for flask
python-flask-lastuser.noarch : Flask extension for LastUser
python-flask-script.noarch : Scripting support for Flask
python-sphinx-theme-flask.noarch : Sphinx Themes for Flask related projects and
                                 : Flask itself	 

..
```

```
> python findpkg.py ubuntu:latest --package flask
python-flask - micro web framework based on Werkzeug, Jinja2 and good intentions
python-flask-doc - documentation for Flask micro web framework

```
