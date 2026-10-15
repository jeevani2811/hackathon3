.PHONY: help install test build run-backend run-frontend clean docker-up docker-down

help:
	@echo "OmniAgent Developer Commands:"
	@echo "  make install       Install frontend and backend dependencies"
	@echo "  make test          Run automated backend pytest suite"
	@echo "  make run-backend   Start the FastAPI development server"
	@echo "  make run-frontend  Start the Next.js development server"
	@echo "  make docker-up     Run entire full-stack platform via Docker Compose"
	@echo "  make docker-down   Stop Docker containers"

install:
	pip install -r backend/requirements.txt
	cd frontend && npm install

test:
	pytest backend/tests -v

build:
	cd frontend && npm run build

run-backend:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	cd frontend && npm run dev

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

clean:
	rm -rf backend/__pycache__ backend/data/*.db frontend/.next
