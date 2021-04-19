
from swift_types import *


@EventDispatcher(
    ['on_event1', 'on_event2', 'on_touch_down', 'on_touch_up', 'on_touch_move', 'on_lastevent']
)
class SwiftStructCall:


    def testDispatches():
        pass

    @callback
    def Func1():
        pass

    # @callback
    # def Func2(l: List[int]):
    #     pass


    # @callback
    # def calltest():
    #     pass
