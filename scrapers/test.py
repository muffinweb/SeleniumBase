import random


def get_random_resolution():
    # Yaygın ekran çözünürlükleri (gerçek kullanıcı verilerinden alınmış)
    COMMON_RESOLUTIONS = [
        (1920, 1080),
        (1366, 768),
        (1280, 720),
        (1024, 768),
        (1280, 800),
        (1360, 768),
        (800, 600),
    ]

    width, height = random.choice(COMMON_RESOLUTIONS)

    return str(width) + "," + str(height)


print(get_random_resolution())
