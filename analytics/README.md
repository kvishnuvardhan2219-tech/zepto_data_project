# Module 2 - Analytics pipeline

This is Titanic analysis for Module 2. I loaded the dataset using seaborn, cleaned it, explored it with some charts, and then built a few models to predict who survived.
I also did a small-task predicting ticket fare using Linear regression.

## How to run :

you need these to be installed:
```bash
pip install pandas seaborn scikit-learn joblib matplotlib
```
open 'analytics/module_2.ipynb' and run all the cells from top to bottom. It'll create 'titanic.csv', Save all the chat images , and save the trained model as a '.joblib' file.

## Missing values - what I did and why

I checked each column for missing data and found 4 columns with gaps:
- 'embarked' was missing 0.22% and 'embark_town' was missing 0.22% - since both were under 5%, I dropped those rows. It was only 2 rows out of 889, So barely any data lost.
- 'age' was missing 19%, Which falls in 5% - 30% range, So i filled the gaps with the median age instead of dropping anything.
- 'deck' was missing  huge 77% of the time - way too much to reliably fill in so dropped whole column, and decided to label the missing columns as 'unknown' and keep the column.

- ## Fare distrubition

- Looking at fare: mean is 32.10, Median was 14,45, and mode is 8.05. since mean > median > mode, that fare is **right-skewed** - most tickets were cheap, but a handful of really expensive tickets pull the average up higher than the typical value.

- For outliers (using the IQR rule), age had 65 outliers and fare had 114.

- ## Correlation findings

- I built a correlation matrix using the 6 numeric columns and made a heatmap. The 2 strongest i found were:

- **pclass and fare (-0.55)** - makes sense, since 1st class (pclass=1) passengers paid way more, so lower pclass number goes with higher fare.
- **sibsp and parch (+0.41)** - people travelling with sibling/spouses also tended to have children wit them too, which lines up with families travelling together.

## About charts
1. **survival by sex** - women survived way more than men (about 74% vs 19%). This is basically the "women and children first" thing playing out in the data.
2. **survival by class** - 1st class passengers survived more than 2nd and 3rd class. Richer passengers had better odds.
3. **Age vs survival** - survivors were slightly younger on average, and I could some young kids among the survivors, which hints kids may have been prioritized a bit too.
4. **class + sex together** - this one was the most dramatic. 1st/2nd class women survived over 90% of the time, but 3rd class men only survived about 14% of the time. So being poor and male was the worst combination.
5. **Fare vs age colored by survival** - survivors clustered more toward higher fares. Age didn't really seperate surviours from non-survivors much, so fare/class mattered a lot more than age.

6. ## Standardizing age and fare

7. I converted age and fare into z-scores just to prove i could do it and that it works - before standarddizing, age had mean 29.32/std 12.98 and fare has mean 32.10/std 49.70. After standardizing, both has mean -0 and -1, which is supposed to happen. That wasn't used anywhere else, just a quick sanity check.

8. ## Why i used a stratified split

9. Since survival rate in the dataset is about 38% survived vs 62% not survived, that a bit imbalanced. If i did a regular random split, I could end up with a test set accidentally has a very different survival ratio than the training set, which would mess up how i evaluate the model. using 'stratify' keeps the same -38/62 ratio i both train and test.

10. ## Preprocessing choices

11. For missing values in the modeling pipeline, I used median for numeric columns and most-frequent for categorical columns - similar idea to before but this time it's built into a proper scikit-learn pipeline so its automatically fit only on training data. I used one-hot encoding for sex and embarked, and standardscalar for the numeric features.

12. ## Model results

13. 
