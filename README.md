# praktikum_new_diplom


"""  backend:
    image: elegantovich/foodback:v1.0
    restart: always
    depends_on:
      - db
    volumes:
      - static_value:/app/backend/staticfiles/
      - media_value:/app/backend/media/
    env_file:
      - ./.env"""


        db:
    env_file:
      - .env
    image: postgres:13.0-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    restart: always