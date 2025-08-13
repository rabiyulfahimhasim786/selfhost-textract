# import layoutparser as lp

# # Example using a Detectron2 model from layoutparser model zoo
# MODEL = lp.Detectron2LayoutModel('lp://HJDataset/faster_rcnn_R_50_FPN_3x/config')

# def detect_layout(cv2_image):
#     lp_image = lp.Image(cv2_image)
#     layout = MODEL.detect(lp_image)
#     # returns list of layout blocks with type, bbox coords
#     return layout

import layoutparser as lp

# This uses Paddle's PubLayNet model (general document layout detection)
MODEL = lp.PaddleDetectionLayoutModel(
    model_path='lp://PubLayNet/paddledetection',  # Paddle version of PubLayNet
    enforce_cpu=True
)

def detect_layout(cv2_image):
    lp_image = lp.Image(cv2_image)
    layout = MODEL.detect(lp_image)
    return layout
