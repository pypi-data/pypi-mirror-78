kodexa-widget
===============================

A Jupyter Widget for Kodexa

Installation
------------

To install use pip:

    $ pip install kodexa_widget
    $ jupyter nbextension enable --py --sys-prefix kodexa_widget

To install for jupyterlab

    $ jupyter labextension install kodexa_widget

For a development installation (requires npm),

    $ git clone https://github.com/kodexa-ai/kodexa-widget.git
    $ cd kodexa-widget
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix kodexa_widget
    $ jupyter nbextension enable --py --sys-prefix kodexa_widget
    $ jupyter labextension install @jupyter-widgets/jupyterlab-manager
    $ jupyter labextension install js

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This takes a minute or so to get started, but then automatically rebuilds JupyterLab when your javascript changes.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.

