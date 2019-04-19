from skimage import io
import skimage.util as utils
from skimage.viewer import ImageViewer 
from skimage.measure import compare_ssim as ssim
import skimage.transform as sk_transform
import os

# import skimage.utils to use util.img_as_float for merging
# from skimage.measure import compare_ssim as ssim for ssim comparison? 

chunk_size = 25

def show_img(image):
    viewer = ImageViewer(image)
    viewer.show()

def square_img(image):
    min_dim = min(len(image), len(image[0]))
    return image[0:min_dim, 0:min_dim]

def get_puzzle_images(src):
    images = []
    for file in src:
        print("Processing puzzle image %s" % file)
        try:
            fl = square_img(io.imread(file))
            images.append(sk_transform.resize(fl,(chunk_size, chunk_size)))
        except Exception as e:
            print("Failed to get image %s, %s" % (file, e))
    return images

def get_src_files():
    files = []
    for r, d, f in os.walk("sources/"):
        for file in f:
            files.append(os.path.join(r, file))
    return files

image = io.imread("image.jpg")

min_dim = min(len(image), len(image[0]))

image = square_img(image)
image = utils.img_as_float(image)
x_iter = len(image[0])//chunk_size
y_iter = len(image)//chunk_size

src_files = get_src_files()
puzzle_imgs = get_puzzle_images(src_files)
iters = x_iter * y_iter
removed_items = 0
for i in range(y_iter):
    for j in range(x_iter):
        print("Getting %d chunk of %d" % (j + j*10 + 1, iters))
        wstart = j*chunk_size
        wend = j*chunk_size + 25
        hstart = i*chunk_size
        hend = i*chunk_size + 25
        src_chunk = image[hstart:hend,wstart:wend]
        best_img = puzzle_imgs[0]
        best_score = ssim(best_img, src_chunk, multichannel = True)
        for im in puzzle_imgs:
            try:
                score = ssim(im, src_chunk, multichannel = True)
                if score > best_score:
                    best_img = im
                    best_score = score
            except Exception as e:
                print(im)
                print("Failed to read image. %s" % e)
                removed_items += 1
                puzzle_imgs.remove(im)
                print("Removed %d item from list" % removed_items)
        image[hstart:hend, wstart:wend] = best_img

print("Result is ready. Couldn't process %d images." % removed_items)
show_img(image)
