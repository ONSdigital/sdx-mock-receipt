from flask import Flask, request, render_template, make_response
import xml.etree.ElementTree as ET
import os
import settings
import logging

app = Flask(__name__)

logging.basicConfig(level=settings.LOGGING_LEVEL, format=settings.LOGGING_FORMAT)


@app.errorhandler(400)
def not_found(error):
    resp = make_response(render_template('error.xml'), 400)
    resp.headers['Content-Type'] = 'application/vnd.ons.error+xml'
    return resp


@app.route('/reportingunits/<ru_ref>/collectionexercises/<exercise_sid>/receipts', methods=['POST'])
def ack(ru_ref, exercise_sid):

    if len(ru_ref) != 11 or len(exercise_sid) != 11:
        app.logger.warning("Got a invalid ru_ref/exercise_sid: Reporting Unit {ru_ref} - Exercise Id {exercise_sid}"
                           .format(ru_ref=ru_ref, exercise_sid=exercise_sid))

    app.logger.debug("Got a response: Reporting Unit {ru_ref} - Exercise Id {exercise_sid}"
                     .format(ru_ref=ru_ref, exercise_sid=exercise_sid))

    data = request.get_data()
    app.logger.debug("Received XML Receipt: {0}".format(data))

    receipt_xml = ET.fromstring(data)
    ns = {'receipt': 'http://ns.ons.gov.uk/namespaces/resources/receipt'}

    respondent = receipt_xml.find('receipt:respondent_id', ns)
    respondent_id = respondent.text

    if respondent_id:
        app.logger.debug("Confirmed receipt for: respondent {respondent_id}"
                         .format(respondent_id=respondent_id))
        return respondent_id, 201
    else:
        return not_found("Couldn't parse respondent_id")

if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    app.run(debug=True, host='0.0.0.0', port=port)
