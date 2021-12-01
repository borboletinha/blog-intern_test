# TestBlog
## Project description
Backend trainee test assignment.
As part of the assignment, the following APIs for the blog have been implemented:
- user registration and user authentication using JWT;
- creation of posts by authorized users;
- viewing created posts by both authorized and unauthorized users;
- displaying a list of all registered users both in chronological (by registration date) and sorted by the number of posts order.

## Usage
Please kindly note that the secret key of the project and the database user password are deliberately excluded from the repository (SECRET_KEY and PASSWORD in testblog/settings.py).

All requirements are listed in the [separate file](https://github.com/borboletinha/blog-intern_test/blob/main/requirements.txt).

## Documentation
Please kindly note that for the project has been provided dynamic Swagger documentation. It could be found at the following link after running the project on your computer: http://127.0.0.1:8000/docs/.

Please also note that for authorization within the Swagger documentation, in the "value" field on the "Authorization" banner (upper right web-page corner), you should manually enter the prefix "Bearer" and then the valid access token.

Also [static documentation](https://github.com/borboletinha/blog-intern_test/blob/main/testblog_documentation_static.html) is provided for convenience.

## Project URLs structure
```
admin/                  # admin panel
api/
└── posts/
│    ├── create/         # creates new blogpost
│    └── <slug>/         # displays a certain post
├── users/
│   ├── all/            # displays users list in default order
│   │   └── sorted/     # displays users list ordered bu number of posts
│   ├── login/          # authentificates user via JWT
│   │   └── refresh/    # refreshes JWT token
│   └── register/       # registers user
docs/                   # provides dynamic Swagger documentation
├── .json               # provides Swagger documentations in JSON format
└── .yaml               # provides Swagger documentations in YAML format
```    

## Project directories and files structure
```bash
├── blogposts
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_setup.py
│   │   └── test_views_and_serializers.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── README.md
├── requirements.txt
├── testblog
├── testblog_documentation_static.html
│   ├── asgi.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── users
    ├── admin.py
    ├── apps.py
    ├── __init__.py
    ├── migrations
    │   ├── 0001_initial.py
    │   ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── tests
    │   ├── __init__.py
    │   ├── test_auth_views_and_serializers.py
    │   ├── test_list_views_and_serializers.py
    │   ├── test_models.py
    │   └── test_setup.py
    ├── urls.py
    └── views.py
```
