# **Determining Heart Disease Mortality Factors**



<img src="images/cover_photo.jpg"
     alt="Heart disease mortalities across states"
     style="float: center; margin-right: 10px;" />

## **Background**

Heart disease mortality rates vary significantly across different counties and states within the United States. I set out to explore what could cause these differences by combining data provided by the government health data website, the US Census Bureau, and the National Oceanic and Atmospheric Administration (NOAA). 


---

## **Dataset**
The data includes values for each year from 2013-2018. During my exploratory data analysis I discovered that changes in time did not significantly change the outcomes of any of my hypothesis tests so I mainly focused on using data from a single year. 



### **Sources:**

Government Healthcare Data - 
[Dataset](https://healthdata.gov/dataset/Heart-Disease-Mortality-Data-Among-US-Adults-35-by/pwn5-iqp5)

The U.S. Census Bureau - 
[Dataset](https://data.census.gov/cedsci/table?t=Income%20and%20Earnings&g=0100000US.050000&y=2017&tid=ACSST1Y2017.S1901&hidePreview=true)

The National Oceanic and Atmospheric Administration (NOAA) - 
[Dataset](https://www.ncdc.noaa.gov/cag/county/mapping/110/pcp/201601/12/value)


### **Key Features:**


|Feature Name     |Data type |Source |Description                              |
|-------------------|-----------|---------|-------------------------------------------------|
| Data_Value    | Float      | Government Healthcare Data | Number of heart disease mortalities per 100k residents of county <sup>1</sup>
| LocationDesc              | String      | Government Healthcare Data, U.S. Census Data| County name
| LocationAbbr             | String      | Government Healthcare Data, U.S. Census Data | Abbreviation of State 
| LocationID             | Integer      | Governnment Healthcare Data, U.S. Census Data | This is a unique number given to each county in the U.S. to identify it
|   Households!!Estimate!!Mean income (dollars)            | Float      | U.S. Census Data  | An Estimate of the mean household income for each county
| Location | String      | NOAA | Name of the County
| Location ID      | String      | NOAA | This is a unique number given to each county in the U.S. to identify it <sup>2</sup>
| Value     | Float      | NOAA | The mean temperature in the county for the given year

<sup>1</sup>This value is per 100,000 residents, spacially smoothed over 3 years, and age-adjusted. [Age-adjusted](https://en.wikipedia.org/wiki/Age_adjustment) is medical definition that attempts to adjust the value so that differences in the age of a population between counties will not skew the value.   

<sup>2</sup>The NOAA Location ID column was not in the same format as the Governement Healthcare Data and U.S. Census data but I was able to use part of this string to merge the different datasets based on county name and the state name (which was pulled from the Location ID column).



### **Notes About the Data**
* I want to reiterate the footnote<sup>1</sup> up above. Because this data has been age-adjusted we can assume that varying aged populations between counties will not affect the values. 

* There were a total of 3,104 rows for each dataset while there are 3,143 counties in the U.S. if you do not include counties in Puerto Rico. This difference is because I chose to ignore counties that had missing values. These missing values mainly came from counties with not enough residents to accurately estimate the mortality rate per 100,000 residents. 

---

## **Exploratory Data Analysis**
Once I combined all of the data into a single dataframe I could then look to see if there were any significant features may be affecting the heart disease mortality rate for each county.

### **Exploration of Temperature feature**

Th first step in comparing the temperature data to the mortality rate was to normalize the data using a [min/max normalization](https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)). I was then able to plot the two features on the same axis as shown below.

---

<img src="images/normalized_temp_death.jpg"
     alt="Normalized temperature data vs heart disease mortality rates across counties"
     style="float: center; margin-right: 10px;" />

---

As you can see there appears to be some correlation between the two but this graph makes it a little unclear how strong that correlation may be. Also note that the large jumps in the graph are caused by moving between states. This would lead me to believe that what state a county in is affecting the graph more than the temperature. In order to be able to directly compare the affect of temperature on each the heart disease mortalities of each county, I decided to break the counties up into two groups. I put counties who's temperature was above the mean temperature across counties into a data frame named "hot_counties" and then put the counties below the mean temperature in a data frame named "cold_counties". The scatter plot below shows the difference in the two data frames. 

---
<img src="images/warm_cold_scatter.jpg"
     alt="Temperature's affect on heart disease mortality"
     style="float: center; margin-right: 10px;" />



From these graphs I was able to see that temperature may be an important factor when in comes to heart disease mortality rates. Because of these findings I will use temperature in my hypothesis testing later. 

### **Exploration of Income Feature**

The first step in exploring the income feature was to order the data by the mean household income feature. By doing this I could then plot the mortality rate with an x-axis of increasing income per county as shown below.

---

<img src="images/mort_income.jpg"
     alt="Heart disease mortality rates vs county wide income"
     style="float: center; margin-right: 10px;" />

---

The trend in this graph is clear that lower income counties have a significantly higher rate of heart disease mortality. In counties where the mean household income is above $80,000 there are very few data points that fall above the overall mean mortality rate while a majority of counties falling below a $50,000 mean household income were above the overall mean mortality rate. 

To take this a step further let's look at the means of the 100 richest, 100 middle, and the 100 poorest counties. We'll define the richest and poorest counties by the mean household income for this example.

---

<img src="images/poor_mid_rich.jpg"
     alt="Heart Disease in the rich and poor counties 2013"
     style="float: center; margin-right: 10px;" />

---

This made it clear that mean household income was certainly a feature worth exploring more. **The difference between the mean of the 100 poorest counties and the 100 richest counties was 209.2 mortalities per 100,000. If these means are truely representitive of the entire population than we can estimate that people in rich counties are 44% less likely to die from heart disease than those in poor counties.** In order to see if this data is significant I will conduct a hypothesis test on these features.

---

### **The Curious Case of Franklin Parish, Louisiana** 
<img src="images/franklin.gif"
     alt="Franklin Parish Heart Disease"
     style="float: center; margin-right: 10px;" />
    
While most of the health data tended to fall into a mostly normal distrubution, there was one county that clearly was an outlier. Franklin Parish is a mostly rural county in Louisiana where the heart disease mortality rate was 1071.6 per 100,000 residents. This is over double the country-wide mean of 361.9 and is 265.2 higher the next highest county, Caldwell Parish, which is also in Louisiana.

I am not the only one who found this interesting as there is currently a study underway at LSU’s Pennington Biomedical Research Center which features Franklin Parish due to the county's high rate of heart disease mortalities. More information about the study can be found [here](https://www.pbrc.edu/news/media/2019/RURAL-Study-Announced-Why-do-Some-but-Not-All-Rural-Southerners-Live-longer-Healthier-Lives.aspx).

Because this outlier is so extreme, I've chosen to ignore this data point in my hypothesis testing.

---

## **Hypothesis Testing**
The results from the exploratory data analysis would lead one to believe that both temperature and income levels of each county will have an affect the rates of heart disease mortality within that county, however, in order to prove this we need to complete a hypothesis test on each feature. 

### **Temperature**
Since the mean mortality rate in warmer counties is higher than that in cold counties I've decided to state my null and alternative hypothesis as listed below.

---

Where "M" is the mean rate of deaths from heart disease.

Null Hypothesis = M<sub>warm counties</sub> = M<sub>cold counties</sub>  

Alternative Hypothesis = M<sub>warm counties</sub> > M<sub>cold counties</sub>  

---

For this test warm counties are defined by all counties there the temperature is above the mean temperature the opposite is true for cold counties

Normally I would choose an Alpha value of .05 but since we are performing 6 hypothesis tests I have to perform a [Bonferroni correction](https://en.wikipedia.org/wiki/Bonferroni_correction) which gives me an Alpha of **.00833**

Now we will perform a T-test to get our P-value and determine if the true means of these populations are different. 

### **Results:**

|Year    |P-value  | Cold Counties Mean | Warm Counties Mean | Effect Size
|---|---|---|---|---|
| 2013    | 6.90 * 10<sup>-132</sup> |326.24|395.57| 70.33 |
| 2014            | 1.82 * 10<sup>-132</sup>      |325.63| 397.48| 71.84|
|    2015       |    1.86 * 10<sup>-132</sup>   | 324.24| 396.55| 72.31
| 2016         | 6.42 * 10<sup>-138</sup>    |323.38| 396.30 | 72.92|
|    2017        |    3.13 * 10<sup>-141</sup>   | 320.87 | 392.52 | 72.65|
|    2018        |    1.53 * 10<sup>-135</sup>      | 320.17| 390.39 | 70.23|

**These values are far below our alpha threshold therefore we can reject the null hypothesis.**



### **Income**
In the exploratory data analysis it became clear that as a county had a higher income there was a significantly lower level of mortalities from heart disease. In order to test this we will divide the counties up based on if they fall above or below the mean income level. We will then test this with the null and alternative hypothesis listed below. 

---

Where "M" is the mean rate of deaths from heart disease.

Null Hypothesis = M<sub>poor counties</sub> = M<sub>wealthy counties</sub>  

Alternative Hypothesis = M<sub>poor counties</sub> != M<sub>wealthy counties</sub>  

---

Again here we will use an Alpha of **.00833**

Now we will perform a T-test to get our P-value and determine if the true means of these populations are different. 

### **Results:**

|Year    |P-value  | Poor County Mean| Wealthy County Mean| Effect Size|
|---|---|---|---|---|
| 2013    | 1.44 * 10<sup>-136</sup> | 391.53| 318.91|  72.63
| 2014            | 1.01 * 10<sup>-139</sup>    |392.58 | 317.78| 74.81
|    2015       |    5.26 * 10<sup>-143</sup> |391.96| 315.86| 76.10
| 2016         | 1.72 * 10<sup>-137</sup>  |390.53 |316.54| 73.99
|    2017        |    1.43 * 10<sup>-134</sup> |387.16|314.95|  72.21
|    2018        |   1.17 * 10<sup>-129</sup>  |384.29| 314.37| 69.92

**These P-values are far below our alpha threshold therefore we can reject the null hypothesis.**



## **Conclusions**
Since both null hypotheses were rejected, we can conclude that both temperature and income of a county are statistically significant features when looking at heart disease mortality rate within that county. 

### **Usability**
Knowing the factors that cause higher rates of heart disease mortalities is an important first step in understanding why these factors matter and what we can do about them. Simply spreading awareness could lead to residents of the higher risk counties to be more proactive about thier heart health. Also lawmakers in these counties could use this information to make better informed decisions when it comes to the health of thier constituents. 

### **Future Exploration**
Now that we know that temperature and income level play a role in the amount of heart disease mortalities, the next big question is "why?". Looking at income first, there are many avenues that might be worth exploring. 

* Do residents in lower income counties not have access to the same quality of healthcare as those in wealthier counties?

* Is the food easily available in lower income counties not as healthy as food available in weathly counties? 

Looking at temperature the next steps might not be as clear. The variations in temperature are not as distinct as the variations in income. 

* Could it be that in warmer counties it is often too hot outside for residents to get excercise?

* Is the heat actaully triggering heart disease events such as a heart attack?

Lastly another interesting topic to dig into deeper would be the topic of Franklin Parish, Louisiana. It is so far outside of the distrubution of the other data points that there must be some other feature playing a role there. 

* Is there an industrial or environmental hazard that is affecting heart health?

* Is there a genetic defect that is prominent among residents of the county?


