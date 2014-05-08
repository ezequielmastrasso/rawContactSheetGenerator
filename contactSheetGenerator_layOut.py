import imageMagick
"""
OBJECT (directoryIn
        directoryOut
        contactSheetWidth
        useEmbebedJpg
        sharpen
        backGroundColor
        textColor
        imageBorder [size, color, opacity]
        imageExpandHistogram
        style=[single, strip, grid]
        stripLength[]
        gridSize[2,5]

        //TEXT POSITION [SIDE, offset%]
        //SIDES LISTED CLOCKWISE STARTING ON THE TOP
        //TOP 0
        //RIGHT 1
        //DOWN 2
        //LEFT 3
        //BOTTOM 4

        //TOP
        EXIF_AutoISOSpeed
        EXIF_AutoISOSpeed_show
        EXIF_AutoISOSpeed_position 0 5
        EXIF_compensation
        EXIF_compensation_show
        EXIF_compensation_position 0 25
        EXIF_shutter
        EXIF_shutter_show
        EXIF_shutter_position 0 50
        EXIF_aperture
        EXIF_aperture_show
        EXIF_aperture_position 0 65
        EXIF_ISO
        EXIF_ISO_show
        EXIF_ISO_position 0 80

        //RIGHT
        EXIF_camera
        EXIF_camera_show
        EXIF_camera_position 1 5
        EXIF_fileName
        EXIF_fileName_show
        EXIF_fileName_position 1 35
        EXIF_Date
        EXIF_Date_show
        EXIF_Date_position 1 60
        EXIF_Time
        EXIF_Time_show
        EXIF_Time_position 1 80

        //LEFT
        EXIF_fileSize
        EXIF_fileSize_show
        EXIF_fileSize_position 2 10
        EXIF_fileResolution
        EXIF_fileResolution_show
        EXIF_fileResolution_position 2 25
        EXIF_whiteBalance
        EXIF_whiteBalance_show
        EXIF_whiteBalance_position 2 55
        EXIF_fileFormat
        EXIF_fileFormat_show
        EXIF_fileFormat_position 2 75
        EXIF_fileColorSpace
        EXIF_fileColorSpace_show
        EXIF_fileColorSpace_position 2 95
        //DOWN
        EXIF_shootingMode
        EXIF_shootingMode_show
        EXIF_shootingMode_position 3 5
        EXIF_meteringMode
        EXIF_meteringMode_show
        EXIF_meteringMode_position 3 25
        EXIF_lens
        EXIF_lens_show
        EXIF_lens_position 3 50
        EXIF_focalLength
        EXIF_focalLength_show
        EXIF_focalLength_position 3 85
        //INFO_PLUS
        EXIF_author
        EXIF_author_show
        EXIF_author_position 4 20
        EXIF_ownersName
        EXIF_ownersName_show
        EXIF_ownersName_position 4 60




        )
    __INIT__
        get images from directoryIn
        for image in images
            if useEmbebedJpg
                thumbNail=extractJPG()
            else
                thumbNail=convertRaw()
            if imageExpandHistogram
                expandHistogram()
            exif=extractShootingInformation()
            contactSheet=expandCanvas( 10%,backgroundColor)
            delete image
            writeExifOncontactSheet()
        if style=single
            writeImage
            clearBuffer
        if style=strip
            createNewImage
            pages=mod(imageCount/stripLenght)
            for page in pages:
                write contactSheetToPage
                writePage
                deleteBuffer
        if style=grid
            createNewImage
            pages=mod(imageCount/(gridSize[0]*gridSize[1])
            index=0
            for page in pages
                writeContactSheetToPage(x,y)
                index++
"""

