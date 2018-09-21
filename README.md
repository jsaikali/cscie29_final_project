# Pset 2

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Pset 2](#pset-2)
  - [Problems (80 points)](#problems-80-points)
    - [Including pset_utils (10 points)](#including-pset_utils-10-points)
      - [Create a Github API token](#create-a-github-api-token)
    - [Feedback (10 points)](#feedback-10-points)
      - [How many hours did this assignment take?  Too hard/easy/just right? (2 points)](#how-many-hours-did-this-assignment-take--too-hardeasyjust-right-2-points)
      - [What did you find interesting? Challenging? Tedious? (8 points)](#what-did-you-find-interesting-challenging-tedious-8-points)
  - [Python Quality (10 points)](#python-quality-10-points)
  - [Git History (10 points)](#git-history-10-points)
  - [Total Grade](#total-grade)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Problems (80 points)

Before you create a local repo for this pset, skim through the problems and
decide how much of the work to include in your cookiecutter template first or
`pset_utils`.  Justify each decision.

Initiate a new local project folder using your cookiecutter repo, then manually
link to this remote origin as you did last time.  

### Including pset_utils (20 points)

Normally, we can pip/pipenv install straight from github to any Docker image or
Travis build.  However, we have a few hoops to jump through since `pset_utils`
is a private repo and we're not managing all of the deploy keys.  Inside a
company with a private VPN/version control/build system, best practice is just
to make everything publicly readable behind the VPN and not deal with deploy
authentication.

We have a few choices:

1. Create a deploy/user key for SSH.  This is preferred, but is a bit trickier
   to manage, especially on windows.
2. Hard code your git username/password into your dockerfile (no, we are not
   going to do that!)
3. Provide an API token through the environment.  This will allow us to clone
   via https without altering our Pipfile.  This option should be the easiest
   for this class.

You can decide how to capture this process in your cookiecutter repo.  
Technically, it would be poor form to automatically install a package you may
not need, but that is ok for this course.  You can also just capture the token
aspects without preinstalling pset_utils.  Document your decisions here.

#### Docker/pipenv prep

We took a shortcut last time by installing our pipenv into the system python
inside the Docker container.  This will cause some small issues later on, so
we can easily fix that by removing the `--system` flag in the last line of our
Dockerfile, so it reads:

```docker
RUN pipenv install --dev
```

Note that we now have to 'enter' the pipenv to use it.  We can do so easily
by modifying drun_app like so:

```bash
docker-compose run app pipenv run "$@"
```

#### Create a Github API token

See Travis docs
[here](https://docs.travis-ci.com/user/private-dependencies/#api-token). Note:
To access personal tokens, on the GitHub Applications page, you need to click
Developer Settings, or directly navigate
[here](https://github.com/settings/tokens).

DO NOT SHARE THIS TOKEN WITH ANYONE.  It gives access to all your github repos.
If it becomes compromised, delete it from github and generate a new one.  You
will be uploading this token to Travis, but it is private only to you.

Add the following lines to your Dockerfile, just below the `FROM` line:
```docker
ARG CI_USER_TOKEN
RUN echo "machine github.com\n  login $CI_USER_TOKEN\n" >~/.netrc
```

And modify the build section in your `docker-compose.yml`:
```
build:
  context: .
  args:
    - CI_USER_TOKEN=${CI_USER_TOKEN}
```

You then need to set `CI_USER_TOKEN` as an environment variable, either in your
`~/.bashrc` or `~/.bash_profile` on Mac/Linux, or create a
[dotenv](https://docs.docker.com/compose/env-file/) file in the project
directory (you ***must*** add files like this to your `.gitignore`), or
similarly with a [docker-compose
override](https://docs.docker.com/compose/extends/#multiple-compose-files)

You must then add the variable to the Travis environment as well; you can do
that via navigating to the settings, eg
https://travis-ci.com/csci-e-29/your_repo/settings, via the [Travis
CLI](https://github.com/travis-ci/travis.rb), or encrypting into the
`.travis.yml` as instructed on the first Travis link above.  The token should
NOT be committed to your repo in plain text anywhere.

You can then install your pset_utils.  Use the template below, substituting
master for a tag if you'd like:

```bash
./drun_app pipenv install -e git+https://github.com/csci-e-29/your_repo@master#egg=pset_utils
```

Upgrade as necessary when you improve your pset_utils

#### Including the utils tests

In your `setup.cfg`, update the `addopts` section to include `--pyargs`.  At
this point, after building the docker image, `pytest pset_utils` should run all
the tests in your utils package!

You can run them by default if you like, by adding `pset_utils` to `testpaths`
in the config file.

Otherwise, you should update your `.travis.yml` to explicitly run them.  You
can do so in the same test stage, or you could create a separate test stage
just to test your utils.  Normally, the latter is preferred - it gives nice
isolation.  However, it will require travis to rebuild your docker image, which
is suboptimal.

### Feedback (10 points)

#### How many hours did this assignment take?  Too hard/easy/just right? (2 points)

#### What did you find interesting? Challenging? Tedious? (8 points)

## Python Quality (10 points)
Notes from TA may go here

## Git History (10 points)
Notes from TA may go here

## Total Grade
Notes from TA may go here
