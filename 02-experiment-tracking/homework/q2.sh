mkdir -p output
python preprocess_data.py --raw_data_path data --dest_path ./output
echo "Q2: $(ls ./output | wc -w)"
