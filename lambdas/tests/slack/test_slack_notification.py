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
        #assert response['body'] == 'Notification sent to Slack!'

    # Returns a successful response with status code 200
    def test_successful_response(self):
        from src.slack.slack_notification import main
        event = {
            'Records': [
                {
                    'Sns': {
                        'Message': '{"AlarmName": "Test Alarm"}',
                        'TopicArn': 'arn:aws:sns:us-west-2:123456789012:TestTopic'
                    }
                }
            ]
        }
        response = main(event, None)
        assert response['statusCode'] == 200
        assert response['body'] == 'Notification sent to Slack!'

    # Handles empty event
    def test_empty_event(self):
        from src.slack.slack_notification import main
        event = {}
        response = main(event, None)
        assert response['statusCode'] == 200
        assert response['body'] == 'Notification sent to Slack!'

    # Handles missing 'Records' key in event
    def test_missing_records_key(self):
        from src.slack.slack_notification import main
        event = {
            'Sns': {
                'Message': '{"AlarmName": "Test Alarm"}',
                'TopicArn': 'arn:aws:sns:us-west-2:123456789012:TestTopic'
            }
        }
        response = main(event, None)
        assert response['statusCode'] == 200
        assert response['body'] == 'Notification sent to Slack!'

    # Handles missing 'Sns' key in record
    def test_missing_sns_key(self):
        from src.slack.slack_notification import main
        event = {
            'Records': [
                {
                    'Message': '{"AlarmName": "Test Alarm"}',
                    'TopicArn': 'arn:aws:sns:us-west-2:123456789012:TestTopic'
                }
            ]
        }
        response = main(event, None)
        assert response['statusCode'] == 200
        assert response['body'] == 'Notification sent to Slack!'

    # Handles missing 'Message' key in Sns
    def test_missing_message_key(self):
        from src.slack.slack_notification import main
        event = {
            'Records': [
                {
                    'Sns': {
                        'TopicArn': 'arn:aws:sns:us-west-2:123456789012:TestTopic'
                    }
                }
            ]
        }
        response = main(event, None)
        assert response['statusCode'] == 200
        assert response['body'] == 'Notification sent to Slack!'