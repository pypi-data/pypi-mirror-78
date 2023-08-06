import json

def JsonToString(input):
    return json.dumps(input)


def StringToJson(input):
    return json.loads(input)


from PIL import Image



def pngToJpg(file,output=""):
    im1 = Image.open(file)
    if(output==""):
        file.split("/")[-1][:-4]
    im1.save(r'path where the PNG will be stored\new file name.png')

