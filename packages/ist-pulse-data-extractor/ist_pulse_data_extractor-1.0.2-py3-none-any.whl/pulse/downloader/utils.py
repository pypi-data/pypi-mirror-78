import random
from loguru import logger as log
from time import time
import pendulum
import pickle

def uid_filter(ratio: float):
    """Returns a list of UID prefixes to facilitate random sampling during searches
    Since document UIDs are randomly distributed, we can approximate the desired
    sampling ratio at search-time using combinations of certain UID prefixes.
    :param ratio:
    :return:
    """
    if ratio < 0 or ratio > 1:
        raise Exception("Ratio must be between 0 and 1")

    x, uids = 0.0, []
    pool_1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]
    pool_2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]

    while x < ratio - (1 / 16.0):
        d1 = random.choice(pool_1)
        pool_1.remove(d1)
        uids.append(f"{d1}*")
        x += 1 / 16.0

    d1 = random.choice(pool_1)
    while x < ratio:
        d2 = random.choice(pool_2)
        pool_2.remove(d2)
        uids.append(f"{d1}{d2}*")
        x += 1 / 256.0

    return sorted([u for u in uids])


def get_dates_in_range(start_date, end_date):
        dates = []
        d = pendulum.parse(start_date, strict=False)
        end = pendulum.parse(end_date, strict=False)
        while d < end:
            d_id = d.date()
            dates.append(str(d_id))
            d += pendulum.duration(days=1)
        return dates

def elapsed_hms(seconds, verbose=False):
    """Get elapsed hours, minutes, and seconds as a string
    :param seconds: number of seconds elapsed/remaining
    :param verbose: get a more verbose readout
    :return:
    """
    return (
        human_time(time() - seconds, verbose)
        if isinstance(seconds, int) or isinstance(seconds, float)
        else human_time((pendulum.now() - seconds).total_seconds())
    )

def human_time(sec, verbose=True):
    """Get elapsed/remaining human-readable time
    :param sec: elapsed seconds or seconds remaining
    :param verbose: a more verbose readout
    :return:
    """
    h, s = divmod(sec, (60 * 60))
    m, s = divmod(s, 60)
    sh, sm, ss = ["s" if t else "" for t in (h, m, s)]
    if verbose:
        return (
            f"{h} hour{sh} {m:1.0f} min{sm} " if h > 0 else f"{m:1.0f} min{sm} "
        ) + f"{s+s % 1:.2f} sec{ss}"
    else:
        return (f"{h}h " if h > 0 else "") + f"{m:1.0f}m {s:5.2f}s"

class LargeBinaryFile(object):
    """A large binary file
    Large pickle files will fail to load if they're over a certain size. This
    class prevents those issues.
    """
    def __init__(self, f):
        self.f = f

    def __getattr__(self, item):
        return getattr(self.f, item)

    def read(self, n):
        if n >= (1 << 31):
            buffer = bytearray(n)
            idx = 0
            while idx < n:
                batch_size = min(n - idx, 1 << 31 - 1)
                buffer[idx : idx + batch_size] = self.f.read(batch_size)
                idx += batch_size
            return buffer
        return self.f.read(n)

    def write(self, buffer):
        n = len(buffer)
        idx = 0
        while idx < n:
            batch_size = min(n - idx, 1 << 31 - 1)
            self.f.write(buffer[idx : idx + batch_size])
            idx += batch_size


def dump_pkl(obj, file_path):
    """Safely dumps an object to a pickle file
    Wraps the object as a LargeBinaryFile to work around pickle size limitations
    :param obj: the object to save
    :param file_path: full filepath
    :return:
    """
    with open(file_path, "wb") as f:
        return pickle.dump(obj, LargeBinaryFile(f), protocol=pickle.HIGHEST_PROTOCOL)


def load_pkl(file_path):
    """Safely loads a pickle file
    Should work regardless of whether or not the pickle file was stored as a
    LargeBinaryFile
    :param file_path: full filepath
    :return: the pickled object
    """
    with open(file_path, "rb") as f:
        return pickle.load(LargeBinaryFile(f))





class Reservoir:
    """
    A fixed-size container that can be used to hold a uniform random sample from an infinite stream of objects

    This implementation is based on Knuth's implementation of the reservoir sampling algorithm.
    It guarantees that each element inserted has an equal probability of being represented.
    """

    def __init__(self, size:int or None=500):
        """
        Initializes the reservoir
        :param size: max number of items to hold in the reservoir
        """
        self._items = []
        self._index = 0
        self._size = size

    def insert(self, item):
        """
        Inserts an item into the reservoir
        :param item: the item
        """
        if self.size is None:
            self._items.append(item)
        elif self._index < self._size:
            self._items.append(item)
        else:
            m = random.randint(0, self._index)
            if m < self._size:
                self._items[m] = item
        self._index += 1

    def bulk_insert(self, items):
        """
        Inserts multiple items into the reservoir
        :param items: a list of items
        :return:
        """
        for item in items:
            self.insert(item)

    @property
    def items(self):
        """
        Elements inserted into the reservoir before the reservoir is full will always be in insertion order
        until they are replaced by additional elements. If random ordering is important, perform a shuffle
        when retrieving the elements by accessing the `items_shuffled` property.

        :return: the items
        """
        return self._items

    @property
    def items_shuffled(self):
        return random.shuffle(self._items)

    @property
    def index(self):
        return self._index

    @property
    def size(self):
        return self._size
