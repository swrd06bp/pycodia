
rm -rf dist
pip3  uninstall -y  pycodya

python3 -m build

if [ "$1" == "prod" ]
  then
    python3 -m twine upload -u "swrd06bp" -p "4oKo7QTQmavTFwZo6WNJ"  dist/*
    pip3 install pycodya
  else  
    python3 -m twine upload -u "swrd06bp" -p "4oKo7QTQmavTFwZo6WNJ"  --repository testpypi  dist/*
    pip3 install --no-cache-dir -i https://test.pypi.org/simple/ pycodya==0.2.1a
    pip3 install --no-cache-dir -i https://test.pypi.org/simple/ pycodya==0.2.1a
fi
