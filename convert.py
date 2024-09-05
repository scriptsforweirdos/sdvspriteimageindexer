import os
from PIL import ImageDraw, ImageFont, Image


def getFiles():
    inbound = "in"
    files = [f for f in os.listdir(inbound) if os.path.isfile(os.path.join(inbound, f)) and not f.startswith(".")]
    return files


def makeGrid(fileName):
    # define the fonts
    fontFace = ImageFont.truetype("Hasubi.ttf", 15)
    fillcolor = "white"
    shadowcolor = "black"

    # get the file
    fileExtension = fileName.rsplit(".", 1)[1]
    fileParts = fileName.split("-")
    spriteWidth = int(fileParts[-2])
    spriteHeight = int(fileParts[-1].split(".")[0])

    # Open image and get dims
    baseImage = Image.open("in/{}".format(fileName))
    width, height = baseImage.size

    # Double the size so everything is legible
    newWidth = width * 2
    newHeight = height * 2
    cols = int(width / spriteWidth)
    rows = int(height / spriteHeight)
    bigImage = baseImage.resize((newWidth, newHeight), Image.Resampling.NEAREST)

    # Add the text
    i = 0
    draw = ImageDraw.Draw(bigImage)
    for row in range(rows):
        for col in range(cols):
            thisX = (spriteWidth * 2) * col
            thisY = (spriteHeight * 2) * row
            # Outlined text. First we draw the black outline
            draw.text((thisX - 1, thisY - 1), str(i), font=fontFace, fill=shadowcolor)
            draw.text((thisX + 1, thisY - 1), str(i), font=fontFace, fill=shadowcolor)
            draw.text((thisX - 1, thisY + 1), str(i), font=fontFace, fill=shadowcolor)
            draw.text((thisX + 1, thisY + 1), str(i), font=fontFace, fill=shadowcolor)

            # Draw the white text on top
            draw.text((thisX, thisY), str(i), font=fontFace, fill=fillcolor)
            i += 1  # increment the number

    # make out and processed dirs if they don't exist
    os.makedirs("out/", exist_ok=True)
    os.makedirs("processed/", exist_ok=True)
    # save new image
    bigImage.save("out/{}-indexed.{}".format(fileParts[0], fileExtension))
    # move source image to processed dir
    os.rename("in/{}".format(fileName), "processed/{}".format(fileName))


if __name__ == "__main__":
    toConvert = getFiles()
    for inFile in toConvert:
        makeGrid(inFile)
