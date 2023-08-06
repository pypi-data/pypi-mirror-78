NX Work Log

I wrote this program originally in Borland C++ Builder. It adds an icon to the windows system tray that is green when it's
measuring time and red when it's paused. I use it to measure my working hours, so I can switch it off when doing non work
related tasks.

When I found `Simon Brunning SysTrayIcon  <http://www.brunningonline.net/simon/blog/archives/SysTrayIcon.py.html>` I decided
to rewrite the application in Python as I wanted to make some improvements to the tool and no longer wanted to use my outdated
version of C++ Builder.

As I was exploring the winpy32 package I found it contains a resource file parser and I thought it would be cool to define
the dialog in Microsoft Visual Studio and see how this can be used in Python.

