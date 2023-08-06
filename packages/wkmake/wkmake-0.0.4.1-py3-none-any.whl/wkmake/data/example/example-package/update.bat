del "dist\*.gz" /f
del "dist\*.whl" /f
del "build\*" /r/f
del "{{pkg_name}}.egg-info\*" /r/f
{{python_name or 'python3'}} setup.py sdist bdist_wheel
{{python_name or 'python3'}} -m twine upload dist/*