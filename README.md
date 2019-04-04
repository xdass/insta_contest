# Programming vacancies compare


This program helps you to find winner on your instagram contest.
You need only take post url in script argument. 

_Note: Script checks such conditions:_
* user is the follower of post's author.
* user liked the post.
* user mentioned in comment 2 of his friends.


### How to install

1. You need to registered account in Instagram.
2. Create .env file and add:
    * login=instagram_username
    * password=instagram_password

3. Install dependencies (written below)

Python3 should be already installed. 
Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```

### Program output example
```
python main.py https://www.instagram.com/p/Bvtd60pnk23/
2019-04-04 09:18:57,615 - INFO - Instabot Started
2019-04-04 09:19:01,250 - INFO - Logged-in successfully as 'dmitryturov2'!
Getting followers of 2253098871: 100%|██████████| 5472/5472 [00:10<00:00, 522.24it/s]
2019-04-04 09:19:41,165 - ERROR - Request returns 404 error!
2019-04-04 09:20:46,653 - ERROR - Request returns 429 error!
2019-04-04 09:20:46,654 - WARNING - That means 'too many requests'. I'll go to sleep for 5 minutes.
2019-04-04 09:26:50,699 - ERROR - Request returns 404 error!
2019-04-04 09:27:19,555 - ERROR - Request returns 429 error!
2019-04-04 09:27:19,556 - WARNING - That means 'too many requests'. I'll go to sleep for 5 minutes.
Getting followers of 3009116786: 100%|█████████▉| 784/785 [00:01<00:00, 440.01it/s]
Getting followers of 1443822182: 100%|█████████▉| 885/886 [00:01<00:00, 499.06it/s]
.......................
Getting followers of 4164227363: 100%|█████████▉| 1143/1144 [00:02<00:00, 468.71it/s]
2019-04-04 09:35:25,496 - INFO - Bot stopped. Worked: 5 days, 19:20:31.307962
2019-04-04 09:35:25,497 - INFO - Total requests: 4189
['elizabeth_bezkorovaina', 'kzkva89', 'goncharova_muastilist', 'miss.marikol', 'kateryna_zhirkova', 'cherkashina_makeup', 'lazorenko_l', 'garmaschgarya', 'natalisha3', '_tanyadybovik_', 'lutai_photo', '_lero4ka_drozd_', 'ingaakulenko']
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).