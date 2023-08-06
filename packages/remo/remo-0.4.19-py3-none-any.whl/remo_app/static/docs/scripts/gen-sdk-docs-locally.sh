#!/usr/bin/env bash
src=$1
dest=$2
echo "Src is $src"
echo "Dest is $dest"

cd "$src" || exit
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
