help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build         builds docker-compose containers"
	@echo "  up            starts docker-compose containers"
	@echo "  down          stops the running docker-compose containers"
	@echo "  rebuild       rebuilds the image from scratch without using any cached layers"

build:
	sudo eval $(cat .envs/.production/.fastapi .envs/.production/.postgres) docker-compose -f docker-compose.yml build

up:
	sudo eval $(cat .envs/.production/.fastapi .envs/.production/.postgres) docker-compose -f docker-compose.yml up

down:
	sudo eval $(cat .envs/.production/.fastapi .envs/.production/.postgres) docker-compose -f docker-compose.yml stop

rebuild:
	sudo eval $(cat .envs/.production/.fastapi .envs/.production/.postgres) docker-compose -f docker-compose.yml build --no-cache
