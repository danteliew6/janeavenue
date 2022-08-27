from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import os

class RF():
    def __init__(self) -> None:
        self.model = RandomForestClassifier(n_estimators=200, criterion="entropy", max_depth=10, random_state=38)
        self.data = None
        self.X = None
        self.y = None

    def load_data(self,df) -> None:
        self.data = df
        self.X = df[["YearFounded","CurrentValuation","InitialValuation","Industry","NumCompetitors","SeriesA","SeriesB","SeriesC","SeriesD","SeriesE"]]
        self.y = df["Success"]
    
    def classify(self,user_input,df) -> bool:
        self.load_data(df)
        self.model.fit(self.X,self.y)
        # convert user input into dataframe
        my_df = {}
        for i,j in user_input.items():
            my_df[i] = [j]
        new_df = pd.DataFrame(data=my_df)
        classification = self.model.predict(new_df)
        return True if classification[0] else False 

# Data
# data = pd.read_csv(os.getcwd() + "/ml_models/data/sample_data_num.csv")

# X = data[["YearFounded","CurrentValuation","InitialValuation","Industry","NumCompetitors","SeriesA","SeriesB","SeriesC","SeriesD","SeriesE"]]
# y = data["Success"]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# rf = RandomForestClassifier(n_estimators=200, criterion="entropy", max_depth=10, random_state=38)
# rf.fit(X_train,y_train)
# d = {"YearFounded":[2013],"CurrentValuation":[300],"InitialValuation":[20],"Industry":[1],"NumCompetitors":[18],"SeriesA":[2],"SeriesB":[1.5],"SeriesC":[0.67],"SeriesD":[0.08],"SeriesE":[0.11]}
# new_d = pd.DataFrame(data=d)
# print(new_d)
# y_pred=rf.predict(new_d)
# print(y_pred)

# Model Accuracy, how often is the classifier correct?
# print("Accuracy:",metrics.accuracy_score(y_test, y_pred))