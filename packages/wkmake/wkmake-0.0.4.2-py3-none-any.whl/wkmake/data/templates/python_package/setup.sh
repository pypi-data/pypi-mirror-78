rm -rf  dist/*.gz
rm -rf  dist/*.whl
rm -rf  build/*
rm -rf  {{pkg_name}}.egg-info/*
{{python_name or 'python3'}} setup.py sdist bdist_wheel
