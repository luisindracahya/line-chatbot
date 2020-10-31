import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage, VideoSendMessage, MessageImagemapAction,
    ImagemapArea, ImagemapSendMessage, BaseSize, URIImagemapAction, 
    MessageImagemapAction
)

import tempfile, errno

app = Flask(__name__)

line_bot_api = LineBotApi('--INSERT HERE--')
handler = WebhookHandler('--INSERT HERE--')

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    app.logger.info("Got Follow event:" + event.source.user_id)
    sticker = StickerSendMessage(package_id='11537', sticker_id='52002735')
    welcome = TextSendMessage(text='Welcome')
    line_bot_api.reply_message(
        event.reply_token, [welcome, sticker])

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text.lower() == 'menu':
        buttons_template = ButtonsTemplate(
            title='Menu', text='SSG2 - IT Division Bina Nusantara', actions=[
                PostbackAction(label='What is SSG2?', data='sas-def', text='I want to know what is SSG2!'),
                PostbackAction(label='SAS Team Member', data='boys', text='I want to know about SAS Team Member!'),
                PostbackAction(label='Location', data='location', text='I want to know SSG2\'s location'),
                URIAction(label='Website', uri='http://ict.binus.edu/')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    # else:
    #     help = TextSendMessage(text='Please type menu')
    #     line_bot_api.reply_message(
    #         event.reply_token, help)


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'boys':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://img.techpowerup.org/200611/284361.jpg',
                                action=PostbackAction(label='Jason', data='jason', text='I choose Jason')),
            ImageCarouselColumn(image_url='https://pbs.twimg.com/profile_images/3334672485/21f739d56c04695f2414b289f7489b70_400x400.png',
                                action=PostbackAction(label='Ryo', data='ryo', text='I choose Ryo')),
            ImageCarouselColumn(image_url='https://pbs.twimg.com/profile_images/591163788511969280/y9X2ODe3_400x400.jpg',
                                action=PostbackAction(label='Elton', data='elton', text='I choose Elton')),
            ImageCarouselColumn(image_url='https://img.techpowerup.org/200611/284360.jpg',
                                action=PostbackAction(label='Liong', data='liong', text='I choose Liong'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        tap_msg = TextSendMessage(text="Tap on the image above!")
        line_bot_api.reply_message(event.reply_token, [template_message, tap_msg])
    elif event.postback.data == 'location':
        bubble = BubbleContainer(
            direction='ltr',
            body=BoxComponent(
                layout='vertical',
                padding_all= "0px",
                contents=[
                ImageComponent(
                    url='https://binus.ac.id/wp-content/uploads/2011/08/syahdan-campus.jpg',
                    size='full',
                    aspect_ratio='1:1',
                    aspect_mode='cover',
                    gravity = 'center'
                 ),
                ImageComponent(
                    url= "https://scdn.line-apps.com/n/channel_devcenter/img/flexsnapshot/clip/clip15.png",
                    position= "absolute",
                    aspect_mode= "fit",
                    aspect_ratio= "1:1",
                    offset_top= "0px",
                    offset_bottom= "0px",
                    offset_start= "0px",
                    offset_end= "0px",
                    size= "full"
                ),
                BoxComponent(
                    layout = "horizontal",
                    position= "absolute",
                    offset_bottom= "0px",
                    offset_start= "0px",
                    offset_end= "0px",
                    padding_all= "20px",
                    contents=[
                        BoxComponent(
                            layout="vertical",
                            spacing="xs",
                            contents=[
                                BoxComponent(
                                    layout= "horizontal",
                                    contents=[
                                    TextComponent(
                                        text= "Binus University Syahdan",
                                        size= "xl",
                                        color= "#ffffff"
                                    )
                                    ]
                                ),
                                BoxComponent(
                                    layout="baseline",
                                    spacing= "xs",
                                    contents=[
                                    IconComponent(
                                        url = "https://i.dlpng.com/static/png/4131435-location-icon-png-free-download-best-location-icon-png-on-gps-png-free-2000_2723_preview.webp"
                                    ),
                                    TextComponent(
                                                text= "Jl. Kyai H. Syahdan No.9, Palmerah, Jakarta Barat, DKI Jakarta",
                                                size= "xs",
                                                max_lines= 2,
                                                color= "#ffffff"
                                            )
                                    ]
                                ),
                                BoxComponent(
                                    layout="horizontal",
                                    flex= 0,
                                    spacing= "lg",
                                    contents=[
                                        BoxComponent(
                                            layout="baseline",
                                            action=URIAction(label= "action", uri= "https://goo.gl/maps/XTgYhUDz9Eruzvtz8")
                                            ,
                                            contents=[
                                                TextComponent(
                                                    text = "open in google map",
                                                    color = "#a9a9a9",
                                                    size= "md",
                                                    flex= 0,
                                                    align= "end"
                                                ),
                                                IconComponent(
                                                    size = "md",
                                                    margin="xxl",
                                                    url =  "https://www.elementconcept.com/wp-content/uploads/2019/11/Open-in-new-window-icon-2.png"
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
               ]
            )
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif event.postback.data == 'jason':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://img.techpowerup.org/200611/284446.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Jason J', weight='bold', size='xl'),
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://image.flaticon.com/icons/png/512/69/69045.png'),
                            TextComponent(text='Junior Programmer at IT Binus', size='sm', color='#999999', margin='md', flex=0)
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Phone',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='0812-3456-7890',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                        margin = 'sm'
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Email',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="jasj@binus.edu",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:081234567890'),
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='LINKEDIN', uri="https://id.linkedin.com/in/jasonkurniadj?trk=pub-pbmap")
                    ),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif event.postback.data == 'ryo':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://img.techpowerup.org/200611/284444.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Ryo Hadinata', weight='bold', size='xl'),
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://image.flaticon.com/icons/png/512/69/69045.png'),
                            TextComponent(text='Senior System Analyst at IT Binus', size='sm', color='#999999', margin='md', flex=0)
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Phone',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='0812-3456-7890',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                        margin = 'sm'
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Email',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="ryo@binus.edu",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:081234567890'),
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='LINKEDIN', uri="https://id.linkedin.com/in/ryo-hadinata-40b43612a")
                    ),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif event.postback.data == 'elton':
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://img.techpowerup.org/200611/284443.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Elton Yeo', weight='bold', size='xl'),
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://image.flaticon.com/icons/png/512/69/69045.png'),
                            TextComponent(text='Junior System Analyst at IT Binus', size='sm', color='#999999', margin='md', flex=0)
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Phone',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='0812-3456-7890',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                        margin = 'sm'
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Email',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="elton@binus.edu",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:081234567890'),
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='INSTAGRAM', uri="https://instagram.com/elton.yeoo?igshid=fiemvl5j376r")
                    ),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif event.postback.data == 'liong':  
        bubble = BubbleContainer(
            direction='ltr',
            hero=ImageComponent(
                url='https://img.techpowerup.org/200611/284445.jpg',
                size='full',
                aspect_ratio='20:13',
                aspect_mode='cover',
            ),
            body=BoxComponent(
                layout='vertical',
                contents=[
                    TextComponent(text='Michael LJ', weight='bold', size='xl'),
                    BoxComponent(
                        layout='baseline',
                        margin='md',
                        contents=[
                            IconComponent(size='sm', url='https://image.flaticon.com/icons/png/512/69/69045.png'),
                            TextComponent(text='Junior Programmer at IT Binus', size='sm', color='#999999', margin='md', flex=0)
                        ]
                    ),
                    BoxComponent(
                        layout='vertical',
                        margin='lg',
                        spacing='sm',
                        contents=[
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Phone',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text='0812-3456-7890',
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                        margin = 'sm'
                                    )
                                ],
                            ),
                            BoxComponent(
                                layout='baseline',
                                spacing='sm',
                                contents=[
                                    TextComponent(
                                        text='Email',
                                        color='#aaaaaa',
                                        size='sm',
                                        flex=1
                                    ),
                                    TextComponent(
                                        text="liong@binus.edu",
                                        wrap=True,
                                        color='#666666',
                                        size='sm',
                                        flex=5,
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            footer=BoxComponent(
                layout='vertical',
                spacing='sm',
                contents=[
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='CALL', uri='tel:081234567890'),
                    ),
                    SeparatorComponent(),
                    ButtonComponent(
                        style='link',
                        height='sm',
                        action=URIAction(label='INSTAGRAM', uri="https://instagram.com/michaelliong?igshid=sk7phfz2cp07")
                    ),
                ]
            ),
        )
        message = FlexSendMessage(alt_text="hello", contents=bubble)
        line_bot_api.reply_message(
            event.reply_token,
            message
        )
    elif event.postback.data == 'sas-def':
        message = 'Software Solution (Group 2)\nThis department is led by/managed by: Mr. Andy Effendi\nThis department is responsible for applications development in areas, which includes, BINUS UNIVERSITY, BINUS BUSINESS SCHOOL, Services Opration Support, Binus TV and BCS (Oracle).'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=message))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
