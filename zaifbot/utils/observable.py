import itertools


class Observable:
    def __init__(self):
        self.__observers = set()

    def register_observers(self, observer, *observers):
        for observer in itertools.chain((observer, ), observers):
            self.__observers.add(observer)
            observer.update()

    def remove_observers(self, observer):
        self.__observers.discard(observer)

    def observers_notify(self):
        for observer in self.__observers:
            observer.update(self)
