from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from datetime import datetime
import json
import functools
import random
from src.olympus.ml_models.knn import KNN
from src.olympus import database
import copy

class AthenaApiController():

    def classify_company():
        # Good models: KNN, RF
        knn = KNN()
        user_input = json.loads(request.data.decode('utf-8'))
        industry_map = database.get_industry()
        #user_input = json.loads(request.data.decode('utf-8'))
        # user_input = request.form.to_dict()
        # convert user input for series to %
        formatted_user_input = copy.deepcopy(user_input)
        formatted_user_input["SeriesA"] = round((user_input["SeriesA"] - user_input["Seed"])/user_input["Seed"],2) if "SeriesA" in user_input else 0
        formatted_user_input["SeriesB"] = round((user_input["SeriesB"] - user_input["SeriesA"])/user_input["SeriesA"],2) if "SeriesB" in user_input else 0
        formatted_user_input["SeriesC"] = round((user_input["SeriesC"] - user_input["SeriesB"])/user_input["SeriesB"],2) if "SeriesC" in user_input else 0
        formatted_user_input["SeriesD"] = round((user_input["SeriesD"] - user_input["SeriesC"])/user_input["SeriesC"],2) if "SeriesD" in user_input else 0
        formatted_user_input["SeriesE"] = round((user_input["SeriesE"] - user_input["SeriesD"])/user_input["SeriesD"],2) if "SeriesE" in user_input else 0
        formatted_user_input.pop("Seed")
        for i,j in industry_map.items():
            if formatted_user_input["Industry"] == j:
                formatted_user_input["Industry"] = i
                break
        classification = knn.classify(formatted_user_input,database.get_private_companies())
        print("Final output")
        print(classification)
        database.add_history(formatted_user_input,classification["Prediction"])
        series_rounds = ["Seed","SeriesA","SeriesB","SeriesC","SeriesD","SeriesE"]
        pred_next_rounds = {}
        curr_series = None
        final_valuation = 0
        if classification["Prediction"]:
            # check the current series
            for i in range(len(series_rounds)):
                if series_rounds[i] != "Seed" and formatted_user_input[series_rounds[i]] == 0:
                    if not curr_series:
                        curr_series = series_rounds[i-1]
                    growth = random.uniform(0,formatted_user_input[series_rounds[i-1]])
                    pred_next_rounds[series_rounds[i]] = growth
                    final_valuation = user_input[series_rounds[i-1]] * (1+growth)
                else:
                    if series_rounds[i] != "Seed":
                        pred_next_rounds[series_rounds[i]] = formatted_user_input[series_rounds[i]]
                        final_valuation = user_input[series_rounds[i]]
                    else:
                        pred_next_rounds["Seed"] = 0
        else:
            # check the current series
            for i in range(len(series_rounds)):
                if series_rounds[i] != "Seed" and formatted_user_input[series_rounds[i]] == 0:
                    if not curr_series:
                        curr_series = series_rounds[i-1]
                    growth = random.uniform(-1,formatted_user_input[series_rounds[i-1]])
                    pred_next_rounds[series_rounds[i]] = growth
                    final_valuation = user_input[series_rounds[i-1]] * (1+growth)
                else:
                    if series_rounds[i] != "Seed":
                        pred_next_rounds[series_rounds[i]] = formatted_user_input[series_rounds[i]]
                        final_valuation = user_input[series_rounds[i]]
                    else:
                        pred_next_rounds["Seed"] = 0
        classification["PredictedGrowth"] = pred_next_rounds
        classification["FinalValuation"] = final_valuation
        result = jsonify(classification)
        result.headers.add('Access-Control-Allow-Origin', '*')
        return result

    def avg_successful_companies_metrics():
        return jsonify(database.get_avg_successful_company_metrics())

    def avg_unsuccessful_companies_metrics():
        return jsonify(database.get_avg_unsuccessful_company_metrics())

    def get_industry_avg():
        priv_companies = database.get_private_companies()
        industry_map = database.get_industry()
        user_input = json.loads(request.data.decode('utf-8'))
        curr_industry = user_input["industry"]

        for i,j in industry_map.items():
            if curr_industry == j:
                curr_industry = i
                break
        
        series_rounds = ["Seed","SeriesA","SeriesB","SeriesC","SeriesD","SeriesE"]
        curr_round = {}
        for i in range(len(series_rounds)):
            if user_input[series_rounds[i]] == 0:
                curr_round["Series"] = series_rounds[i-1]
                curr_round["Growth"] = round((user_input[series_rounds[i-1]] - user_input[series_rounds[i-2]]) / user_input[series_rounds[i-2]],2)
                break
        seriesSum = 0
        seriesCounter = 0
        companyCounter = 0
        peRatioSum = 0
        arrSum = 0
        grossMarginSum = 0
        schRankingSum = 0
        for i,j in priv_companies.items():
            if j["Success"] and j["Industry"] == curr_industry:
                seriesSum += j[curr_round["Series"]]
                seriesCounter += 1 if j[curr_round["Series"]] else 0
                companyCounter += 1
                peRatioSum += j["PeRatio"]
                arrSum += j["AnnualRecurringRevenueGrowthRate"]
                grossMarginSum += j["GrossMargin"]
                schRankingSum += j["SchRanking"]
        toSend = {
            "AvgGrowthForRound":round(seriesSum/seriesCounter,2),
            "CurrentCompanyGrowth":curr_round["Growth"],
            "AvgPeRatio":round(peRatioSum/companyCounter,2),
            "AvgARR":round(arrSum/companyCounter,2),
            "AvgGrossMargin":round(grossMarginSum/companyCounter,2),
            "AvgSchRanking":round(schRankingSum/companyCounter,2)
        }
        return jsonify(toSend)

    def get_all_industry_avg():
        priv_companies = database.get_private_companies()
        industry_map = database.get_industry()
        toSend = {
            "sSeriesA": 0,
            "sSeriesB": 0,
            "sSeriesC": 0,
            "sSeriesD": 0,
            "sSeriesE": 0,
            "sCounter": 0,
            "uSeriesA": 0,
            "uSeriesB": 0,
            "uSeriesC": 0,
            "uSeriesD": 0,
            "uSeriesE": 0,
            "uCounter": 0,
        }
        sSeriesACounter = 0
        sSeriesBCounter = 0
        sSeriesCCounter = 0
        sSeriesDCounter = 0
        sSeriesECounter = 0
        uSeriesACounter = 0
        uSeriesBCounter = 0
        uSeriesCCounter = 0
        uSeriesDCounter = 0
        uSeriesECounter = 0
        industry_metric = {}
        for i,j in priv_companies.items():
            if j["Success"]:
                toSend["sSeriesA"] += j["SeriesA"]
                sSeriesACounter += 1 if j["SeriesA"] else 0
                toSend["sSeriesB"] += j["SeriesB"]
                sSeriesBCounter += 1 if j["SeriesB"] else 0
                toSend["sSeriesC"] += j["SeriesC"]
                sSeriesCCounter += 1 if j["SeriesC"] else 0
                toSend["sSeriesD"] += j["SeriesD"]
                sSeriesDCounter += 1 if j["SeriesD"] else 0
                toSend["sSeriesE"] += j["SeriesE"]
                sSeriesECounter += 1 if j["SeriesE"] else 0
                toSend["sCounter"] += 1
                if industry_map[j["Industry"]] not in industry_metric:
                    industry_metric[industry_map[j["Industry"]]] = {
                        "sSeriesA" : j["SeriesA"],
                        "sSeriesACounter" : 1 if j["SeriesA"] else 0,
                        "sSeriesB" : j["SeriesB"],
                        "sSeriesBCounter" : 1 if j["SeriesB"] else 0,
                        "sSeriesC" : j["SeriesC"],
                        "sSeriesCCounter" : 1 if j["SeriesC"] else 0,
                        "sSeriesD" : j["SeriesD"],
                        "sSeriesDCounter" : 1 if j["SeriesD"] else 0,
                        "sSeriesE" : j["SeriesE"],
                        "sSeriesECounter" : 1 if j["SeriesE"] else 0,
                        "sCounter" : 1,
                        "uSeriesA" : 0,
                        "uSeriesACounter" : 0,
                        "uSeriesB" : 0,
                        "uSeriesBCounter" : 0,
                        "uSeriesC" : 0,
                        "uSeriesCCounter" : 0,
                        "uSeriesD" : 0,
                        "uSeriesDCounter" : 0,
                        "uSeriesE" : 0,
                        "uSeriesECounter" : 0,
                        "uCounter" : 0
                    }
                else:
                    industry_metric[industry_map[j["Industry"]]]["sSeriesA"] += j["SeriesA"]
                    industry_metric[industry_map[j["Industry"]]]["sSeriesACounter"] += 1 if j["SeriesA"] else 0
                    industry_metric[industry_map[j["Industry"]]]["sSeriesB"] += j["SeriesB"]
                    industry_metric[industry_map[j["Industry"]]]["sSeriesBCounter"] += 1 if j["SeriesB"] else 0
                    industry_metric[industry_map[j["Industry"]]]["sSeriesC"] += j["SeriesC"]
                    industry_metric[industry_map[j["Industry"]]]["sSeriesCCounter"] += 1 if j["SeriesC"] else 0
                    industry_metric[industry_map[j["Industry"]]]["sSeriesD"] += j["SeriesD"]
                    industry_metric[industry_map[j["Industry"]]]["sSeriesDCounter"] += 1 if j["SeriesD"] else 0
                    industry_metric[industry_map[j["Industry"]]]["sSeriesE"] += j["SeriesE"]
                    industry_metric[industry_map[j["Industry"]]]["sSeriesECounter"] += 1 if j["SeriesE"] else 0
                    industry_metric[industry_map[j["Industry"]]]["sCounter"] += 1
            else:
                toSend["uSeriesA"] += j["SeriesA"]
                uSeriesACounter += 1 if j["SeriesA"] else 0
                toSend["uSeriesB"] += j["SeriesB"]
                uSeriesBCounter += 1 if j["SeriesB"] else 0
                toSend["uSeriesC"] += j["SeriesC"]
                uSeriesCCounter += 1 if j["SeriesC"] else 0
                toSend["uSeriesD"] += j["SeriesD"]
                uSeriesDCounter += 1 if j["SeriesD"] else 0
                toSend["uSeriesE"] += j["SeriesE"]
                uSeriesECounter += 1 if j["SeriesE"] else 0
                toSend["uCounter"] += 1
                if industry_map[j["Industry"]] not in industry_metric:
                    industry_metric[industry_map[j["Industry"]]] = {
                        "sSeriesA" : 0,
                        "sSeriesACounter" : 0,
                        "sSeriesB" : 0,
                        "sSeriesBCounter" : 0,
                        "sSeriesC" : 0,
                        "sSeriesCCounter" : 0,
                        "sSeriesD" : 0,
                        "sSeriesDCounter" : 0,
                        "sSeriesE" : 0,
                        "sSeriesECounter" : 0,
                        "sCounter" : 0,
                        "uSeriesA" : j["SeriesA"],
                        "uSeriesACounter" : 1 if j["SeriesA"] else 0,
                        "uSeriesB" : j["SeriesB"],
                        "uSeriesBCounter" : 1 if j["SeriesB"] else 0,
                        "uSeriesC" : j["SeriesC"],
                        "uSeriesCCounter" : 1 if j["SeriesC"] else 0,
                        "uSeriesD" : j["SeriesD"],
                        "uSeriesDCounter" : 1 if j["SeriesD"] else 0,
                        "uSeriesE" : j["SeriesE"],
                        "uSeriesECounter" : 1 if j["SeriesE"] else 0,
                        "uCounter" : 1
                    }
                else:
                    industry_metric[industry_map[j["Industry"]]]["uSeriesA"] += j["SeriesA"]
                    industry_metric[industry_map[j["Industry"]]]["uSeriesACounter"] += 1 if j["SeriesA"] else 0
                    industry_metric[industry_map[j["Industry"]]]["uSeriesB"] += j["SeriesB"]
                    industry_metric[industry_map[j["Industry"]]]["uSeriesBCounter"] += 1 if j["SeriesB"] else 0
                    industry_metric[industry_map[j["Industry"]]]["uSeriesC"] += j["SeriesC"]
                    industry_metric[industry_map[j["Industry"]]]["uSeriesCCounter"] += 1 if j["SeriesC"] else 0
                    industry_metric[industry_map[j["Industry"]]]["uSeriesD"] += j["SeriesD"]
                    industry_metric[industry_map[j["Industry"]]]["uSeriesDCounter"] += 1 if j["SeriesD"] else 0
                    industry_metric[industry_map[j["Industry"]]]["uSeriesE"] += j["SeriesE"]
                    industry_metric[industry_map[j["Industry"]]]["uSeriesECounter"] += 1 if j["SeriesE"] else 0
                    industry_metric[industry_map[j["Industry"]]]["uCounter"] += 1
        
        toSend["sSeriesA"] = round(toSend["sSeriesA"]/sSeriesACounter,2)
        toSend["sSeriesB"] = round(toSend["sSeriesB"]/sSeriesBCounter,2)
        toSend["sSeriesC"] = round(toSend["sSeriesC"]/sSeriesCCounter,2)
        toSend["sSeriesD"] = round(toSend["sSeriesD"]/sSeriesDCounter,2)
        toSend["sSeriesE"] = round(toSend["sSeriesE"]/sSeriesECounter,2)
        toSend["uSeriesA"] = round(toSend["uSeriesA"]/uSeriesACounter,2)
        toSend["uSeriesB"] = round(toSend["uSeriesB"]/uSeriesBCounter,2)
        toSend["uSeriesC"] = round(toSend["uSeriesC"]/uSeriesCCounter,2)
        toSend["uSeriesD"] = round(toSend["uSeriesD"]/uSeriesDCounter,2)
        toSend["uSeriesE"] = round(toSend["uSeriesE"]/uSeriesECounter,2)
        print(industry_metric)
        for i,j in industry_metric.items():
            j["sSeriesA"] = round(j["sSeriesA"]/j["sSeriesACounter"],2)
            j["sSeriesB"] = round(j["sSeriesB"]/j["sSeriesBCounter"],2)
            j["sSeriesC"] = round(j["sSeriesC"]/j["sSeriesCCounter"],2)
            j["sSeriesD"] = round(j["sSeriesD"]/j["sSeriesDCounter"],2)
            j["sSeriesE"] = round(j["sSeriesE"]/j["sSeriesECounter"],2)
            j["uSeriesA"] = round(j["uSeriesA"]/j["uSeriesACounter"],2)
            j["uSeriesB"] = round(j["uSeriesB"]/j["uSeriesBCounter"],2)
            j["uSeriesC"] = round(j["uSeriesC"]/j["uSeriesCCounter"],2)
            j["uSeriesD"] = round(j["uSeriesD"]/j["uSeriesDCounter"],2)
            j["uSeriesE"] = round(j["uSeriesE"]/j["uSeriesECounter"],2)
        toSend["IndustryMetrics"] = industry_metric
        
        return jsonify(toSend)
        







