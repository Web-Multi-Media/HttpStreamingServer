BUILD=prod
sudo rm -rf Videos
git checkout Videos
if [ "$BUILD" = "prod" ]; then
    docker-compose -f docker-compose-$BUILD.yml build
fi
docker-compose -f docker-compose-$BUILD.yml down -v 
docker-compose -f docker-compose-$BUILD.yml run --rm web ./wait-for-it.sh db:5432 -- python3 manage.py migrate
docker-compose -f docker-compose-$BUILD.yml up 
