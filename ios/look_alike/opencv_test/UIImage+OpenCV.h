//
//  UIImage+OpenCV.h
//  opencv_test
//
//  Created by Matsumoto Taichi on 5/4/13.
//  Copyright (c) 2013 Matsumoto Taichi. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <opencv2/opencv.hpp>

@interface UIImage (OpenCV)

+ (IplImage*)IplImageFromUIImage:(UIImage*)image;
+ (UIImage*)UIImageFromIplImage:(IplImage*)image;
- (UIImage *)crop:(CGRect)rect;

@end
