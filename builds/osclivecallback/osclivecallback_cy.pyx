import json
cdef extern from "osclivecallback.h":
	ctypedef void (*cfunc_ptr0)(int arg0)
	ctypedef void (*cfunc_ptr1)(const char* arg0)
	ctypedef void (*cfunc_ptr2)(float arg0)

	struct OSCLiveCallbackStruct:
		cfunc_ptr0 seq1
		cfunc_ptr1 padnames
		cfunc_ptr2 send_clock
		cfunc_ptr0 clip_is_triplet
		cfunc_ptr0 clip_is_playing
		cfunc_ptr1 cur_track_name
		cfunc_ptr1 cur_clip_name
		cfunc_ptr0 has_clip
		cfunc_ptr1 device_list
		cfunc_ptr1 drum_device_list
		cfunc_ptr1 drum_device_prelist
		cfunc_ptr1 track_list

	ctypedef OSCLiveCallbackStruct osclivecallback


	void SendCallback(osclivecallback callback)

cdef void cy_seq1(int value) with gil:
	(<object> classtest).seq1change_seq_color(value)

cdef void cy_padnames(const char* conchar) with gil:
	(<object> classtest).padnamessync_note_names(json.loads(conchar))

cdef void cy_send_clock(float clock) with gil:
	(<object> classtest).send_clockget_clock(clock)

cdef void cy_clip_is_triplet(int value) with gil:
	(<object> classtest).clip_is_tripletclip_is_triplet(value)

cdef void cy_clip_is_playing(int value) with gil:
	(<object> classtest).clip_is_playingclip_is_playing(value)

cdef void cy_cur_track_name(const char* conchar) with gil:
	(<object> classtest).cur_track_namecurrent_track_name(conchar.decode('utf-8'))

cdef void cy_cur_clip_name(const char* conchar) with gil:
	(<object> classtest).cur_clip_namecurrent_clip_name(conchar.decode('utf-8'))

cdef void cy_has_clip(int value) with gil:
	(<object> classtest).has_cliphas_clip(value)

cdef void cy_device_list(const char* conchar) with gil:
	(<object> classtest).device_listshow_fx_track(json.loads(conchar))

cdef void cy_drum_device_list(const char* conchar) with gil:
	(<object> classtest).drum_device_listshow_drumpad_devices(json.loads(conchar))

cdef void cy_drum_device_prelist(const char* conchar) with gil:
	(<object> classtest).drum_device_prelistupdate_drumpad_pre_names(json.loads(conchar))

cdef void cy_track_list(const char* conchar) with gil:
	(<object> classtest).track_listupdate_tracks(json.loads(conchar))

cdef public void* classtest
cdef class OSCLiveCallback:
	def __init__(self,object _classtest):
		global classtest 
		classtest = <void*>_classtest
		print("classtest init:", (<object>classtest))

		cdef OSCLiveCallbackStruct callbacks = [
			cy_seq1,
			cy_padnames,
			cy_send_clock,
			cy_clip_is_triplet,
			cy_clip_is_playing,
			cy_cur_track_name,
			cy_cur_clip_name,
			cy_has_clip,
			cy_device_list,
			cy_drum_device_list,
			cy_drum_device_prelist,
			cy_track_list
			]
		SendCallback(callbacks)
