#!/bin/sh


adelaide=`wget -q -O- "http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-106946031&p_stn_num=023123" | egrep "<tr><th scope=" | tr '\d|<|>' ','`
# brisbane = "http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-334786119&p_stn_num=040913"
# sydney = "http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-871369812&p_stn_num=066006"
# melbourne = "http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-1487202970&p_stn_num=086232"
# townsville = "http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=193&p_display_type=dailyDataFile&p_startYear=2017&p_c=-205323725&p_stn_num=032040"
# perth =
# darwin = 

echo "$adelaide"