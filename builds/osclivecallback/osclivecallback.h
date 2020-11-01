#import <Foundation/Foundation.h>
typedef void (*cfunc_ptr0)(int arg0);
typedef void (*cfunc_ptr1)(const char* _Nonnull arg0);
typedef void (*cfunc_ptr2)(float arg0);

struct OSCLiveCallbackStruct {
	cfunc_ptr0 _Nonnull seq1;
	cfunc_ptr1 _Nonnull padnames;
	cfunc_ptr2 _Nonnull send_clock;
	cfunc_ptr0 _Nonnull clip_is_triplet;
	cfunc_ptr0 _Nonnull clip_is_playing;
	cfunc_ptr1 _Nonnull cur_track_name;
	cfunc_ptr1 _Nonnull cur_clip_name;
	cfunc_ptr0 _Nonnull has_clip;
	cfunc_ptr1 _Nonnull device_list;
	cfunc_ptr1 _Nonnull drum_device_list;
	cfunc_ptr1 _Nonnull drum_device_prelist;
	cfunc_ptr1 _Nonnull track_list;
};

typedef struct OSCLiveCallbackStruct osclivecallback;


@protocol OSCLiveCallbackDelegate <NSObject>
- (void)SendCallback:(osclivecallback)callback;
@end

typedef id<OSCLiveCallbackDelegate> OSCLiveCallbackDelegate;

static OSCLiveCallbackDelegate _Nonnull o_s_c_live_callback;
void InitOSCLiveCallbackDelegate(OSCLiveCallbackDelegate _Nonnull callback);

void SendCallback(osclivecallback callback);
