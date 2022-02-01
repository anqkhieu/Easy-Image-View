# Easy Image View 🖼️

Conveniently generate colorblind-friendly images with automatic alt-text in Slack!

![Easy Image View - Title / Cover](https://cdn.discordapp.com/attachments/931114609434308609/938018111683178496/1.png)

___

## Preqrequisites ✔️
1. A Slack Workspace 
2. An Azure Computer Vision Instance
3. Python 3


## Set Up 🔢
1. Create a Slack app with the following scopes. Basically, you're letting the app have the ability to read/write files, read channels and reactions, and send messages as the app. 

    - Bot Token Scopes: `files:write, files:write:user, channels:history, chat:write, chat:write.public, im:history, im:read, mpim:history, and mpim:read, and reactions:read`

    - User Token Scopes: `links:write, files:read, files:write, im:history, im:read`

2. Create an [Azure Computer Vision](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/) instance. You can use the free tier! 

3. To download all the Python library dependencies, use `pip install -r requirements.txt` in your terminal. 

4. In a `.env` file, set up your environment variables-- you'll be using your Slack Oauth tokens and Azure key here. 

    ```
    SLACK_BOT_TOKEN=xoxb-token-#
    SLACK_APP_TOKEN=xapp-token-#
    SLACK_USER_TOKEN=xoxp-token-#
    SLACK_SIGNING_SECRET=string-here

    AZURE_ACCOUNT_REGION=string-here
    AZURE_ACCOUNT_KEY=string-here
    ```

5. Install the Slack app to your workspace. 

6. Run `app.py` and navigate to the App Home to try it out!
___

## Inspiration 🧠
Color blindness affects 1 in 12 men (8%), and that's just one gender! In humans, some form of visual impairment is pretty common and affects millions of people present-day. But people use red-green and blue-yellow visuals all the time... in charts, heatmaps, market data, and images. 

It's highly likely you're going to have teammates, customers, or community members with some form of visual impairment. **How do we improve visual communication and make things more accessible?** 

![Easy Image View - For Whom](https://cdn.discordapp.com/attachments/931114609434308609/938018112232640582/3.png)

**NOTE:** To see all showcase images in full resolution with lossless quality, here's the **[slidedeck link](https://www.canva.com/design/DAE3EpQB4Cg/zAYja1_APkSIn556lzD1Vg/view?utm_content=DAE3EpQB4Cg&utm_campaign=designshare&utm_medium=link&utm_source=sharebutton)**! Please use this link if you see blurry image quality on Devpost images. 
___

## What it does 🌟
**Easy Image View** is a free, opensource Slack app that creates colorblind-friendly images with auto-generated alt-text... all within seconds! Make communication inclusive and accessibility convenient.

With HSV Hue Shift Color Correction, we can make images red- green- blue- color deficiency friendly for those with Deuteranopia, Protanopia, and Tritanopia (the most common forms of color blindness). For those with screen readers, the Slack app utilizes Azure AI Computer Vision to automatically caption images with alt text.  There's even settings in the App Home so that you can customize the app to your vision!

![Easy Image View - Value Proposition](https://cdn.discordapp.com/attachments/931114609434308609/938020193274318908/4.png)

___

## How we built it 🖥️
I'm not color blind myself, but I've had teammates with some form of visual impairment. For user-centered design, I did research into the community's pain points by reading their subreddit r/ColorBlind.  From here, I learned that though some devices have colorblind modes, several users don't know about it since it's well-hidden, and others even _choose_ not to use them because of issues like weird, off-putting recoloring and bugs (eg: Netflix appearing black) or shared PCs. 

This made me think that a Slack app could be an effective solution to quickly generate colorblind-friendly images with alt text. Slack is used by teams and communities all over the world for all types of purposes... with lots of visual communication in workspaces, this seemed like the perfect opportunity to create an app that makes accessibility convenient! With the opensource Colorblind library for Python, I scripted a Slack app that uses HSV Hue Shift Color Correction and Computer Vision to (1) recolor (2) resize and (3) caption images. 

> - **Language:** Python 
> - **Slack App Development:** Bolt Py API and Events Subscription
> - **Computer Vision:** Azure AI Computer Vision and OpenCV
> - **Opensource Library:** Colorblind Py

To learn more, you can find the commented code in the GitHub repo!

___

## Challenges we ran into 🤔
I used the Bolt Py for Slack app development for the first time, so I'm really happy with my creation! For challenges, sometimes I was confused how to get everything to work together (eg: when to use the Slack Web API versus Bolt Py and how Event Subscriptions tie in). 

Luckily, there was a lot of documentation and examples in the Github repo for me to refer to. Occasionally I would run into bugs and have no idea how to fix them by myself as a solo developer. I'd like to give **special thanks** to the people in the Slackathon workspace support channel who served as a second pair of eyes! (Get it, second pair of eyes? Haha.) 

___

## Accomplishments that we're proud of  🙌
I'm happy that I think I created something with real-world value and use-case! I'm also proud that I picked up so many new skills for this project and quashed so many bugs. I didn't have any experience with Slack Bolt Py and had never used Azure for anything before. 

I'm also quite pleased with myself with the project scoping because I was able to make something polished in a short time... with more features that could easily be added on. For example, the original app idea was only for color correction, but I was able to add alt text and resizing options so that the app would be more accessible for more types of users. 

![Easy Image View - Tech Magic](https://cdn.discordapp.com/attachments/931114609434308609/938018113176338442/6.png)

___

## What's next for Easy Image View 🚀
For next steps, Easy Image View could be further improved by using OCR computer vision to read text on images and add that to the alt text. For the scope of this hackathon project, computer vision is only used for image analysis for captions, yet OCR could make the app more effective for those with screen readers and also help those who struggle to read certain fonts if they have dyslexia.

![Easy Image View - Showcase](https://cdn.discordapp.com/attachments/931114609434308609/938018112853389342/5.png)



**Questions?**
You can contact me at [@Ocarune](https://twitter.com/Ocarune).