from collections import deque
from utils.constant import PERIODS
from abc import ABC, abstractmethod
import abc


class MovingAverage(ABC):
    def __init__(self):
        self.current_price = None

    @abstractmethod
    def add_element(self, price):
        pass

    @abstractmethod
    def cal_moving_average(self) -> float | None:
        pass


class SimpleMovingAverage(MovingAverage):
    def __init__(self):
        super().__init__()
        self.sum = 0
        self.queue = deque()
        self.length = 0

    def add_element(self, price: float):
        self.sum += price
        self.length += 1
        self.queue.append(price)
        self.current_price = price

    def cal_moving_average(self) -> float | None:
        if self.length == 0:
            return None
        return self.sum / self.length

    def remove_first(self):
        self.sum -= self.queue[0]
        self.queue.popleft()
        self.length -= 1


class ExpoMovingAverage(MovingAverage):
    ALPHA = 2 / (PERIODS + 1)

    def __init__(self):
        super().__init__()
        self.prev_price = None

    def add_element(self, price):
        self.prev_price = self.current_price
        self.current_price = price

    def cal_moving_average(self) -> float | None:
        if not self.current_price or not self.prev_price:
            return None
        return (
            self.ALPHA * self.current_price + (1 - self.ALPHA) * self.prev_price
        )
