poetry-build-min-version:
	poetry version minor && poetry build

poetry-deploy-package:
	poetry publish