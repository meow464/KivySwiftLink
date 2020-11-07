

class OSCLiveCallback2:

    @callback
    def func0(test: list(int),test2: int):
        """([test[x] for x in range(test_count)],test2)"""

    # @callback
    # def funcX(test: float,test2: int):
    #     "(test,test2)"

    def func0b(test: str,test2: int):
        pass

    # @callback
    def func1(test: list(long),test2: int):
        "([test[x] for x in range(test_count)],test2)"

    @callback
    def func2(test: list(uint8),test2: float):
        "(list(test[0:test_count]),test2)"
        
    @callback
    def func2b(test: list(uint8),test2: float):
        "(list(test[0:test_count]),test2)"

    
    def func3(test: list(float), test2: list(double), test3:list(int),test4:list(str) ):
        "([test[x] for x in range(test_count)],test2)"

    
    def func4(test: list(double),test2: float):
        "([test[x] for x in range(test_count)],test2)"

    # @callback
    # def func5(test: str,test2: float):
    #     "(test.decode('utf-8'),test2)"
    # @callback
    # def seq1(value: int):
    #     "change_seq_color(value)"

    # @callback
    # def padnames(conchar:str):
    #     "sync_note_names(json.loads(conchar))"
    
    # @callback 
    # def send_clock(clock:float):
    #     "get_clock(clock)"
    
    # @callback
    # def clip_is_triplet(value:int):
    #     "clip_is_triplet(value)"
    
    # @callback  
    # def clip_is_playing(value: int):
    #     "clip_is_playing(value)"

    # @callback
    # def cur_track_name(conchar:str):
    #     "current_track_name(conchar.decode('utf-8'))"

    # @callback
    # def cur_clip_name(conchar:str):
    #     "current_clip_name(conchar.decode('utf-8'))"

    # @callback
    # def has_clip(value:int):
    #     "has_clip(value)"

    # @callback
    # def device_list(conchar:str):
    #     "show_fx_track(json.loads(conchar))"

    # @callback
    # def drum_device_list(conchar:str):
    #     "show_drumpad_devices(json.loads(conchar))"

    # @callback
    # def drum_device_prelist(conchar:str):
    #     "update_drumpad_pre_names(json.loads(conchar))"

    # @callback
    # def track_list(conchar:str):
    #     "update_tracks(json.loads(conchar))"

    
    def update_btn(test0:str) -> str:
        "pass"