civis-jupyter-extensions
========================

.. image:: https://travis-ci.org/civisanalytics/civis-jupyter-extensions.svg?branch=master
    :target: https://travis-ci.org/civisanalytics/civis-jupyter-extensions

Tools for using the Civis Platform with Jupyter notebooks

Installation and Setup
----------------------

Run the following commands in a shell::

    pip install civis-jupyter-extensions
    jupyter nbextension install --py civis_jupyter_ext
    jupyter nbextension enable --py civis_jupyter_ext

In order to use the extensions, make sure to have your Civis Platform API key in
your local environment as `CIVIS_API_KEY`.

Magic Commands
--------------

To load the magic commands, use the following in ipython or a
Jupyter notebook::

    %load_ext civis_jupyter_ext

You can also autoload the magic commands every time a notebook is opened by
adding::

    c.InteractiveShellApp.extensions = ['civis_jupyter_ext']

to your ``~/.ipython/profile_default/ipython_config.py``.

SQL Queries
~~~~~~~~~~~

To get a table preview, use the cell magic like this::

    %%civisquery my-database
    select * from dummy.table limit 10;

To return a DataFrame for further processing, use the line magic like this::

    df = %civisquery my-database; select * from dummy.table;
