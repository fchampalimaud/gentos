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


## Configuration

```
ACCOUNT_ALLOW_REGISTRATION (=True)
```


## Notes

...


## Credits

<div>Icons made by <a href="https://www.freepik.com/" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/"                 title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"                 title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>
