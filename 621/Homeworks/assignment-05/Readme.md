# Homework #4

## Overview

In this homework assignment, you will explore, analyze and model a data set containing information on approximately 12,000 commercially available wines. The variables are mostly related to the chemical properties of the wine being sold. The response variable is the number of sample cases of wine that were purchased by wine distribution companies after sampling a wine. These cases would be used to provide tasting samples to restaurants and wine stores around the United States. The more sample cases purchased, the more likely is a
wine to be sold at a high end restaurant. A large wine manufacturer is studying the data in order to predict the number of wine cases ordered based upon the wine characteristics. If the wine manufacturer can predict the number of cases, then that manufacturer will be able to adjust their wine offering to maximize sales.

## Objective

Your objective is to build a count regression model to predict the number of cases of wine that will be sold given certain properties of the wine. HINT: Sometimes, the fact that a variable is missing is actually predictive of the target. You can only use the variables given to you (or variables that you derive from the variables provided).

## Description

Below is a short description of the variables of interest in the data set:

- **INDEX** Identification Variable (do not use)
- **TARGET** Number of Cases Purchased
- **AcidIndex**	Proprietary method of testing total acidity of wine by using a weighted average
- **Alcohol** Alcohol Content
- **Chlorides** Chloride content of wine
- **CitricAcid** Citric Acid Content
- **Density** Density of Wine
- **FixedAcidity** Fixed Acidity of Wine
- **FreeSulfurDioxide** Sulfur Dioxide content of wine
- **LabelAppeal** Marketing Score indicating the appeal of label design for consumers. High numbers suggest customers like the label design. Negative numbers suggest customes don't like the design.
- **ResidualSugar** Residual Sugar of wine
- **STARS** Wine rating by a team of experts. 4 Stars = Excellent, 1 Star = Poor A high number of stars suggests high sales
- **Sulphates** Sulfate conten of wine
- **TotalSulfurDioxide** Total Sulfur Dioxide of Wine
- **VolatileAcidity** Volatile Acid content of wine
- **pH** pH of wine
