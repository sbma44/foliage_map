fetch:
	rm -rf reports
	mkdir reports
	cd reports && csvcut -c 3 ../foliage_report_urls.csv | xargs -I % curl % -O

extract:
	find reports | grep gif | xargs -I {} sh extract_regions.sh {}

combine:
	python combine_json.py

	# embarrassing Tom-specific fix. I hate Dropbox.
	sed -i.bak -e 's/\/Users\/tomlee\/Dropbox (MapBox)\//\/Users\/tomlee\/mapbox\//g' foliage.tm2source/data.yml

clean:
	rm -f work/* json/* reports/*

all: clean fetch extract combine