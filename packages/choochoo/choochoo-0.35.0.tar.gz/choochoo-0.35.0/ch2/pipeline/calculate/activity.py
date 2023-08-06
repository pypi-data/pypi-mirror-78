
import datetime as dt
from collections import defaultdict
from json import loads
from logging import getLogger

from sqlalchemy import desc

from .elevation import ElevationCalculator
from .impulse import ImpulseCalculator
from .power import PowerCalculator
from .utils import ProcessCalculator, ActivityJournalCalculatorMixin, DataFrameCalculatorMixin
from ..pipeline import OwnerInMixin, LoaderMixin
from ..read.segment import SegmentReader
from ...data import Statistics
from ...data.activity import active_stats, times_for_distance, hrz_stats, max_med_stats, max_mean_stats, \
    direction_stats, copy_times
from ...data.climb import find_climbs, Climb, add_climb_stats
from ...data.frame import present
from ...data.response import response_stats
from ...lib import time_to_local_time
from ...lib.data import safe_dict
from ...common.log import log_current_exception
from ...names import N, T, Summaries as S, Units, titles_for_names, SPACE, simple_name
from ...sql import StatisticJournalFloat, Constant, StatisticJournalText, StatisticJournalTimestamp, \
    ActivityJournal, StatisticJournal

log = getLogger(__name__)


class ActivityCalculator(LoaderMixin, OwnerInMixin,
                         ActivityJournalCalculatorMixin, DataFrameCalculatorMixin, ProcessCalculator):

    def __init__(self, *args, climb=None, response_prefix=None, **kargs):
        self.climb_ref = climb
        self.response_prefix = response_prefix
        super().__init__(*args, add_serial=False, **kargs)

    def _read_dataframe(self, s, ajournal):
        try:
            adf = Statistics(s, activity_journal=ajournal, with_timespan=True). \
                by_name(SegmentReader, N.DISTANCE, N.HEART_RATE, N.SPHERICAL_MERCATOR_X, N.SPHERICAL_MERCATOR_Y). \
                by_name(ElevationCalculator, N.ELEVATION). \
                by_name(ImpulseCalculator, N.HR_ZONE). \
                by_name(PowerCalculator, N.POWER_ESTIMATE).df
            if self.response_prefix:
                start, finish = ajournal.start - dt.timedelta(hours=1), ajournal.finish + dt.timedelta(hours=1)
                fitness = self.response_prefix + SPACE + N.FITNESS_ANY
                fatigue = self.response_prefix + SPACE + N.FATIGUE_ANY
                sdf = Statistics(s, start=start, finish=finish). \
                    by_name(self.owner_in, fitness, fatigue, like=True).with_. \
                    drop_prefix(self.response_prefix).df
            else:
                sdf = None
            prev = s.query(ActivityJournal). \
                filter(ActivityJournal.start < ajournal.start). \
                order_by(desc(ActivityJournal.start)). \
                first()
            delta = (ajournal.start - prev.start).total_seconds() if prev else None
            return adf, sdf, delta
        except Exception as e:
            log.warning(f'Failed to generate statistics for activity: {e}')
            raise

    def _calculate_stats(self, s, ajournal, data):
        adf, sdf, delta = data
        stats, climbs = {}, None
        stats.update(copy_times(ajournal))
        stats.update(active_stats(adf))
        stats.update(self.__average_power(s, ajournal, stats[N.ACTIVE_TIME]))
        stats.update(times_for_distance(adf))
        stats.update(hrz_stats(adf))
        stats.update(max_med_stats(adf))
        stats.update(max_mean_stats(adf))
        stats.update(direction_stats(adf))
        if sdf is not None:
            stats.update(response_stats(sdf, delta))
        if present(adf, N.ELEVATION):
            params = Climb(**loads(Constant.from_name(s, self.climb_ref).at(s).value))
            climbs = list(find_climbs(adf, params=params))
            add_climb_stats(adf, climbs)
        return data, stats, climbs

    @safe_dict
    def __average_power(self, s, ajournal, active_time):
        # this doesn't fit nicely anywhere...
        energy = StatisticJournal.at(s, ajournal.start, N.ENERGY_ESTIMATE, PowerCalculator,
                                     ajournal.activity_group)
        if energy and active_time:
            return {N.MEAN_POWER_ESTIMATE: 1000 * energy.value / active_time}
        else:
            return {N.MEAN_POWER_ESTIMATE: 0}

    def _copy_results(self, s, ajournal, loader, data):
        df, stats, climbs = data
        self.__copy(ajournal, loader, stats, T.START, None,
                    None, ajournal.start, type=StatisticJournalTimestamp)
        self.__copy(ajournal, loader, stats, T.FINISH, None,
                    None, ajournal.start, type=StatisticJournalTimestamp)
        self.__copy(ajournal, loader, stats, T.TIME, Units.S,
                    S.join(S.MAX, S.SUM, S.MSR), ajournal.start)
        self.__copy(ajournal, loader, stats, T.ACTIVE_DISTANCE, Units.KM,
                    S.join(S.MAX, S.CNT, S.SUM, S.MSR), ajournal.start)
        self.__copy(ajournal, loader, stats, T.ACTIVE_TIME, Units.S,
                    S.join(S.MAX, S.SUM, S.MSR), ajournal.start)
        self.__copy(ajournal, loader, stats, T.ACTIVE_SPEED, Units.KMH,
                    S.join(S.MAX, S.AVG, S.MSR), ajournal.start)
        self.__copy(ajournal, loader, stats, T.MEAN_POWER_ESTIMATE,Units. W,
                    S.join(S.MAX, S.AVG, S.MSR), ajournal.start)
        self.__copy(ajournal, loader, stats, T.DIRECTION, Units.DEG,
                    None, ajournal.start)
        self.__copy(ajournal, loader, stats, T.ASPECT_RATIO, None,
                    None, ajournal.start)
        self.__copy_all(ajournal, loader, stats, T.MIN_KM_TIME_ANY, Units.S,
                        S.join(S.MIN, S.MSR), ajournal.start)
        self.__copy_all(ajournal, loader, stats, T.MED_KM_TIME_ANY, Units.S,
                        S.join(S.MIN, S.MSR), ajournal.start)
        self.__copy_all(ajournal, loader, stats, T.PERCENT_IN_Z_ANY, Units.PC,
                        None, ajournal.start)
        self.__copy_all(ajournal, loader, stats, T.TIME_IN_Z_ANY, Units.S,
                        None, ajournal.start)
        self.__copy_all(ajournal, loader, stats, T.MAX_MED_HR_M_ANY, Units.BPM,
                        S.join(S.MAX, S.MSR), ajournal.start)
        self.__copy_all(ajournal, loader, stats, T.MAX_MEAN_PE_M_ANY, Units.W,
                        S.join(S.MAX, S.MSR), ajournal.start)
        self.__copy_all(ajournal, loader, stats, T._delta(T.FITNESS_ANY), Units.FF,
                        S.join(S.MAX, S.MSR), ajournal.start)
        self.__copy_all(ajournal, loader, stats, T._delta(T.FATIGUE_ANY), Units.FF,
                        S.join(S.MAX, S.MSR), ajournal.start)
        self.__copy_all(ajournal, loader, stats, T.EARNED_D_ANY, Units.S,
                        S.join(S.MAX, S.MSR), ajournal.start)
        self.__copy_all(ajournal, loader, stats, T.RECOVERY_D_ANY, Units.S,
                        S.join(S.MAX, S.MSR), ajournal.start)
        self.__copy_all(ajournal, loader, stats, T.PLATEAU_D_ANY, Units.FF,
                        None, ajournal.start)
        if climbs:
            loader.add(T.TOTAL_CLIMB, Units.M, S.join(S.MAX, S.MSR), ajournal,
                       sum(climb[N.CLIMB_ELEVATION] for climb in climbs), ajournal.start, StatisticJournalFloat,
                       description=DESCRIPTIONS[T.TOTAL_CLIMB])
            for climb in sorted(climbs, key=lambda climb: climb[N.TIME]):
                self.__copy(ajournal, loader, climb, T.CLIMB_ELEVATION, Units.M,
                            S.join(S.MAX, S.SUM, S.MSR), climb[N.TIME])
                self.__copy(ajournal, loader, climb, T.CLIMB_DISTANCE, Units.KM,
                            S.join(S.MAX, S.SUM, S.MSR), climb[N.TIME])
                self.__copy(ajournal, loader, climb, T.CLIMB_TIME, Units.S,
                            S.join(S.MAX, S.SUM, S.MSR), climb[N.TIME])
                self.__copy(ajournal, loader, climb, T.CLIMB_GRADIENT, Units.PC,
                            S.join(S.MAX, S.MSR), climb[N.TIME])
                self.__copy(ajournal, loader, climb, T.CLIMB_POWER,Units. W,
                            S.join(S.MAX, S.MSR), climb[N.TIME])
                if T.CLIMB_CATEGORY in climb:
                    self.__copy(ajournal, loader, climb, T.CLIMB_CATEGORY, None,
                                None, climb[T.TIME], type=StatisticJournalText)
        if stats:
            log.warning(f'Unsaved statistics: {list(stats.keys())}')

    def __copy_all(self, ajournal, loader, stats, pattern, units, summary, time, type=StatisticJournalFloat):
        description = DESCRIPTIONS[pattern]
        for title in list(titles_for_names(pattern, stats)):  # list to avoid reading after modification
            self.__copy(ajournal, loader, stats, title, units, summary, time, type=type, description=description)

    def __copy(self, ajournal, loader, stats, title, units, summary, time, type=StatisticJournalFloat,
               description=None):
        if not description: description = DESCRIPTIONS[title]
        name = simple_name(title)
        if name in stats:
            try:
                loader.add(title, units, summary, ajournal, stats[name], time, type, description=description)
            except:
                log.warning(f'Failed to load {title}')
                log_current_exception(traceback=True)
            del stats[name]
        else:
            log.warning(f'Did not calculate {title} '
                        f'({time_to_local_time(ajournal.start)} / {ajournal.activity_group.name})')


DESCRIPTIONS = defaultdict(lambda: None, {
    T.START: '''The start time for the activity.''',
    T.FINISH: '''The finish time for the activity.''',
    T.TIME: '''The total duration of the activity.''',
    T.ACTIVE_DISTANCE: '''The total distance travelled while active (ie not paused).''',
    T.ACTIVE_TIME: '''The total time while active (ie not paused).''',
    T.ACTIVE_SPEED: '''The average speed while active (ie not paused).''',
    T.MEAN_POWER_ESTIMATE: '''The average estimated power.''',
    T.DIRECTION: '''The angular direction (clockwise from North) of the mid-point of the activity relative to the start.''',
    T.ASPECT_RATIO: f'''The relative extent of the activity along and across the {T.DIRECTION}.''',
    T.MIN_KM_TIME_ANY: '''The shortest time required to cover the given distance.''',
    T.MED_KM_TIME_ANY: '''The median (typical) time required to cover the given distance.''',
    T.PERCENT_IN_Z_ANY: '''The percentage of time in the given HR zone.''',
    T.TIME_IN_Z_ANY: '''The total time in the given HR zone.''',
    T.MAX_MED_HR_M_ANY: '''The highest median HR in the given interval.''',
    T.MAX_MEAN_PE_M_ANY: '''The highest average power estimate in the given interval.''',
    T._delta(T.FATIGUE_ANY): '''The change (over the activity) in the SHRIMP Fatigue parameter.''',
    T._delta(T.FITNESS_ANY): '''The change (over the activity) in the SHRIMP Fitness parameter.''',
    T.EARNED_D_ANY: '''The time before Fitness returns to the value before the activity.''',
    T.RECOVERY_D_ANY: '''The time before Fatigue returns to the value before the activity.''',
    T.PLATEAU_D_ANY: '''The maximum Fitness achieved if this activity was repeated (with the same time gap to the previous).''',
    T.TOTAL_CLIMB: '''The total height climbed in the detected climbs (only).''',
    T.CLIMB_ELEVATION: '''The difference in elevation between start and end of the climb.''',
    T.CLIMB_DISTANCE: '''The distance travelled during the climb''',
    T.CLIMB_TIME: '''The time spent on the climb.''',
    T.CLIMB_GRADIENT: '''The average inclination of the climb (elevation / distance).''',
    T.CLIMB_POWER: '''The average estimated power during the climb.''',
    T.CLIMB_CATEGORY: '''The climb category (text, "4" to "1" and "HC").'''
})