
"""Facebook User approximate creation time determiner."""

import datetime
import urllib.parse as urlparse
from concurrent.futures import as_completed, ThreadPoolExecutor

import facebook
import settings


class FBUserCreationProcessor:

    """This class tries to determine date user was created.

    As Facebook didn't provide account creation time this method tries to find
    it by looking at photos and posts and searching for an oldest one.
    """

    def __init__(self, uaccess_data_keeper, result_data_keeper, max_workers=10):
        """Initialize FBUserCreationProcessor class

        @params uaccess_data_keeper: list of (fbid, token) elements;
        @params result_data_keeper: object with implemented `push` method to store results;
        @params max_workers: maximun number of thread workers, default=10;

        return:
            FBUserCreationProcessor object
        """
        self._uaccess_data_keeper = uaccess_data_keeper
        self._result_data_keeper = result_data_keeper
        self._max_workers = max_workers
        self.__search_methods = [
            self._search_by_photos,
            self._search_by_posts
        ]

    def process_all(self):
        """Lopping all users in threads find it approximate account creation dates."""
        with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
            future_to = {executor.submit(self._prosess_user, fbid, token):
                         (fbid, token) for (fbid, token) in self._uaccess_data_keeper}

            for future in as_completed(future_to):
                fbid, token = future_to[future]
                try:
                    data = future.result()
                except Exception as exc:
                    self._result_data_keeper.push(
                        '%s,%s generated an exception: %s' % (fbid, token, exc)
                    )
                else:
                    self._result_data_keeper.push(data)

    def _prosess_user(self, fbid, token):
        """Find user creation time by fbib + UserAccessToken.
        For determining approximate account creation date uses method defined
        by `__search_methods`.

        @param fbid: Facebook User's ID
        @param token: Facebook User Access Token

        return:
            String '<fbid>, <account_creation_date>'
        """
        reg_date = None
        errors = []
        fbclient = facebook.GraphAPI(access_token=token, version='2.7')
        for method in self.__search_methods:
            try:
                returden_date = method(fbclient, fbid)
            except facebook.GraphAPIError as err:
                errors.append('API Error, %s' % (err))
            except Exception as err:
                errors.append('Unexpected error, %s' % (err))
            else:
                if returden_date is not None:
                    reg_date = self.__find_oldest_date(returden_date, reg_date)

        if reg_date is not None:
            reg_date = reg_date.strftime(settings.CREATION_DATE_FORMAT)
        elif errors:
            reg_date = ', '.join(errors)
        else:
            reg_date = 'Could not determine registration data possible to ' \
                       'lack of permissions'

        return settings.RESULT_FORMAT % ({'fbid': fbid, 'creation_date': reg_date})

    def _search_by_posts(self, fbclient, fbid, **kwargs):
        """Defines search by uses posts logic.
        It looks all users posts and takes oldest one as a base of account
        creation date.
        This is recursive function to loop through FB response pages.
        """
        oldest_date = None
        posts = fbclient.get_object('%s/posts' % (fbid), **kwargs)
        if posts['data']:
            oldest_date = self.__find_oldest_date(
                oldest_date,
                self.__parse_datetime(posts['data'][-1]['created_time']),
            )
        if posts.get('paging'):
            url_splitted = urlparse.urlsplit(posts['paging']['previous'])
            url_params = urlparse.parse_qs(url_splitted.query)
            oldest_date = self.__find_oldest_date(
                oldest_date,
                self._search_by_posts(fbclient, fbid, **url_params),
            )
        return oldest_date

    def _search_by_photos(self, fbclient, fbid, **kwargs):
        """Defines search by uses photos logic.
        It looks all users photos and takes oldest one as a base of account
        creation date.
        This is recursive function to loop through FB response pages.
        """
        oldest_date = None
        photos = fbclient.get_object('%s/photos/uploaded' % (fbid), **kwargs)
        if photos['data']:
            oldest_date = self.__find_oldest_date(
                oldest_date,
                self.__parse_datetime(photos['data'][-1]['created_time']),
            )
        if photos.get('cursors'):
            prev_params = {'after': photos['cursors']['after']}
            oldest_date = self.__find_oldest_date(
                oldest_date,
                self._search_by_photos(fbclient, fbid, **prev_params),
            )
        return oldest_date

    def __find_oldest_date(self, previous_date, current_date):
        """Return oldest date from previous_date and current_date"""
        if current_date is None:
            return previous_date
        if previous_date is None:
            return current_date
        return previous_date if previous_date is None else min(previous_date, current_date)

    def __parse_datetime(self, strdatetime):
        """Passes datetime Facebook format"""
        return datetime.datetime.strptime(strdatetime, '%Y-%m-%dT%H:%M:%S%z')

