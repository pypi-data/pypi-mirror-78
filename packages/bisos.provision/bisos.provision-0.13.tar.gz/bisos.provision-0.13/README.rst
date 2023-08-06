=======================
bisos.provision Scripts
=======================

.. contents::
   :depth: 3
..

Overview
========

Bash scripts (Interactive Command Modules – ICM) for provisionping BISOS
(ByStar Internet Services OS) software profiles on a virgin Linux
distro. Or for creating fully automated KVM guests that are ByStar
Platforms.

Running **bx2Genesis.sh** will go through a complete ByStar Platform
installation on the local host.

Running **bxProvisionGuest.sh** will create a fully automated KVM Guest
ByStar Platform.

Support
=======

| For support, criticism, comments and questions; please contact the
  author/maintainer
| `Mohsen Banan <http://mohsen.1.banan.byname.net>`__ at:
  http://mohsen.1.banan.byname.net/contact

Documentation
=============

Part of ByStar Digital Ecosystem http://www.by-star.net.

This module’s primary documentation is in
http://www.by-star.net/PLPC/180047

Installation
============

::

    sudo pip install bisos.provision

Usage
=====

bx2Genesis.sh
-------------

On a virgin BxP-Distro, run “sudo /usr/local/bin/bx2Genesis.sh” and you
will end up with a Generic BISOS Platform. Which you can then apply to a
desired bxpCharacter.

bxProvisionGuest
----------------

On any Linux machine that has kvm in its distro, run
/usr/local/bin/bxProvisionGuest.sh and you will end up with a guest at
the specified desired level (as ByStar Platforms).

“./bin/bxHostGenGuestVagrant”
-----------------------------

On any Linux Machine that has VirtualBox and Vagrant installed, run
bxHostGenGuestVagrant and based on params and args build a VM that
includes what is specified.

The Steps are as follows:

-  Create A VM

-  In the created VM as root:

   -  install python and pip

   -  install git

   -  pip install bisos.provision

   -  Run xxx to create user bxGenesis and add it to sudoers

-  In the created VM as bxGenesis run bisos.provision/bin/bxGenWithRepo

-  Login to the VM as bxGenesis

-  Run the post install script.

“./bin/bxGenWithRepo”
---------------------

Does the following:

-  Clone specified repo

-  From within that repo executes specified entry point with params and
   args. This typically involves creating an account
