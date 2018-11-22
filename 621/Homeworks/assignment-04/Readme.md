# Homework #4

## Overview

In this homework assignment, you will explore, analyze and model a data set containing approximately $8000$ records representing a customer at an auto insurance company. Each record has two response variables. The first response variable, **TARGET_FLAG**, is a $1$ or a $0$. A "$1$" means that the person was in a car crash. A zero means that the person was not in a car crash. The second response variable is **TARGET_AMT**. This value is zero if the person did not crash their car. But if they did crash their car, this number will be a value greater than zero.

## Objective

Your objective is to build multiple linear regression and binary logistic regression models on the training data to predict the probability that a person will crash their car and also the amount of money it will cost if the person does crash their car. You can only use the variables given to you (or variables that you derive from the variables provided).

## Description

Below is a short description of the variables of interest in the data set:

- **INDEX**	Identification Variable (do not use)
- **TARGET_FLAG**	Was Car in a crash? 1=YES 0=NO
- **TARGET_AMT**	If car was in a crash, what was the cost
- **AGE**	Age of Driver
- **BLUEBOOK**	Value of Vehicle
- **CAR_AGE**	Vehicle Age
- **CAR_TYPE**	Type of Car
- **CAR_USE**	Vehicle Use
- **CLM_FREQ**	# Claims (Past 5 Years)
- **EDUCATION**	Max Education Level
- **HOMEKIDS**	# Children at Home
- **HOME_VAL**	Home Value
- **INCOME**	Income
- **JOB**	Job Category
- **KIDSDRIV**	# Driving Children
- **MSTATUS**	Marital Status
- **MVR_PTS**	Motor Vehicle Record Points
- **OLDCLAIM**	Total Claims (Past 5 Years)
- **PARENT1**	Single Parent
- **RED_CAR**	A Red Car
- **REVOKED**	License Revoked (Past 7 Years)
- **SEX**	Gender
- **TIF**	Time in Force
- **TRAVTIME**	Distance to Work
- **URBANICITY**	Home/Work Area
- **YOJ**	Years on Job

