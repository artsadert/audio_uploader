from dotenv import load_dotenv

from os import environ, getenv


def load():
    load_dotenv()

    required_variables = ["POSTGRES_USER",
                        "POSTGRES_PASSWORD",
                        "POSTGRES_DB",
                        "PGADMIN_DEFAULT_EMAIL",
                        "PGADMIN_DEFAULT_PASSWORD"]

    for required_var in required_variables:
        if getenv(required_var) == None:
            raise Exception(f"required variable is missing: {required_var}")

    environ["PGLINK"] = f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@localhost/{getenv('POSTGRES_DB')}"

if __name__ == "__main__":
    load()
