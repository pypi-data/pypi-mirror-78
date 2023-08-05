import json
from typing import List, Union
from datetime import datetime

from plexapi.video import Video, Movie, Episode
from plexapi.server import PlexServer as PServer

import dizqueTV.helpers as helpers
from dizqueTV.templates import MOVIE_PROGRAM_TEMPLATE, EPISODE_PROGRAM_TEMPLATE, \
    REDIRECT_PROGRAM_TEMPLATE, FILLER_ITEM_TEMPLATE
from dizqueTV.exceptions import MissingParametersError


class BaseMediaItem:
    def __init__(self, data: json, dizque_instance, channel_instance):
        self._data = data
        self._dizque_instance = dizque_instance
        self._channel_instance = channel_instance
        self.type = data.get('type')
        self.isOffline = data.get('isOffline')
        self.duration = data.get('duration')


class Redirect(BaseMediaItem):
    def __init__(self, data: json, dizque_instance, channel_instance):
        super().__init__(data=data, dizque_instance=dizque_instance, channel_instance=channel_instance)
        self.channel = data.get('channel')


class MediaItem(BaseMediaItem):
    def __init__(self, data: json, dizque_instance, channel_instance):
        super().__init__(data=data, dizque_instance=dizque_instance, channel_instance=channel_instance)
        self.title = data.get('title')
        self.key = data.get('key')
        self.ratingKey = data.get('ratingKey')
        self.duration = data.get('duration')
        self.icon = data.get('icon')
        self.summary = data.get('summary')
        self.date = data.get('date')
        self.year = data.get('year')
        self.plexFile = data.get('plexFile')
        self.file = data.get('file')
        self.showTitle = data.get('showTitle')
        self.episode = data.get('episode')
        self.season = data.get('season')
        self.serverKey = data.get('serverKey')

        self.showIcon = data.get('showIcon')
        self.episodeIcon = data.get('episodeIcon')
        self.seasonIcon = data.get('seasonIcon')


class Filler(MediaItem):
    def __init__(self, data: json, dizque_instance, channel_instance):
        super().__init__(data=data, dizque_instance=dizque_instance, channel_instance=channel_instance)

    @helpers._check_for_dizque_instance
    def delete(self) -> bool:
        """
        Delete this filler
        :return: True if successful, False if unsuccessful
        """
        return self._channel_instance.delete_filler(filler=self)


class Program(MediaItem, Redirect):
    def __init__(self, data: json, dizque_instance, channel_instance):
        super().__init__(data=data, dizque_instance=dizque_instance, channel_instance=channel_instance)
        self.rating = data.get('rating')

    @helpers._check_for_dizque_instance
    def delete(self) -> bool:
        """
        Delete this program
        :return: True if successful, False if unsuccessful
        """
        return self._channel_instance.delete_program(program=self)


class Channel:
    def __init__(self, data: json, dizque_instance):
        self._data = data
        self._dizque_instance = dizque_instance
        self._program_data = data.get('programs')
        self._fillerContent_data = data.get('fillerContent')
        self.fillerRepeatCooldown = data.get('fillerRepeatCooldown')
        self.fallback = [Filler(data=filler_data, dizque_instance=dizque_instance, channel_instance=self)
                         for filler_data in data.get('fallback')]
        self.icon = data.get('icon')
        self.disableFillerOverlay = data.get('disableFillerOverlay')
        self.iconWidth = data.get('iconWidth')
        self.iconDuration = data.get('iconDuration')
        self.iconPosition = data.get('iconPosition')
        self.overlayIcon = data.get('overlayIcon')
        self.startTime = data.get('startTime')
        self.offlinePicture = data.get('offlinePicture')
        self.offlineSoundtrack = data.get('offlineSoundtrack')
        self.offlineMode = data.get('offlineMode')
        self.number = data.get('number')
        self.name = data.get('name')
        self.duration = data.get('duration')
        self._id = data.get('_id')

    @property
    def programs(self):
        """
        Get all programs on this channel
        :return: List of MediaItem objects
        """
        return [Program(data=program, dizque_instance=self._dizque_instance, channel_instance=self)
                for program in self._program_data]

    @helpers._check_for_dizque_instance
    def get_program(self, program_title: str = None, redirect_channel_number: int = None) -> Union[Program, None]:
        """
        Get a specific program on this channel
        :param program_title: Title of program
        :return: Program object or None
        """
        if not program_title and not redirect_channel_number:
            raise MissingParametersError("Please include either a program_title or a redirect_channel_number.")
        for program in self.programs:
            if (program_title and program.title == program_title) \
                    or (redirect_channel_number and redirect_channel_number == program.channel):
                return program
        return None

    @property
    def filler(self):
        """
        Get all filler (Flex) items on this channel
        :return: List of MediaItem objects
        """
        return [Filler(data=filler, dizque_instance=self._dizque_instance, channel_instance=self)
                for filler in self._fillerContent_data]

    @helpers._check_for_dizque_instance
    def get_filler(self, filler_title: str) -> Union[Filler, None]:
        """
        Get a specific filler item on this channel
        :param filler_title: Title of filler item
        :return: Filler object or None
        """
        for filler in self.filler:
            if filler.title == filler_title:
                return filler
        return None

    @helpers._check_for_dizque_instance
    def refresh(self):
        """
        Reload current Channel object
        Use to update program and filler data
        """
        temp_channel = self._dizque_instance.get_channel(channel_number=self.number)
        if temp_channel:
            json_data = temp_channel._data
            self.__init__(data=json_data, dizque_instance=self._dizque_instance)
            del temp_channel

    @helpers._check_for_dizque_instance
    def update(self, **kwargs) -> bool:
        """
        Edit this Channel on dizqueTV
        Automatically refreshes current Channel object
        :param kwargs: keyword arguments of Channel settings names and values
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        if self._dizque_instance.update_channel(channel_number=self.number, **kwargs):
            self.refresh()
            return True
        return False

    @helpers._check_for_dizque_instance
    def delete(self) -> bool:
        """
        Delete this channel
        :return: True if successful, False if unsuccessful
        """
        return self._dizque_instance.delete_channel(channel_number=self.number)

    @helpers._check_for_dizque_instance
    def add_program(self,
                    plex_item: Union[Video, Movie, Episode] = None,
                    plex_server: PServer = None,
                    program: Program = None,
                    **kwargs) -> bool:
        """
        Add a program to this channel
        :param plex_item: plexapi.video.Video, plexapi.video.Movie or plexapi.video.Episode object (optional)
        :param plex_server: plexapi.server.PlexServer object (optional)
        :param program: Program object (optional)
        :param kwargs: keyword arguments of Program settings names and values
        :return: True if successful, False if unsuccessful (Channel reloads in place)
        """
        if not plex_item and not program and not kwargs:
            raise MissingParametersError("Please include either a program, a plex_item/plex_server combo, or kwargs")
        if plex_item and plex_server:
            temp_program = self._dizque_instance.convert_plex_item_to_program(plex_item=plex_item,
                                                                              plex_server=plex_server)
            kwargs = temp_program._data
        elif program:
            kwargs = program._data
        template = MOVIE_PROGRAM_TEMPLATE
        if kwargs['type'] == 'episode':
            template = EPISODE_PROGRAM_TEMPLATE
        elif kwargs['type'] == 'redirect':
            template = REDIRECT_PROGRAM_TEMPLATE
        if helpers._settings_are_complete(new_settings_dict=kwargs,
                                          template_settings_dict=template,
                                          ignore_id=True):
            channel_data = self._data
            channel_data['programs'].append(kwargs)
            channel_data['duration'] += kwargs['duration']
            return self.update(**channel_data)
        return False

    @helpers._check_for_dizque_instance
    def add_programs(self, programs: List[Union[Program, Video, Movie, Episode]], plex_server: PServer = None) -> bool:
        """
        Add multiple programs to this channel
        :param programs: List of Program, plexapi.video.Video, plexapi.video.Movie or plexapi.video.Episode objects
        :param plex_server: plexapi.server.PlexServer object
        (required if adding PlexAPI Video, Movie or Episode objects)
        :return: True if successful, False if unsuccessful (Channel reloads in place)
        """
        channel_data = self._data
        for program in programs:
            if type(program) != Program:
                if not plex_server:
                    raise MissingParametersError("Please include a plex_server if you are adding PlexAPI Video, "
                                                 "Movie, or Episode items.")
                program = self._dizque_instance.convert_plex_item_to_program(plex_item=program, plex_server=plex_server)
            channel_data['programs'].append(program._data)
            channel_data['duration'] += program.duration
        return self.update(**channel_data)

    @helpers._check_for_dizque_instance
    def delete_program(self, program: Program) -> bool:
        """
        Delete a program from this channel
        :param program: Program object to delete
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        channel_data = self._data
        for a_program in channel_data['programs']:
            if (program.type == 'redirect' and a_program['type'] == 'redirect') \
                    or (a_program['title'] == program.title):
                channel_data['duration'] -= a_program['duration']
                channel_data['programs'].remove(a_program)
                return self.update(**channel_data)
        return False

    @helpers._check_for_dizque_instance
    def delete_all_programs(self) -> bool:
        """
        Delete all programs from this channel
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        channel_data = self._data
        channel_data['duration'] -= sum(program.duration for program in self.programs)
        channel_data['programs'] = []
        return self.update(**channel_data)

    # Sort Programs
    @helpers._check_for_dizque_instance
    def sort_programs_by_release_date(self) -> bool:
        """
        Sort all programs on this channel by release date
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        sorted_programs = sort_media_by_release_date(media_items=self.programs)
        if self.delete_all_programs():
            return self.add_programs(programs=sorted_programs)
        return False

    @helpers._check_for_dizque_instance
    def sort_programs_by_season_order(self) -> bool:
        """
        Sort all programs on this channel by season order
        Movies are added at the end of the list
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        sorted_programs = sort_media_by_season_order(media_items=self.programs)
        if self.delete_all_programs():
            return self.add_programs(programs=sorted_programs)
        return False

    @helpers._check_for_dizque_instance
    def sort_programs_alphabetically(self) -> bool:
        """
        Sort all programs on this channel in alphabetical order
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        sorted_programs = sort_media_alphabetically(media_items=self.programs)
        if self.delete_all_programs():
            return self.add_programs(programs=sorted_programs)
        return False

    @helpers._check_for_dizque_instance
    def sort_programs_by_duration(self) -> bool:
        """
        Sort all programs on this channel by duration
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        sorted_programs = sort_media_by_duration(media_items=self.programs)
        if self.delete_all_programs():
            return self.add_programs(programs=sorted_programs)
        return False

    @helpers._check_for_dizque_instance
    def sort_programs_randomly(self) -> bool:
        """
        Sort all programs on this channel randomly
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        sorted_programs = sort_media_randomly(media_items=self.programs)
        if self.delete_all_programs():
            return self.add_programs(programs=sorted_programs)
        return False

    @helpers._check_for_dizque_instance
    def remove_duplicate_programs(self) -> bool:
        """
        Delete duplicate programs on this channel
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        sorted_programs = remove_duplicate_media_items(media_items=self.programs)
        if self.delete_all_programs():
            return self.add_programs(programs=sorted_programs)
        return False

    @helpers._check_for_dizque_instance
    def remove_specials(self) -> bool:
        """
        Delete all specials from this channel
        Note: Removes all redirects
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        non_redirects = [item for item in self.programs if
                         (helpers._object_has_attribute(object=item, attribute_name='type')
                          and item.type != 'redirect')]
        non_specials = [item for item in non_redirects if
                        (helpers._object_has_attribute(object=item, attribute_name='season')
                         and item.season != 0)]
        if self.delete_all_programs():
            return self.add_programs(programs=non_specials)
        return False

    @helpers._check_for_dizque_instance
    def add_filler(self,
                   plex_item: Union[Video, Movie, Episode] = None,
                   plex_server: PServer = None,
                   filler: Filler = None, **kwargs) -> bool:
        """
        Add a filler item to this channel
        :param plex_item: plexapi.video.Video, plexapi.video.Movie or plexapi.video.Episode object (optional)
        :param plex_server: plexapi.server.PlexServer object (optional)
        :param filler: Filler item (optional)
        :param kwargs: keyword arguments of Filler settings names and values
        :return: True if successful, False if unsuccessful (Channel reloads in place)
        """
        if not plex_item and not filler and not kwargs:
            raise MissingParametersError("Please include either a program, a plex_item/plex_server combo, or kwargs")
        if plex_item and plex_server:
            temp_filler = self._dizque_instance.convert_plex_item_to_filler(plex_item=plex_item,
                                                                            plex_server=plex_server)
            kwargs = temp_filler._data
        if filler:
            kwargs = filler._data
        if helpers._settings_are_complete(new_settings_dict=kwargs,
                                          template_settings_dict=FILLER_ITEM_TEMPLATE,
                                          ignore_id=True):
            channel_data = self._data
            channel_data['fillerContent'].append(kwargs)
            channel_data['duration'] += kwargs['duration']
            return self.update(**channel_data)
        return False

    @helpers._check_for_dizque_instance
    def add_fillers(self, fillers: List[Union[Filler, Video, Movie, Episode]], plex_server: PServer = None) -> bool:
        """
        Add multiple programs to this channel
        :param fillers: List of Filler, plexapi.video.Video, plexapi.video.Movie or plexapi.video.Episode objects
        :param plex_server: plexapi.server.PlexServer object
        (required if adding PlexAPI Video, Movie or Episode objects)
        :return: True if successful, False if unsuccessful (Channel reloads in place)
        """
        channel_data = self._data
        for filler in fillers:
            if type(filler) != Filler:
                if not plex_server:
                    raise MissingParametersError("Please include a plex_server if you are adding PlexAPI Video, "
                                                 "Movie, or Episode items.")
                filler = self._dizque_instance.convert_plex_item_to_filler(plex_item=filler, plex_server=plex_server)
            channel_data['fillerContent'].append(filler._data)
            channel_data['duration'] += filler.duration
        return self.update(**channel_data)

    @helpers._check_for_dizque_instance
    def delete_filler(self, filler: Filler) -> bool:
        """
        Delete a filler item from this channel
        :param filler: Filler object to delete
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        channel_data = self._data
        for a_filler in channel_data['fillerContent']:
            if a_filler['title'] == filler.title:
                channel_data['duration'] -= a_filler['duration']
                channel_data['fillerContent'].remove(a_filler)
                return self.update(**channel_data)
        return False

    @helpers._check_for_dizque_instance
    def delete_all_fillers(self) -> bool:
        """
        Delete all filler items from this channel
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        channel_data = self._data
        channel_data['duration'] -= sum(filler.duration for filler in self.filler)
        channel_data['fillerContent'] = []
        return self.update(**channel_data)

    # Sort Filler
    @helpers._check_for_dizque_instance
    def sort_filler_by_duration(self) -> bool:
        """
        Sort all filler items on this channel by duration
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        sorted_filler = sort_media_by_duration(media_items=self.filler)
        if self.delete_all_fillers():
            return self.add_fillers(fillers=sorted_filler)
        return False

    @helpers._check_for_dizque_instance
    def sort_filler_randomly(self) -> bool:
        """
        Sort all filler items on this channel randomly
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        sorted_filler = sort_media_randomly(media_items=self.filler)
        if self.delete_all_fillers():
            return self.add_fillers(fillers=sorted_filler)
        return False

    @helpers._check_for_dizque_instance
    def remove_duplicate_fillers(self) -> bool:
        """
        Delete duplicate filler items on this channel
        :return: True if successful, False if unsuccessful (Channel reloads in-place)
        """
        sorted_filler = remove_duplicate_media_items(media_items=self.filler)
        if self.delete_all_fillers():
            return self.add_fillers(fillers=sorted_filler)
        return False


# Helper Functions
def sort_media_alphabetically(media_items: List[Union[Program, Filler]]) -> List[Union[Program, Filler]]:
    """
    Sort media items alphabetically.
    Note: Shows will be grouped and sorted by series title, but episodes may be out of order
    :param media_items: List of Program and Filler objects
    :return: List of Program and Filler objects
    """
    items_with_titles, items_without_titles = helpers._separate_with_and_without(items=media_items,
                                                                                 attribute_name='title')
    sorted_items = sorted(items_with_titles, key=lambda x: (x.showTitle if x.type == 'episode' else x.title))
    sorted_items.extend(items_without_titles)
    return sorted_items


def sort_media_by_release_date(media_items: List[Union[Program, Filler]]) -> List[Union[Program, Filler]]:
    """
    Sort media items by release date.
    Note: Items without release dates are appended (alphabetically) at the end of the list
    :param media_items: List of Program and Filler objects
    :return: List of Program and Filler objects
    """
    items_with_dates, items_without_dates = helpers._separate_with_and_without(items=media_items,
                                                                               attribute_name='date')
    sorted_items = sorted(items_with_dates, key=lambda x: datetime.strptime(x.date, "%Y-%m-%d"))
    sorted_items.extend(sort_media_alphabetically(media_items=items_without_dates))
    return sorted_items


def _sort_shows_by_season_order(shows_dict: dict) -> List[Union[Program, Filler]]:
    """
    Sort a show dictionary by series-season-episode.
    Series are ordered alphabetically
    :param shows_dict: Series-season-episode dictionary
    :return: List of Program and Filler objects
    """
    sorted_list = []
    sorted_shows = sorted(shows_dict.items(), key=lambda show_name: show_name)
    for show in sorted_shows:
        sorted_seasons = sorted(show[1].items(), key=lambda season_number: season_number)
        for season in sorted_seasons:
            sorted_episodes = sorted(season[1].items(), key=lambda episode_number: episode_number)
            for item in sorted_episodes:
                sorted_list.append(item[1])
    return sorted_list


def sort_media_by_season_order(media_items: List[Union[Program, Filler]]) -> List[Union[Program, Filler]]:
    """
    Sort media items by season order.
    Note: Series are ordered alphabetically, movies appended (alphabetically) at the end of the list.
    :param media_items: List of Program and Filler objects
    :return: List of Program and Filler objects
    """
    non_shows = [item for item in media_items if
                 (helpers._object_has_attribute(object=item, attribute_name='type') and item.type != 'episode')]
    show_dict = helpers.make_show_dict(media_items=media_items)
    sorted_shows = _sort_shows_by_season_order(shows_dict=show_dict)
    sorted_movies = sort_media_alphabetically(media_items=non_shows)
    sorted_all = sorted_shows + sorted_movies
    return sorted_all


def sort_media_by_duration(media_items: List[Union[Program, Filler]]) -> List[Union[Program, Filler]]:
    """
    Sort media by duration.
    Note: Automatically removes redirect items
    :param media_items: List of Program and Filler objects
    :return: List of Program and Filler objects
    """
    non_redirects = [item for item in media_items if
                     (helpers._object_has_attribute(object=item, attribute_name='duration')
                      and helpers._object_has_attribute(object=item, attribute_name='type')
                      and item.type != 'redirect')]
    sorted_media = sorted(non_redirects, key=lambda x: x.duration)
    return sorted_media


def sort_media_randomly(media_items: List[Union[Program, Filler]]) -> List[Union[Program, Filler]]:
    """
    Sort media randomly.
    :param media_items: List of Program and Filler objects
    :return: List of Program and Filler objects
    """
    return helpers.shuffle(items=media_items)


def remove_duplicate_media_items(media_items: List[Union[Program, Filler]]) -> List[Union[Program, Filler]]:
    """
    Remove duplicate items from list of media items.
    Check by ratingKey.
    Note: Automatically removes redirect items
    :param media_items: List of Program and Filler objects
    :return: List of Program and Filler objects
    """
    non_redirects = [item for item in media_items if
                     (helpers._object_has_attribute(object=item, attribute_name='type')
                      and item.type != 'redirect')]
    return helpers.remove_duplicates_by_attribute(items=non_redirects, attribute_name='ratingKey')
