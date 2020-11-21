# Chatbot api

## You need docker and docker-compose in order to build the project locally

Clone the repo and then just run docker-compose up -d --build to build and start up the api.

Then do migrations by doing: docker-compose exec api alembic upgrade head.

To access the api ui, go to localhost:8000/docs.

There you can create your own user and test out the different routes.
For creating the user, you need to give the path the secret key defined in .env for this to work. You will then need to go to the database (through pgadmin for example, localhost:5050, credentials in docker-compose) and set your users is_active = True.

Now that you have your user and it is active, you can access the Authorization route in /docs. Press the green "Authorize" button and type in your new credentials, you will then be given a token and it is set to request headers.

You need to save some intents for the bot to use, you can take the sample intents.json file from the repo to do it.
