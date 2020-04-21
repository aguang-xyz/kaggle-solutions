notebooks=$(find . -not -path '*/\.*' -name '*.ipynb')

for notebook in $notebooks; do

	folder=$(dirname "./docs/$notebook")

	mkdir -p $folder

	jupyter nbconvert --to html --output-dir $folder $notebook

done
