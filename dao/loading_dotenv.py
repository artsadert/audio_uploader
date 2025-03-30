from dotenv import load_dotenv

from os import environ, getenv


def load():
    """
    More advansed load_dotenv funtion
    """
    load_dotenv()

    required_variables = ["POSTGRES_USER",
                        "POSTGRES_PASSWORD",
                        "POSTGRES_DB",
                        "PGADMIN_DEFAULT_EMAIL",
                        "PGADMIN_DEFAULT_PASSWORD",
                          "client_id",
                          "client_secret",
                          "client_redirect"]

    for required_var in required_variables:
        if getenv(required_var) == None:
            raise Exception(f"required variable is missing: {required_var}")

    environ["PGLINK"] = f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('POSTGRES_HOST')}/{getenv('POSTGRES_DB')}"

