# cogento-client

[Congento](https://congento.org/)


## Development

Clone this repository and install all dependencies.

```bash
git clone git@github.com:fchampalimaud/congento-client.git
git pull --recurse-submodules
git submodule update --init --recursive

pipenv sync --dev
```

Configure the development environment from the example provided

```bash
cp .env.example .env
```

Setup MySQL database schema `congento` and apply the migrations.

```bash
python manage.py migrate
```

Use a local running instance of [MailHog](https://github.com/mailhog/MailHog)
to test e-mails.


## Deployment

...


## Notes

...
