run:
	python manage.py runserver

run_local:
	python manage.py runserver 192.168.103:8000

shell:
	python manage.py shell_plus --print-sql

notebook_shell:
	python manage.py shell_plus --notebook

migrate:
	python manage.py migrate

makemigrations:
	python manage.py makemigrations

makedatamigration:
	python manage.py makemigrations --empty $(app)

clean_pyc:
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;

test:
	py.test -s --cov
	# py.test -s --cov --ds=settings.local_settings
	# py.test where_is_my_stuff/apps/users/tests/test_model.py::UserModelTestCase::test_create_user -s

html_test_cov:
	py.test --cov --cov-report=html
	# py.test --cov --cov-report=html --ds=settings.local_settings

flake8:
	flake8

celery:
	celery worker -A where_is_my_stuff -B

deploy_docs:
	mkdocs gh-deploy
	rm -rf _docs_html
