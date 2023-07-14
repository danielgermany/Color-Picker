import cv2
import numpy as np
import pandas as pd
import argparse
import sys


class ColorDetector:
    def __init__(self, img_path):
        self.img_path = img_path
        self.img = cv2.imread(self.img_path)
        self.index = ["color", "color_name", "hex", "R", "G", "B"]
        self.color_data = pd.read_csv('colors.csv', names=self.index, header=None)
        self.clicked = False
        self.r = self.g = self.b = self.xpos = self.ypos = 0
        self.setup()

    def setup(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_function)

    def getColorName(self, R, G, B):
        minimum = 10000
        for i in range(len(self.color_data)):
            d = abs(R - int(self.color_data.loc[i, "R"])) + abs(G - int(self.color_data.loc[i, "G"])) + abs(
                B - int(self.color_data.loc[i, "B"]))
            if (d <= minimum):
                minimum = d
                cname = self.color_data.loc[i, "color_name"]
        return cname

    def draw_function(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.clicked = True
            self.xpos, self.ypos = x, y
            self.b, self.g, self.r = map(int, self.img[y, x])

    def run(self):
        while True:
            cv2.imshow("image", self.img)
            if (self.clicked):
                cv2.rectangle(self.img, (20, 20), (750, 60), (self.b, self.g, self.r), -1)
                text = self.getColorName(self.r, self.g, self.b) + ' R=' + str(self.r) + ' G=' + str(
                    self.g) + ' B=' + str(self.b)
                cv2.putText(self.img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                if (self.r + self.g + self.b >= 600):
                    cv2.putText(self.img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                self.clicked = False
            if cv2.waitKey(20) & 0xFF == 27:
                break
        cv2.destroyAllWindows()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--image', required=True, help="Image Path")
    args = vars(ap.parse_args())
    img_path = args['image']
    color_detector = ColorDetector(img_path)
    color_detector.run()