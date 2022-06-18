from config import Config
from imio import ImageIO
from visualizer import ProcessingVisualizer

from improc import ImageProcessor

def main() -> None:
    """
    Test function for intermediate visualizations
    """
    cfg = Config.auto()
    done = False

    with ProcessingVisualizer(cfg) as vis, ImageIO(cfg) as io, ImageProcessor(cfg) as proc:
        for img in io.read_images():
            ## Do not remove these two lines!!
            vis.reset()
            vis.store(img)

            smoothed = proc.smooth(img)
            vis.store(smoothed)

            # eq = proc.equalize(smoothed)
            # vis.store(eq)

            mask = proc.extract_color_mask(smoothed)
            vis.store(mask)

            cnt = proc.extract_largest_contour(mask)
            vis.store(cnt)

            distance, radius, center = proc.inscribe_circle(cnt)
            vis.store(distance)

            no_wrist = proc.removing_wrist(distance, radius, center)
            vis.store(no_wrist)

            ## Add finger extraction here

            done = vis.show()
            if done: break




if __name__ == '__main__':
    main()