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

Clone this repository into the production machine and synchronize the submodules.

```bash
git clone --branch master --single-branch https://github.com/fchampalimaud/gentos.git
cd gentos
perl -i -p -e 's|git@(.*?):|https://\1/|g' .gitmodules
```

> **Note:** the `perl` script is required to change submodules URLs to `https://` schema.

Pull the latest modifications and update the submodules.

```bash
git pull --recurse-submodules
git submodule update --init --recursive
```

Configure environment variables in `.env`

```bash
cp .env.example .env
```

Launch the containers

```bash
docker-compose -f docker-compose.production.yml up --build -d
```

and create a superuser

```bash
docker-compose -f docker-compose.production.yml exec django pipenv run python manage.py createsuperuser
```

Log in to the `/admin` panel and configure

- [ ] Admin account and email
- [ ] Sites framework
- [ ] Social Apps


## Configuration

```
ACCOUNT_ALLOW_REGISTRATION (=True)
```


## Notes

...
