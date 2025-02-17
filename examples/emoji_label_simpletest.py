import board
import displayio

from emoji_label import EmojiLabel


main_group = displayio.Group(scale=4)
board.DISPLAY.root_group = main_group

emojilbl = EmojiLabel("Circuit😎Python\n🌈E🐍m💾o💻j💙i🎉")

emojilbl.x = 4
emojilbl.y = 4

main_group.append(emojilbl)
while True:
    pass