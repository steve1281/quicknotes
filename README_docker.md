# build
docker build -t quicknotes:0.1 . --no-cache

# run
docker run -d -v d:\shared:/docs -p 8000:8000 quicknotes:0.1

# or, with environment variables:
docker run -d -v ~/docs_old/:/docs -p 8001:8001 -e "PORT=8001" -e IPADDRESS="10.74.86.243" quicknotes:0.1
