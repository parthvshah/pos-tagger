python3 hmmlearn.py ./data/it_isdt_train_tagged.txt
python3 hmmdecode.py ./data/it_isdt_dev_raw.txt
wc -l hmmoutput.txt
python3 score.py hmmoutput.txt ./data/it_isdt_dev_tagged.txt
echo
python3 hmmlearn.py ./data/ja_gsd_train_tagged.txt
python3 hmmdecode.py ./data/ja_gsd_dev_raw.txt
wc -l hmmoutput.txt
python3 score.py hmmoutput.txt ./data/ja_gsd_dev_tagged.txt
echo
python3 hmmlearn.py ./data/catalan_corpus_train_tagged.txt
python3 hmmdecode.py ./data/catalan_corpus_dev_raw.txt
wc -l hmmoutput.txt
python3 score.py hmmoutput.txt ./data/catalan_corpus_dev_tagged.txt
echo