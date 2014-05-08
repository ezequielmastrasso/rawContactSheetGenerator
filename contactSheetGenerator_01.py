from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps
from PIL import ImageFilter


#import getopt
import sys
import os
import subprocess
from cStringIO import StringIO
import time
class contactSheetGenerator (object):
    contactSheetConfiguration = {
                         "directoryIn"    :"",
                         "directoryOut"    :"",
                         "contactSheetWidth"   :600,
                         "panelInfo"   :False,
                         "histogramInfo"   :False,
                         "histogramAlpha"   :128,
                         "histogramWidth"   :255,#pixels!
                         "histogramHeight"   :100,#pixels!
                         "expandPercent"   :5,
                         "fontColor"   :"#ff9c00",
                         "useEmbebedJpg"      :False,
                         "expandHistogram": False,
                         "sharpen"    :True,
                         "sharpenAmount"    :1,
                         "format":["jpg", "tiff","ppm"],
                         "bitDepth":[8],
                         "JPG_Quality"    :95,
                         "dcrawOption_extractJPG":[False],
                         "dcrawOption_half":[True],
                         "dcrawOption_quality":[True,0],
                         "dcrawOption_dontStretchRotatePixels":[True],
                         "dcrawOption_whiteBalance":["w"], #w use cameras if possible, a average the image
                         "style":["single","strip","grid"],
                         "stripLenght":4,
                         "gridSize":[2,5]
                         }
    catchCanonExifTags={"EXIF_camera":                  "Exif.Image.Model",
                        "EXIF_make":                    "Exif.Image.Make",
                        "EXIF_Date":                    "Exif.Image.DateTime",
                        "EXIF_shutter":                 "Exif.Photo.ExposureTime",
                        "EXIF_author":                  "Exif.Image.Artist",
                        "EXIF_aperture":                "Exif.Photo.FNumber",
                        "EXIF_shootingMode":            "Exif.Photo.ExposureProgram",
                        "EXIF_ISO":                     "Exif.Photo.ISOSpeedRatings",
                        "EXIF_compensation":            "Exif.Photo.ExposureBiasValue",
                        "EXIF_meteringMode":            "Exif.Photo.MeteringMode",
                        "EXIF_focalLength":             "Exif.Photo.FocalLength",
                        "EXIF_fileFormat":              "Exif.CanonCs.Quality",
                        "EXIF_lens":                    "Exif.Canon.LensModel",
                        "EXIF_fileColorSpace":          "Exif.Canon.ColorSpace",
                        "EXIF_whiteBalance":            "Exif.CanonPr.ColorTemperature",
                        "EXIF_fileResolutionWidth":     "Exif.Image.ImageWidth",
                        "EXIF_fileResolutionHeight":    "Exif.Image.ImageHeight"}
    ExifTags={          "customText":                   "IIQ|Phase One"
                        }

    ExifTagsPositions={ "customText":                   ["top",0],
                        "EXIF_camera":                  ["bottom",5],
                        "EXIF_make":                    ["panel",0],
                        "EXIF_Date":                    ["panel",0],
                        "EXIF_shutter":                 ["bottom",55],
                        "EXIF_author":                  ["panel",0],
                        "EXIF_aperture":                ["bottom",90],
                        "EXIF_shootingMode":            ["panel",60],
                        "EXIF_ISO":                     ["top",45],
                        "EXIF_compensation":            ["top",75],
                        "EXIF_meteringMode":            ["panel",0],
                        "EXIF_focalLength":             ["panel",0],
                        "EXIF_fileFormat":              ["panel",0],
                        "EXIF_lens":                    ["panel",50],
                        "EXIF_fileColorSpace":          ["panel",0],
                        "EXIF_whiteBalance":            ["panel",0],
                        "EXIF_fileResolutionWidth":     ["panel",0],
                        "EXIF_fileResolutionHeight":    ["panel",0]}
    ExifTagsShow={      "customText":                   True,
                        "EXIF_camera":                  True,
                        "EXIF_make":                    True,
                        "EXIF_Date":                    True,
                        "EXIF_shutter":                 True,
                        "EXIF_author":                  True,
                        "EXIF_aperture":                True,
                        "EXIF_shootingMode":            True,
                        "EXIF_ISO":                     True,
                        "EXIF_compensation":            True,
                        "EXIF_meteringMode":            True,
                        "EXIF_focalLength":             True,
                        "EXIF_fileFormat":              True,
                        "EXIF_lens":                    True,
                        "EXIF_fileColorSpace":          True,
                        "EXIF_whiteBalance":            True,
                        "EXIF_fileResolutionWidth":     True,
                        "EXIF_fileResolutionHeight":    True}
    fileList=[]
    imageWidth=0
    imageHeight=0
    imageExpandedHeigth=0
    imageExpandedWidth=0
    imageMargin=20



    def __init__(self, previz=False,directoryIn=""):
        self.getImagesFromDirectory(directoryIn)
        print "benchmarking time:"
        for fileName in self.fileList:
            t0 = time.time()
            self.extractShootingInformation(fileName)
            image=self.makeThumb(fileName)
            self.saveImage(image,fileName)
            t1 = time.time()
            print fileName, " done in ", t1-t0

    def saveImage(self,image,filePath):
        fileName, fileExtension = os.path.splitext(filePath)
        fileName=fileName+"_cs.jpg"
        quality_val = self.contactSheetConfiguration["JPG_Quality"]
        image.save(fileName,'JPEG', quality=quality_val)
    def setConfigurationOption(self, option):
        pass
    def getImagesFromDirectory(self,directory):
        path=directory
        extensionTypes = [".cr2",".jpg", ".tiff", ".tif"]
        fileList=os.listdir(path)
        i=0
        for i in range(0,len(fileList)):
            fileList[i]=fileList[i].lower()
        print "this will overWrite previously generated contactSheets:"
        for fileName in fileList:
            for type in extensionTypes:
                if fileName.endswith(type):
                    if not os.path.splitext(fileName)[0].endswith("_cs"):
                        fileName=path+"/"+fileName
                        self.fileList.append(fileName)
                    else:
                        print "---overwrite warning:", fileName

        print self.fileList

    def imageCanvasExpand(self,image,percent,panelCrop=False):
        if image.size[0]>image.size[1]:
            cropWidth=(image.size[0]/100)*percent
            cropHeight=cropWidth
        else:
            cropHeight=(image.size[1]/100)*percent
            cropWidth=cropHeight
        image=image.crop((-cropWidth, -cropHeight, image.size[0]+cropWidth,image.size[1]+cropHeight))
        self.imageExpandedWidth=image.size[0]
        self.imageExpandedHeight=image.size[1]
        return image
    def imageCanvasExpandRight(self,image,percent):
        bbox = image.getbbox()
        cropRightWidth=(image.size[0]/percent)
        image=image.crop((bbox[0], bbox[1],bbox[2], bbox[3]+cropRightWidth))
        return image
    def imageSharpen(self,image, amount):
        image = image.filter(ImageFilter.SHARPEN)
        return image
    def extractShootingInformation(self, imagePath):
        dcraw_opts = ["exiv2.exe", "-p","a", imagePath]
        dcraw_proc=subprocess.Popen(dcraw_opts, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        rawExif=dcraw_proc.communicate()[0]
        rawExifLines=rawExif.split("\n")
        for line in rawExifLines:
            for key in self.catchCanonExifTags.keys():
                if self.catchCanonExifTags[key] in line:
                    self.ExifTags[key]=line.split("  ")[-1][:-1]
                    #print key + "\t:\t" + line.split("  ")[-1][:-1]
    def imageGenerateText(self,image, tag):
        text=self.ExifTags[tag]
        fontColor=self.contactSheetConfiguration["fontColor"]
        fontsize = self.contactSheetConfiguration["contactSheetWidth"]/10
        fontScale=.35
        # portion of image width you want text width to be
        font = ImageFont.truetype("verdana.ttf", fontsize)
        #text=self.ExifTags[text]
        text_width, text_height = font.getsize(text)
        textImage = Image.new('RGBA', (text_width, text_height))
        textImageDraw = ImageDraw.Draw(textImage)
        textImageDraw.text((0, -fontsize/4), text,font=font, fill=fontColor)
        
        
        textImage=textImage.resize(( int(textImage.size[0]*fontScale), int(textImage.size[1]*fontScale)),Image.ANTIALIAS)
        if self.ExifTagsPositions[tag][0]=="top":
            #align text to the center of the top margin, image-((expandedImage-image)/4)-textWidth/2
            vertOffset=(self.imageMargin/2)-(textImage.size[1]/2)
            horOffset=(((image.size[0]-(self.imageMargin*2))*self.ExifTagsPositions[tag][1])/100)+self.imageMargin
            image.paste(textImage,(horOffset,vertOffset),textImage)
        elif self.ExifTagsPositions[tag][0]=="bottom":
            #align text to the center of the top margin, image-((expandedImage-image)/4)-textWidth/2
            vertOffset=(image.size[1]-(self.imageMargin/2))-(textImage.size[1]/2)
            horOffset=(((image.size[0]-(self.imageMargin*2))*self.ExifTagsPositions[tag][1])/100)+self.imageMargin
            image.paste(textImage,(horOffset,vertOffset),textImage)
        elif self.ExifTagsPositions[tag][0]=="right":
            textImage=textImage.rotate(-90)
            vertOffset=((image.size[1]-self.imageMargin*2)/100.0)*self.ExifTagsPositions[tag][1]+self.imageMargin
            #align right text to the center of the right margin, imageWidth-((expandedImage-image)/4)-textWidth/2
            horOffset=(image.size[0]-((self.imageExpandedWidth-self.imageWidth)/4))-textImage.size[0]/2
            image.paste(textImage,(int(horOffset),int(vertOffset)),textImage)
        elif self.ExifTagsPositions[tag][0]=="panel":
            pass
        elif self.ExifTagsPositions[tag][0]=="left":
            textImage=textImage.rotate(90)
            vertOffset=((image.size[1]-self.imageMargin*2)/100.0)*self.ExifTagsPositions[tag][1]+self.imageMargin
            #align left text to the center of the left margin, ((expandedImage-image)/4)-textWidth/2
            horOffset=((self.imageExpandedWidth-self.imageWidth)/4)-textImage.size[0]/2
            image.paste(textImage,(int(horOffset),int(vertOffset)),textImage)
        else:
            pass
        return image

    def imageWriteExif(self,image):
        for tag in self.ExifTags.keys():
            if self.ExifTagsShow[tag]:
                textImage=self.imageGenerateText(image,tag)
        return textImage
    def makePanelInfo(self,image,imageHistogram):

        panelWidth=(image.size[0]/100.0)*30
        imagePanel= Image.new('RGBA', ((panelWidth, image.size[1])))
        fontsize = self.contactSheetConfiguration["contactSheetWidth"]/22
        # portion of image width you want text width to be
        font = ImageFont.truetype("verdana.ttf", fontsize)
        fontColor=self.contactSheetConfiguration["fontColor"]
        offsetText=(imagePanel.size[1]/100.0)*5
        for tag in self.ExifTags.keys():
            if self.ExifTagsPositions[tag][0]=="panel":
                if self.ExifTagsShow[tag]:
                    text=self.ExifTags[tag]
                    text_width, text_height = font.getsize(text)
                    textImage = Image.new('RGBA', (text_width, text_height))
                    textImageDraw = ImageDraw.Draw(textImage)
                    textImageDraw.text((0, 0), text,font=font, fill=fontColor)
                    textImage=textImage.resize((textImage.size[0]/2,textImage.size[1]/2),Image.ANTIALIAS)
                    if textImage.size[0]>imagePanel.size[0]:
                        textImage=textImage.resize((panelWidth*.9,textImage.size[1]),Image.ANTIALIAS)
                    imagePanel.paste(textImage,(0,offsetText))
                    offsetText=offsetText+text_height*.8
        width=image.size[0]
        newWidth=int(image.size[0]+((image.size[0])/100.0)*30)
        image=image.crop((0, 0, newWidth, image.size[1]))
        image.paste(imagePanel,(width,0))

        return image
    def pasteHistogram(self, image, imageHistogram):

        if self.contactSheetConfiguration["panelInfo"]:
            panelWidth=(image.size[0]/130.0)*30
        else:
            panelWidth=(image.size[0]/100.0)*30
        imageHistogram.putalpha(self.contactSheetConfiguration["histogramAlpha"])
        if self.contactSheetConfiguration["panelInfo"]:
            #RESIZE TO PANEL WIDTH, PIXEL HEIGHT
            imageHistogramWidth=panelWidth-(self.imageMargin*2)
            imageHistogramHeight=self.contactSheetConfiguration["histogramHeight"]
            imageHistogram=imageHistogram.resize((imageHistogramWidth,imageHistogramHeight))
            #PASTE
            image.paste(imageHistogram,((image.size[0]-imageHistogram.size[0])-self.imageMargin,  (image.size[1]-imageHistogram.size[1])-self.imageMargin    ))
        else:
            #RESIZE TO PIXEL WIDTH AND HEIGHT
            imageHistogramWidth=self.contactSheetConfiguration["histogramWidth"]
            imageHistogramHeight=self.contactSheetConfiguration["histogramHeight"]
            imageHistogram=imageHistogram.resize((imageHistogramWidth,imageHistogramHeight))
            #PASTE
            image.paste(imageHistogram,((image.size[0]-imageHistogram.size[0])-self.imageMargin,  (image.size[1]-imageHistogram.size[1])-self.imageMargin    ),imageHistogram)
        return image

    def imageHistogram(self,image):
        histogramImage = Image.new('RGBA', (255, 100))
        histogramImageR=image.histogram()[0:255]
        histogramImageG=image.histogram()[256:511]
        histogramImageB=image.histogram()[512:767]
        histogramImageMax=[max(histogramImageR), max(histogramImageG),max(histogramImageB)]
        histogramImageMaxL=max(histogramImageMax)
        histogramImageDraw=ImageDraw.Draw(histogramImage)
        for i in range(0,len(histogramImageR)):
            histogramImageDraw.line( (  (i,0),    (i,  (histogramImageR[i]/float(histogramImageMaxL))*100)), fill="#FF0000")
            histogramImageDraw.line( (  (i,0),    (i,  (histogramImageG[i]/float(histogramImageMaxL))*100)), fill="#00FF00")
            histogramImageDraw.line( (  (i,0),    (i,  (histogramImageB[i]/float(histogramImageMaxL))*100)), fill="#0000FF")
            i=i+1
        histogramImage=histogramImage.transpose(Image.FLIP_TOP_BOTTOM)
        return histogramImage

    def imageResize(self,image):
        self.imageWidth=image.size[0]
        self.imageHeight=image.size[1]
        imageOrigWidth=image.size[0]
        imageOrigHeight=image.size[1]
        imageRatio=image.size[1]/float(image.size[0])
        if (image.size[0]<image.size[1]):
            self.imageHeight=self.contactSheetConfiguration["contactSheetWidth"]
            self.imageWidth=self.imageHeight/imageRatio
            image=image.resize((int(self.imageWidth),int(self.imageHeight)))
        else:
            self.imageWidth=self.contactSheetConfiguration["contactSheetWidth"]
            self.imageHeight=(imageOrigHeight*self.imageWidth)/imageOrigWidth
            image=image.resize((self.imageWidth,self.imageHeight))
        return image

    def makeThumb(self,file):
        expandPercent=self.contactSheetConfiguration["expandPercent"]
        sharpenAmount=self.contactSheetConfiguration["sharpenAmount"]
        if file.endswith(".jpg"):
            image = Image.open(file)
        elif file.endswith(".TIF".lower()):
            # Extract thumbnail from image
            dcraw_opts = ["dcraw.exe", "-c", "-4", "-T", file]
            print "commandRunning: ", dcraw_opts
            dcraw_proc=subprocess.Popen(dcraw_opts, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            # Read image from standard in, place in StringIO buffer
            
            rawImage = StringIO(dcraw_proc.communicate()[0])
            # Feed PIL Image object with StringIO buffer

            image = Image.open(rawImage)
            del rawImage
        elif file.endswith(".CR2".lower()):
            # Extract thumbnail from image
            dcraw_opts = ["dcraw.exe", "-c", file]
            print "commandRunning: ", dcraw_opts
            dcraw_proc=subprocess.Popen(dcraw_opts, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            # Read image from standard in, place in StringIO buffer
            
            rawImage = StringIO(dcraw_proc.communicate()[0])
            # Feed PIL Image object with StringIO buffer

            image = Image.open(rawImage)
            del rawImage
        

        imageHistogram=self.imageHistogram(image)
        image=self.imageResize(image)

        if image.size[0]>image.size[1]:
            self.imageMargin=(image.size[0]/100)*self.contactSheetConfiguration["expandPercent"]
        else:
            self.imageMargin=(image.size[1]/100)*self.contactSheetConfiguration["expandPercent"]

        if self.contactSheetConfiguration["expandHistogram"]:
            image=ImageOps.autocontrast(image)
        image=self.imageSharpen(image, sharpenAmount)
        image=self.imageCanvasExpand(image, expandPercent, panelCrop=True)
        image=self.imageWriteExif(image)
        if self.contactSheetConfiguration["panelInfo"]:
            image=self.makePanelInfo(image,imageHistogram)
        if self.contactSheetConfiguration["histogramInfo"]:
            image=self.pasteHistogram(image,imageHistogram)
        return image

#contactSheet=contactSheetGenerator(directoryIn="J:/photoCatalog/all_byDate/2013/2013_12_23_london-stonehenge")
contactSheet=contactSheetGenerator(directoryIn="/media/Misc/test")
