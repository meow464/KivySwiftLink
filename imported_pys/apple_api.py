from swift_types import *


class AppleApi:

    def open_files():
        pass

    def open_pdf(path: str):
        pass

    def open_web_view(path: str):
        pass
    
    def open_camera():
        pass

    @callback
    def returned_path(path: str):
        pass

    @callback
    def returned_image_data(data: data):
        """
        print(arg0, arg0_size)
        """