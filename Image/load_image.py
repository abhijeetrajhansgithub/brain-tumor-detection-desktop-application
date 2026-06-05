def return_image_path() ->str :
    import os
    current_path = os.path.dirname(os.path.abspath(__file__))

    jpg_image_file_path = os.path.join(current_path, 'image.jpg')

    return jpg_image_file_path

# print(return_image_path())

def return_fetched_image_dir() ->str :
    import os
    current_path = os.path.dirname(os.path.abspath(__file__))

    fi_dir = os.path.join(current_path, 'FetchedImage')

    return fi_dir


def return_xai_button_bg_image_path() -> str:
    import os
    current_path = os.path.dirname(os.path.abspath(__file__))

    xai_button_bg_image_path = os.path.join(current_path, 'xai_button_bg.png')

    return xai_button_bg_image_path


# print(return_xai_button_bg_image_path())