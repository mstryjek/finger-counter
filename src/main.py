from config import Config
from imio import ImageIO
from visualizer import ProcessingVisualizer


def test() -> None:
    """
    Test function for intermediate visualizations
    """
    cfg = Config.auto()
    ## Add logic class creation here
    done = False

    with ProcessingVisualizer(cfg) as vis, ImageIO(cfg) as io:
        for img in io.read_images():
            ## Do not remove these two lines!!
            vis.reset()
            vis.store(img)

            ## Add image processing steps here

            done = vis.show()
            if done: break




if __name__ == '__main__':
    test()