
import unittest
from unittest.mock import patch, MagicMock, Mock

from src.fb_data import FBUserCreationProcessor


TEST_UD1 = 'fbid123'
TEST_UD2 = 'fbid124'
TEST_TOKEN1 = 'asdaarewfr34'
TEST_TOKEN2 = '5yjtyj56utrs'
TEST_PHOTOS_DATA = {'paging':
    {'cursors':
        {'before': 'NDUzMzgyNDY0Njk1MTUx', 'after': 'NDUzMzgwNDYxMzYyMDE4'},},
    'data': [
        {'id': 'fbid123', 'created_time': '2012-07-26T09:45:55+0000'},
        {'id': 'fbid123', 'created_time': '2012-07-26T09:37:14+0000'}
    ]}
TEST_POST_DATA = {'paging':
    {'next': 'https://graph.facebook.com/v2.7/137081sdcsd/posts?access_token=asfsfa&limit=25&until=1299960116&__paging_token=sdfdsf',
     'previous': 'https://graph.facebook.com/v2.7/137081sdcsd/posts?since=137081sdcsd&access_token=sdfdsfs&limit=25&__paging_token=sdgsdg&__previous=1'},
     'data': [
        {'id': '137081sdcsd', 'message': 'sdchoice!', 'created_time': '2013-04-04T11:48:10+0000'},
        {'story': 'asdfasd', 'id': '137081sdcsd', 'created_time': '2011-03-12T20:01:56+0000'}
    ]
}
TEST_EMPTY_DATA = {'data': []}
MAX_WORKERS = 5


class FBUserProcessorTest(unittest.TestCase):

    def setUp(self):
        self.stab_csv_data = [
            (TEST_UD1, TEST_TOKEN1),
            (TEST_UD2, TEST_TOKEN2)
        ]
        self.mock_data_writer = MagicMock()
        self.mock_get_object = Mock()
        self.mock_fbclient = Mock()
        self.mock_fbclient.get_object = self.mock_get_object
        self.mock_GraphAPI = Mock()
        self.mock_GraphAPI.return_value = self.mock_fbclient
        self.processor = FBUserCreationProcessor(
            uaccess_data_keeper=self.stab_csv_data,
            result_data_keeper=self.mock_data_writer,
            max_workers=MAX_WORKERS
        )

    @patch('src.fb_data.facebook', create=True)
    def test_process_all(self, facebook):
        facebook.GraphAPI = self.mock_GraphAPI
        self.mock_get_object.side_effect = [
            TEST_PHOTOS_DATA, TEST_PHOTOS_DATA, TEST_EMPTY_DATA,
            TEST_POST_DATA, TEST_POST_DATA, TEST_EMPTY_DATA
        ]
        self.processor.process_all()
        self.mock_data_writer.assert_called_once()


if __name__ == '__main__':
    unittest.main()
