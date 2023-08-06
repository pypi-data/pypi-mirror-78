`Tutor <https://docs.tutor.overhang.io>`__ Long Term Support (LTS) plugin
=========================================================================

This is a plugin for `Tutor LTS <https://overhang.io/tutor/lts>`__ customers. Running this plugin requires a valid license key. An LTS subscription grants unlimited online Tutor and Open edX support, and access to a selection of premium plugins.


Installation
------------

The Tutor LTS plugin requires a working installation of Tutor. To install Tutor, please check the `official installation instructions <https://docs.tutor.overhang.io/install.html>`__.

Then, install and enable the plugin with::

    pip install tutor-lts
    tutor plugins enable lts

Quickstart
----------

Obtain a Tutor LTS license at https://overhang.io/tutor/lts. Then, find your license ID and run::
    
    tutor lts license save <yourlicenseid>

Your license can only be used on a limited number of computers. Any activated computer can be deactivated at any time, but beware: you will not be able to re-activate it later.

To activate your license, run::
    
    tutor lts users activate

You can then install Tutor LTS plugins by running ``tutor lts install``. For instance::
    
    tutor lts install tutor-monitor

The plugin should now appear in the plugin list::
    
    tutor plugins list

Note that to start using LTS plugins, you will have to install Tutor from source, and not by downloading the Tutor binary. You will also need to install ``pip`` for Python 3+. To do so, follow the `official instructions <https://pip.pypa.io/en/stable/installing/>`__.

Once a plugin has been installed, you need to enable it to start using it. For instance::
    
    tutor plugins enable monitor
    tutor local quickstart

How-to guides
-------------

Storing the Tutor LTS license in a different location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, the license file is stored in the ``~/.config/tutorlts/license.json`` file on Linux, and ``~/Library/Application Support/tutorlts/license.json`` on Mac OS. To specify a different location, use the ``--license-path`` option::
    
    tutor lts --license-path=/your/custom/path/license.json license ...
    
Alternatively, define the following environment variable::
    
    export TUTOR_LTS_LICENSE_PATH=/your/custom/path/license.json
    tutor lts license ...

Managing ephemeral machines
---------------------------

You may want to deactivate the license associated to a production machine that was terminated. This is frequent in cloud environments. It is possible to do so by setting specific properties to this machine. For instance, on the production machine, before it was terminated, run::
    
    tutor lts users activate --name=myinstance

Then, after it was terminated, fetch its id from another machine with::
    
    tutor lts users list --name=myinstance

Use this ID to deactivate it::

    tutor lts users deactivate --id=<myinstanceid>

Or in a single command, with no confirmation prompt::
    
    tutor lts users deactivate --yes \
        --id=$(tutor lts users list --name=myinstance --format="{id}")

License
-------

All rights reserved to SASU NULI NULI.