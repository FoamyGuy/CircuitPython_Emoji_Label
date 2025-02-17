# SPDX-FileCopyrightText: Copyright (c) 2025 Tim C
#
# SPDX-License-Identifier: MIT
import displayio
import adafruit_imageload
import terminalio
import bitmaptools

class EmojiLabel(displayio.Group):
    WIDTH = 10
    MULTI_CODE_RANGES = [[35, 35], [42, 42], [48, 57], [9977, 9977], [10084, 10084], [127462, 127487], [127939, 127940], [127946, 127948], [127987, 127988], [128008, 128008], [128021, 128021], [128038, 128038], [128059, 128059], [128065, 128065], [128104, 128105], [128113, 128113], [128115, 128115], [128129, 128130], [128134, 128135], [128558, 128558], [128565, 128566], [128581, 128583], [128587, 128587], [128675, 128675], [128692, 128694], [129336, 129337], [129341, 129342], [129485, 129486], [129489, 129489], [129492, 129492], [129495, 129495], [129497, 129497]]
    FIVE_WIDES = [127947, 9977, 128105, 127948, 128104, 128065, 127987]
    def __init__(self, text, ascii_font=terminalio.FONT):
        super().__init__()
        self.font = ascii_font
        self.ascii_palette = displayio.Palette(2)
        self.ascii_palette[0] = 0x000000
        self.ascii_palette[1] = 0xffffff

        self._last_x = 0
        self._last_y = 0

        skip_count = 0
        for i, char in enumerate(text):
            if skip_count > 0:
                skip_count -= 1
                continue
            print(char)
            if char == "\n":
                print("newline")
                self._last_y += 12
                self._last_x = 0
                continue

            found_glyph = self.font.get_glyph(ord(char))
            if found_glyph is not None:
                bmp = displayio.Bitmap(found_glyph.width, found_glyph.height, 2)
                glyph_offset_x = (
                        found_glyph.tile_index * found_glyph.width
                )
                bitmaptools.blit(bmp, found_glyph.bitmap, 0,0,
                                 x1=glyph_offset_x,
                                 y1=0,
                                 x2=glyph_offset_x + found_glyph.width,
                                 y2=found_glyph.height,
                                 skip_source_index=0)
                tg = displayio.TileGrid(bitmap=bmp, pixel_shader=self.ascii_palette)
                tg.x = self._last_x
                tg.y = self._last_y
                self._last_x += found_glyph.width
                self.append(tg)
            else:
                bmp = None
                for cur_range in EmojiLabel.MULTI_CODE_RANGES:
                    # is it a valid multi code prefix
                    if cur_range[0] <= ord(char) <= cur_range[1]:

                        if ord(char) in EmojiLabel.FIVE_WIDES:
                            # try 5 wide file
                            try:
                                filename = 'emoji/U+{:X}_U+{:X}_U+{:X}_U+{:X}_U+{:X}.png'.format(
                                    ord(char),
                                    ord(text[i + 1]),
                                    ord(text[i + 2]),
                                    ord(text[i + 3]),
                                    ord(text[i + 4]),
                                )
                                print(filename)
                                bmp, palette = adafruit_imageload.load(filename)
                                skip_count = 4
                                break
                            except (OSError,IndexError):
                                pass

                        # try 4 wide file
                        try:
                            filename = 'emoji/U+{:X}_U+{:X}_U+{:X}_U+{:X}.png'.format(
                                ord(char),
                                ord(text[i + 1]),
                                ord(text[i + 2]),
                                ord(text[i + 3])
                            )
                            print(filename)
                            bmp, palette = adafruit_imageload.load(filename)
                            skip_count = 3
                            break
                        except (OSError, IndexError):
                            # try double wide file
                            try:
                                filename = 'emoji/U+{:X}_U+{:X}.png'.format(ord(char), ord(text[i + 1]))
                                print(filename)
                                bmp, palette = adafruit_imageload.load(filename)
                                skip_count = 1
                                break
                            except (OSError, IndexError):
                                pass

                if bmp is None:
                    # it's not a multi code prefix
                    filename = 'emoji/U+{:X}.png'.format(ord(char))
                    print(filename)
                    try:
                        bmp, palette = adafruit_imageload.load(filename)
                    except OSError:
                        print(f"Unable to render: {hex(ord(char))}")



                # filename = 'emoji/U+{:X}.png'.format(ord(char))
                # print(filename)
                # try:
                #     bmp, palette = adafruit_imageload.load(filename)
                # except OSError:
                #     # try double wide file
                #     try:
                #         filename = 'emoji/U+{:X}_U+{:X}.png'.format(ord(char), ord(text[i+1]))
                #         print(filename)
                #         bmp, palette = adafruit_imageload.load(filename)
                #         skip_count = 1
                #     except OSError:
                #
                #         # try 4 wide file
                #         try:
                #             filename = 'emoji/U+{:X}_U+{:X}_U+{:X}_U+{:X}.png'.format(
                #                 ord(char),
                #                 ord(text[i + 1]),
                #                 ord(text[i + 2]),
                #                 ord(text[i + 3])
                #             )
                #             print(filename)
                #             bmp, palette = adafruit_imageload.load(filename)
                #             skip_count = 3
                #         except OSError:
                #             pass
                #
                #         print(f"Unable to render: {hex(ord(char))}")

                try:
                    tg = displayio.TileGrid(bitmap=bmp, pixel_shader=palette)
                    tg.x = self._last_x
                    tg.y = self._last_y
                    self._last_x += bmp.width + 1
                    self.append(tg)
                except TypeError:
                    # Unsupported bitmap type
                    print(f"Unable to render {hex(ord(char))}. Unsupported bitmap")


