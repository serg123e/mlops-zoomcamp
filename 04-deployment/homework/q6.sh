docker build -t mlops-homework4:latest .
docker run --rm -it mlops-homework4:latest --year=2023 --month=5 | tee q6.txt
