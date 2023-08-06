#!/usr/bin/env bash
dest=$1
echo "Dest is $dest"

echo "Creating folder $PWD/tmp_doc"
mkdir -p "$PWD"/tmp_doc && cd "$PWD"/tmp_doc
git clone --depth=1 https://github.com/rediscovery-io/remo-python.git
cd remo-python
pip install -r requirements.txt
pip install -r doc/requirements.txt
make markdown
mkdir -p "$dest"
cp doc/build/markdown/*.md "$dest"

cd examples

notebooks=("intro_to_remo-python" "tutorial_upload_annotations" "tutorial_pytorch_image_classification" "tutorial_pytorch_object_detection")
for notebook in "${notebooks[@]}"; do
  jupyter nbconvert "$notebook.ipynb" --to markdown
  cp "$notebook.md" "$dest"/../
  cp "$notebook.ipynb" "$dest"/../assets
done

cp assets/* "$dest"/../assets/

cd ../../../
echo "Deleting folder $PWD/tmp_doc"
rm -rf "$PWD"/tmp_doc
