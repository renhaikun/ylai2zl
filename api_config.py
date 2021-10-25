#conding=utf-8
#author rhk
#YUE_LI

class api_config():

    pro_config = {
        "video":"",
        "nmt":"http://10.129.15.88:8868/translation",
        "label":"",
        "text_correction":"",
        "speech2text":""
    }

    test_config = {
        "video":"http://10.129.15.88:6666/video_audio_sum",
        "nmt":"http://10.129.15.88:8868/translation",
        "label":"http://10.129.15.88:8863/label_plus",
        "text_correction":"",
        "speech2text":""
    }

    bendi_config = {
        "video":"http://127.0.0.1:8999/test",
        "nmt":"http://10.129.15.88:8868/translation",
        "label":"http://10.129.15.88:8863/label_plus",
        "text_correction":"",
        "speech2text":""

    }

    mini_config = {
        "video": "http://127.0.0.1:8760/videos_sum",
        "nmt": "http://127.0.0.1:2222/translation",

    }