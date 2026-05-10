.. MOOD documentation master file, created by
   sphinx-quickstart on Sun May 10 00:06:51 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MOOD documentation
==================

MOOD is a multiplayer MUD game with cowsay monsters.

The project contains an asynchronous server and command-line clients.
Players can move around the field, add monsters, attack monsters, send
messages to all connected players and meet wandering monsters.

Run server
----------

.. code-block:: console

   python -m mood.server

Run client
----------

.. code-block:: console

   python -m mood.client username

Main commands
-------------

.. code-block:: text

   up
   down
   left
   right
   addmon dragon hp 30 hello "I am dragon" coords 1 0
   attack dragon with sword
   sayall hello
   quit

Technical documentation
-----------------------

.. toctree::
   :maxdepth: 2

   API
