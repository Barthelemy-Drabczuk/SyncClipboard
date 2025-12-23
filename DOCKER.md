# Docker Deployment Guide

This guide explains how to run SyncClipboard using Docker Compose.

## Prerequisites

- Docker installed (version 20.10+)
- Docker Compose installed (version 2.0+)

## Quick Start

### 1. Build and Start Services

From the project root directory:

```bash
docker-compose up -d
```

This will:
- Pull the MongoDB 7.0 image
- Build the webapp Docker image
- Start both services
- Create a persistent volume for MongoDB data

### 2. Check Status

```bash
docker-compose ps
```

You should see both services running:
- `syncclipboard-mongodb` on port 27017
- `syncclipboard-webapp` on port 5000

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

### 4. View Logs

To see webapp logs:
```bash
docker-compose logs -f webapp
```

To see MongoDB logs:
```bash
docker-compose logs -f mongodb
```

To see all logs:
```bash
docker-compose logs -f
```

## Managing the Services

### Stop Services

```bash
docker-compose stop
```

### Stop and Remove Containers

```bash
docker-compose down
```

### Stop and Remove Everything (including volumes)

⚠️ This will delete all your data!

```bash
docker-compose down -v
```

### Restart Services

```bash
docker-compose restart
```

### Rebuild and Restart

If you've made code changes:

```bash
docker-compose up -d --build
```

## Architecture

The docker-compose setup includes:

### Services

1. **MongoDB** (`mongodb`)
   - Image: `mongo:7.0`
   - Port: 27017
   - Volume: `mongodb_data` for persistent storage
   - Health check enabled

2. **WebApp** (`webapp`)
   - Built from local Dockerfile
   - Port: 5000
   - Depends on MongoDB being healthy
   - Source code mounted as volume (for development)

### Networks

- Custom bridge network `syncclipboard-network` for service communication

### Volumes

- `mongodb_data`: Persists MongoDB data across container restarts

## Environment Variables

The webapp supports these environment variables (set in docker-compose.yml):

- `MONGODB_HOST`: MongoDB hostname (default: `mongodb` in Docker)
- `MONGODB_PORT`: MongoDB port (default: `27017`)
- `FLASK_ENV`: Flask environment (default: `development`)

## Development Workflow

### Editing Code

The source code is mounted as a volume, so changes to files in `src/` will be reflected immediately. However, you may need to restart the webapp for some changes:

```bash
docker-compose restart webapp
```

### Accessing MongoDB

To access the MongoDB shell:

```bash
docker-compose exec mongodb mongosh
```

Then you can query the database:

```javascript
use prod_env
db.users.find()
db.transactions.find()
```

### Running Tests

To run tests in the Docker container:

```bash
docker-compose exec webapp python -m pytest tests/ -v
```

Or run tests locally:

```bash
source venv/bin/activate
cd src
python -m pytest tests/ -v
```

## Production Considerations

For production deployment, you should:

1. **Update the secret key** in `webapp.py`:
   ```python
   app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'generate-a-secure-random-key')
   ```

2. **Set Flask to production mode**:
   ```yaml
   environment:
     - FLASK_ENV=production
   ```

3. **Add MongoDB authentication**:
   ```yaml
   mongodb:
     environment:
       MONGO_INITDB_ROOT_USERNAME: admin
       MONGO_INITDB_ROOT_PASSWORD: secure_password
   ```

4. **Use a reverse proxy** (nginx, traefik) for HTTPS

5. **Add resource limits**:
   ```yaml
   webapp:
     deploy:
       resources:
         limits:
           cpus: '0.5'
           memory: 512M
   ```

## Troubleshooting

### MongoDB Connection Failed

Check if MongoDB is healthy:
```bash
docker-compose ps mongodb
```

View MongoDB logs:
```bash
docker-compose logs mongodb
```

### Port Already in Use

If port 5000 or 27017 is already in use, edit `docker-compose.yml`:

```yaml
webapp:
  ports:
    - "5001:5000"  # Change external port

mongodb:
  ports:
    - "27018:27017"  # Change external port
```

### Container Won't Start

Check logs for errors:
```bash
docker-compose logs webapp
```

Rebuild the image:
```bash
docker-compose build --no-cache webapp
docker-compose up -d
```

### Clear All Data and Start Fresh

```bash
docker-compose down -v
docker-compose up -d
```

## Backup and Restore

### Backup MongoDB Data

```bash
docker-compose exec mongodb mongodump --out /data/backup
docker cp syncclipboard-mongodb:/data/backup ./mongodb-backup
```

### Restore MongoDB Data

```bash
docker cp ./mongodb-backup syncclipboard-mongodb:/data/backup
docker-compose exec mongodb mongorestore /data/backup
```

## Using with Desktop Client

The desktop client needs to connect to the Docker webapp:

```bash
python main_client.py --user-id YOUR_USER_ID --server http://localhost:5000
```

If running Docker on a remote server:

```bash
python main_client.py --user-id YOUR_USER_ID --server http://your-server-ip:5000
```
