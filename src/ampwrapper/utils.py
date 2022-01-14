import os
from textwrap import TextWrapper
import configparser
import sys
from pathlib import Path
from blessed import Terminal
from simple_term_menu import TerminalMenu
import numpy as np
import uproot
import pandas as pd
import enlighten

def get_environment():
    config_path = Path.home() / ".amptoolstools"
    config = configparser.ConfigParser()
    if config_path.exists():
        config.read(config_path)
        env = config['DEFAULT']['Path']
        return Path(env).resolve()
    else:
        print(wrap("No active environment found! Use amptools-setup and amptools-activate to create one!"))
        sys.exit(1)
        

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

    def __call__(self, text: str, scale=1.0, alignment="center", justify="left"):
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

wrap = TextWrapper(width=os.get_terminal_size().columns - 4, tabsize=4).fill

######################## Histogram Preview

def get_binning(data, weights=None):
    dbox = DOUBLE
    box = DEFAULT
    hchars = " ▁▂▃▄▅▆▇█"
    term = Terminal()
    def refresh():
        print(term.home + term.clear)
        # draw bounding box and position cursor on the lower-left for histogram drawing
        print(" " + dbox.ul + dbox.u * (term.width - 4) + dbox.ur + " ")
        print((" " + dbox.l + term.move_right(term.width - 4) + dbox.r + " " + term.move_down()) * (term.height - 5))
        print(term.move_up() + " " + dbox.dl + dbox.d * (term.width - 4) + dbox.dr + " ")
        print(term.move_up(6) + term.move_right(4) + box.d * (term.width - 8))
        print(term.move_up(2) + term.move_right(4), end='', flush=True)
        # end drawing box
    
    def draw_hist(width, height, origin, counts):
        print(term.blue)
        bin_max = np.amax(counts)
        bin_scale = (height * 8) / bin_max
        full_bins = [int((bin_count * bin_scale) // 8) for bin_count in counts]
        partials = [int((bin_count * bin_scale) % 8) for bin_count in counts]
        x_scale = len(counts) / width
        i_bins = [int(x_loc * x_scale) for x_loc in range(width)]
        for i, i_bin in enumerate(i_bins):
            # move to bottom of bin
            print(term.move_xy(origin[1] + i, origin[0]), end='', flush=True)
            for j in range(full_bins[i_bin]):
                # print a "full" character for every 8 scaled counts
                print(term.move_xy(origin[1] + i, origin[0] - j) + hchars[8], end='', flush=True)
            # print a remainder character for whatever is left over
            print(term.move_xy(origin[1] + i, origin[0] - full_bins[i_bin]) + hchars[partials[i_bin]], end='', flush=True)
        print(term.normal)
    # Begin interface
    with term.cbreak():
        key_pressed = ''
        l_range, r_range = round(np.amin(data), 2), round(np.amax(data), 2)
        increment_index = 0
        increment_list = [0.001, 0.01, 0.1, 1]
        increment = increment_list[0]
        ### initialize histograms (one for display, one real)
        counts, binning = np.histogram(data, bins=20, range=(l_range, r_range), weights=weights)
        counts_display, _ = np.histogram(data, bins=binning, weights=weights)
        counts_unweighted, _ = np.histogram(data, bins=binning)
        ####
        n_bins = len(binning) - 1
        n_bins_display = n_bins
        while key_pressed.lower() != 'q':
            refresh()
            draw_width = term.width - 8
            draw_height = term.height - 11
            hist_origin = term.get_location()
            info_origin = (hist_origin[0] + 2, hist_origin[1])
            width_origin = (hist_origin[0] - draw_height, hist_origin[1])
            draw_hist(draw_width, draw_height, hist_origin, counts_display)
            # print number of bins
            print(term.move_xy(info_origin[1], info_origin[0]) + term.black_on_white(" Decrease/Increase Number of Bins (n/N) "), end='', flush=True)
            if n_bins == n_bins_display:
                print("   " + term.black_on_white(f" #Bins/#Displayed: {n_bins}/{n_bins_display} "), end='', flush=True)
            else:
                print("   " + term.black_on_white(f" #Bins/#Displayed: {n_bins}/") + term.red_on_white(f"{n_bins_display} "), end='', flush=True)
            print(term.black_on_white(" " * (draw_width - term.get_location()[1] + 4)), end='', flush=True)
            # print left edge
            print(term.move_xy(info_origin[1], info_origin[0] + 1) + term.black_on_white(" Decrease/Increase Left Edge (l/L)      "), end='', flush=True)
            print("   " + term.black_on_white(f" Left Edge:  {int(l_range * 1000):4} MeV "), end='', flush=True)
            print(term.black_on_white(" " * (draw_width - term.get_location()[1] + 4)), end='', flush=True)
            # print right edge
            print(term.move_xy(info_origin[1], info_origin[0] + 2) + term.black_on_white(" Decrease/Increase Right Edge (r/R)     "), end='', flush=True)
            print("   " + term.black_on_white(f" Right Edge: {int(r_range * 1000):4} MeV "), end='', flush=True)
            print(term.black_on_white(" " * (draw_width - term.get_location()[1] + 4)), end='', flush=True)
            # print increment
            print(term.move_xy(info_origin[1], info_origin[0] + 3) + term.black_on_white(" Decrease/Increase Increment (x/X)      "), end='', flush=True)
            inc_string = ""
            for ind in range(len(increment_list)):
                if increment_index == ind:
                    inc_string += term.white_on_blue(f" {int(increment_list[ind] * 1000)}")
                else:
                    inc_string += term.black_on_white(f" {int(increment_list[ind] * 1000)}")
            print("   " + term.black_on_white(f" Increment: {inc_string} MeV "), end='', flush=True)
            print(term.black_on_white(" " * (draw_width - term.get_location()[1] + 4)), end='', flush=True)
            # print bin width
            print(term.move_xy(width_origin[1], width_origin[0]) + term.black_on_white(f" Bin Width: {int(np.diff(binning)[0] * 1000)} MeV ") + "   " + term.black_on_white(f" Minimum Counts/Bin: {np.amin(counts_unweighted)} ") + "   " + term.black_on_white(" Press 'q' to confirm this selection "), end='', flush=True)
            print(term.home)
            key_pressed = term.inkey()
            if key_pressed == 'n':
                n_bins -= 1
                if n_bins < 1:
                    n_bins = 1
                n_bins_display = n_bins
            elif key_pressed == 'N':
                n_bins += 1
                n_bins_display = n_bins
            elif key_pressed == 'l':
                l_range -= increment
                if l_range < 0:
                    l_range = 0
                l_range = round(l_range, 3)
            elif key_pressed == 'L':
                l_range += increment
                if l_range >= r_range:
                    lrange -= increment
                l_range = round(l_range, 3)
            elif key_pressed == 'r':
                r_range -= increment
                if r_range <= l_range:
                    r_range += increment
                r_range = round(r_range, 3)
            elif key_pressed == 'R':
                r_range += increment
                r_range = round(r_range, 3)
            elif key_pressed == 'x':
                increment_index -= 1
                if increment_index < 0:
                    increment_index = len(increment_list) - 1
                increment = increment_list[increment_index]
            elif key_pressed == 'X':
                increment_index += 1
                if increment_index >= len(increment_list):
                    increment_index = 0
                increment = increment_list[increment_index]
            if n_bins_display > draw_width:
                n_bins_display = draw_width
            # Regenerate histograms with new binning info
            counts_display, _ = np.histogram(data, bins=n_bins_display, range=(l_range, r_range), weights=weights)
            counts, binning = np.histogram(data, bins=n_bins, range=(l_range, r_range), weights=weights)
            counts_unweighted, _ = np.histogram(data, bins=n_bins, range=(l_range, r_range))
        print(term.clear)
        return n_bins, l_range, r_range

def file_selector(root=Path.cwd(), multiselect=False, suffix=""):
    if suffix == "":
        title = "  Select File"
        files = [child for child in root.iterdir() if child.is_file()]
    else:
        title = f"  Select {suffix} File"
        files = [child for child in root.iterdir() if child.suffix == suffix and child.is_file()]
    if multiselect:
        title += "s"
    options = ["Cancel"] + [child.name for child in files]
    print(options)
    menu = TerminalMenu(
            menu_entries=options,
            title=title,
            menu_cursor="► ",
            menu_cursor_style=("fg_red", "bold"),
            menu_highlight_style=("standout",),
            multi_select=multiselect,
            show_multi_select_hint=multiselect,
            cycle_cursor=True,
            clear_screen=True,
            cursor_index=1)
    selected_indices = menu.show()
    selected_paths = [Path(files[ind - 1].resolve()) for ind in selected_indices if ind != 0]
    # returns (selection list, T/F was "Cancel" selected?)
    return selected_paths, 0 in selected_indices


def split_mass(flattree: Path, output_dir: Path, low: float, high: float, nbins: int, manager):
    with uproot.open(flattree) as tfile:
        ttree = tfile['kin']
        # using library='df' results in a double-indexed dataframe
        # which can't be properly written to a new file
        df = pd.DataFrame(ttree.arrays(library='np'))
        df.dropna(inplace=True)
    _, bin_edges = np.histogram(df['M_FinalState'], bins=nbins, range=(low, high))
    pbar = manager.counter(total=nbins, desc=flattree.stem, unit='bin', leave=False)
    for ibin in pbar(range(nbins)):
        bin_df = df.loc[df['M_FinalState'].between(bin_edges[ibin], bin_edges[ibin + 1])]
        output_path = output_dir / (flattree.stem + f"_{ibin}.root")
        if output_path.exists():
            output_path.unlink() # delete existing output (overwrite)
        # create output file
        with uproot.recreate(output_path) as tfile_out:
            tfile_out['kin'] = bin_df
    pbar.close()
