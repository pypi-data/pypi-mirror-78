import matplotlib.pyplot as plt


class MatPlot:
    def __init__(self):
        pass

    def draw_plot(self, x, y, linewdith, title, xlabel, ylabel):
        plt.plot(x, y, linewdith=linewdith)
        plt.title(title, fontsize=24)
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        plt.tick_params(axis='both', labelsize=14)
        plt.show()

    def draw_scatter(self, x, y):
        plt.scatter(x, y, s=40)

    def show_img(self, img_name):
        from matplotlib.image import imread
        img = imread(img_name)
        plt.imshow(img)
        plt.show()
