import enum
import typing
from typing import Optional, Any, List

from . import base
from .base_model import BaseObject


class AccountCounters(BaseObject):
    """VK Object account/AccountCounters

    app_requests - New app requests number
    events - New events number
    faves - New faves number
    friends - New friends requests number
    friends_suggestions - New friends suggestions number
    friends_recommendations - New friends recommendations number
    gifts - New gifts number
    groups - New groups number
    menu_discover_badge -
    messages - New messages number
    memories - New memories number
    notes - New notes number
    notifications - New notifications number
    photos - New photo tags number
    sdk - New sdk number
    """

    app_requests: Optional[int] = None
    events: Optional[int] = None
    faves: Optional[int] = None
    friends: Optional[int] = None
    friends_suggestions: Optional[int] = None
    friends_recommendations: Optional[int] = None
    gifts: Optional[int] = None
    groups: Optional[int] = None
    menu_discover_badge: Optional[int] = None
    messages: Optional[int] = None
    memories: Optional[int] = None
    notes: Optional[int] = None
    notifications: Optional[int] = None
    photos: Optional[int] = None
    sdk: Optional[int] = None


class Info(BaseObject):
    """VK Object account/Info

    2fa_required - Two factor authentication is enabled
    country - Country code
    https_required - Information whether HTTPS-only is enabled
    intro - Information whether user has been processed intro
    mini_apps_ads_slot_id - Ads slot id for MyTarget
    lang - Language ID
    no_wall_replies - Information whether wall comments should be hidden
    own_posts_default - Information whether only owners posts should be shown
    """

    wishlists_ae_promo_banner_show: Optional[base.BoolInt] = None
    _2fa_required: Optional[base.BoolInt] = None
    country: Optional[str] = None
    https_required: Optional[base.BoolInt] = None
    intro: Optional[base.BoolInt] = None
    show_vk_apps_intro: Optional[bool] = None
    mini_apps_ads_slot_id: Optional[int] = None
    qr_promotion: Optional[int] = None
    link_redirects: Optional[typing.Dict[Any, Any]] = None
    lang: Optional[int] = None
    no_wall_replies: Optional[base.BoolInt] = None
    own_posts_default: Optional[base.BoolInt] = None
    subscriptions: Optional[List[int]] = None


class NameRequest(BaseObject):
    """VK Object account/NameRequest"""

    first_name: Optional[str] = None
    id: Optional[int] = None
    last_name: Optional[str] = None
    status: Optional["NameRequestStatus"] = None
    lang: Optional[str] = None
    link_href: Optional[str] = None
    link_label: Optional[str] = None


class NameRequestStatus(enum.Enum):
    """ Request status """

    SUCCESS = "success"
    PROCESSING = "processing"
    DECLINED = "declined"
    WAS_ACCEPTED = "was_accepted"
    WAS_DECLINED = "was_declined"
    DECLINED_WITH_LINK = "declined_with_link"
    RESPONSE = "response"
    RESPONSE_WITH_LINK = "response_with_link"


class Offer(BaseObject):
    """VK Object account/Offer

    description - Offer description
    id - Offer ID
    img - URL of the preview image
    instruction - Instruction how to process the offer
    instruction_html - Instruction how to process the offer (HTML format)
    price - Offer price
    short_description - Offer short description
    tag - Offer tag
    title - Offer title
    currency_amount - Currency amount
    link_id - Link id
    link_type - Link type
    """

    description: Optional[str] = None
    id: Optional[int] = None
    img: Optional[str] = None
    instruction: Optional[str] = None
    instruction_html: Optional[str] = None
    price: Optional[int] = None
    short_description: Optional[str] = None
    tag: Optional[str] = None
    title: Optional[str] = None
    currency_amount: Optional[float] = None
    link_id: Optional[int] = None
    link_type: Optional[str] = None


class PushConversations(BaseObject):
    """VK Object account/PushConversations

    count - Items count
    """

    count: Optional[int] = None
    items: Optional[List["PushConversationsItem"]] = None


class PushConversationsItem(BaseObject):
    """VK Object account/PushConversationsItem

    disabled_until - Time until that notifications are disabled in seconds
    peer_id - Peer ID
    sound - Information whether the sound are enabled
    """

    disabled_until: Optional[int] = None
    peer_id: Optional[int] = None
    sound: Optional[base.BoolInt] = None


class PushParams(BaseObject):
    """VK Object account/PushParams"""

    msg: Optional[List["PushParamsMode"]] = None
    chat: Optional[List["PushParamsMode"]] = None
    like: Optional[List["PushParamsSettings"]] = None
    repost: Optional[List["PushParamsSettings"]] = None
    comment: Optional[List["PushParamsSettings"]] = None
    mention: Optional[List["PushParamsSettings"]] = None
    reply: Optional[List["PushParamsOnoff"]] = None
    new_post: Optional[List["PushParamsOnoff"]] = None
    wall_post: Optional[List["PushParamsOnoff"]] = None
    wall_publish: Optional[List["PushParamsOnoff"]] = None
    friend: Optional[List["PushParamsOnoff"]] = None
    friend_found: Optional[List["PushParamsOnoff"]] = None
    friend_accepted: Optional[List["PushParamsOnoff"]] = None
    group_invite: Optional[List["PushParamsOnoff"]] = None
    group_accepted: Optional[List["PushParamsOnoff"]] = None
    birthday: Optional[List["PushParamsOnoff"]] = None
    event_soon: Optional[List["PushParamsOnoff"]] = None
    app_request: Optional[List["PushParamsOnoff"]] = None
    sdk_open: Optional[List["PushParamsOnoff"]] = None


class PushParamsMode(enum.Enum):
    """ Settings parameters """

    ON = "on"
    OFF = "off"
    NO_SOUND = "no_sound"
    NO_TEXT = "no_text"


class PushParamsOnoff(enum.Enum):
    """ Settings parameters """

    ON = "on"
    OFF = "off"


class PushParamsSettings(enum.Enum):
    """ Settings parameters """

    ON = "on"
    OFF = "off"
    FR_OF_FR = "fr_of_fr"


class PushSettings(BaseObject):
    """VK Object account/PushSettings

    disabled - Information whether notifications are disabled
    disabled_until - Time until that notifications are disabled in Unixtime
    """

    disabled: Optional[base.BoolInt] = None
    disabled_until: Optional[int] = None
    settings: Optional["PushParams"] = None
    conversations: Optional["PushConversations"] = None


class UserSettings(BaseObject):
    """VK Object account/UserSettings"""


class UserSettingsInterest(BaseObject):
    """VK Object account/UserSettingsInterest"""

    title: Optional[str] = None
    value: Optional[str] = None


class UserSettingsInterests(BaseObject):
    """VK Object account/UserSettingsInterests"""

    activities: Optional["UserSettingsInterest"] = None
    interests: Optional["UserSettingsInterest"] = None
    music: Optional["UserSettingsInterest"] = None
    tv: Optional["UserSettingsInterest"] = None
    movies: Optional["UserSettingsInterest"] = None
    books: Optional["UserSettingsInterest"] = None
    games: Optional["UserSettingsInterest"] = None
    quotes: Optional["UserSettingsInterest"] = None
    about: Optional["UserSettingsInterest"] = None
