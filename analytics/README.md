# Module 2 - Analytics pipeline

This is Titanic analysis for Module 2. I loaded the dataset using seaborn, cleaned it, explored it with some charts, and then built a few models to predict who survived.
I also did a small-task predicting ticket fare using Linear regression.

## How to run :

you need these to be installed:
```bash
pip install pandas seaborn scikit-learn imbalanced=learn joblib matplotlib
```
open 'analytics/module_2.ipynb' and run all the cells from top to bottom. It'll create 'titanic.csv', Save all the chat images , and save the trained model as a '.joblib' file.

## Missing values - what I did and why

I checked each column for missing data and found 4 columns with gaps:
- 'embarked' was missing 0.22% and 'embark_town' was missing 0.22% - since both were under 5%, I dropped those rows. It was only 2 rows out of 889, So barely any data lost.
- 'age' was missing 19.87%, Which falls in 5%-30% range, So i filled the gaps with the median age instead of dropping anything.
- "'deck' was missing a huge 77% of the time - way too much to reliably fill in. Instead of dropping the whole column, I decided to label the missing columns as 'unknown' and keep the column, Since it might still carry some signal."

- ## Fare distrubition

- Looking at fare: mean is 32.10, Median was 14.45, and mode is 8.05. since mean > median > mode, that fare is **right-skewed** - most tickets were cheap, but a handful of really expensive tickets pull the average up higher than the typical value.

- For outliers (using the IQR rule), age had 65 outliers and fare had 114.

- ## Correlation findings

- I built a correlation matrix using the 6 numeric columns and made a heatmap. The 2 strongest i found were:

- **pclass and fare (0.55)** - makes sense, since 1st class (pclass=1) passengers paid way more, so lower pclass number goes with higher fare.
- **sibsp and parch (+0.41)** - people travelling with sibling/spouses also tended to have children wit them too, which lines up with families travelling together.

## About charts
1. **survival by sex** - women survived way more than men (about 74% vs 19%). This is basically the "women and children first" thing playing out in the data.
2. **survival by class** - 1st class passengers survived more than 2nd and 3rd class. Richer passengers had better odds.
3. **Age vs survival** - survivors were slightly younger on average, and I could some young kids among the survivors, which hints kids may have been prioritized a bit too.
4. **class + sex together** - this one was the most dramatic. 1st/2nd class women survived over 90% of the time, but 3rd class men only survived about 14% of the time. So being poor and male was the worst combination.
5. **Fare vs age colored by survival** - survivors clustered more toward higher fares. Age didn't really seperate surviours from non-survivors much, so fare/class mattered a lot more than age.

## Standardizing age and fare

I converted age and fare into z-scores just to prove i could do it and that it works - before standarddizing, age had mean 29.32/std 12.98 and fare has mean 32.10/std 49.70. After standardizing, both has mean -0 and -1, which is supposed to happen. That wasn't used anywhere else, just a quick sanity check.

## Why i used a stratified split

Since survival rate in the dataset is about 38% survived vs 62% not survived, that a bit imbalanced. If i did a regular random split, I could end up with a test set accidentally has a very different survival ratio than the training set, which would mess up how i evaluate the model. using 'stratify' keeps the same -38/62 ratio i both train and test.

## Preprocessing choices

For missing values in the modeling pipeline, I used median for numeric columns and most-frequent for categorical columns - similar idea to before but this time it's built into a proper scikit-learn pipeline so its automatically fit only on training data. I used one-hot encoding for sex and embarked, and standardscalar for the numeric features.

## Model results

| Model | Accuracy | Precision | Recall | F1 | AUC |
|---|---|---|---|---|---|
| Logistic Regression | 0.8090 | 0.7833 |0.6912 | 0.7344 | 0.8610 |
| Decision Tree | 0.8090 | 0.8148 | 0.6471 | 0.7213 | 0.8560 |
| Random Forest | 0.8202 | 0.7812 | 0.7353 | 0.7576 | 0.8179 |

## Handling the class imbalance 

I compared 3 ways of dealing with the survived/not-survived imbalance:

| Strategy | Precision | Recall | F1 |
|---|---|---|---|
| Baseline | 0.7833 | 0.6912 | 0.7344 |
| class_weight = 'balanced | 0.7183 | 0.7500 | 0.7338 |
| SMOTE (train only) | 0.7353 | 0.7353 | 0.7353 |

SMOTE ended up being the best pick since it had highest F1 score - it balances precision and recall better than the other 2 options. The baseline was more precise but missed more survivors, and class_weigth caught more survivors but had more false alarms.

## Hyperparameter tuning 

Ran GridSearchCV on the Random Forest and got these as the best settings: 'max_depth=5', max_features='sqrt', 'n_estimators=50'. Best cross-validation accuracy was 0.8214, and the OOB score was 0.8172, Which is close to the CV score = that's a good sign the model isn't overfitting.

## Regression side-task: predicting fare

| Metric | Value |
|---|---|
| MAE | 21.0986 |
| RMSE | 41.7021 |
| R2 | 0.3482 |
| Adjusted R2 | 0.3091 |

## Final recommendation 

I'd go with **Random Forest** as the model to actually use It had the best accuracy, best recall, and best F1 score out of the three models, so it does the best job over all at catching actual survivors without too many wrong guesses. Logistic regression technically had a slightly better AUC score, but Random Forest performed better on the metrics that matter more for a real prediction task. It also went through hyperparameter tuning, so I'm fairly confident it should generalize well to new data too.

## saved model

The final trained pipeline is saved as 'titanic_full_pipeline.joblib'. I tested reloading it and running it on raw, un-preprocessed data, and it predicted correctly = so it's ready to be resued without needing to rebuild any of the preprocessing steps.
