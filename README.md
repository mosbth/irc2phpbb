Marvin, an IRC/discord bot
==================

[![Build Status GitHub Actions](https://github.com/mosbth/irc2phpbb/actions/workflows/ci.yml/badge.svg)](https://github.com/mosbth/irc2phpbb/actions)
[![Build Status Scrutinizer](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/badges/build.png?b=master)](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/build-status/master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/?branch=master)
[![Code Coverage](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/badges/coverage.png?b=master)](https://scrutinizer-ci.com/g/mosbth/irc2phpbb/?branch=master)
=======

Marvin was originally an IRC bot (now also supporting discord) that responds to basic questions and provides guidance in the life of anyone involved in any [dbwebb](https://www.dbwebb.se) courses. 


Contribute
--------------------------

Before you actually start contributing, create an issue and discuss what you want to do. This is just to avoid that your PR will be denied for some random reason. 


This project uses [`uv`](https://github.com/astral-sh/uv) to manage dependencies and tools. Refer their [documentation](https://docs.astral.sh/uv/getting-started/) for instructions how to install it and getting started.


Running tests and code coverage
--------------------------

Run the unittests.

```bash
uv run pytest
```

Run code coverage and report results in terminal.

```bash
uv run pytest --cov=irc2phpbb
```

Run pylint on both production code and the tests.
```bash
uv run pylint irc2phpbb
uv run pylint tests
```

Run code coverage and create an html report. An html report of the code coverage is generated in `htmlcov/index.html`. [Other report formats](https://pytest-cov.readthedocs.io/en/latest/reporting.html) are also supported. If you generate other formats, take care not to commit them to the repository.
```bash
uv run pytest --cov=irc2phpbb --cov-report=html
```

Execute marvin in docker
--------------------------
The easiest way to run marvin in a *real* setting is to run it in IRC mode, as that doesn't require any registration with discord services.


Build the python package and the docker image, then start marvin as a container in the background.
```bash
uv build
docker compose build
docker compose up -d marvin
```

Now you can connect to `localhost` with any IRC client of your choice, or you can follow the instructions below to run [irssi](https://irssi.org/) in a [container](https://hub.docker.com/_/irssi).

```bash
docker compose run --rm irssi
```
You should be automatically connected to the server and join the `#marvin` channel.


When you are done, you can shut down all the containers.
```bash
docker compose down
```

API documentation 
--------------------------

The code and API documentation is generated using [pdoc](https://pdoc.dev/).

```bash
uv run pdoc --output-dir=docs/pdoc irc2phpbb
```
The docs are saved at `docs/pdoc` and can be [viewed online](https://mosbth.github.io/irc2phpbb/pdoc/).



History
--------------------------
Marvin started out as a single irc bot script, reading incoming entries from a directory
that external scripts (a PHP-based forum aggregator, since retired) could drop messages
into for posting to the channel. It's since been restructured into the `irc2phpbb` Python
package installed and run through `uv`, as described above.

The basic code is from: http://osix.net/modules/article/?id=780 and 
http://oreilly.com/pub/h/1968. From there its further developed and customized to fit the target
forum and target irc-channel.

The rfc for the irc protocol is quite helpful: http://www.irchelp.org/irchelp/rfc/


Customized for dbwebb.se
----------------------------

The bot was initially created for use in irc://irc.bsnet.se/#db-o-webb which is an irc channel for 
teaching & learning programming and web technologies.

Years later it was further developed to work within Discord as a bot, still in a teaching and learning environment.

This means that the code contains some settings to work in that environment and can therefore
not just be cloned and installed. Modifications are needed. The script may anyhow be useful 
as a study object for those in need of similar functionality.



 .   
..:  Copyright 2011-2026 by Mikael Roos (mos@bth.se)
