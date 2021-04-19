from swift_types import *


class CameraApi:

    def start_capture(mode: str):
        pass

    def stop_capture(mode: str):
        pass

    def set_camera_mode(mode: str):
        pass

    def select_camera(index: long):
        pass

    def take_photo():
        pass

    def take_multi_photo(count: long):
        pass

    @callback
    def returned_image_data(data: data, width: long, height: long):
        pass

    @callback
    def returned_thumbnail_data(data: data, width: long, height: long):
        pass
    
    @callback
    def returned_pixel_data(data: data):
        pass
    
    @callback
    def change_cam_res(width: long, height: long):
        pass