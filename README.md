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

Oh no! We made a slight mistake last time with our `Dockerfile`.  According to
[this
post](https://stackoverflow.com/questions/46503947/how-to-get-pipenv-running-in-docker),
best practices indicate that we should only install the locked requirements
(`--ignore-pipfile`) and also enable the `--deploy` flag.  While we're editing,
let's add some of those `ENV` arguments linked in the
[template](https://github.com/wemake-services/wemake-django-template/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/docker/django/Dockerfile)
there:

```docker
ENV \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIPENV_HIDE_EMOJIS=true \
  PIPENV_COLORBLIND=true \
  PIPENV_NOSPIN=true \
  PYTHONPATH="/app:${PYTHONPATH}"

WORKDIR /build

...

RUN pipenv install --system --deploy --ignore-pipfile --dev
WORKDIR /app
```

Also note the new WORKDIR directive before we start copying files into the Docker
image, and the revert back to the app dir after we're done.  This will prevent
some issues between the editable repo installs when we're mounting the local
folder into /app when we're running.

Be sure to update this part in your cookiecutter!

#### Create a Github API token

See Travis docs
[here](https://docs.travis-ci.com/user/private-dependencies/#api-token). Note:
To access personal tokens, on the GitHub Applications page, you need to click
Developer Settings, or directly navigate
[here](https://github.com/settings/tokens).

DO NOT SHARE THIS TOKEN WITH ANYONE.  It gives access to all your github repos.
If it becomes compromised, delete it from github and generate a new one.  You
will be uploading this token to Travis, but it is private only to you.

For more reference on security, see [Travis Best
Practices](https://docs.travis-ci.com/user/best-practices-security/#recommendations-on-how-to-avoid-leaking-secrets-to-build-logs)
and [Removing Sensitive
Data](https://help.github.com/articles/removing-sensitive-data-from-a-repository/).

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
override](https://docs.docker.com/compose/extends/#multiple-compose-files).  Note
that environment variables can be tricky if you aren't familiar with how to use
them; the `.env` file may be the easiest approach, but will need to be copied
to each new project, since you can't commit it to your cookiecutter repo
(although, you could keep the file in your local cookiecutter repo, so long
as it is ignored by git!).

You must then add the variable to the Travis environment as well; you can do
that via navigating to the settings, eg
https://travis-ci.com/csci-e-29/your_repo/settings, via the [Travis
CLI](https://github.com/travis-ci/travis.rb), or encrypting into the
`.travis.yml` as instructed on the first Travis link above.  The token should
NOT be committed to your repo in plain text anywhere.  You could automate the
encryption via cookiecutter, but it would take a bit of experimentation with
your hooks - you would need to run something like `travis encrypt -r {{ owner
}}/{{ repo }} CI_USER_TOKEN=123 --add`.  You are not required to automate this
for the purpose of this pset!

#### Install the utils!

You can now install your `pset_utils` as below.  Note that the #egg part is
important, it is not a comment!

```bash
./drun_app pipenv install -e git+https://github.com/csci-e-29/pset_utils-you#egg=pset_utils
```

This will include the latest master commit (presumably tagged) and will be
automatically updated whenever you run `pipenv update`.  If you want to be more
specific about the version, you can use the `@v1.2.3` syntax when you install,
or add `ref='v1.2.3` to the specification in the `Pipfile`.  Leaving this to
automatically check out the latest master is easiest and a good reason to have
merge-only master releases!

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
