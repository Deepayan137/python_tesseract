import Augmentor
def augment(pathn num_samples):
    p = Augmentor.Pipeline(path)
    p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=8)
    p.scale(probability=0.3, scale_factor=2.0)
    p.skew(probability=0.5, magnitude=0.5)
    p.sample(num_samples)


