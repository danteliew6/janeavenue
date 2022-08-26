from flask import Blueprint
from ..controllers.HermesApiController import HermesApiController


api_bp = Blueprint("api_bp", __name__)

# class_bp.route('/classlist', methods=['GET'])(ClassController.getClassList)
api_bp.route('/get-all-investments', methods=['GET'])(HermesApiController.getAllInvestments)
api_bp.route('/deposit', methods=['POST'])(HermesApiController.addDeposit)
# api_bp.route('/add-matches', methods=['POST'])(MatchController.addMatches)
# api_bp.route('/get-team-rankings', methods=['GET'])(MatchController.getTeamRankings)
# api_bp.route('/delete-competition-data', methods=['DELETE'])(MatchController.deleteCompetitionData)




