BUILD=debug
sudo rm -rf Videos
git checkout Videos
#docker-compose -f docker-compose-$BUILD.yml build
docker-compose -f docker-compose-$BUILD.yml down -v 
docker-compose -f docker-compose-$BUILD.yml run --rm web ./wait-for-it.sh db:5432 -- python3 manage.py migrate
docker-compose -f docker-compose-$BUILD.yml up 
