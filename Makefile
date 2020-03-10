help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  build         builds docker-compose containers"
	@echo "  up            starts docker-compose containers"
	@echo "  down          stops the running docker-compose containers"
	@echo "  rebuild       rebuilds the image from scratch without using any cached layers"

build:
	sudo docker-compose -f docker-compose.yml build

up:
	sudo docker-compose -f docker-compose.yml up

down:
	sudo docker-compose -f docker-compose.yml stop

rebuild:
	sudo docker-compose -f docker-compose.yml build --no-cache
