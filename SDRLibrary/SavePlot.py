import matplotlib.pyplot as plt
import logging

def givePlot(x, y, title: str, xlabel: str, ylabel: str):
    logger = logging.getLogger("givePlot")
    logger.info("Drawing plot")
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, color='blue', marker='o')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

    plt.show()


def savePlot(x, y, title: str, xlabel: str, ylabel: str, path: str):
    logger = logging.getLogger("savePlot")
    logger.info("Drawing plot")
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, color='blue', marker='o')

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()

    plt.savefig(path)

def saveData(x, path:str):
    n = len(x)
    with open(path, "a") as f:
        for i in range(n):
            f.write(str(x[i])+"\n")

    logger = logging.getLogger("saveData")
    logger.info("Save {} data.", n)
