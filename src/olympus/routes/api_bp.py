from flask import Blueprint
from ..controllers.HermesApiController import HermesApiController
from ..controllers.AthenaApiController import AthenaApiController


api_bp = Blueprint("api_bp", __name__)

# class_bp.route('/classlist', methods=['GET'])(ClassController.getClassList)
api_bp.route('/get-all-investments', methods=['GET'])(HermesApiController.getAllInvestments)
api_bp.route('/deposit', methods=['POST'])(HermesApiController.addDeposit)
api_bp.route('/withdraw', methods=['POST'])(HermesApiController.withdrawDeposit)

api_bp.route('/athena/classify', methods=['POST'])(AthenaApiController.classify_company)
api_bp.route('/athena/avgsuccessfulmetrics', methods=['POST'])(AthenaApiController.avg_successful_companies_metrics)
api_bp.route('/athena/avgunsuccessfulmetrics', methods=['POST'])(AthenaApiController.avg_unsuccessful_companies_metrics)
api_bp.route('/athena/classify', methods=['POST'])(AthenaApiController.classify_company)


# api_bp.route('/add-matches', methods=['POST'])(MatchController.addMatches)
# api_bp.route('/get-team-rankings', methods=['GET'])(MatchController.getTeamRankings)
# api_bp.route('/delete-competition-data', methods=['DELETE'])(MatchController.deleteCompetitionData)




