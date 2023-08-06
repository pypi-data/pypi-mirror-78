import os
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from telegram_news.template.common import (
    NewsPostman,
    InfoExtractor,
)

channel = os.getenv("CHANNEL")

if __name__ == '__main__':

    # Page to test:
    #
    # - Pure text: https://t.me/s/telegram/122
    # - Text with single image: https://t.me/s/telegram/72
    # - Text with single video: passed
    # - Text with multiple images: https://t.me/s/cnbeta_com_news/17531
    # - Text with multiple videos: https://t.me/s/cnbeta_com_news/17531
    # - Single image: passed
    # - Single video: passed
    # - Multiple images: https://t.me/s/RocheLimit/5042
    # - Multiple videos: passed
    # - Image(s) with video(s): https://t.me/s/cnbeta_com_news/17748
    # - Media not supported: https://t.me/radio_television_hong_kong/20780

    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    db = Session(bind=conn)

    tgtg = NewsPostman(listURLs=['https://t.me/s/MarxismLife/20'], sendList=[channel], db=db, tag='TgTg Test')
    tgtgIE = InfoExtractor()
    def tgtglpp(text):
        def img_rep(matchobj):
            return """\"><img class="fake-image" src=\"""" + matchobj.group(1) + """\" """
        text = re.sub(r"background-image:url\([\"']?([^\"']*)[\"']?\)", img_rep, text)
        def rep(matchobj):
            return '</a><time class="fake-time">' + re.findall(r'\d+.\d+.\d+.\d+.\d+.\d+.\d+.\d+', matchobj.group(0))[0] + '</time><a>'
        return re.sub('<time datetime=".*?">.*?</time>', rep, text)
    tgtgIE.set_list_pre_process_policy(tgtglpp)
    tgtgIE.set_list_selector('div.tgme_widget_message_wrap')
    tgtgIE.set_outer_link_selector('a.tgme_widget_message_date')
    # tgtgIE.set_outer_title_selector('div.tgme_widget_message_text > b')
    tgtgIE.set_outer_paragraph_selector('.tgme_widget_message_text, '
                                        '.message_media_not_supported_label, '
                                        'a.tgme_widget_message_reply')
    tgtgIE.set_outer_time_selector('time.fake-time')
    tgtgIE.set_outer_source_selector('.tgme_widget_message_author')
    tgtgIE.set_outer_image_selector('.tgme_widget_message_photo_wrap > img.fake-image, '
                                    '.tgme_widget_message_sticker img.fake-image')
    tgtgIE.set_outer_video_selector('.tgme_widget_message_video_wrap > video')
    tgtg.set_extractor(tgtgIE)
    tgtg.set_table_name('test')
    tgtg.enable_auto_retry()
    tgtg.enable_download_and_send()
    tgtg._DEBUG = True
    tgtg.poll()

    # TODO: adapt for different text length
