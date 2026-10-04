+++
date = '2026-09-04T16:26:14-04:00'
draft = true
title = 'OnStep CG5 Conversion'
+++
Jessie Ray – October 2026

# Overview

This article details my journey in converting my Celestron CG5 mount to OnStep. I am not quite done tweaking it just yet, so this article may get updated in the future or I will write additional articles and link them here. 

Included here will be:
- The purchases I made
- An explanation of the config
- Some difficulties I had

# The Reason

One may wonder why even bother doing an OnStep conversion. And honestly, I probably wouldn't have even bothered, except that the electronics in my mount went haywire. It would often freak out, not knowing where it was, and then my scope would end up crashing into my tripod at night. The tracking was also completely off due to these errors. It would also just stop communicating between ASCOM and the hand controller. (Note that these old mounts do not have USB, so the best way to interface with them is via USB on the bottom of the HC).

I had already sent the mount to Celestron, who were able to replace the components after I had fried them by plugging something in incorrectly, but unfortunately the components they sent back only worked for a little while. Between the cost to send it to them and the cost of the repairs, I decided I was better off to take matters into my own hands. 

Given this, I started doing research on OnStep. At first, I thought I might go about doing all of it manually, but at the time I didn't know enough about ESP32's, motors, motor drivers, etc. to feel that I was comfortable getting all of the parts. Given this, I got in contact with George Cushing, from whome I was able to purchase a whole kit for a very reasonable price. 

# The Setup

Fortunately, once some bugs were figured out the setup itself is quite simple. Simple enough that I feel that if I go about motorizing another mount I will probably purchase the individual parts and put it together myself. The most important thing is that you know what the gear ratio of your mount is and that you then also know what the gear reduction is that you are using between your drive and your axis control. 

For example, for a CG5 mount or its siblings, that is 144:1 for both axis. If your mount has a different ratio per axis, you will need to look that up and do the math accordingly. The pullys supplied to me from George were 48 and 16 tooth, giving a 3:1 ratio. You also need to know how many steps are in one full rotation of your motors. The ones supplied with my kit were 400 step NEMA 17s. You also need to know how many microsteps there are per step (modern stepper motors are capable of making smaller steps in between their full physical steps) my motors do 32 microsteps perstep. All of this comes together to create the magic number. That being how many microsteps are there per one full rotation of your mount. The formula for that is below

motor steps * micro steps per full step * pully gear reduction * worm gear reduction

So for my mount that is 400 * 32 * 3 * 144 which gives us 5,529,600 steps per full rotation. You then divide that by 360 to get 15,360 microsteps per degree. Remember that, because we need that number to put into our OnStep config later. Also, if you're interested in your resolution you can use this here. Divide your number by 3600 to get steps per arc second. In my case that is about 4.26 microsteps per arc second. Which means that a single microstep is about 0.23 arc seconds, which is well below the resoltuion of all but the largest scopes. Meaning that any tracking errors are not likely to come from not having enough tracking resolution and much more likely to come from manufacturing errors in the system, polar alignment, or wind.

## The Config

Once all of the hardware was accounted for it, was time to configure everything. As I state later, this is where I had some trouble. My troubles came from the Wifi module, but as long as you don't have one of those, then all you have to do is get all of the settings you want into config.h. Theoretically if you order from George, it should come pre-shipped with a working config, however as stated I had some issues so I ended up working through this from the beginning.

Anyway, step one is to get the Arduino IDE installed, then get the associated plugins for OnStep installed. There are many guides on that, so I will not go into that here. From there, all that needs doing is to change the approprite settings, mainly the ones pertaining to you hemisphere and the microstepping numbers we figured out earlier as well as what direction your motors turn and the settings that control the safety stop point that keeps the telescope from crashing into the mount. Once all of the settings are as they should be, simply connect the board to your computer, select it in the menu, and compile/flash. Again, there are many tutorials for this online.

## The Hardware Install

After the config is done, the pulleys need to be installed on the mount and the belts put in place. Of course, my mount came as a go-to, but I had already taken all of the electronics and motors off because of the issues I was having and had been using it as a manual mount for a little while so by the time I got to the installation the mount was ready anyway. This is the tricky part honestly. In the package I purchased, George supplied two L shaped brackets designed specifically for this purpose. They do work well, but getting them mounted in place properly turned out to be a bit of a pain. I may revisit this later and attempt to 3d print an easier solution and then possibly order it from one of the various metal working websites out there. If I do, I will write a new article about that. 

The brackets must be mounted just right in order to get the appropriate tension for the belt teeth to engage prowith the pulley, which with the brackets supplied by George is possible, but only by turning the whole bracket and then tightening it down. This can lead to some slight misalignment of the belts on the pulley, but as long as it isn't severe enough to cause the belts to slip off it should not matter. 

# The Issues

As alluded to earlier, I had some issues pretty much immediately. And much to my embarassment it took me much longer to figure out what the problem was than it should have. 

## The First Issue: The Config

Unfortunately the first issue I ran into was pretty major. That was that the settings I was inputting into config.h simply were not doing what they should have. Eventually I figured out that the problem was the WiFi module. It turns out that if you have a WiFi module installed, it has its own settings cache that get loaded AFTER the main config.h. What that means is that any settings input in the web GUI will override whatever you put in config.h. That means you have two options. The first is to simply use the web GUI to configure the mount, and the second is to disable the WiFi module entirely and work through config.h. In my case, I elected to do get it working via the WiFi module, but I think in the near future I am going to remove that because it simply is not as smooth as I would prefer and the devices I use to connect to everything are very pickey about connecting to WiFi networks that do not have internet. Especially my Windows laptop for some reason. 

## The Second Issue: The Motor Cables

All good things must come to an end, and something that came to an end VERY quickly was the motor cables that were provided by George. These were standard 6 pin JST connectors used to connect to the NEMA17 motors that George had crimped into RJ45 ends. That solution worked for a while, but I quickly found out that these cables are not made in a way that makes them good for moving applications. One of the cables broke off right where the cable connects to the JST connector during an imaging session. 

My soltuion to this was to buy some new JST connectors, sus out the pin out that George had used, and then crimp those down into RJ45 keystone jacks and 3d print a bracket to mount that onto the mount. That way the JST connectors stay stationary and I use standard cat5e ethernet cables to connect the motors to the controller. So far, that has worked quite well, though I need to adjust the design for the keystone mount bracket because they don't stay in very well. 
