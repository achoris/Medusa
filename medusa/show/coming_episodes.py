# coding=utf-8
# This file is part of Medusa.
#
# Medusa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Medusa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Medusa. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals

from builtins import object
from builtins import str
from datetime import date, timedelta
from operator import itemgetter

from medusa import app
from medusa.common import (
    ARCHIVED,
    DOWNLOADED,
    IGNORED,
    SNATCHED,
    SNATCHED_BEST,
    SNATCHED_PROPER,
    UNAIRED,
    WANTED
)
from medusa.db import DBConnection
from medusa.helper.common import dateFormat, timeFormat
from medusa.helpers.quality import get_quality_string
from medusa.network_timezones import parse_date_time
from medusa.sbdatetime import sbdatetime
from medusa.tv.series import Series, SeriesIdentifier


class ComingEpisodes(object):
    """
    Missed:   yesterday...(less than 1 week)
    Today:    today
    Soon:     tomorrow till next week
    Later:    later than next week
    """

    categories = ['later', 'missed', 'soon', 'today']
    sorts = {
        'date': itemgetter('localtime'),
        'network': itemgetter('network', 'localtime'),
        'show': itemgetter('show_name', 'localtime'),
    }

    def __init__(self):
        pass

    @staticmethod
    def get_coming_episodes(categories, sort, group, paused=app.COMING_EPS_DISPLAY_PAUSED):
        """
        :param categories: The categories of coming episodes. See ``ComingEpisodes.categories``
        :param sort: The sort to apply to the coming episodes. See ``ComingEpisodes.sorts``
        :param group: ``True`` to group the coming episodes by category, ``False`` otherwise
        :param paused: ``True`` to include paused shows, ``False`` otherwise
        :return: The list of coming episodes
        """
        categories = ComingEpisodes._get_categories(categories)
        sort = ComingEpisodes._get_sort(sort)

        today = date.today().toordinal()
        next_week = (date.today() + timedelta(days=7)).toordinal()
        recently = (date.today() - timedelta(days=app.COMING_EPS_MISSED_RANGE)).toordinal()
        status_list = [DOWNLOADED, SNATCHED, SNATCHED_BEST, SNATCHED_PROPER,
                       ARCHIVED, IGNORED]

        db = DBConnection()
        fields_to_select = ', '.join(
            ['airdate', 'airs', 'e.description as description', 'episode', 'imdb_id', 'e.indexer',
             'indexer_id', 'name', 'network', 'paused', 's.quality', 'runtime', 'season', 'show_name',
             'showid', 's.status']
        )
        results = db.select(
            'SELECT %s ' % fields_to_select +
            'FROM tv_episodes e, tv_shows s '
            'WHERE season != 0 '
            'AND airdate >= ? '
            'AND airdate < ? '
            'AND s.indexer = e.indexer '
            'AND s.indexer_id = e.showid '
            'AND e.status NOT IN (' + ','.join(['?'] * len(status_list)) + ')',
            [today, next_week] + status_list
        )

        done_shows_list = [int(result['showid']) for result in results]
        placeholder = ','.join(['?'] * len(done_shows_list))
        placeholder2 = ','.join(['?'] * len([DOWNLOADED, SNATCHED, SNATCHED_BEST, SNATCHED_PROPER]))

        # FIXME: This inner join is not multi indexer friendly.
        results += db.select(
            'SELECT %s ' % fields_to_select +
            'FROM tv_episodes e, tv_shows s '
            'WHERE season != 0 '
            'AND showid NOT IN (' + placeholder + ') '
            'AND s.indexer_id = e.showid '
            'AND airdate = (SELECT airdate '
            'FROM tv_episodes inner_e '
            'WHERE inner_e.season != 0 '
            'AND inner_e.showid = e.showid '
            'AND inner_e.indexer = e.indexer '
            'AND inner_e.airdate >= ? '
            'ORDER BY inner_e.airdate ASC LIMIT 1) '
            'AND e.status NOT IN (' + placeholder2 + ')',
            done_shows_list + [next_week] + [DOWNLOADED, SNATCHED, SNATCHED_BEST, SNATCHED_PROPER]
        )

        results += db.select(
            'SELECT %s ' % fields_to_select +
            'FROM tv_episodes e, tv_shows s '
            'WHERE season != 0 '
            'AND s.indexer_id = e.showid '
            'AND airdate < ? '
            'AND airdate >= ? '
            'AND e.status IN (?,?) '
            'AND e.status NOT IN (' + ','.join(['?'] * len(status_list)) + ')',
            [today, recently, WANTED, UNAIRED] + status_list
        )

        for index, item in enumerate(results):
            identifier = SeriesIdentifier.from_id(int(item['indexer']), item['indexer_id'])
            show = Series.find_by_identifier(identifier)
            item['series_slug'] = identifier.slug
            results[index]['localtime'] = sbdatetime.convert_to_setting(
                parse_date_time(item['airdate'], item['airs'], item['network']))
            results[index]['externals'] = show.externals

        results.sort(key=ComingEpisodes.sorts[sort])

        if not group:
            return results

        grouped_results = ComingEpisodes._get_categories_map(categories)

        for result in results:
            if result['paused'] and not paused:
                continue

            result['airs'] = str(result['airs']).replace('am', ' AM').replace('pm', ' PM').replace('  ', ' ')
            result['airdate'] = result['localtime'].toordinal()

            if result['airdate'] < today:
                category = 'missed'
            elif result['airdate'] >= next_week:
                category = 'later'
            elif result['airdate'] == today:
                category = 'today'
            else:
                category = 'soon'

            if len(categories) > 0 and category not in categories:
                continue

            if not result['network']:
                result['network'] = ''

            result['qualityValue'] = result['quality']
            result['quality'] = get_quality_string(result['quality'])
            result['airs'] = sbdatetime.sbftime(result['localtime'], t_preset=timeFormat).lstrip('0').replace(' 0', ' ')
            result['weekday'] = 1 + date.fromordinal(result['airdate']).weekday()
            result['tvdbid'] = result['indexer_id']
            result['airdate'] = sbdatetime.sbfdate(result['localtime'], d_preset=dateFormat)
            result['localtime'] = result['localtime'].toordinal()

            grouped_results[category].append(result)

        return grouped_results

    @staticmethod
    def _get_categories(categories):
        if not categories:
            return []

        if not isinstance(categories, list):
            return categories.split('|')

        return categories

    @staticmethod
    def _get_categories_map(categories):
        if not categories:
            return {}

        return {category: [] for category in categories}

    @staticmethod
    def _get_sort(sort):
        sort = sort.lower() if sort else ''

        if sort not in ComingEpisodes.sorts:
            return 'date'

        return sort
