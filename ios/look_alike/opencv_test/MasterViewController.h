//
//  MasterViewController.h
//  opencv_test
//
//  Created by Matsumoto Taichi on 5/4/13.
//  Copyright (c) 2013 Matsumoto Taichi. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <opencv2/opencv.hpp>

@interface MasterViewController : UIViewController
<UINavigationControllerDelegate, UIImagePickerControllerDelegate>

@property (nonatomic, retain) IBOutlet UIImageView *imageView;
@property (nonatomic, retain) IBOutlet UILabel *label;
@property (nonatomic, retain) UIImagePickerController *picker;
@property (nonatomic, retain) UIAlertView *alert;
@property (nonatomic, retain) UIImage *faceImage;

- (IBAction)push:(id)sender;

@end
