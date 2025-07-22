Installation
============

Requirements
------------

- Python 3.8 or higher
- Robot Framework 4.0 or higher
- GPG/GnuPG installed on your system

System Dependencies
-------------------

The library requires GnuPG to be installed on your system:

**Ubuntu/Debian:**

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install gnupg

**CentOS/RHEL/Fedora:**

.. code-block:: bash

   sudo yum install gnupg2
   # or for newer versions:
   sudo dnf install gnupg2

**macOS:**

.. code-block:: bash

   brew install gnupg

**Windows:**

Download and install from: https://www.gnupg.org/download/

Installing the Library
----------------------

Install from PyPI
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install robotframework-pgp

Install from Source
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/robotframework/robotframework-pgp.git
   cd robotframework-pgp
   pip install -e .

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

For development, install with development dependencies:

.. code-block:: bash

   git clone https://github.com/robotframework/robotframework-pgp.git
   cd robotframework-pgp
   pip install -r requirements-dev.txt
   pip install -e .

Verifying Installation
----------------------

You can verify the installation by running:

.. code-block:: bash

   python -c "from RobotFrameworkPGP import RobotFrameworkPGP; print('Installation successful')"

Or create a simple Robot Framework test:

.. code-block:: robotframework

   *** Settings ***
   Library    RobotFrameworkPGP

   *** Test Cases ***
   Test Installation
       ${version}    Get GPG Version
       Log    GPG Version: ${version}

Configuration
-------------

The library will automatically create a temporary GPG home directory if none is specified. You can also specify a custom GPG home directory:

.. code-block:: robotframework

   *** Settings ***
   Library    RobotFrameworkPGP    gnupg_home=/path/to/gnupg

   *** Test Cases ***
   Use Custom GPG Home
       Set GPG Home Directory    /path/to/custom/gnupg