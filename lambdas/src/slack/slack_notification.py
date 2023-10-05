import os
import json
import requests

def main(event, context):
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"
    print(f'event: {event}')
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        topic_from = record['Sns']['TopicArn'].split(":")
        print(topic_from)
        payload = {
            "text": f":rotating_light: Alert from CloudWatch Alarm: {message['AlarmName']} :rotating_light: " + "\n" + f" Account: {topic_from[4]} zone: {topic_from[3]} Lambda: {topic_from[5]}"
        }
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload),
                                 headers={'Content-Type': 'application/json'})
    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent to Slack!')
    }