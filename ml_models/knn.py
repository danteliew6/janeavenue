from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import os

class KNN():
    def __init__(self) -> None:
        self.model = KNeighborsClassifier(n_neighbors=3)
        self.data = None
        self.X = None
        self.y = None

    def load_data(self,priv_comp) -> None:
        df = pd.DataFrame(data=priv_comp)
        df = df.T
        self.data = df
        self.X = df[["YearFounded","CurrentValuation","InitialValuation","Industry","NumCompetitors","SeriesA","SeriesB","SeriesC","SeriesD","SeriesE"]]
        self.y = df["Success"]
        print(self.X)
        print(self.y)
    
    def classify(self,user_input,priv_comp) -> bool:
        self.load_data(priv_comp)
        self.model.fit(self.X,self.y)
        # convert user input into dataframe
        my_df = {}
        for i,j in user_input.items():
            my_df[i] = [j]
        new_df = pd.DataFrame(data=my_df)
        classification = self.model.predict(new_df)
        print(classification)
        return True if classification[0] else False 


# Data
data = pd.read_csv(os.getcwd() + "/ml_models/data/sample_data_num.csv")
data.set_index("CompanyName",inplace=True)
data.to_json("company_data.json",orient="index")
# X = data[["YearFounded","CurrentValuation","InitialValuation","Industry","NumCompetitors","SeriesA","SeriesB","SeriesC","SeriesD","SeriesE"]]
# y = data["Success"]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

# clf = KNeighborsClassifier(n_neighbors=3)
# clf.fit(X_train, y_train)
# da = {"YearFounded":2013,"CurrentValuation":300,"InitialValuation":20,"Industry":1,"NumCompetitors":18,"SeriesA":2,"SeriesB":1.5,"SeriesC":0.67,"SeriesD":0.08,"SeriesE":0.11}
# d = {"YearFounded":[2013],"CurrentValuation":[300],"InitialValuation":[20],"Industry":[1],"NumCompetitors":[18],"SeriesA":[2],"SeriesB":[1.5],"SeriesC":[0.67],"SeriesD":[0.08],"SeriesE":[0.11]}
# print(new_d)
# y_pred=clf.predict(new_d)
# print(y_pred)

# Model Accuracy, how often is the classifier correct?
# print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
# print(y_test)
# print(y_pred)

# knn = KNN()
# print(knn.classify(d,pd.read_csv(os.getcwd() + "/ml_models/data/sample_data_num.csv")))

# d = {"CompanyA":{"YearFounded":2013,"CurrentValuation":300,"InitialValuation":20,"Industry":1,"NumCompetitors":18,"SeriesA":2,"SeriesB":1.5,"SeriesC":0.67,"SeriesD":0.08,"SeriesE":0.11,"Success":0},"CompanyB":{"YearFounded":2013,"CurrentValuation":400,"InitialValuation":10,"Industry":0,"NumCompetitors":14,"SeriesA":2,"SeriesB":2.5,"SeriesC":0.57,"SeriesD":0.08,"SeriesE":0.11,"Success":0},
# "CompanyC":{"YearFounded":2013,"CurrentValuation":300,"InitialValuation":20,"Industry":1,"NumCompetitors":18,"SeriesA":2,"SeriesB":1.5,"SeriesC":0.67,"SeriesD":0.08,"SeriesE":0.11,"Success":0},"CompanyD":{"YearFounded":2013,"CurrentValuation":400,"InitialValuation":10,"Industry":0,"NumCompetitors":14,"SeriesA":2,"SeriesB":2.5,"SeriesC":0.57,"SeriesD":0.08,"SeriesE":0.11,"Success":0}}
# asd = pd.DataFrame(data=d)
# asd = asd.T
# print(asd)

# knn = KNN()
# print(knn.classify(da,d))