# praktikum_new_diplom


name: Yamdb workflow
on: [push]
jobs:

  tests:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.7'
    - name: Install dependencies
      run: | 
        python -m pip install --upgrade pip 
        pip install flake8 pep8-naming flake8-broken-line flake8-return flake8-isort
        pip install -r api_yamdb/requirements.txt 
    - name: Test with flake8 and django tests
      run: |
        python -m flake8
        pytest