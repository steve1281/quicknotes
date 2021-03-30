# build
docker build -t quicknotes:0.1 . --no-cache

# run
docker run -d -v d:\shared:/docs -p 8000:8000 quicknotes:0.1
