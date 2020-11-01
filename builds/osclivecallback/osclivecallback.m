#import <Foundation/Foundation.h>
#import "osclivecallback.h"

void InitOSCLiveCallbackDelegate(OSCLiveCallbackDelegate _Nonnull callback){
    o_s_c_live_callback = callback;
    NSLog(@"setting OSCLiveCallback delegate %@",o_s_c_live_callback);
}

void SendCallback(osclivecallback callback){
    [o_s_c_live_callback SendCallback:callback];
}
