//
//  MasterViewController.m
//  opencv_test
//
//  Created by Matsumoto Taichi on 5/4/13.
//  Copyright (c) 2013 Matsumoto Taichi. All rights reserved.
//

#import "MasterViewController.h"
#import "UIImage+OpenCV.h"
#import "AFNetworking/AFNetworking.h"

@interface MasterViewController ()

- (void)load:(UIImage *)faceImage;
- (NSDictionary *)detectFace:(UIImage *)image;

@end

@implementation MasterViewController

- (void)dealloc {
	self.picker = nil;
	self.imageView = nil;
	self.alert = nil;
	self.faceImage = nil;
	self.label = nil;
	[super dealloc];
}

- (void)awakeFromNib {
	[super awakeFromNib];
	self.title = @"Celebrity Look Alike";
}

- (IBAction)push:(id)sender {
	self.label.text = @"";
	self.picker = [[[UIImagePickerController alloc] init] autorelease];
	self.picker.delegate = self;
	[self.picker setSourceType:UIImagePickerControllerSourceTypePhotoLibrary];
	[self presentViewController:self.picker animated:YES completion:nil];	
}

- (NSDictionary *)detectFace:(UIImage *)image {
	NSString* resDir = [[NSBundle mainBundle] resourcePath];
    char cascade_path[1024];
    sprintf(cascade_path, "%s/%s", [resDir cStringUsingEncoding:NSASCIIStringEncoding],
			"haarcascade_frontalface_default.xml");
    CvHaarClassifierCascade *cascade = (CvHaarClassifierCascade *)cvLoad(cascade_path, 0, 0, 0);
	
    IplImage *inImg = [UIImage IplImageFromUIImage:image];
    CvMemStorage *storage = cvCreateMemStorage(0);
    if (!inImg || !storage || !cascade) {
        NSLog(@"Initilization error : %@" , (!inImg)? @"cant load image" : (!cascade)? 
            @"cant load haar cascade" : 
            @"unable to locate memory storage");
        return nil;
    }
 
    CvSeq *faceRectSeq = cvHaarDetectObjects(inImg, cascade, storage,
											 1.2,
											 3,
											 CV_HAAR_DO_CANNY_PRUNING,
											 cvSize(25,25));

	NSInteger faceCnt = (faceRectSeq ? faceRectSeq->total : 0);
	CGRect faceRect = {};
	if (faceCnt > 0) {
        CvRect *r = (CvRect*)cvGetSeqElem(faceRectSeq, 0);
        CvPoint p1 = { r->x, r->y };
        CvPoint p2 = { r->x + r->width, r->y + r->height };
         
        cvRectangle(inImg, p1, p2,
					CV_RGB(0, 255, 0),
					1, 4, 0);
		faceRect.origin.x = r->x + 1;
		faceRect.origin.y = r->y + 1;
		faceRect.size.width = r->width - 2;
		faceRect.size.height = r->height - 2;
	}
	
	UIImage *orig = [UIImage UIImageFromIplImage:inImg];
	UIImage *face = nil;
	if (faceCnt > 0) {
		face = [orig crop:faceRect];
	}
	
	NSDictionary *result = @{@"orig":orig, @"face":face};

    cvReleaseImage(&inImg);
    if(cascade) cvReleaseHaarClassifierCascade(&cascade);
    if(storage)  cvReleaseMemStorage(&storage);

	return result;
}


- (void)load:(UIImage *)faceImage {
	NSURL *url = [NSURL URLWithString:@"http://localhost:8000"];
	AFHTTPClient *client = [AFHTTPClient clientWithBaseURL:url];
	
	NSMutableURLRequest *request =
		[client multipartFormRequestWithMethod:@"POST"
											  path:@"/"
										parameters:nil
						 constructingBodyWithBlock: ^(id <AFMultipartFormData>formData) {
				[formData appendPartWithFileData:UIImagePNGRepresentation(faceImage)
										name:@"face"
									fileName:@"face.png"
									mimeType:@"image/png"];
		}];
	
	AFJSONRequestOperation *operation =
		[AFJSONRequestOperation
			JSONRequestOperationWithRequest:request
			success:^(NSURLRequest *request, NSHTTPURLResponse *response, id JSON) {
				__block NSString *name = [JSON[@"name"] retain];
				NSString *imageURL = [NSString stringWithFormat:@"http://localhost:8000%@", JSON[@"url"]];
				NSURLRequest *imageRequest = [NSURLRequest requestWithURL:[NSURL URLWithString:imageURL]];
				[self.imageView setImageWithURLRequest:imageRequest
								 placeholderImage:nil
										  success:^(NSURLRequest *request , NSHTTPURLResponse *response , UIImage *image) {
						self.imageView.image = image;
						self.label.text = [NSString stringWithFormat:@"You looks like: %@", name];
						[name release];
					}
				  failure:nil];
				
			}
		    failure:^( NSURLRequest *request, NSHTTPURLResponse *response, NSError *error, id JSON) {
				NSLog(@"failed %@", JSON);
			}];

	[operation start];
}

#pragma mark -
#pragma mark UIImagePickerControllerDelegate

- (void)imagePickerController:(UIImagePickerController *)picker
didFinishPickingMediaWithInfo:(NSDictionary *)info {

	[[self.picker presentingViewController]
        dismissViewControllerAnimated:YES completion:nil];
	
	UIImage *orig = [info objectForKey:UIImagePickerControllerOriginalImage];
	NSDictionary *result = [self detectFace:orig];
	self.imageView.image = result[@"orig"];
	
	if (result[@"face"]) {
		self.faceImage = result[@"face"];
		self.alert = [[[UIAlertView alloc] initWithTitle:@"Send this face?"
												 message:nil
												delegate:self
									   cancelButtonTitle:@"Cancel"
									   otherButtonTitles:@"OK", nil] autorelease];
		[self.alert show];
	}
	else {
		NSLog(@"no face detected");
	}	
}

- (void)imagePickerControllerDidCancel:(UIImagePickerController *)picker {
	[[self.picker presentingViewController]
        dismissViewControllerAnimated:YES completion:nil];
}


#pragma mark -
#pragma mark UIAlertViewDelegate
- (void)alertView:(UIAlertView *)alertView clickedButtonAtIndex:(NSInteger)buttonIndex {
	NSLog(@"%d", buttonIndex);
	if (buttonIndex != alertView.cancelButtonIndex) {
		[self load:self.faceImage];
	}
}


@end
