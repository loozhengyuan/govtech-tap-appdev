# Government Grant Disbursement API

![Main Workflow](https://github.com/loozhengyuan/govtech-tap-appdev/workflows/Main%20Workflow/badge.svg) [![codecov](https://codecov.io/gh/loozhengyuan/govtech-tap-appdev/branch/master/graph/badge.svg?token=DUHFG0bfko)](https://codecov.io/gh/loozhengyuan/govtech-tap-appdev)

This project is done in fulfillment for the assessment requirements of GovTech's Technology Associate Program.

## Getting Started

### Installing with Docker

If you do not already have Docker installed, you may refer to Docker's [installation instructions](https://docs.docker.com/install/) to get started.

First, pull the latest image from [Docker Hub](https://hub.docker.com/r/loozhengyuan/govtech-tap-appdev):

```sh
docker pull loozhengyuan/govtech-tap-appdev
```

Run the server by executing `docker run`:

```sh
docker run -it \
    -p 8000:8000
    -e SECRET_KEY=<YOUR_SECRET_KEY_HERE>
    loozhengyuan/govtech-tap-appdev
```

_NOTE: Make sure you generate a secret key and substitute `<YOUR_SECRET_KEY_HERE>` in the above._

### Installing from source

If you do not already have Git installed, you may refer to Github's [guide](https://help.github.com/en/github/getting-started-with-github/set-up-git).

Firstly, pull the contents of the repository into your environment:

```sh
git clone https://github.com/loozhengyuan/govtech-tap-appdev
cd govtech-tap-appdev
```

Next, install dependencies:

```sh
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Create database and run database migrations:

```sh
python manage.py migrate
```

With the database set up, we probably still need some initial data so we can get started right away. You can load these data fixtures from `initial.json` and `sample.json`.

```sh
python manage.py loaddata initial.json sample.json
```

Finally, execute the following commands to start running your server:

```sh
python manage.py runserver
```

## Endpoints

### `GET /households/`

This endpoint lists all households and its associated members.

Request:

```sh
curl 127.0.0.1:8000/households/ \
    -H 'Accept: application/json; indent=4' \
    -X GET
```

Response:

```json
[
    {
        "id": 1,
        "housing_type": "Landed",
        "members": [
            {
                "id": 1,
                "name": "Paul Tan",
                "gender": "Male",
                "marital_status": "Single",
                "spouse": null,
                "occupation_type": "Employed",
                "annual_income": 10000,
                "dob": "2010-01-01",
                "household": 1
            }
        ]
    }
]
```
