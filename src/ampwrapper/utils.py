import os
from textwrap import TextWrapper


class Box:
    width = os.get_terminal_size().columns

    def __init__(self, box: str):
        box = box.replace("\n", "")
        self.ul = box[0]
        self.u = box[1]
        self.ud = box[2]
        self.ur = box[3]
        self.l = box[4]
        self.fill = box[5]
        self.r = box[6]
        self.lr = box[8]
        self.m = box[9]
        self.x = box[10]
        self.rl = box[11]
        self.dl = box[12]
        self.d = box[13]
        self.du = box[14]
        self.dr = box[15]

    def box(self, text: str, scale=1.0, alignment="center", justify="left"):
        assert scale <= 1.0
        width = int(Box.width * scale)
        wrapper = TextWrapper(width=width - 4, tabsize=4)
        wrapped_text = wrapper.fill(text)
        if justify == "center":
            wrapped_text = "\n".join(
                [
                    wrapped_line.center(width - 4, " ").rstrip()
                    for wrapped_line in wrapped_text.split("\n")
                ]
            )
        elif justify == "right":
            wrapped_text = "\n".join(
                [
                    wrapped_line.rjust(width - 4, " ")
                    for wrapped_line in wrapped_text.split("\n")
                ]
            )
        elif justify == "left":
            pass
        else:
            print(f'Unknown justification option: "{justify}"')
        if alignment == "center":
            spacer = int((Box.width - width) / 2)
        elif alignment == "left":
            spacer = 0
        elif alignment == "right":
            spacer = int((Box.width - width))
        else:
            print(f'Unknown alignment option: "{alignment}"')
            spacer = 0
        box_top = " " * spacer + self.ul + self.u * (width - 2) + self.ur
        box_content = [
            " " * spacer
            + self.l
            + " "
            + wrapped_line
            + " " * (width - 3 - len(wrapped_line))
            + self.r
            for wrapped_line in wrapped_text.split("\n")
        ]
        box_bottom = " " * spacer + self.dl + self.d * (width - 2) + self.dr
        return "\n".join([box_top, *box_content, box_bottom])

    def titlebox(
        self,
        title: str,
        text: str,
        scale=1.0,
        title_scale=0.7,
        alignment="center",
        justify="left",
        title_alignment="center",
        title_justify="center",
    ):
        assert scale <= 1.0
        assert title_scale <= 1.0
        width = int(Box.width * scale)
        title_width = int(width * title_scale)
        wrapper = TextWrapper(width=width - 4, tabsize=4)
        title_wrapper = TextWrapper(width=title_width - 4, tabsize=4)
        wrapped_text = wrapper.fill(text)
        wrapped_title = title_wrapper.fill(title)
        if alignment == "center":
            spacer = int((Box.width - width) / 2)
        elif alignment == "left":
            spacer = 0
        elif alignment == "right":
            spacer = int((Box.width - width))
        else:
            print(f'Unknown alignment option: "{alignment}"')
            spacer = 0
        if justify == "center":
            wrapped_text = "\n".join(
                [
                    wrapped_line.center(width - 4, " ").rstrip()
                    for wrapped_line in wrapped_text.split("\n")
                ]
            )
        elif justify == "right":
            wrapped_text = "\n".join(
                [
                    wrapped_line.rjust(width - 4, " ")
                    for wrapped_line in wrapped_text.split("\n")
                ]
            )
        elif justify == "left":
            pass
        else:
            print(f'Unknown justification option: "{justify}"')
        if title_alignment == "center":
            extra = (width - title_width) % 2
            title_spacer_l = int((width - title_width) / 2)
            title_spacer_r = int((width - title_width) / 2) + extra
            title_l = self.du
            title_r = self.du
        elif title_alignment == "left":
            title_spacer_l = 0
            title_spacer_r = int(width - title_width)
            title_l = self.lr
            title_r = self.du
        elif title_alignment == "right":
            title_spacer_l = int((width - title_width))
            title_spacer_r = 0
            title_l = self.du
            title_r = self.rl
        else:
            print(f'Unknown alignment option: "{title_alignment}"')
            title_spacer_l = 0
            title_spacer_r = int(width - title_width)
            title_l = self.lr
            title_r = self.du
        if title_justify == "center":
            wrapped_title = "\n".join(
                [
                    wrapped_line.center(title_width - 4, " ").rstrip()
                    for wrapped_line in wrapped_title.split("\n")
                ]
            )
        elif title_justify == "right":
            wrapped_title = "\n".join(
                [
                    wrapped_line.rjust(title_width - 4, " ")
                    for wrapped_line in wrapped_title.split("\n")
                ]
            )
        elif title_justify == "left":
            pass
        else:
            print(f'Unknown justification option: "{title_justify}"')
        title_top = (
            " " * (spacer + title_spacer_l)
            + self.ul
            + self.u * (title_width - 2)
            + self.ur
        )
        title_content = [
            " " * (spacer + title_spacer_l)
            + self.l
            + " "
            + wrapped_line
            + " " * (title_width - 3 - len(wrapped_line))
            + self.r
            for wrapped_line in wrapped_title.split("\n")
        ]
        if title_scale != 1.0:
            middle = (
                " " * spacer
                + self.ul * (title_alignment != "left")
                + self.u * (title_spacer_l - 1)
                + title_l
                + self.m * (title_width - 2)
                + title_r
                + self.u * (title_spacer_r - 1) * (title_alignment != "right")
                + self.ur * (title_alignment != "right")
            )
        else:
            middle = " " * spacer + self.lr + self.m * (title_width - 2) + self.rl
        box_content = [
            " " * spacer
            + self.l
            + " "
            + wrapped_line
            + " " * (width - 3 - len(wrapped_line))
            + self.r
            for wrapped_line in wrapped_text.split("\n")
        ]
        box_bottom = " " * spacer + self.dl + self.d * (width - 2) + self.dr
        return "\n".join([title_top, *title_content, middle, *box_content, box_bottom])

    def subtitlebox(
        self,
        title: str,
        text: str,
        scale=1.0,
        title_scale=0.7,
        alignment="center",
        justify="left",
        title_alignment="center",
        title_justify="center",
    ):
        assert scale <= 1.0
        assert title_scale <= 1.0
        width = int(Box.width * scale)
        title_width = int(width * title_scale)
        wrapper = TextWrapper(width=width - 4, tabsize=4)
        title_wrapper = TextWrapper(width=title_width - 4, tabsize=4)
        wrapped_text = wrapper.fill(text)
        wrapped_title = title_wrapper.fill(title)
        if alignment == "center":
            spacer = int((Box.width - width) / 2)
        elif alignment == "left":
            spacer = 0
        elif alignment == "right":
            spacer = int((Box.width - width))
        else:
            print(f'Unknown alignment option: "{alignment}"')
            spacer = 0
        if justify == "center":
            wrapped_text = "\n".join(
                [
                    wrapped_line.center(width - 4, " ").rstrip()
                    for wrapped_line in wrapped_text.split("\n")
                ]
            )
        elif justify == "right":
            wrapped_text = "\n".join(
                [
                    wrapped_line.rjust(width - 4, " ")
                    for wrapped_line in wrapped_text.split("\n")
                ]
            )
        elif justify == "left":
            pass
        else:
            print(f'Unknown justification option: "{justify}"')
        if title_alignment == "center":
            extra = (width - title_width) % 2
            title_spacer_l = int((width - title_width) / 2)
            title_spacer_r = int((width - title_width) / 2) + extra
            title_l = self.ud
            title_r = self.ud
        elif title_alignment == "left":
            title_spacer_l = 0
            title_spacer_r = int(width - title_width)
            title_l = self.lr
            title_r = self.ud
        elif title_alignment == "right":
            title_spacer_l = int((width - title_width))
            title_spacer_r = 0
            title_l = self.ud
            title_r = self.rl
        else:
            print(f'Unknown alignment option: "{title_alignment}"')
            title_spacer_l = 0
            title_spacer_r = int(width - title_width)
            title_l = self.lr
            title_r = self.ud
        if title_justify == "center":
            wrapped_title = "\n".join(
                [
                    wrapped_line.center(title_width - 4, " ").rstrip()
                    for wrapped_line in wrapped_title.split("\n")
                ]
            )
        elif title_justify == "right":
            wrapped_title = "\n".join(
                [
                    wrapped_line.rjust(title_width - 4, " ")
                    for wrapped_line in wrapped_title.split("\n")
                ]
            )
        elif title_justify == "left":
            pass
        else:
            print(f'Unknown justification option: "{title_justify}"')
        box_top = " " * spacer + self.ul + self.u * (width - 2) + self.ur
        box_content = [
            " " * spacer
            + self.l
            + " "
            + wrapped_line
            + " " * (width - 3 - len(wrapped_line))
            + self.r
            for wrapped_line in wrapped_text.split("\n")
        ]
        if title_scale != 1.0:
            middle = (
                " " * spacer
                + self.dl * (title_alignment != "left")
                + self.d * (title_spacer_l - 1)
                + title_l
                + self.m * (title_width - 2)
                + title_r
                + self.d * (title_spacer_r - 1) * (title_alignment != "right")
                + self.dr * (title_alignment != "right")
            )
        else:
            middle = " " * spacer + self.lr + self.m * (title_width - 2) + self.rl
        title_content = [
            " " * (spacer + title_spacer_l)
            + self.l
            + " "
            + wrapped_line
            + " " * (title_width - 3 - len(wrapped_line))
            + self.r
            for wrapped_line in wrapped_title.split("\n")
        ]

        title_bottom = (
            " " * (spacer + title_spacer_l)
            + self.dl
            + self.d * (title_width - 2)
            + self.dr
        )
        return "\n".join([box_top, *box_content, middle, *title_content, title_bottom])


DEFAULT = Box(
    """
┌─┬┐
│░││
├─┼┤
└─┴┘
"""
)
BOLD = Box(
    """
┏━┳┓
┃▓┃┃
┣━╋┫
┗━┻┛
"""
)
DOUBLE = Box(
    """
╔═╦╗
║▒║║
╠═╬╣
╚═╩╝
"""
)
HBOLD = Box(
    """
┍━┯┑
│█││
┝━┿┥
┕━┷┙
"""
)
VBOLD = Box(
    """
┎─┰┒
┃█┃┃
┠─╂┨
┖─┸┚
"""
)
HDOUBLE = Box(
    """
╒═╤╕
│█││
╞═╪╡
╘═╧╛
"""
)
VDOUBLE = Box(
    """
╓─╥╖
║█║║
╟─╫╢
╙─╨╜
"""
)
CURVED = Box(
    """
╭─┬╮
│╳││
├─┼┤
╰─┴╯
"""
)

for scale in range(30, 100, 2):
    for title_scale in range(2, 11):
        print(title_scale)
        print("----------")
        print(
            BOLD.subtitlebox(
                "This is the Title of the Box",
                "This is a test of the title box system, here is a really long line that will probably need to be wrapped. It is just one line not separated by newline characters, so the program wraps it according to a set width",
                scale=scale / 100,
                title_alignment="left",
                title_scale=title_scale / 10,
            )
        )
        print(
            BOLD.subtitlebox(
                "This is the Title of the Box",
                "This is a test of the title box system, here is a really long line that will probably need to be wrapped. It is just one line not separated by newline characters, so the program wraps it according to a set width",
                scale=scale / 100,
                title_alignment="center",
                title_scale=title_scale / 10,
            )
        )
        print(
            BOLD.subtitlebox(
                "This is the Title of the Box",
                "This is a test of the title box system, here is a really long line that will probably need to be wrapped. It is just one line not separated by newline characters, so the program wraps it according to a set width",
                scale=scale / 100,
                title_alignment="right",
                title_scale=title_scale / 10,
            )
        )
