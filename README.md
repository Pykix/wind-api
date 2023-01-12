# windforlife-Ludovic-Py

## Getting started

---

First, at the root of the project, duplicate or rename the file ```.env.dev``` in ```.env```

To launch the project, in your terminal, run the following command to build and start the Docker containers:

```sh
docker-compose up -d --build
```

When the containers running, make all the migration:

```sh
docker-compose exec api python manage.py migrate
```

Then load the json file ```data.json``` it contain all the data necessary to test the project:

```sh
docker-compose exec api python manage.py loaddata data.json
```

## Authentication

---

To use the API you need to create an account to get the auth token, however an account is already available if you want:

You need a basic auth (username, password) to get the token, so there is a cURL request to get it:

```cURL
curl -X POST \
  'http://localhost:8000/auth-token/' \
  --header 'Content-Type: application/json' \
  --data-raw '{
  "username": "root",
  "password": "password"
}'
```

And the return of this request, save the token because you need it for **every following requests**:

```json
{
  "token": "23debdb9888b1561785d572a22cee52079feaee1"
}
```

## Consume API

---

Once you have the token you can consume the endpoints of the API

*here is one exemple, if you use Thunder-Client for VScode you can import all endpoints collection from the file **thunder-collection_Wind_For_Life.json** (I dont know if work for Postman...)*

To list all Anemometers:

```cURL
curl -X GET \
  'http://localhost:8000/api/anemometers/' \
  --header 'Authorization: Token 23debdb9888b1561785d572a22cee52079feaee1'
```

And you get a response like this:

```json
[
  {
    "id": 1,
    "name": "Rue Rousseau",
    "coordinates": "SRID=4326;POINT (-12.2 2.34)",
    "tags": [
      "Perpignan"
    ],
    "daily_average": 4.0,
    "weekly_average": 7.833333333333333
  },
  {
    "id": 2,
    "name": "Avenue Bruges",
    "coordinates": "SRID=4326;POINT (-12.1 2.34)",
    "tags": [
      "Paris"
    ],
    "daily_average": null,
    "weekly_average": null
  }
  ...
```
