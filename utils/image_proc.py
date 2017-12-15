import Augmentor
def augment(path, num_samples):
    p = Augmentor.Pipeline(path)
    p.random_distortion(probability=0.5, grid_width=4, grid_height=4, magnitude=8)
    p.scale(probability=0.3, scale_factor=2.0)
    p.random_erasing(probability=0.3, rectangle_area=0.4)
    p.sample(num_samples)


