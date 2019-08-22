import os
import sys
import tarfile
import numpy as np
import matplotlib.image as mpimg
from pathlib import Path
from six.moves import urllib

class FlowerModel:
    def __init__(self, path=None):
        ''' path is local directory to save flower samples. '''
        if path is None:
            tf_sample_repository = 'http://download.tensorflow.org/example_images'
            self.dataset_url = os.path.join(tf_sample_repository, 'flower_photos.tgz')
            self.resource_dir = os.path.join(Path.home(), 'workspace/machine-learning/resource')
            path = os.path.join(self.resource_dir, 'flower_photos')
        self.path = path
        self.labels = None
        self.class_to_image_paths = None
        self.class_to_images = None
    
    def get_class_labels(self):
        if self.labels is not None:
            return self.labels

        labels = []
        for flower_class in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, flower_class)):
                labels.append(flower_class)
        self.labels = sorted(labels)
        return self.labels
    
    def _extract_jpg_image_paths(self, image_dir_path):
        file_paths = []
        for fname in os.listdir(image_dir_path):
            if fname.endswith('.jpg'):
                file_paths.append(os.path.join(image_dir_path, fname))
        if len(file_paths) > 0:
            return file_paths
        else:
            return None
    
    def get_class_to_image_paths(self):
        if self.class_to_image_paths is not None:
            return self.class_to_image_paths

        self.class_to_image_paths = {}
        for flower_class in self.labels:
            dir_path = os.path.join(self.path, flower_class)
            image_paths = self._extract_jpg_image_paths(dir_path)
            if image_paths is not None:
                self.class_to_image_paths[flower_class] = np.asarray(image_paths)
        return self.class_to_image_paths  

    def download(self):
        if os.path.exist(self.path):
            return

        os.makedirs(self.path, exist_ok=True)
        # Download flower dataset from tensorflow sample dataset repository.
        tgz_path = os.path.join(self.resource_dir, 'flower_photos.tgz')
        urllib.request.urlretrieve(self.dataset_url, tgz_path)
        # Extract a tar file.
        with tarfile.open(tgz_path) as flowers_tgz:
            flowers_tgz.extractall(path=self.resource_dir)
        os.remove(tgz_path)
    
    def fetch(self):
        if os.path.exists(self.path) is False:
            download()
        
        self.labels = self.get_class_labels()
        self.class_to_image_paths = self.get_class_to_image_paths()
    
    def load_images(self):
        if self.class_to_images is not None:
            return self.class_to_images

        self.class_to_images = {}
        for flower_class, image_paths in self.class_to_image_paths.items():
            self.class_to_images[flower_class] = np.array([mpimg.imread(fname) for fname in image_paths])
        return self.class_to_images  
    
    def get_random_samples(self, flower_class, n_samples):
        n_images = len(self.class_to_image_paths[flower_class])
        rand_idx = np.random.choice(n_images-1, n_samples)
        return np.array([mpimg.imread(fname) for fname in self.class_to_image_paths[flower_class][rand_idx]])