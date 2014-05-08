rawContactSheetGenerator
========================

Raw contact Sheet Generator, uses DCRaw,Exifv2 and PIL to create thumbnails of raw files, lighting fast, with custom fields like good old times transparencies.


Intro:
------
After upgrading from the 400D to the 7d and subsequently to the 5d Mark II and later to a Phase One P+ digital back, I noticed a huge performance hit on developing the raw files, no matter what software i would use.
Its understandable as the 18mp from 7d are 25mb, 21mp raw files from the 5d are almost 30 Mb, and the Phase One P+ images can go up to 200mb depending on the DB.
After the first long field trip bringing home around 100Gb of raw material, I had to figure a way to quickly export jpg thumbnails to be able to review them, as my laptop took more than 9 sec for each raw file to show up in full res with DPP, about the same with C1, Bible, and DxO. On top of that i also wanted information from the exif to be printed on the picture for quick review of the settings. Its easier to pick one shot from several of the same subject when you know which ones will have more depth of field, be less noisy, and have less hand held blur.
After going through numerous softwares trying to get exactly what I wanted, I got really frustrated.
DCRaw came into play here (opensource!!), huge perfomance difference, even more with www.heliconsoft.com modification to make dcraw multithread!.
The code quickly built up to have a few more options than expected, as to be able to pick exactly which info to print in the picture, where to print it, a histogram overlay, custom text (for ie: the place where they where taken, see the sample images), and an extra panel for even showing more info as the lens used, focal length, focal distance, photographer (from camera settings), all read from the picture itself of course.
It can go through 100 21megapixels Phase one raw photos within a directory, in less than 10 minutes, highly customizable to even look like a Mamiya AFD AFDII AFDIII or Phaso One AF film strip info, and this is the result.

Check the screenshots folder for some examples made from 5dmarkII, and Phase Ones P25+ files.
