By default the result is storing for 1 day in redis db

docker run -d \
  --name redis-local \
  -p 6379:6379 \
  redis:7-alpine

 docker run -d \
  --name qdrant-local \
  -p 6333:6333 \
  -v "$(pwd)/qdrant_data:/qdrant/storage" \
  qdrant/qdrant:dev