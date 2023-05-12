import re
import validators

class Utilities:

    @staticmethod
    def string_to_id(s):
        s = s.strip()
        s = re.sub(r"[^\w\s]", '', s)
        s = re.sub(r"\s+", '_', s)
        return s

    @staticmethod
    def link_to_id(s):
        s = s.strip()
        s = s.split("wiki/")[-1]
        return s

    @staticmethod
    def get_image_url(img):
        image_url = None
        if img is not None:
            if img.has_attr('src'):
                image_url = img['src']
                if not validators.url(image_url):
                    image_url = None
                    if img.has_attr('data-src'):
                        image_url = img['data-src']
                        if not validators.url(image_url):
                            image_url = None
            if image_url is not None:
                image_url = image_url.split("/revision/latest")[0]
                return image_url
        else:
            return image_url
