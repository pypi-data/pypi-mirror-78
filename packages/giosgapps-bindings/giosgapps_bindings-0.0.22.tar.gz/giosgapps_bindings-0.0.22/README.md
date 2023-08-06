# giosgapps-bindings
![Modules](modules.png)  

## Changelog
* TODO when 1.0.0 released

## Publishing
* Finalize code changes and push/merge them to git  
* Change version and download_url version in setup.py, and push/merge that  
* Create a git release with that version  
* (Download twine, `pip3 install twine`)  
* Run `python3 setup.py sdist` to create source distribution  
* Run `twine upload dist/*` to upload source distribution to PyPI  
* Enter prompted username and password, from https://github.com/giosg/dev-pwdb-shared  
