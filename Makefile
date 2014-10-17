fetch:
	rm -rf reports
	mkdir reports
	cd reports && csvcut -c 3 ../foliage_report_urls.csv | xargs -I % curl % -O

extract:
	sh extract_regions.sh reports/*.gif

clean:
	rm -f work/* json/* reports/*