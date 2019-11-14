# gentos

Custom genetically modified organisms database developed to support the [Congento](https://congento.org/) network.


## Docker: configurations available

| Compose file | Usage |
| --- | --- |
| `docker-compose.yml` | Launch a development server |

## Development

Clone this repository and sync its submodules.

```bash
git clone git@github.com:fchampalimaud/gentos.git
git pull --recurse-submodules
git submodule update --init --recursive
```

Configure the development environment from the example provided

```bash
cp .env.example .env
```

Build the image and launch it. To create an admin user or run any command inside the container, see the examples below.

```bash
docker-compose build
docker-compose up
docker-compose exec django pipenv run python manage.py createsuperuser
```

You may also load a fixture with initial data:

```bash
docker-compose exec django pipenv run python manage.py loaddata initial_data
```

| Service | Address |
| --- | --- |
| Django | http://localhost:8000 |
| MailHog | http://localhost:8025 |


## Deployment

...


## Configuration

```
ACCOUNT_ALLOW_REGISTRATION (=True)
```


## Notes

...
