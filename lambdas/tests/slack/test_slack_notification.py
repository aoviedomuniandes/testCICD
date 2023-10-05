import pytest

class TestMain:

    # Sends a notification to Slack for each record in the event
    def test_send_notification_to_slack(self):
        from src.slack.slack_notification import main
        event = {
            'Records': [
                {
                    'Sns': {
                        'Message': '{"AlarmName": "Test Alarm"}',
                        'TopicArn': 'arn:aws:sns:us-west-2:123456789012:TestTopic'
                    }
                },
                {
                    'Sns': {
                        'Message': '{"AlarmName": "Another Test Alarm"}',
                        'TopicArn': 'arn:aws:sns:us-west-2:123456789012:AnotherTestTopic'
                    }
                }
            ]
        }
        response = main(event, None)
        assert response['statusCode'] == 200
