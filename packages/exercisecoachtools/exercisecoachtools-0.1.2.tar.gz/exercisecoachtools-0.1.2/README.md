[![Build Status](https://travis-ci.com/chandojo/ExerciseCoachTools.svg?branch=master)](https://travis-ci.com/chandojo/ExerciseCoachTools)

# Exercise Coach Tools

Exercise Coach Tools is an open source library of tools for fitness/exercise coaches, fitness specialists, exercise physiologists, and personal trainers.  The objective of Exercise Coach Tools is to help these people be more efficient and spend more time focusing on their clients instead of the equations/formulas needed to make analyses.

## Table of Contents
1. [Getting Started](#gettingstarted)
2. [ACSM Risk Stratification](#acsmriskstratification)
3. [Percentage Calculators](#percentagecalculators)
4. [Metabolic Rate Calculators](#metabolicratecalculators)
5. [Testing](#testing)

## Getting Started <a name="gettingstarted"></a>
### Prerequisites

This package requires **>= Python 3.7.4**

### Installing

`pip install exercisecoachtools`

## ACSM Risk Stratification <a name="acsmriskstratification"></a>
This is a tool for determining risk of cardiovascular disease based on *ACSM’s Guidelines for Exercise Testing and Prescription-8th ed. Philadelphia: Lippincott Williams & Wilkins*

This tool is not a substitute for advice from a doctor and is used to help fitness specialists refer potential clients to physicians due to possible cardiovascular health risk.

### Using the Stratification
A `Patient` object must be created to use methods.

`Patient` takes the following parameters in the order listed:
- sex (str *male or female*)
- age (int *positive only*)
- smoker (str *yes or no*)
- sedentary (str *yes or no*)
- bmi (str *yes or no* ; input *0* if no available value but waist_girth value is available )
- waist_girth (int *positive only* ; input *0* if no available value but bmi value is available)
- male_family_death_before_55 (str *yes or no*)
- female_family_death_before_65 (str *yes or no*)
- systolic (int *positive only*)
- diastolic (int *positive only*)
- hypertensive (str *yes or no*)
- ldl (int *positive only*)
- hdl (int *positive only*)
- using_lipid_lowering_medication (str *yes or no*)
- cholesterol (int *positive only*)
- fasting_glucose (int *positive only* ; input *0* if no available value but oral_glucose_tolerance value is available)
- oral_glucose_tolerance (int *positive only* ; input *0* if no available value but fasting_glucose value is available)

**Useful functions:**
- `risk_classification(Patient)`
  - Returns patient's risk classification based off of the ACSM Guidelines. Classifications range from low, moderate, and high.
- `total_risk_factors(Patient)`
  - Returns patient's net total risk factors. This total is based off of ACSM's algorithm.


#### Examples
```
from risk.risk_stratification import Patient, risk_classification, total_risk_factors

steve_buscemi = Patient('male', 61, 'no', 'yes', 25, 0, 'yes', 'no', 119, 78, 'no', 100, 70, 'no', 100, 60, 0)

risk_classification(steve_buscemi)
# 'Your risk total is 2. You are at a moderate risk for cardiovascular disease. Medical check-up recommended for participation in vigorous physical activity.'

total_risk_factors(steve_buscemi)
# returns 2

```

## Percentage Calculators <a name="percentagecalculators"></a>

**Useful functions:**
- `percentage_value(desired_percentage, 1_rep_max_weight)`
  - Returns weight value associated with desired percentage. Can use kg or lbs
- `one_rep_max_estimation(reps completed, weight)`
  - Returns dictionary of estimated 1-rep max using Brzycki, Epley, Mayhew, Lander, and Lombardi formulas
  - Note: Reps completed **must be** > 1

#### Examples

```
from percentage_calculators.percentage_calculators import percentage_value

percentage_value(80, 100)
# returns 80.0
```

```
from percentage_calculators.one_rep_max_estimation import one_rep_max_estimation

one_rep_max_estimation(2, 100)
# returns {'brzycki_formula': 102.85949393128985, 'epley_formula': 106.66666666666667, 'mayhew_formula': 106.41304152560984, 'lander_formula': 104.21275910157765, 'lombardi_formula': 107.17734625362931}
```

## Metabolic Rate Calculators <a name="metabolicratecalculators"></a>

A `MetabolicClient` object must be created to use methods.

`MetabolicClient` takes the following parameters in the order listed:
- sex (str *male or female*)
- age (int *positive only*)
- weight (pounds - float *positive only*)
- height (inches - float *positive only*)

**Useful functions:**
- `bmr_results(MetabolicClient)`
  - Returns client's estimated BMR using Harris-Benedict and Mifflin formulas
- `harris_benedict_bmr(MetabolicClient)`
  - Returns client's estimated BMR using Harris-Benedict formula
- `mifflin_bmr(MetabolicClient)`
  - Returns client's estimated BMR using Mifflin St Jeor formula

- `get_calories_by_activity(activity_level, bmr)`
  - Returns client's daily metabolic rate based on activity level
  - Activity level options:
      - Sedentary — desk job and little to no exercise
      - Lightly Active — light exercise/sports 1–3 days/week
      - Moderately Active — moderate exercise/sports 3–5 days/week
      - Very Active — hard exercise/sports 6–7 days/week
      - Extremely Active — hard daily exercise/sports and physical job or training


#### Examples
```
from kcal.metabolic_rate_prediction import MetabolicClient, bmr_results, harris_benedict_bmr, mifflin_bmr
from kcal.daily_kcal_by_lifestyle import get_calories_by_activity

sue_bird = MetabolicClient('female', 39, 150, 69)

bmr_results(sue_bird)
# returns {'harris_benedict_bmr': 974.5799999999999, 'mifflin_st_jeor_bmr': 826.6300000000001}

sue_bird_bmr = harris_benedict_bmr(sue_bird)
# returns 974.5799999999999

mifflin_bmr(sue_bird)
# returns 826.6300000000001

get_calories_by_activity('very active', sue_bird_bmr)
# returns 1681.1505 (kcal/day)
```

## Running the tests <a name="testing"></a>
`python setup.py test`

## Authors
chandojo
