# Deployment

## Required .env with params

### Postgres

    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - POSTGRES_DB
    - POSTGRES_HOST

### PGadmin

    - PGADMIN_DEFAULT_EMAIL
    - PGADMIN_DEFAULT_PASSWORD
    
### Yandex Oauth

    - client_id 
    - client_secret
    - client_redirect: (default "localhost:8000/login")

## Start docker compose

```console
sudo docker compose up -d
```

# features

- list of all user audiofiles superuser can see
- delete account also can do owner of account
- added pgadmin
