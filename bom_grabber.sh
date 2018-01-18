#!/bin/sh

# http://www.bom.gov.au/climate/data/index.shtml
# bom uses dynamic links for their weather station data


# Cities:
# NSW: Sydney, Wagga Wagga, Newcastle, Wollongong, Canberra, 
#      Port Macquarie, Coffs Harbour, Ballina, Tamworth, Albury
# WA: Perth
# NT: Darwin
# Victoria: Melbourne, Geelong, Bendigo
# SA: Adelaide, Port Augusta, Burra
# QLD: Brisbane, Cairns, Toowoomba, Gold Coast, 
#      Mackay, Rockhampton, Bundaberg, Gympie

echo "Enter the weather station location (e.g. Sydney or Coffs Harbour):"
read location

echo "Enter the datatype (solar or temp):"
read datatype

echo "Enter the URL for 2017 data:"
read URL

year=`echo $URL | cut -d'=' -f4 | sed 's/[^0-9]//g'`
prevyear=$year

# change 2 to 3 if the year is 2019
for run in {1..2}
do
	if ((run == 2)); then
		URL="${URL/$prevyear/$year}"
		eval "var$prevyear=$year";
	fi

	dataset=`wget -q -O- "$URL" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
	echo "$location$year$datatype" > weather_data/"$location$year$datatype".txt
	echo "$dataset" >> weather_data/"$location$year$datatype".txt
	year=$(($year+1))
done

