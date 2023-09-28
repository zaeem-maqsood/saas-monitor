up:
	@echo "Starting containers in docker-compose.yaml"
	docker-compose up -d --build  

up-prod:
	@echo "Starting containers in docker-compose.yaml"
	docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d --build  --build --detach

stop-all:
	@echo "Stopping all running containers"
	docker stop `docker ps -a -q`;

delete-containers:
	@echo "Stopping all running containers"
	-docker stop `docker ps -a -q`;
	@echo "Deleting all containers"
	-docker rm `docker ps -a -q`;

delete-images:
	@echo "Deleting all images"
	docker rmi -f `docker images -a -q`;

delete-all:
	-docker stop `docker ps -a -q`;
	-docker rm `docker ps -a -q`;
	-docker rmi -f `docker images -a -q`;
	-docker volume prune -f
