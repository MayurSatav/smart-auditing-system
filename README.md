# SmartAuditing [ Major Project ]

## Project Title
Develop UI for data extraction from invoices pdf using computer vision

## Abstract
In businesses we receives many pdf documents of bills and invoices, which we later proceed manually so consumes time and non productive activity.Management of invoices and maintaining their records for further processing sometimes it is hectic and buying specially developed software is not worth for small enterprises. The majority of the businesses has similar requirements and most of them use the traditional management system like recording data manually and maintaining hard copies, a result, it consumes a lot of time as well as space.  In this project we have developed  UI where user can upload invoice file (pdf or jpg) then using image processing it will automatically extract text and segregate it into different parts like Vendor name, Invoice number, item name and item quantity. it is a django web-based application specially built for small businesses like retailers and wholesalers. It is a standard business application made according to the standard requirements of businesses. Our system tries to find out a better Management solution for auditing.We have initially focus on pdf/image invoices.

![ProjectFlow](https://github.com/MayurSatav/smart-auditing-system/blob/master/other/basicflow.png)

Our system follows three main modules first one is pre-processing with the help of different OpenCV’s techniques like dilation and otsu binarization algorithms, then the next step is data extraction with the help of OCR based Tesseract technology and post-processing with the help of RegEx technology for better accuracy. The prime objective is to make data available for the user so that the user can access it anytime from anywhere and can modify it if need. Considering availability and accessibility, this web-based application will help to achieve objectives.

## Otsu's Binarization

In global thresholding, we used an arbitrary chosen value as a threshold. In contrast, Otsu's method avoids having to choose a value and determines it automatically.
Consider an image with only two distinct image values (bimodal image), where the histogram would only consist of two peaks. A good threshold would be in the middle of those two values. Similarly, Otsu's method determines an optimal global threshold value from the image histogram.

## Architecture

## Technology Stack








## Developers

* Mayur Satav - [ Maintainer And Contributor ]
    * B.Tech (Information Technology)
    * mayursatav9@gmail.com

* Tanmay Varade - [ Contributor ]
    * B.Tech (Information Technology)
    * tpvarade@mitaoe.ac.in


## Keywords
Python, OpenCV, Tesseract, OTSU's Binerisation (for UI web based solution so HTML, CSS and javascript)






