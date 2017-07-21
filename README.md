where_is_my_stuff_api
==============================

__Version:__ 0.0.0

Add a short project description here.

## Getting up and running

Minimum requirements: **pip, fabric & [postgres][install-postgres] with postgis**, setup is tested on Mac OSX only.

```
brew install postgres
[sudo] pip install fabric
```

[install-postgres]: http://www.gotealeaf.com/blog/how-to-install-postgresql-on-a-mac

In your terminal, type or copy-paste the following:

    git clone git@github.com:vladymyrgo/where_is_my_stuff_api.git; cd where_is_my_stuff_api; fab init

Go grab a cup of coffee, we bake your hot development machine.

Useful commands:

- `mkvirtualenv where_is_my_stuff --python=$(which python3)` - set up virtual environment using python 3
- `fab serve` - start [django server](http://localhost:8000/)
- `fab deploy_docs` - deploy docs to server
- `fab test` - run the test locally with ipdb
- `celery worker -A rs_exchange -B` - run celery worker for all queues
- `celery worker -A rs_exchange -Q my_queue` - run celery worker for specific queue

**NOTE:** Checkout `fabfile.py` for all the options available and what/how they do it.

Also make sure that your default OS version of python is **python 2** so that fab works, otherwise you'll have to do everything without fabric


## Deploying Project

The deployment are managed via travis, but for the first time you'll need to set the configuration values on each of the server.

Check out detailed server setup instruction [here](docs/backend/server_config.md).

General deployment guidelines [here](http://docs.byjakt.com/backend-development-standards/standards/deployment/)

## How to release where_is_my_stuff_api

Execute the following commands:

```
git checkout master
fab test
bumpversion release
bumpversion --no-tag patch # 'patch' can be replaced with 'minor' or 'major'
git push origin master
git push origin master --tags
git checkout qa
git rebase master
git push origin qa
```

## Project init using Fueled/django-init (python3)

**You won't have to do this for setting up this project!** However, this is a useful note on setting up future projects with python3 if setup fails due to a [virtualenv bug](https://github.com/PythonCharmers/python-future/issues/148):

    cookiecutter git@github.com:jakt/django-fullstack-init.git

If setup fails you'll have to start where it left off.

Drop the newly setup database:

    dropdb where_is_my_stuff

Initialize:

    cd where_is_my_stuff; fab init

## Contributing

Golden Rule:

> Anything in **master** is always **deployable**.

Avoid working on `master` branch, create a new branch with meaningful name, send pull request asap. Be vocal!

Refer to [CONTRIBUTING.md][contributing]

[contributing]: http://github.com/vladymyrgo/where_is_my_stuff_api/tree/master/CONTRIBUTING.md
