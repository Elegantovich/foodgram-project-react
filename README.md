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
  build_and_push_to_docker_hub:
    name: Push Docker image to Docker Hub
    runs-on: ubuntu-latest
    needs: tests
    steps:
      - name: Check out the repo
        uses: actions/checkout@v2 
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v1 
      - name: Login to Docker 
        uses: docker/login-action@v1 
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - name: Push to Docker Hub
        uses: docker/build-push-action@v2 
        with:
          push: true
          tags: elegantovich/foodback:v3.0
          file: backend/Dockerfile 
  
  