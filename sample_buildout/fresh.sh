rm -rf /tmp/sample_pyeclipse_proj
./make_clean.sh .
python2.4 bootstrap.py
bin/buildout -v
