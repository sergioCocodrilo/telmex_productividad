
class Plotter:
    def __init__(self, max_width):
        self.max_width = max_width

        self.color_palette = (
            '\x1b[7;30;40m',
            '\x1b[7;30;41m',
            '\x1b[7;30;42m',
            '\x1b[7;30;43m',
            '\x1b[7;30;44m',
            '\x1b[7;30;45m',
            '\x1b[7;30;46m',
            '\x1b[7;30;47m',
            )

    def set_values(self, xs, ys, x_title, y_title):
        if len(xs) != len(ys):
            raise ValueError('xs and ys should have the same lengths.')
        self.xs = xs
        self.ys = ys
        if len(x_title) < 11:
            self.x_title = x_title
        else:
            self.x_title = x_title[:7] + '...'
        if len(y_title) < 11:
            self.y_title = y_title
        else:
            self.y_title = y_title[:7] + '...'

    def show(self, title = ''):

        # title bar
        if len(title) > 0:
            pre_title_space = self.max_width - 5 - len(title)
            print('╭' + '─' * pre_title_space + ' ' + title + ' ─╮')
        else:
            print('╭' + '─' * (self.max_width - 2) + '╮')

        # normalization to fit in the max_width space
        max_y = max(self.ys)
        max_y_str = len(str(max_y))
        y_bar_space = self.max_width - 11 - max_y_str - 8
        xs_width = max(len(self.x_title), len(str(max(self.xs))))

        # titles
        title_str = '│ ' + f'{self.x_title:{xs_width}}' + ' ' + self.y_title
        print(f'{title_str}', ' ' * (self.max_width - len(title_str) - 2) + '│')

        # color end
        CEND = '\x1b[0m'

        color_index = 0

        for x, y in zip(self.xs, self.ys):
            y_bar = y * y_bar_space // max_y
            
            data_string = '│ {0:>{3}} [{1:{2}}]'.format(str(x), y, max_y_str, xs_width)
            bars_string = self.color_palette[color_index] + '{0}'.format('█' * y_bar) + CEND
            print(data_string, bars_string, ' ' * (self.max_width - len(data_string) - len(bars_string) + 10), '│')
            color_index = (color_index  + 1) % len(self.color_palette)
            # print(x, y, xs_width)

        print('╰' + '─' * (self.max_width - 2) + '╯')



# xs = [x for x in range(10)]
# ys = [x ** 2 for x in xs]
# p = Plotter(60)
# p.set_values(xs, ys)
# p.show()


# p = Plotter(80)
# p.set_values(xs, ys)
# p.show('Some Title')
