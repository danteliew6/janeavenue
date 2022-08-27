import xgboost as XGBRegressor
from sklearn.model_selection import cross_val_score


#scores = cross_val_score(XGBRegressor(), X, y, scoring='neg_mean_squared_error')