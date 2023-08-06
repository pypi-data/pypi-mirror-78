import boto3
from boto3.dynamodb.conditions import Attr, Key
from botocore.exceptions import ClientError

from fdbk import DBConnection
from fdbk.utils import (
    generate_data_entry,
    generate_topic_dict,
    generate_topic_response,
    generate_topics_list,
    timestamp_as_str)
from fdbk.utils.messages import *

from .utils import obj_decimals_to_numbers, obj_numbers_to_decimals


class DynamoDbConnection(DBConnection):
    def __init__(
            self,
            topics_table_name="fdbk_topics",
            data_table_name="fdbk_data",
            *args, **kwargs):
        self._dynamodb = boto3.resource('dynamodb', *args, **kwargs)
        self._topics_table = self._dynamodb.Table(  # pylint: disable=no-member
            topics_table_name)
        self._data_table = self._dynamodb.Table(  # pylint: disable=no-member
            data_table_name)

        # Ensure tables exist
        self._topics_table.table_status
        self._data_table.table_status

    def add_topic(self, name, overwrite=False, **kwargs):
        topic_d = generate_topic_dict(name, add_id=True, **kwargs)
        self.validate_template(topic_d)

        params = {}
        if not overwrite:
            params["ConditionExpression"] = Attr('id').not_exists()

        try:
            self._topics_table.put_item(Item=topic_d, **params)
        except ClientError:
            raise KeyError(duplicate_topic_id(topic_d["id"]))

        return topic_d["id"]

    def add_data(self, topic_id, values, overwrite=False):
        topic_d = self.get_topic(topic_id)
        fields = topic_d["fields"]

        if topic_d.get('type') != 'topic':
            raise AssertionError('Can not add data to template.')

        values = obj_numbers_to_decimals(values)
        params = {}
        if not overwrite:
            params["ConditionExpression"] = Attr(
                'topic_id').not_exists() | Attr('timestamp').not_exists()

        data = generate_data_entry(
            topic_id, fields, values, convert_timestamps=True)
        try:
            self._data_table.put_item(Item=data, **params)
        except ClientError:
            raise AssertionError(duplicate_topic_id(topic_d["id"]))

        return data["timestamp"]

    def get_topics_without_templates(self, type_=None, template=None):
        if type_:
            topics = self._topics_table.scan(
                FilterExpression=Attr("type").eq(type_)).get('Items')
        elif template:
            topics = self._topics_table.scan(
                FilterExpression=Attr("template").eq(template)).get('Items')
        else:
            topics = self._topics_table.scan().get('Items')
        return generate_topics_list(topics)

    def get_topic_without_templates(self, topic_id):
        topic = self._topics_table.get_item(
            Key=dict(id=topic_id)
        ).get('Item')
        if not topic:
            raise KeyError(topic_not_found(topic_id))

        return generate_topic_response(topic)

    def get_data(self, topic_id, since=None, until=None, limit=None):
        if not limit:
            limit = 500

        # Check that topic exists
        self.get_topic(topic_id)

        key = Key('topic_id').eq(topic_id)

        if since and until:
            key &= Key('timestamp').between(
                timestamp_as_str(since), timestamp_as_str(until))
        else:
            if since:
                key &= Key('timestamp').gte(timestamp_as_str(since))
            if until:
                key &= Key('timestamp').lte(timestamp_as_str(until))

        data = list(obj_decimals_to_numbers(i) for i in self._data_table.query(
            Limit=limit,
            KeyConditionExpression=key,
            ScanIndexForward=False,
        ).get('Items'))
        data.reverse()

        return data
