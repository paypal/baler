//
//  BalerAppDelegate.m
//
//  Copyright (c) 2014 PayPal. All rights reserved.
//

#import "BalerAppDelegate.h"
#import "MyBalerBundle.h"
#import "MyBalerBundleUncompressed.h"

@implementation BalerAppDelegate

- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions {
  self.window = [[UIWindow alloc] initWithFrame:[[UIScreen mainScreen] bounds]];
  self.window.backgroundColor = [UIColor whiteColor];
  [self.window makeKeyAndVisible];

  MyBalerBundle *bundle = [MyBalerBundle sharedInstance];
  NSLog(@"MyBalerBundle: %@", bundle);

  MyBalerBundleUncompressed *bundleUncompressed = [MyBalerBundleUncompressed sharedInstance];
  NSLog(@"MyBalerBundleUncompressed: %@", bundleUncompressed);

  return YES;
}

@end
