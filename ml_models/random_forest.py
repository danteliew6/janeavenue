from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import os

# Data
data = pd.read_csv(os.getcwd() + "/ml_models/data/sample_data_num.csv")

X = data[["YearFounded","CurrentValuation","InitialValuation","Industry","NumCompetitors","SeriesA","SeriesB","SeriesC","SeriesD","SeriesE"]]
y = data["Success"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

rf = RandomForestClassifier(n_estimators=200, criterion="entropy", max_depth=10, random_state=38)
rf.fit(X_train,y_train)
y_pred=rf.predict(X_test)

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))