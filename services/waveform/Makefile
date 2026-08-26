DOCKER_HOST = 10.10.8.202
DOCKER_TAG = waveform-service

deploy:
	docker build -t $(DOCKER_TAG):latest .
	docker save $(DOCKER_TAG):latest | ssh -C $(DOCKER_HOST) docker load
	ssh root@$(DOCKER_HOST) "docker stop $(DOCKER_TAG)"
	ssh root@$(DOCKER_HOST) "docker rm $(DOCKER_TAG)"
	ssh root@$(DOCKER_HOST) "docker run -d -p 2001:8000 --name $(DOCKER_TAG) --restart unless-stopped $(DOCKER_TAG):latest"

