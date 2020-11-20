import paddlehub as hub


def checkTextwithModule(text, module):
    input_dict = {"text": [text]}
    results = module.detection(data=input_dict, use_gpu=False, batch_size=1)
    print(repr(results))
    return results[0]['porn_detection_label']