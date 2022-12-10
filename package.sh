VERSION_NUMBER=$1 # for example 0.1
GIT_TAG=v${VERSION_NUMBER}

sed -i "s/version='.*',/version='${VERSION_NUMBER}',/g" setup.py

git push
git tag -a ${GIT_TAG} -m "version ${GIT_TAG}"
git push origin ${GIT_TAG}

# build data dictionary
python tools/build_data.py

# build python module , upload to pypi
python setup.py sdist
twine upload dist/*