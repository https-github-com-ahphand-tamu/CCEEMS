import logging
from datetime import datetime

from flask import Blueprint, request, jsonify, render_template
from flask_login import current_user
from sqlalchemy import text

from app import db

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/get_years', methods = ['GET'])
def get_year_graphs():
    year_data = []
    query_for_get_years = """
    select distinct(extract(year from outreach_date)) as year from cases order by year desc;
    """
    with db.engine.connect() as connection:
        result_get_years = connection.execute(
            text(query_for_get_years))
        for row in result_get_years:
            year_data.append(row[0])

    return jsonify({
        'message': 'success',
        'data': year_data
    }), 200

@analytics_bp.route('/analytics/packets_sent', methods=['GET'])
def get_packets_sent_graph():
    year = request.args.get('year')
    month_data = [0] * 12
    query_for_sent_packets = f"""
        select extract(month from outreach_date) as month, count(id) from cases where 
        extract(year from outreach_date) = '{year}' group by month;
        """
    
    with db.engine.connect() as connection:
        result_sent_packets = connection.execute(
            text(query_for_sent_packets))
        for row in result_sent_packets:
            month_data[int(row[0]) - 1] = row[1]
        
    return jsonify({
        'message': 'success',
        'data': month_data
    }), 200

@analytics_bp.route('/analytics/packets_status', methods=['GET'])
def get_packets_return_graph():
    year = request.args.get('year')
    return_status_data = [0] * 3
    quey_for_packet_return_status = f"""
         select count(id) from  cases where 
        extract(year from outreach_date) = '{year}' group by packet_return_status order by packet_return_status asc;
        """
    with db.engine.connect() as connection:
        result_packet_return_status = connection.execute(
            text(quey_for_packet_return_status))

        i = 0
        for row in result_packet_return_status:
            return_status_data[i] = row[0]
            i += 1
    
    return jsonify({
        'message': 'success',
        'data': return_status_data
    }), 200

@analytics_bp.route('/analytics/children_enrolled', methods=['GET'])
def get_children_enrolled_graph():
    year = request.args.get('year')
    children_enrolled_data = [0] * 12
    query_for_children_enrolled = f"""
         select extract(month from outreach_date) as month, sum(num_children_enrolled) from cases where 
        extract(year from outreach_date) = '{year}' group by month;
        """
    
    with db.engine.connect() as connection:
        result_children_enrolled = connection.execute(
            text(query_for_children_enrolled))
        for row in result_children_enrolled:
            children_enrolled_data[int(row[0]) - 1] = row[1]

    return jsonify({
        'message': 'success',
        'data': children_enrolled_data
    }), 200

@analytics_bp.route('/analytics/children_not_enrolled', methods=['GET'])
def get_children_not_enrolled_enrolled():
    year = request.args.get('year')
    children_not_enrolled_data = [0] * 12
    query_for_children_not_enrolled = f"""
         select extract(month from outreach_date) as month, sum(num_of_children)-sum(num_children_enrolled) from cases where 
        extract(year from outreach_date) = '{year}' group by month;
        """
    
    with db.engine.connect() as connection:
        result_children_not_enrolled = connection.execute(
            text(query_for_children_not_enrolled))
        for row in result_children_not_enrolled:
            children_not_enrolled_data[int(row[0]) - 1] = row[1]

    return jsonify({
        'message': 'success',
        'data': children_not_enrolled_data
    }), 200

@analytics_bp.route('/analytics/children_not_enrolled_reasons', methods=['GET'])
def get_not_enrolled_reasons_graph():
    year = request.args.get('year')
    not_enrolled_reasons_count = [0] * 15
    not_enrolled_reasons = ["Does not meet employment/activity requirement", "Fee too high", "No Child Care Slots",
                            "No longer in Dallas County", "No longer needing services", "No packet received",
                            "No Provider Choice", "Not a Priority", "Not working/training", "On leave/STD",
                            "Over the income guidelines", "Unable to Reach Client", "Under participation requirement",
                            "Verification Docs Needed", "Other"
                            ]
    not_enrolled_reasons_dict = dict(
    map(lambda i, j: (i, j), not_enrolled_reasons, not_enrolled_reasons_count))

    query_for_not_enrolled_reason = f"""
         select not_enrolled_reason, count(id) from cases where 
        extract(year from outreach_date) = '{year}' group by not_enrolled_reason having not_enrolled_reason <> '' order by not_enrolled_reason asc;
        """
    
    with db.engine.connect() as connection:
        result_not_enrolled_reason = connection.execute(
            text(query_for_not_enrolled_reason))
        for row in result_not_enrolled_reason:
            not_enrolled_reasons_dict[str(row[0])] = row[1]

    return jsonify({
        'message': 'success',
        'data': list(not_enrolled_reasons_dict.values())
    }), 200

@analytics_bp.route('/analytics/processing_time', methods=['GET'])
def get_processing_time_graph():
    year = request.args.get('year')
    processing_time = [0] * 5

    query_for_processing_time = f"""
        select CASE
            WHEN decision_date - outreach_date > 0 AND decision_date - outreach_date < 10 THEN 1
            WHEN decision_date - outreach_date > 10 AND decision_date - outreach_date < 20 THEN 2
            WHEN decision_date - outreach_date > 20 AND decision_date - outreach_date < 30 THEN 3
            WHEN decision_date - outreach_date > 30 THEN 4
            WHEN decision_date - outreach_date is NULL THEN 5
            END Processing_Time, count(id) from cases where 
            extract(year from outreach_date) = '{year}' group by Processing_Time order by processing_time asc
            ;
    """
    
    with db.engine.connect() as connection:
        result_processing_time = connection.execute(
            text(query_for_processing_time))
        for row in result_processing_time:
            processing_time[int(row[0]) - 1] = row[1]

    return jsonify({
        'message': 'success',
        'data': processing_time
    }), 200