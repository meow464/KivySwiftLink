#Not Used But works
# @struct
# class BrowserItemTemp:
#     uuid: str
#     name: str
#     index: str
#     source: str
#     category: str
#     sub_category0: str
#     sub_category1: str
#     sub_category2: str
#     sub_category3: str
#     type: str
#     sub_type: str
#     ext: str
#     is_plugin: bool

# #not used but works
# @struct
# class InterfacePresetTemp :
    
#     uuid: str
#     id: int
#     name: str
#     category: str
#     sub_category0: str
#     sub_category1: str
#     sub_category2: str
#     sub_category3: str
#     value_list: str
#     userdata: str
#     has_userdata: bool

class RealmDatabase:

    # @callback
    # def receiveBrowseritem(item:BrowserItemTemp):
    #     pass

    
    def loadBrowserItem(item:long):
        pass

    @callback
    def getItemNames(names:json):
        pass

    def searchBrowser(search_string:str):
        pass

    def inject_test_items():
        pass

    def inject_categories(search:str):
        pass

    def transferBrowserData(data:bytes):
        pass


    @callback
    def receiveInterfacePreset(item:json):
        pass

    @callback    
    def receiveInterfacePreList(prelist:json):
        pass

    def searchInterfacePresets(realmID:str,key:str):
        pass

    def loadInterfacePreset(realmID:str,index:long):
        pass

    def saveInterfacePreset(realmID:str,item:json):
        pass

    def updateInterfacePreset(realmID:str,item:json):
        pass

    def loadInterfaceFile(db_name:str) -> long:
        pass
    ##### clipslots #####

    #@callback
    #@call_target(clipslots)
    #@call_args(arg0, arg1 , Red, Green, Blue)
    # def slot_color(arg0: int,arg1: int,arg2: int):    
    #     """
    #     cdef dict _dict = arg0[]
    #     """
