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

# Usage

This API primarily allows one to determine the eligible households of a specific grant.

As part of the requirements, the following are the five of the fictitious grants and how its eligible households.
To better illustrate their usage, the examples provided are based on the sample dataset `sample.json`.

<details>
<summary><b>View Full Sample Dataset</b></summary>

```jsonc
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
    },
    {
        "id": 2,
        "housing_type": "HDB",
        "members": [
            {
                "id": 2,
                "name": "John Doe",
                "gender": "Male",
                "marital_status": "Married",
                "spouse": "Mary Doe",
                "occupation_type": "Employed",
                "annual_income": 88000,
                "dob": "1980-01-01",
                "household": 2
            },
            {
                "id": 3,
                "name": "Mary Doe",
                "gender": "Female",
                "marital_status": "Married",
                "spouse": "John Doe",
                "occupation_type": "Employed",
                "annual_income": 88000,
                "dob": "2010-01-01",
                "household": 2
            }
        ]
    },
    {
        "id": 3,
        "housing_type": "HDB",
        "members": [
            {
                "id": 4,
                "name": "Tan Ah Kow",
                "gender": "Male",
                "marital_status": "Single",
                "spouse": null,
                "occupation_type": "Employed",
                "annual_income": 10000,
                "dob": "1960-01-01",
                "household": 3
            }
        ]
    },
    {
        "id": 4,
        "housing_type": "HDB",
        "members": [
            {
                "id": 5,
                "name": "Linus Torvalds",
                "gender": "Male",
                "marital_status": "Single",
                "spouse": null,
                "occupation_type": "Employed",
                "annual_income": 200000,
                "dob": "2019-01-01",
                "household": 4
            }
        ]
    }
]
```

</details>

## 1. Student Encouragement Bonus

The conditions of the grant qualifies:
- Households with children of less than 16 years old
- Household income of less than $150,000

In order to filter recipients, we can use the `max_age` and `max_income` query parameters.
The API request will thus look like: `GET /households/?max_age=16&max_income=150000`

<details>
<summary><b>See Example</b></summary>

```sh
curl '127.0.0.1:8000/households/?max_age=16&max_income=150000' \
    -H 'Accept: application/json; indent=4' \
    -X GET
```
```jsonc
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
                "annual_income": 10000,         // max_income=150000
                "dob": "2010-01-01",            // max_age=16
                "household": 1
            }
        ]
    }
]
```

</details>

## 2. Family Togetherness Scheme

The conditions of the grant qualifies:
- Households with husband & wife
- Has child(ren) younger than 18 years old

In order to filter recipients, we can use the `with_spouse` and `max_age` query parameters.
The API request will thus look like: `GET /households/?with_spouse=true&max_age=18`

<details>
<summary><b>See Example</b></summary>

```sh
curl '127.0.0.1:8000/households/?with_spouse=true&max_age=18' \
    -H 'Accept: application/json; indent=4' \
    -X GET
```
```jsonc
[
    {
        "id": 2,
        "housing_type": "HDB",
        "members": [
            {
                "id": 2,
                "name": "John Doe",
                "gender": "Male",
                "marital_status": "Married",
                "spouse": "Mary Doe",           // with_spouse=true
                "occupation_type": "Employed",
                "annual_income": 88000,
                "dob": "1980-01-01",
                "household": 2
            },
            {
                "id": 3,
                "name": "Mary Doe",
                "gender": "Female",
                "marital_status": "Married",
                "spouse": "John Doe",           // with_spouse=true
                "occupation_type": "Employed",
                "annual_income": 88000,
                "dob": "2010-01-01",            // max_age=18
                "household": 2
            }
        ]
    }
]
```

</details>

## 3. Elder Bonus

The conditions of the grant qualifies:
- HDB household with family members above the age of 50

In order to filter recipients, we can use the `housing_type` and `min_age` query parameters.
The API request will thus look like: `GET /households/?housing_type=hdb&min_age=50`

<details>
<summary><b>See Example</b></summary>

```sh
curl '127.0.0.1:8000/households/?housing_type=hdb&min_age=50' \
    -H 'Accept: application/json; indent=4' \
    -X GET
```
```jsonc
[
    {
        "id": 3,
        "housing_type": "HDB",                  // housing_type=hdb
        "members": [
            {
                "id": 4,
                "name": "Tan Ah Kow",
                "gender": "Male",
                "marital_status": "Single",
                "spouse": null,
                "occupation_type": "Employed",
                "annual_income": 10000,
                "dob": "1960-01-01",            // min_age=50
                "household": 3
            }
        ]
    }
]
```

</details>

## 4. Baby Sunshine Grant

The conditions of the grant qualifies:
- Household with young children younger than 5

In order to filter recipients, we can use the `max_age` query parameter.
The API request will thus look like: `GET /households/?max_age=5`

<details>
<summary><b>See Example</b></summary>

```sh
curl '127.0.0.1:8000/households/?max_age=5' \
    -H 'Accept: application/json; indent=4' \
    -X GET
```
```jsonc
[
    {
        "id": 4,
        "housing_type": "HDB",
        "members": [
            {
                "id": 5,
                "name": "Linus Torvalds",
                "gender": "Male",
                "marital_status": "Single",
                "spouse": null,
                "occupation_type": "Employed",
                "annual_income": 200000,
                "dob": "2019-01-01",            // max_age=5
                "household": 4
            }
        ]
    }
]
```

</details>

## 5. YOLO GST Grant

The conditions of the grant qualifies:
- HDB households with annual income of less than $100,000

In order to filter recipients, we can use the `housing_type` and `max_income` query parameters.
The API request will thus look like: `GET /households/?housing_type=hdb&max_income=100000`

<details>
<summary><b>See Example</b></summary>

```sh
curl '127.0.0.1:8000/households/?housing_type=hdb&max_income=100000' \
    -H 'Accept: application/json; indent=4' \
    -X GET
```
```jsonc
[
    {
        "id": 3,
        "housing_type": "HDB",                  // housing_type=hdb
        "members": [
            {
                "id": 4,
                "name": "Tan Ah Kow",
                "gender": "Male",
                "marital_status": "Single",
                "spouse": null,
                "occupation_type": "Employed",
                "annual_income": 10000,         // max_income=100000
                "dob": "1960-01-01",
                "household": 3
            }
        ]
    }
]
```

</details>

# Endpoints

### `POST /households/`

This endpoint creates an instance of the Household resource.

<details>
<summary><b>See Example</b></summary>

```sh
curl 127.0.0.1:8000/households/ \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json; indent=4' \
    -X POST \
    -d '{"housing_type":"Landed"}'
```
```jsonc
{
    "id": 1,
    "housing_type": "Landed",
    "members": []
}
```

</details>

### `POST /households/<id>/add_member/`

This endpoint appends FamilyMember instance to a specific Household instance.

**Note:** Currently, spousal relations can only be set on the second spouse. To illustrate, if Paul (in the example below) were to put Alice as his spouse, it will not work because Alice does not exist in the database. However, if Paul was created and Alice adds Paul as her spouse, both spouses will have their `member.spouse` field updated to reflect each other.

<details>
<summary><b>See Example</b></summary>

```sh
curl 127.0.0.1:8000/households/1/add_member/ \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json; indent=4' \
    -X POST \
    -d '{"name":"Paul Tan","gender":"Male","marital_status":"Single","spouse":null,"occupation_type":"Employed","annual_income":10000,"dob":"2010-01-01"}'
```
```jsonc
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
```

</details>

### `GET /households/`

This endpoint lists all households and its associated members.

<details>
<summary><b>See Example</b></summary>

```sh
curl 127.0.0.1:8000/households/ \
    -H 'Accept: application/json; indent=4' \
    -X GET
```
```jsonc
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

</details>

### `GET /households/<id>/`

This endpoint shows the details of a household and its related members.

<details>
<summary><b>See Example</b></summary>

```sh
curl 127.0.0.1:8000/households/1/ \
    -H 'Accept: application/json; indent=4' \
    -X GET
```
```jsonc
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
```

</details>

### `DELETE /households/<id>/`

This endpoint deletes a household and its related members.

<details>
<summary><b>See Example</b></summary>

```sh
curl 127.0.0.1:8000/households/1/ \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json; indent=4' \
    -X DELETE
```

_NOTE: This endpoint has no API response: `HTTP 204 NO CONTENT`_

</details>

### `DELETE /households/<id>/remove_member`

This endpoint deletes a member from its associated household.

<details>
<summary><b>See Example</b></summary>

```sh
curl 127.0.0.1:8000/households/1/remove_member/ \
    -H 'Content-Type: application/json' \
    -H 'Accept: application/json; indent=4' \
    -X DELETE \
    -d '{"name":"Paul Tan","gender":"Male","marital_status":"Single","spouse":null,"occupation_type":"Employed","annual_income":10000,"dob":"2010-01-01"}'
```

_NOTE: This endpoint has no API response: `HTTP 204 NO CONTENT`_

</details>

# Notes

This section highlights about the design assumptions, motivations, limitations, etc.

**Monogamy marriages only**

To make things easy, let us pretend that you can only be married to one person at any one point in time.

**Spouse field available in all endpoints**

In the task requirements, it is noted that the `spouse` field is left out for the `GET /households/<id>` endpoint.
This seems to be a deviation from all other endpoints and it does not seem to have a good justification why this was the case,
thus it shall be assumed that the `spouse` field was intended to be included in all endpoints.

**Family names are unique**

Obviously, this is not a practical assumption but this will make it much easier to interact with the API without dealing with all the primary keys.
By making this assertion, all `FamilyMember` instances can be referred to by their names because they are unique, e.g. Bob can add "Alice" as it spouse
without knowing her primary key. Unfortunately though, you will not be able to create a user with the same name.
