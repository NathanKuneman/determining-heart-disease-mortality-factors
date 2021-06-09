# Predicting Heart Disease Mortality



<img src="images/heart_dis_by_state.jpg"
     alt="Markdown Monster icon"
     style="float: center; margin-right: 10px;" />

## Background

Heart disease mortality rates vary significatly across different counties and states within the United States. I set out to explore what could cause these differences by combining data provided by the government health data website, the US Census Bureau, and the National Oceanic and Atmospheric Administration (NOAA).

---

## Dataset
The data includes values for each year from 2013-2018. During my exploratory data analysis I discovered that changes in time did not significantly change the outcomes of any of my hypothesis tests so I mainly focused on using data from a single year. 



### Sources: 

Government Healthcare Data - 
[Dataset](https://healthdata.gov/dataset/Heart-Disease-Mortality-Data-Among-US-Adults-35-by/pwn5-iqp5)

The U.S. Census Bureau - 
[Dataset](https://data.census.gov/cedsci/table?t=Income%20and%20Earnings&g=0100000US.050000&y=2017&tid=ACSST1Y2017.S1901&hidePreview=true)

The National Oceanic and Atmospheric Administration (NOAA) - 
[Dataset](https://www.ncdc.noaa.gov/cag/county/mapping/110/pcp/201601/12/value)


### Key Features:


|Feature Name     |Data type |Source |Description                              |
|-------------------|-----------|---------|-------------------------------------------------|
| Data_Value    | Float      | Government Healthcare Data | Number of heart disease mortalities per 100k residents of county <sup>1</sup>
| LocationDesc              | String      | Government Healthcare Data, U.S. Census Data| County name
| LocationAbbr             | String      | Government Healthcare Data, U.S. Census Data | Abbreviation of State 
| LocationID             | Integer      | Governnment Healthcare Data, U.S. Census Data | This is a unique number given to each county in the U.S. to identify it
|   Households!!Estimate!!Mean income (dollars)            | Float      | U.S. Census Data  | An Estimate of the mean household income for each county
| Location | String      | NOAA | Name of the County
| Location ID      | String      | NOAA | This is a unique number given to each county in the U.S. to identify it <sup>2</sup>
| Value     | Float      | NOAA | The mean tempurature in the county for the given year

<sup>1</sup>This value is per 100,000 residents, spacially smoothed over 3 years, and age-adjusted. [Age-adjusted](https://en.wikipedia.org/wiki/Age_adjustment) is medical definition that attempts to adjust the value so that differences in the age of a population between counties will not skew the value.   

<sup>2</sup>The NOAA Location ID column was not in the same format as the Governement Healthcare Data and U.S. Census data but I was able to use part of this string to merge the different datasets based on county name and the state name (which was pulled from the Location ID column).



### Notes About the Data
There were a total of 3,104 rows for each dataset while there are 3,143 counties in the U.S. if you do not include counties in Puerto Rico. This difference is because I chose to ignore counties that had missing values. These missing values mainly came from counties with not enough residents to accurately estimate the mortality rate per 100,000 residents. 

---

## Exploratory Data Analysis
Once I combined all of the data into a single dataframe I could then look to see if there were any significant features may be affecting the heart disease mortality rate for each county.

### Exploration of Temperature feature

Th first step in comparing the temperature data to the mortality rate was to normalize the data using a [min/max normalization](https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)). I was then able to plot the two features on the same axis as shown below.




Our model will be using the following features, seperated into summary features of the user and time series features that use the specific day-to-day/week-to-week features. 

* **Summary and Demographic Features**
    * User's age at the cutoff
    * The maximium hold (loss) in a single day 
    * User's Fixed-Odds to Live-Action Sports hold ratio
* **Time Series Features**
    * Weekly Hold
    * Rolling Average of the Weekly Hold
    * Weekly (Weighted) Bets

### Making the Frames

Recall that the Responsible Gaming inteventions are only between November 2008 and November 2009. To create frames for a model to train and evaluate on, I split that period and the preceding six months with intervals of 3 months; the frame can sees the data from two years before the cutoff and attempts to predict if that subscriber had a Responsible Gaming intervention event in the next year. The frame is labelled positive if that's the case and negative otherwise.

![](images/frame_show.gif)

We outright discard the frame if an RG event happened _before_ the cutoff (such as the last frame in the slide above), as that's not particually representative of what the model's trying to accomplish.

### Sampling

The initial dataset was balanced between RG-flagged and non-RG users. But the positive and negative frames have become significantly unbalanced:

* We've discarded over half of our RG set because of "Reopen" codes. 
* All frames created from a non-RG user are going to be negative class, while frames from an RG user are going to be a mix of positive and negative class.
* We're discarding a frame if it has an RG event in it, further cutting our positive frame.

Naively applying our framing process to all valid entries creates roughly 20000 negative frames and 4000 positive frames, which is rather unbalanced. I undersample the control users until I had a roughly 50:50 ratio of positive and negative samples, and I end up using about 300 control users to maintain this.

### Model Performance

I first created a training and holdout set of user IDs, applied my processing and framing seperately, then fit a Random Forest Model to the training set. I use a grid search for hyperparameter tuning, optimizing on the F1 score:

 | Parameter        | Optimal | Gridsearch Values |
 |------------------|--------:|------------------:|
  | n_estimators    |     200 |        [100, 200] |
 | max_depth        |      None |            [None, 3, 5] |
 | min_samples_split |      2 |    [2, 4, 8] |
  | min_samples_leaf |      5 |    [1, 5, 10, 20] |
 | bootstrap     |       True |            [False, True] |

And performs the following metric scores on the validation set: 

 | Metric        | Score |
|------------------|--------:|
| Recall | 0.66 
| Precision | 0.71
| F1 | 0.68 |

## Conclusions

### Usability

How can we use this model for early interventions? That depends entirely on what planned early intervention we want to do. If we're simply sending the subscriber a non-compulsory email about gambling addiction and availiable resources, we can accept a much larger false positive rate than if we were taking a drastic action like a deposit limit or account block. We can construct an ROC curve from our model's predictions on the validation set, which allows us to fine-tune the trade off between the false positive rate and false negative rate by adjusting the acceptance threshold:

![](images/roc_curve.png)

This curve suggests that an interventionist could, for example, send information to about 60% of eventual RG-flagged users at the cost of unnecessarily sending the same information to 20% of non-flagged users.

### Test Set Performance

On the final unseen data, the model (predictably) performed modestly worse but still seemed to generalize well.

 | Metric        | Score |
|------------------|--------:|
| Recall | 0.63 
| Precision | 0.67
| F1 | 0.65 |

## Future Work

* **Adding Appeals:** I discarded interventions that were appeals of earlier blocks, which turned out to be almost half of the positive data set. In many cases, the prior ban date can be pretty easily inferred by a sudden drop in activity:

![](images/RG_reopenTrue.png)

And extracting this information from even a portion of the appeals would substantially increase the sample size.

* **Feature Engineering:** My feature engineering was rather limited; I'd like to try varying the size of the lookback window (there's no fundamental reason not to use the entire prior history!), try different granularities of the data, try different rolling windows and different metrics in the rolling windows.
    * I'd particually like to try and featurize [loss chasing](https://www.gamblingtherapy.org/en/chasing-losses), which likely requires finer granularity than the week-wise I used in the model.
