#!/bin/sh

adelaide_link="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-106946061&p_stn_num=023123"
# melbourne_link="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-1487202970&p_stn_num=086232"
# sydney_link="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-871369812&p_stn_num=066006"
# brisbane_link="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-334786119&p_stn_num=040913"
# townsville_link="http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-205323725&p_stn_num=032040"


adelaide=`wget -q -O- "$adelaide_link" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g'`
# brisbane =`wget -q -O- "$brisbane_link" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g'`
# sydney =`wget -q -O- "$sydney_link" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g'`
# melbourne =`wget -q -O- "$melbourne_link" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g'`
# townsville =`wget -q -O- "$townsville_link" | egrep "<tr><th scope=" | sed -e 's/<[^>]*>/ /g'`


echo "$adelaide"