#!/bin/sh

# http://www.bom.gov.au/climate/data/index.shtml
# bom uses dynamic links for their weather station data
# to get a working link, use the above url and search for the weather stations and copy in below
# sorry BOM

adelaide17_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-106909102&p_stn_num=023119"
melbourne17_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-1487203034&p_stn_num=086232"
sydney17_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-871369877&p_stn_num=066006"
brisbane17_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-334786183&p_stn_num=040913"
townsville17_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-205323790&p_stn_num=032040"

adelaide18_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2018&p_c=-106909102&p_stn_num=023119"
melbourne18_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2018&p_c=-1487203034&p_stn_num=086232"
sydney18_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2018&p_c=-871369877&p_stn_num=066006"
brisbane18_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2018&p_c=-334786183&p_stn_num=040913"
townsville18_solar="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2018&p_c=-205323790&p_stn_num=032040"

adelaide17_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2017&p_c=-106106609&p_stn_num=023034"
melbourne17_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2017&p_c=-1490843626&p_stn_num=086338"
sydney17_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2017&p_c=-872831146&p_stn_num=066062"
brisbane17_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2017&p_c=-334768291&p_stn_num=040913"
townsville17_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2017&p_c=-205305898&p_stn_num=032040"

adelaide18_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2018&p_c=-106106609&p_stn_num=023034"
melbourne18_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2018&p_c=-1490843626&p_stn_num=086338"
sydney18_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2018&p_c=-872831146&p_stn_num=066062"
brisbane18_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2018&p_c=-334768291&p_stn_num=040913"
townsville18_temp="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=122&p_display_type=dailyDataFile&p_startYear=2018&p_c=-205305898&p_stn_num=032040"

adelaide17_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2017&p_c=-106626087&p_stn_num=023090"
melbourne17_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2017&p_c=-1490846516&p_stn_num=086338"
sydney17_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2017&p_c=-871354874&p_stn_num=066006"
brisbane17_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2017&p_c=-334771181&p_stn_num=040913"
townsville17_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2017&p_c=-205308787&p_stn_num=032040"

adelaide18_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2018&p_c=-106626087&p_stn_num=023090"
melbourne18_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2018&p_c=-1490846516&p_stn_num=086338"
sydney18_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2018&p_c=-871354874&p_stn_num=066006"
brisbane18_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2018&p_c=-334771181&p_stn_num=040913"
townsville18_rain="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=2018&p_c=-205308787&p_stn_num=032040"


adelaide17solar=`wget -q -O- "$adelaide17_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
brisbane17solar=`wget -q -O- "$brisbane17_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
sydney17solar=`wget -q -O- "$sydney17_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
melbourne17solar=`wget -q -O- "$melbourne17_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
townsville17solar=`wget -q -O- "$townsville17_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`

adelaide18solar=`wget -q -O- "$adelaide18_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
brisbane18solar=`wget -q -O- "$brisbane18_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
sydney18solar=`wget -q -O- "$sydney18_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
melbourne18solar=`wget -q -O- "$melbourne18_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
townsville18solar=`wget -q -O- "$townsville18_solar" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`

adelaide17temp=`wget -q -O- "$adelaide17_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
brisbane17temp=`wget -q -O- "$brisbane17_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
sydney17temp=`wget -q -O- "$sydney17_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
melbourne17temp=`wget -q -O- "$melbourne17_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
townsville17temp=`wget -q -O- "$townsville17_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`

adelaide18temp=`wget -q -O- "$adelaide18_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
brisbane18temp=`wget -q -O- "$brisbane18_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
sydney18temp=`wget -q -O- "$sydney18_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
melbourne18temp=`wget -q -O- "$melbourne18_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
townsville18temp=`wget -q -O- "$townsville18_temp" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`

adelaide17rain=`wget -q -O- "$adelaide17_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
brisbane17rain=`wget -q -O- "$brisbane17_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
sydney17rain=`wget -q -O- "$sydney17_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
melbourne17rain=`wget -q -O- "$melbourne17_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
townsville17rain=`wget -q -O- "$townsville17_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`

adelaide18rain=`wget -q -O- "$adelaide18_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
brisbane18rain=`wget -q -O- "$brisbane18_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
sydney18rain=`wget -q -O- "$sydney18_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
melbourne18rain=`wget -q -O- "$melbourne18_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`
townsville18rain=`wget -q -O- "$townsville18_rain" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g' | sed -e 's/^[ \t]*//g'`

echo "Adelaide17solar" > bom_data/adelaide17solar.txt
echo "$adelaide17solar" >> bom_data/adelaide17solar.txt
echo "Adelaide18solar" > bom_data/adelaide18solar.txt
echo "$adelaide18solar" >> bom_data/adelaide18solar.txt

echo "Brisbane17solar" > bom_data/brisbane17solar.txt
echo "$brisbane17solar" >> bom_data/brisbane17solar.txt
echo "Brisbane18solar" > bom_data/brisbane18solar.txt
echo "$brisbane18solar" >> bom_data/brisbane18solar.txt

echo "Sydney17solar" > bom_data/sydney17solar.txt
echo "$sydney17solar" >> bom_data/sydney17solar.txt
echo "Sydney18solar" > bom_data/sydney18solar.txt
echo "$sydney18solar" >> bom_data/sydney18solar.txt

echo "Melbourne17solar" > bom_data/melbourne17solar.txt
echo "$melbourne17solar" >> bom_data/melbourne17solar.txt
echo "Melbourne18solar" > bom_data/melbourne18solar.txt
echo "$melbourne18solar" >> bom_data/melbourne18solar.txt

echo "Townsville17solar" > bom_data/townsville17solar.txt
echo "$townsville17solar" >> bom_data/townsville17solar.txt
echo "Townsville18solar" > bom_data/townsville18solar.txt
echo "$townsville18solar" >> bom_data/townsville18solar.txt

echo "Adelaide17temp" > bom_data/adelaide17temp.txt
echo "$adelaide17temp" >> bom_data/adelaide17temp.txt
echo "Adelaide18temp" > bom_data/adelaide18temp.txt
echo "$adelaide18temp" >> bom_data/adelaide18temp.txt

echo "Brisbane17temp" > bom_data/brisbane17temp.txt
echo "$brisbane17temp" >> bom_data/brisbane17temp.txt
echo "Brisbane18temp" > bom_data/brisbane18temp.txt
echo "$brisbane18temp" >> bom_data/brisbane18temp.txt

echo "Sydney17temp" > bom_data/sydney17temp.txt
echo "$sydney17temp" >> bom_data/sydney17temp.txt
echo "Sydney18temp" > bom_data/sydney18temp.txt
echo "$sydney18temp" >> bom_data/sydney18temp.txt

echo "Melbourne17temp" > bom_data/melbourne17temp.txt
echo "$melbourne17temp" >> bom_data/melbourne17temp.txt
echo "Melbourne18temp" > bom_data/melbourne18temp.txt
echo "$melbourne18temp" >> bom_data/melbourne18temp.txt

echo "Townsville17temp" > bom_data/townsville17temp.txt
echo "$townsville17temp" >> bom_data/townsville17temp.txt
echo "Townsville18temp" > bom_data/townsville18temp.txt
echo "$townsville18temp" >> bom_data/townsville18temp.txt

echo "Adelaide17rain" > bom_data/adelaide17rain.txt
echo "$adelaide17rain" >> bom_data/adelaide17rain.txt
echo "Adelaide18rain" > bom_data/adelaide18rain.txt
echo "$adelaide18rain" >> bom_data/adelaide18rain.txt

echo "Brisbane17rain" > bom_data/brisbane17rain.txt
echo "$brisbane17rain" >> bom_data/brisbane17rain.txt
echo "Brisbane18rain" > bom_data/brisbane18rain.txt
echo "$brisbane18rain" >> bom_data/brisbane18rain.txt

echo "Sydney17rain" > bom_data/sydney17rain.txt
echo "$sydney17rain" >> bom_data/sydney17rain.txt
echo "Sydney18rain" > bom_data/sydney18rain.txt
echo "$sydney18rain" >> bom_data/sydney18rain.txt

echo "Melbourne17rain" > bom_data/melbourne17rain.txt
echo "$melbourne17rain" >> bom_data/melbourne17rain.txt
echo "Melbourne18rain" > bom_data/melbourne18rain.txt
echo "$melbourne18rain" >> bom_data/melbourne18rain.txt

echo "Townsville17rain" > bom_data/townsville17rain.txt
echo "$townsville17rain" >> bom_data/townsville17rain.txt
echo "Townsville18rain" > bom_data/townsville18rain.txt
echo "$townsville18rain" >> bom_data/townsville18rain.txt