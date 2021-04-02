#import <Foundation/Foundation.h>

//######## cdef extern Callback Function Pointers: ########//
typedef void (*realmdatabase_ptr0)(const char* _Nonnull arg0, const void* _Nonnull arg1);

//######## cdef extern Callback Struct: ########//
typedef struct RealmDatabaseCallback {
	realmdatabase_ptr0 _Nonnull getItemNames;
	realmdatabase_ptr0 _Nonnull receiveInterfacePreset;
	realmdatabase_ptr0 _Nonnull receiveInterfacePreList;
} RealmDatabaseCallback;


//######## cdef extern Send Functions: ########//
@protocol RealmDatabaseDelegate <NSObject>
- (void)set_RealmDatabase_Callback:(struct RealmDatabaseCallback)callback;
- (void)setInterfaceCallback:(const char* _Nonnull)realmID obj:(const void* _Nonnull)obj;
- (void)loadBrowserItem:(long)item;
- (void)searchBrowser:(const char* _Nonnull)search_string;
- (void)inject_test_items;
- (void)inject_categories:(const char* _Nonnull)search;
- (void)transferBrowserData:(const char*  _Nonnull)data;
- (void)searchInterfacePresets:(const char* _Nonnull)realmID key:(const char* _Nonnull)key;
- (void)loadInterfacePreset:(const char* _Nonnull)realmID index:(long)index;
- (void)saveInterfacePreset:(const char* _Nonnull)realmID item:(const char* _Nonnull)item;
- (void)updateInterfacePreset:(const char* _Nonnull)realmID item:(const char* _Nonnull)item;
- (long)loadInterfaceFile:(const char* _Nonnull)db_name;
@end


static id<RealmDatabaseDelegate> _Nonnull realm_database;
//######## Send Functions: ########//
void InitRealmDatabaseDelegate(id<RealmDatabaseDelegate> _Nonnull callback);

void set_RealmDatabase_Callback(struct RealmDatabaseCallback callback);

void setInterfaceCallback(const char* _Nonnull realmID, const void* _Nonnull obj);

void loadBrowserItem(long item);

void searchBrowser(const char* _Nonnull search_string);

void inject_test_items();

void inject_categories(const char* _Nonnull search);

void transferBrowserData(const char*  _Nonnull data);

void searchInterfacePresets(const char* _Nonnull realmID, const char* _Nonnull key);

void loadInterfacePreset(const char* _Nonnull realmID, long index);

void saveInterfacePreset(const char* _Nonnull realmID, const char* _Nonnull item);

void updateInterfacePreset(const char* _Nonnull realmID, const char* _Nonnull item);

long loadInterfaceFile(const char* _Nonnull db_name);
