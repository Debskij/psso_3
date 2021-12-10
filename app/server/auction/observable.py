from abc import ABC


class Observable(ABC):
    def __init__(self):
        self.observers: set[str] = set()
    
    def add_observer(self, observer_name: str):
        self.observers.add(observer_name)

    def remove_observer(self, observer) -> bool:
        if observer in self.observers:
            self.observers.remove(observer)
            return True
        return False

    def notify_observers(self):
        return self.observers
