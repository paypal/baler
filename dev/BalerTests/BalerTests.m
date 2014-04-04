//
//  BalerTests.m
//
//  Copyright (c) 2014 PayPal. All rights reserved.
//

#import "BalerTests.h"
#import "MyBalerBundle.h"
#import "MyBalerBundleUncompressed.h"

@implementation BalerTests

- (void)testCompressed {
  NSError *testError = nil;
  MyBalerBundle *bundle = [MyBalerBundle sharedInstance];
  STAssertNotNil(bundle, @"MyBalerBundle's sharedInstance should instantiate");
  BOOL pass = [bundle passesSelfTest:&testError];
  STAssertTrue(pass, @"MyBalerBundle failed self-test with error %@", testError);
  MyBalerBundle *bundle2 = [MyBalerBundle sharedInstance];
  STAssertEqualObjects(bundle, bundle2, @"MyBalerBundle should be a true singleton");
}

- (void)testUncompressed {
  NSError *testError = nil;
  MyBalerBundleUncompressed *bundle = [MyBalerBundleUncompressed sharedInstance];
  STAssertNotNil(bundle, @"MyBalerBundleUncompressed's sharedInstance should instantiate");
  BOOL pass = [bundle passesSelfTest:&testError];
  STAssertTrue(pass, @"MyBalerBundleUncompressed failed self-test with error %@", testError);
  MyBalerBundleUncompressed *bundle2 = [MyBalerBundleUncompressed sharedInstance];
  STAssertEqualObjects(bundle, bundle2, @"MyBalerBundle should be a true singleton");
}

@end
