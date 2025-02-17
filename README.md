# CircuitPython Emoji Label

***Note: this is a placeholder repo, it's likely this module will move somewhere else
and added to one of the CircuitPython Library bundles. But for now it can live here***


## Thank You to SerenityOS
[SerenityOS project](https://serenityos.org/) is an open source unix-like operating system with a 90s style user interface.
They have kindly made their emoji files available for others to use, and spent time and effort
making it convenient for 3rd parties to do so. Their efforts are appreciated.

## Download Emoji Image Files

**Emoji PNG files required for this library to work!**

The Library expects to find PNG files inside the `emoji/` directory in the root
of the `CIRCUITPY` drive. Each file should be named with its code value in the format 
`U+00000.png`. Multi-code emoji should have underscores separating the different values
i.e. `U+00000_U+00001.png`. 

This is the format used by the [Serenity OS Emoji project](https://emoji.serenityos.org/) which is the only set of icons
that have been tested and are considered even remotely "supported" by this library, however others may work if named
appropriately.

I would encourage you to backup your `CIRCUITPY` drive before you start,
just incase it gets too full or anything goes wrong during copying and causes corrupted storage.

On https://emoji.serenityos.org/ click on Download Images, and then unzip the file that is downloaded. 
Copy all the files from within it into a directory named `emoji/` on your `CIRCUITPY` drive. At the time of this
writing the files are about 333.6 Kb in total, so your device must have at least that much available. It has to copy 
over 1700 different files and there seems to be some per-file overhead even though each file is quite small. So it
may take several minutes to copy the files. 

## Imageload caveat (remove after patched)

At the time of writing there is an issue with the Imageload library that affects some PNG files which are included in
the emoji files. https://github.com/adafruit/Adafruit_CircuitPython_ImageLoad/issues/95 the change mentioned in the issue
allows many of the emoji images to render properly. 

However, there are still some get seem to be corrupted or "garbled". I think there may be a different issue with imageload
resulting in this, but I haven't pinned it down fully. For now just know that some emoji pictures don't look right.