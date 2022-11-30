# OneFin-Movie-Detail-Collector-v1.0.0

OneFin-Movie-Detail-Collector-v1.0.0 is a backend REST API application that can be paired with a frontend of your choice which can consume endpoints. All the APIs are developed to be authenticated with JWT and used in the form of cookies in httponly method.

It comes with the following functionalities:

1.  Get all the movie details from a third-party source
2. Store movies in collections of your choice
3. Get all the collection details along with the top 3 genres which are most stored by the user
4. Update the information for any collection that you have created along with the movies in it
5. Delete a collection of your choice
6. Get the request count of the server & reset it 


## Setup

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements.py present in the base folder.

```bash
$pip install -r requirements.txt

```
Now go ahead and create a database, once you are done with that we can configure the settings.py under the OneFin directory to make the connection.
## OneFin/settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<DB_NAME>',
        'USER': '<USERNAME>',
        'PASSWORD': '<PASSWORD>',
        'HOST': '<HOST>',
        'PORT': '<PORT>'
    }
}
```
Supported DB

* Mysql
* Postgres

Now migrate the required tables to the database

```bash
$python3 manage.py migrate

```
Now the tables are created and the connection is live, let's start the server

```bash
$python3 manage.py runserver

```
The server is live now !

## Usage
Once the server is live we are all set to test the collector APIs using POSTMAN, just fork the collection and start exploring all the APIs with its documentation. Postman also provides you all code snippets to integrate the requests in your desired system.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/21835276-b7228d01-f96a-42d1-a6bf-3c88b2795eb4?action=collection%2Ffork&collection-url=entityId%3D21835276-b7228d01-f96a-42d1-a6bf-3c88b2795eb4%26entityType%3Dcollection%26workspaceId%3D4d42ec1c-5267-45a5-8480-7285b575f56c)

The usage example is for localhost but it can also be deployed on a cloud host.
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Tests are yet to be developed 

