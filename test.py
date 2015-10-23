#! /usr/bin/env python
# coding=utf-8

import os
import json
import unittest
import logging
from tornado import gen
from rong import ApiClient

#app_key = ""
#app_secret = ""

#os.environ.setdefault('rongcloud_app_key', app_key)
#os.environ.setdefault('rongcloud_app_secret', app_secret)

logging.basicConfig(level=logging.INFO)

client = ApiClient()


class ApiTest(AsyncTestCase):
    @gen_test
    def test_token_get(self):
        result = yield client.user_get_token(
            'test-userid1',
            'test-name1',
            'http://www.rongcloud.cn/images/logo.png')

        result2 = yield client.user_get_token(
            'test-userid2',
            'test-name2',
            'http://www.rongcloud.cn/images/logo.png')

        self.assertEqual(result[u'code'], 200)
        self.assertEqual(result2[u'code'], 200)
        self.assertEqual(result[u'userId'], 'test-userid1')
        self.assertEqual(result2[u'userId'], 'test-userid2')

        self.assertTrue(u"token" in result)

    @gen_test
    def test_user_refresh(self):
        result = yield client.user_refresh(
            'test-userid2',
            'test-name2',
            'http://www.rongcloud.cn/images/logo_new.png'
        )

        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_user_check_online(self):
        result = yield client.user_check_online(
            'test-userid2'
        )

        self.assertEqual(result[u'code'], 200)
        self.assertTrue(u"status" in result)

    @gen_test
    def test_user_block(self):
        result = yield client.user_block('test-userid1', 10)
        self.assertEqual(result[u'code'], 200)

        block_user_list = yield client.user_block_query()
        self.assertEqual(block_user_list[u'code'], 200)
        self.assertTrue('test-userid1' in [r.get("userId") for r in block_user_list.get("users")])

    @gen_test
    def test_user_unblock(self):
        result = yield client.user_unblock('test-userid2')
        self.assertEqual(result[u'code'], 200)

        block_user_list = yield client.user_block_query()
        self.assertEqual(block_user_list[u'code'], 200)
        self.assertTrue('test-userid2' not in [r.get("userId") for r in block_user_list.get("users")], "检查解封是否成功")

    @gen_test
    def test_user_blocklist_add(self):
        result = yield client.user_blocklist_add('test-userid1', ['test-userid2', 'test-userid3'])
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_user_blocklist_query(self):
        result = yield client.user_blocklist_query('test-userid1')
        self.assertTrue('test-userid2' in result.get('users'))
        self.assertTrue('test-userid3' in result.get('users'))

    @gen_test
    def test_user_blocklist_remove(self):
        yield client.user_blocklist_remove('test-userid1', ['test-userid2', 'test-userid3'])
        result = yield client.user_blocklist_query('test-userid1')
        self.assertTrue('test-userid2' not in result.get('users'))
        self.assertTrue('test-userid3' not in result.get('users'))

    @gen_test
    def test_message_publish(self):
        result = yield client.message_publish(
            from_user_id='test-userid1',
            to_user_id='test-userid2',
            object_name='RC:TxtMsg',
            content=json.dumps({"content": "hello"}),
            push_content='thisisapush',
            push_data='aa')

        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_message_system_publish(self):
        result = yield client.message_system_publish(
            from_user_id='test-userid1',
            to_user_id='test-userid2',
            object_name='RC:TxtMsg',
            content=json.dumps({"content": "hello"}),
            push_content='thisisapush',
            push_data='aa')

        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_group_create(self):
        result = yield client.group_create(
            user_id_list=["test-userid1", "test-userid2"],
            group_id="groupid1",
            group_name="groupname1"
        )

        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_message_group_publish(self):
        result = yield client.message_group_publish(
            from_user_id='test-userid1',
            to_group_id="groupid1",
            object_name='RC:TxtMsg',
            content=json.dumps({"content": "hello"}),
            push_content='this is push content',
            push_data='this is pushdata'
        )
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_chatroom_create(self):
        result = yield client.chatroom_create(
            chatrooms={
                'tr001': 'room1',
                'tr002': 'room2'
            }
        )
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_message_chatroom_publish(self):
        result = yield client.message_chatroom_publish(
            from_user_id="test-userid1",
            to_chatroom_id="tr001",
            object_name="RC:TxtMsg",
            content=json.dumps({"content": "hello"})
        )
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_message_history(self):
        result = yield client.message_history(
            date=2014010101
        )
        self.assertEqual(result[u'code'], 200)
        self.assertTrue(u'url' in result)

    @gen_test
    def test_group_sync(self):
        result = yield client.group_sync(
            user_id='test-userid1',
            groups={
                "groupid1": "groupname1"
            }
        )
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_group_join(self):
        result = yield client.group_join(
            user_id_list=['test-userid1', 'test-userid2'],
            group_id="groupid1",
            group_name="groupname1"
        )
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_group_quit(self):
        result = yield client.group_quit(
            user_id_list=['test-userid1', 'test-userid2'],
            group_id="groupid1"
        )
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_group_refresh(self):
        result = yield client.group_refresh(
            group_id="groupid1",
            group_name="groupname1"
        )
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_group_dismiss(self):
        result = yield client.group_dismiss(
            user_id='test-userid1',
            group_id="groupid1")
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_chatroom_query(self):
        result = yield client.chatroom_query(["tr001", "tr002"])
        self.assertEqual(result[u'code'], 200)

    @gen_test
    def test_chatroom_destroy(self):
        result = yield client.chatroom_destroy(
            chatroom_id_list=["tr001", "tr002"]
        )

        self.assertEqual(result[u'code'], 200)


if __name__ == "__main__":
    unittest.main()
