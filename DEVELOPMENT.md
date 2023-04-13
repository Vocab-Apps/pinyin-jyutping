## running tests
`pytest tests`
## test coverage
run tests and generate coverage report
```
coverage run -m pytest tests
coverage html
```
reset coverage report
```
coverage erase
```
start up http server:
```
python -m http.server --bind :: 8000
```