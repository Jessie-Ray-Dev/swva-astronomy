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

# The Issues

Unfortunately, I had some issues right away. The motor drivers that were sent turned out to not be the appropriate drivers and they did not use the right protocol to talk to the OnStep firmware. I ended up having to purchase replacement drivers. For future reference, be sure to get TMC2130 drivers.

Once that was straightened out, I ran into a new issue
