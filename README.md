# Synchornised clipboard within all possible devices

The idea is to create a webservice, that would probably be a stack with all the clipped values of the user and be called to stack when Ctrl+C is pressed and peeked when Ctrl+C is. Could be parametrized to pop when Ctrl+Ced. Hence are needed:

- A client for all devices, that would be on observer on the Ctrl+C/Ctrl+V commands.
- A server, that would host the stack for each user and stack/peek or pop on the notification event.
- A database for the users accounts and stacks.

## Client

Could use python and the [PyClip](https://pypi.org/project/pyclip/) and/or [Pillow](https://pypi.org/project/Pillow/) libraries. Just have a quick GUI to login the user account and start the listener deamon and a few settings (peek/pop; shortcut to use instead of Ctrl+C/Ctrl+V). Maybe in the futures adding a way to view the clipboard history ?

## Server

Python would still work just fine, probably with a docker image of django or something of the sort running the observer and the user's stack via database's calls.

## Database

Docker container with [MariaDB](https://hub.docker.com/_/mariadb/) I think would be nice ? Maybe [Postgres](https://hub.docker.com/_/postgres%20%20/) if it works better. Just need something quick anyway since there would only be 2 tables:

1. User
   1. ID
   2. Username
   3. Password (hash)
   4. Membership
2. Clipboard
   1. Clip_stamp
   2. #User.ID
   3. Clip_value

### Update 12/02/23

Keeping the docker container idea, but seeing the amount of possible data stored in the database, switching for a NoSQL solution. Picking [MongoDB](https://pythongeeks.org/python-nosql-database/) because it looks the most used and python has a direct connecter to it.
