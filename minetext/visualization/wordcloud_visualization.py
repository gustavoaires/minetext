from wordcloud import WordCloud
import matplotlib.pyplot as plt


def generate_word_cloud(corpus, save_dir):
    wc = WordCloud().generate(corpus)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(save_dir)


if __name__ == "__main__":
    pass