from random import randint
import string


images_random_ids = [
    "1jMXR6Z8hcaefNpy0onfj02DxXoUaH07t",
    "1j3WSIKdk6oxB9pQGzHFU0DBDKZ4X41MD",
    "1V1ICCns-Lmb3hSHEICAnARB8g9elsoi-",
    "14cWoHbhQ6nEJAC-nESZqltBLBuoSfsU9",
    "1Eb_0sjjEPADUGN8LPvja95NSP1u5rj2j",
    "1Ir7qmxQv7Ovg0PiDwDUGJwHj8PGdRKQf",
    "1NtXst6YtFsKtehB1bMARJ2nmk9OfGR3Q",
    "1VC4iwmzidL0hAPvzi8EAiJxCE6uau7En",
    "1rIgoOXYfc0v3sRB7dOujhqU4V4tTBHUH",
    "1BIhJNBvecOy6iaXe1I1IrKLfdCr5OhcX",
    "1O1sJdclVCmPBucSo7qpD7wEk-HYKxkPz",
]

STRING_SHARING = "https://drive.google.com/uc?id"


def randoString(num):
    letters = string.ascii_lowercase
    return "".join([letters[randint(0, len(letters) - 1)] for i in range(num)])


def get_image_id_from_link(link: str) -> str:
    return link.replace("/view", "").replace("https://drive.google.com/file/d/", "")


def get_random_images_list(images = images_random_ids):
    photos_random = ["1Xbks6kNge06OAKOIGRQjbV1Fc5szm3XW"]
    for i in range(len(images) - 2, 0, -1):
        ends = i - 1 if i > 0 else i
        photos_random.append(images.pop(randint(0, ends)) )
    images_random_ids.extend(photos_random[1:])
    return photos_random
