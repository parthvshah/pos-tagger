time python3 hmmlearn.py ./data/it_isdt_train_tagged.txt
time python3 hmmdecode.py ./data/it_isdt_dev_raw.txt
wc -l hmmoutput.txt
python3 score.py hmmoutput.txt ./data/it_isdt_dev_tagged.txt
echo
time python3 hmmlearn.py ./data/ja_gsd_train_tagged.txt
time python3 hmmdecode.py ./data/ja_gsd_dev_raw.txt
wc -l hmmoutput.txt
python3 score.py hmmoutput.txt ./data/ja_gsd_dev_tagged.txt
echo