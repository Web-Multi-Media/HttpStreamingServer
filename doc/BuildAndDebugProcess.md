RELEASE BUILD
-------------------
Be aware that the file coming from the frontend build are copied to backend/static during the build process. If you do some modification in the frontend, don't forget to erase this folder as it can lead to some erratic behavior.

DEBUG BUILD
-------------------

Build the frontend:

    docker-compose -f docker-compose-debug.yml build

Run the server:

    docker-compose -f docker-compose-debug.yml up

Now the application should be accessible from your browser at `http://localhost:3000`.

You can access Django REST Framework API from `http://localhost:8000`.