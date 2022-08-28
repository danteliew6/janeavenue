from flask import Blueprint
from flask_cors import CORS, cross_origin
from ..controllers.HermesApiController import HermesApiController
from ..controllers.AthenaApiController import AthenaApiController


api_bp = Blueprint("api_bp", __name__)
CORS(api_bp)


# class_bp.route('/classlist', methods=['GET'])(ClassController.getClassList)
api_bp.route('/get-all-investments', methods=['GET'])(HermesApiController.getAllInvestments)
api_bp.route('/deposit', methods=['POST'])(HermesApiController.addDeposit)
api_bp.route('/withdraw', methods=['POST'])(HermesApiController.withdrawDeposit)
api_bp.route('/get-user-investments/<name>', methods=['GET'])(HermesApiController.getUserInvestments)
api_bp.route('/toggle-fund-selection', methods=['GET'])(HermesApiController.toggleFundSelection)

api_bp.route('/athena/classify', methods=['POST'])(AthenaApiController.classify_company)
api_bp.route('/athena/avgsuccessfulmetrics', methods=['GET'])(AthenaApiController.avg_successful_companies_metrics)
api_bp.route('/athena/avgunsuccessfulmetrics', methods=['GET'])(AthenaApiController.avg_unsuccessful_companies_metrics)
api_bp.route('/athena/all-industry-average', methods=['GET'])(AthenaApiController.get_all_industry_avg)
api_bp.route('/athena/get-industry-average', methods=['POST'])(AthenaApiController.get_industry_avg)

# api_bp.route('/add-matches', methods=['POST'])(MatchController.addMatches)
# api_bp.route('/get-team-rankings', methods=['GET'])(MatchController.getTeamRankings)
# api_bp.route('/delete-competition-data', methods=['DELETE'])(MatchController.deleteCompetitionData)




