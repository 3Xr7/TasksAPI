# TasksAPI

## Local Dev
### Prerequisites
 - docker installed and running, see https://docs.docker.com/engine/install

### Starting the App
1. Create a `.env` file by copying `.env.example`
2. Update `SQLITE_FILENAME="foo.db"` so that it equals your desired database filename
```ini
SQLITE_FILENAME="dev.db"
```
3. Start and build the container environment
```sh
docker compose up -d --build
```
1. Give it a moment to start up, then interact with the API. See "Calling Tasks API Via Command Line" below.

### Making Changes
While the `tasks-api` container is running changes to `src/*.py` files hot reload allowing for quick iteration cycles due to change effects visible near instantaniously.

### Running Tests
For the time being the test suite runs from within a secondary compose file `docker-compoes.test.yml`.

#### Run
```sh
docker compose -f .\docker-compose.test.yml up
```

The command promt may appear to be left attached to the container output, its likely done pressing any key will clear that up.

## Calling Tasks API Via Command Line
### Linux Shell
#### Get Tasks
```sh
curl http://localhost:8000/tasks
```
#### Create Task
```sh
curl -X POST http://localhost:8000/tasks -H 'Content-Type: application/json' -d '{"title": "foo"}'
```

### Windows Powershell
#### Get Tasks
```pwsh
Invoke-WebRequest -Uri http://localhost:8000/tasks/
```
#### Create Task
```pwsh
Invoke-WebRequest -Uri http://localhost:8000/tasks/ -Method POST -ContentType "application/json" -Body (@{"title" = "foo"}|ConvertTo-Json)
```
