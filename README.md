# praktikum_new_diplom


  tests: 
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.7

    - name: Install dependencies
      run: | 
        python -m pip install --upgrade pip 
        pip install flake8 pep8-naming flake8-broken-line flake8-return flake8-isort
        pip install -r backend/requirements.txt 
    - name: Test with flake8
      run: |
        python -m flake8 