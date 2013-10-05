import cv2, asmlib, argparse, sys
import cv2, argparse, sys

# import argparse

def loadModel(model_file):
  model = asmlib.ASMModel()
  model.loadFromFile(model_file)
  return model

def fitAndShow(classifier, model, img, mode, verbose):
  if mode == 'all':
    flags = cv2.CASCADE_SCALE_IMAGE
  else:
    flags = cv2.CASCADE_FIND_BIGGEST_OBJECT|cv2.CASCADE_SCALE_IMAGE

  faces  = classifier.detectMultiScale(img, scaleFactor=1.2, minNeighbors=2, minSize=(60, 60), flags=flags)
  # the rects come back as numpy.int32, this cant be handled by the pyopencv_from functions
  faces = map(lambda t: tuple(map(int, t)), faces)
  result = model.fitAll(img, faces, verbose)
  model.showResult(img, result)

def buildModel(model_file, def_file, list_file):
  model = asmlib.ASMModel()
  model.buildModel(def_file, list_file)
  model.saveToFile(model_file)

def viewModel(model):
  model.viewShapeModel()
  cv2.waitKey()

def fitModelToWebcam(classifier, model, verbose):
  capture = cv2.VideoCapture()
  capture.open(0)
  if not capture.isOpened():
    print "could not open webcam"
    sys.exit(1)

  while cv2.waitKey(5) == -1:
    retval, img = capture.read()
    img2 = cv2.flip(img, 1)
    fitAndShow(classifier, model, img2, 'biggest', verbose)

def fitModelToImage(classifier, model, image_file, verbose):
  img = cv2.imread(image_file)
  if img.empty():
    print "could not load image"
    sys.exit(1)

  fitAndShow(classifier, model, img, 'all', verbose)
  cv2.waitKey()


if __name__ == "__main__":
  parser = argparse.ArgumentParser(epilog="For details and examples, please check: http://code.google.com/p/asmlib-opencv/wiki/RunningDemo")

  # Tasks
  parser.add_argument('-b', dest='build', action='store_true', help='Build a model')
  parser.add_argument('-v', dest='view',  action='store_true', help='View a model')
  parser.add_argument('-f', dest='fit',   action='store_true', help='Fit images to a model')

  # General options
  parser.add_argument('-m', dest='model_file', required=True,       help="Path to the model file")
  parser.add_argument('-V', dest='verbose',    type=int, default=0, help="Verbosity level")

  # Build specific options
  parser.add_argument('-d', dest='def_file',  help="Model definition file, see wiki")
  parser.add_argument('-l', dest='list_file', help="List of labelled points, see wiki")

  # Fitting specific options
  parser.add_argument('-C',  dest='detector_file',               help="Face/Object detector XML (OpenCV)")
  parser.add_argument('-p',  dest='image_file',                  help="Path to an image")
  parser.add_argument('-pc', dest='webcam', action='store_true', help="Run on your webcam")

  args = parser.parse_args()

  if args.build:
    if not args.def_file:
      print "you must specify the -d (def_file) option"
      sys.exit(1)
    if not args.list_file:
      print "you must specify the -d (def_file) option"
      sys.exit(1)

    buildModel(args.model_file, args.def_file, args.list_file)
  elif args.view:
    viewModel(load_model(args.model_file))
  elif args.fit:
    if not args.image_file and not args.webcam:
      print "you must specify either the -p (image_file) option or the -pc (webcam) option"
      sys.exit(1)

    classifier = cv2.CascadeClassifier()
    if not classifier.load(args.detector_file):
      print "loading the cascade classifier failed"
      sys.exit(1)

    if args.webcam:
      fitModelToWebcam(classifier, loadModel(args.model_file), args.verbose)
    else:
      fitModelToImage(classifier, loadModel(args.model_file), args.image_file, args.verbose)
  else:
    print 'you must specify either the -b (build), -v (view) or -f (fit) parameter'
