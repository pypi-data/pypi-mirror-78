class UnsupportedService(Exception):
    """
    - **API Code** : 100
    - **API Message** : Unsupported service. Your client may be out of date. Please update it to the latest version.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class FileTooLarge(Exception):
    """
    - **API Code** : 102
    - **API Message** : ``Unknown Message``
    - **API String** : API_STD_ERR_ENTITY_TOO_LARGE_RAW
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidRequest(Exception):
    """
    - **API Code** : 103, 104
    - **API Message** : Invalid Request. Please update to the latest version. If the problem continues, please contact us.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidSession(Exception):
    """
    - **API Code** : 105
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AccessDenied(Exception):
    """
    - **API Code** : 106
    - **API Message** : Access denied.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UnexistentData(Exception):
    """
    - **API Code** : 107
    - **API Message** : The requested data does not exist.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class MessageNeeded(Exception):
    """
    - **API Code** : 113
    - **API Message** : Be more specific, please.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidAccountOrPassword(Exception):
    """
    - **API Code** : 200
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AccountDisabled(Exception):
    """
    - **API Code** : 210
    - **API Message** : This account is disabled.
    - **API String** : AUTH_DISABLED_ACCOUNT
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidEmail(Exception):
    """
    - **API Code** : 213
    - **API Message** : Invalid email address.
    - **API String** : API_ERR_EMAIL
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidPassword(Exception):
    """
    - **API Code** : 214
    - **API Message** : Invalid password. Password must be 6 characters or more and contain no spaces.
    - **API String** : API_ERR_PASSWORD
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class EmailAlreadyTaken(Exception):
    """
    - **API Code** : 215
    - **API Message** : Hey this email ``X`` has been registered already. You can try to log in with the email or edit the email.
    - **API String** : API_ERR_EMAIL_TAKEN
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UnsupportedEmail(Exception):
    """
    - **API Code** : 215
    - **API Message** : This email address is not supported.
    - **API String** : API_ERR_EMAIL_TAKEN
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AccountDoesntExist(Exception):
    """
    - **API Code** : 216
    - **API Message** : ``Unknown Message``
    - **API String** : AUTH_ACCOUNT_NOT_EXISTS
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidDevice(Exception):
    """
    - **API Code** : 218
    - **API Message** : Error! Your device is currently not supported, or the app is out of date. Please update to the latest version.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AccountLimitReached(Exception):
    """
    - **API Code** : 219
    - **API Message** : A maximum of 3 accounts can be created from this device. If you forget your password, please reset it.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class TooManyRequests(Exception):
    """
    - **API Code** : 219
    - **API Message** : Too many requests. Try again later.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CantFollowYourself(Exception):
    """
    - **API Code** : 221
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UserUnavailable(Exception):
    """
    - **API Code** : 225
    - **API Message** : This user is unavailable.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class YouAreBanned(Exception):
    """
    - **API Code** : 229
    - **API Message** : You are banned.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UserNotMemberOfCommunity(Exception):
    """
    - **API Code** : 230
    - **API Message** : You have to join this Community first.
    - **API String** : API_ERR_USER_NOT_IN_COMMUNITY
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CantLeaveCommunity(Exception):
    """
    - **API Code** : 239
    - **API Message** : Sorry, you can not do this before transferring your Agent status to another member.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class ReachedTitleLength(Exception):
    """
    - **API Code** : 240
    - **API Message** : Sorry, the max length of member's title is limited to 20.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AccountDeleted(Exception):
    """
    - **API Code** : 246
    - **API Message** : ``Unknown Message``
    - **API String** : AUTH_RECOVERABLE_DELETED_ACCOUNT
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class API_ERR_EMAIL_NO_PASSWORD(Exception):
    """
    - **API Code** : 251
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_EMAIL_NO_PASSWORD
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class API_ERR_COMMUNITY_USER_CREATED_COMMUNITIES_VERIFY(Exception):
    """
    - **API Code** : 257
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_COMMUNITY_USER_CREATED_COMMUNITIES_VERIFY
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class ReachedMaxTitles(Exception):
    """
    - **API Code** : 262
    - **API Message** : You can only add up to 20 Titles. Please choose the most relevant ones.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class VerificationRequired(Exception):
    """
    - **API Code** : 270
    - **API Message** : Verification Required.
    - **API String** : API_ERR_NEED_TWO_FACTOR_AUTHENTICATION
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class API_ERR_INVALID_AUTH_NEW_DEVICE_LINK(Exception):
    """
    - **API Code** : 271
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_INVALID_AUTH_NEW_DEVICE_LINK
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CommandCooldown(Exception):
    """
    - **API Code** : 291
    - **API Message** : Whoa there! You've done too much too quickly. Take a break and try again later.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UserBannedByTeamAmino(Exception):
    """
    - **API Code** : 293
    - **API Message** : Sorry, this user has been banned by Team Amino.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class BadImage(Exception):
    """
    - **API Code** : 300
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidThemepack(Exception):
    """
    - **API Code** : 313
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidVoiceNote(Exception):
    """
    - **API Code** : 314
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class RequestedNoLongerExists(Exception):
    """
    - **API Code** : 500, 700, 1600
    - **API Message** : Sorry, the requested data no longer exists. Try refreshing the view.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class PageRepostedTooRecently(Exception):
    """
    - **API Code** : 503
    - **API Message** : Sorry, you have reported this page too recently.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InsufficientLevel(Exception):
    """
    - **API Code** : 551
    - **API Message** : This post type is restricted to members with a level ``X`` ranking and above.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class WallCommentingDisabled(Exception):
    """
    - **API Code** : 702
    - **API Message** : This member has disabled commenting on their wall.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CommunityNoLongerExists(Exception):
    """
    - **API Code** : 801
    - **API Message** : This Community no longer exists.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidCodeOrLink(Exception):
    """
    - **API Code** : 802
    - **API Message** : Sorry, this code or link is invalid.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CommunityNameAlreadyTaken(Exception):
    """
    - **API Code** : 805
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CommunityCreateLimitReached(Exception):
    """
    - **API Code** : 806
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_COMMUNITY_USER_CREATED_COMMUNITIES_EXCEED_QUOTA
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CommunityDeleted(Exception):
    """
    - **API Code** : 833
    - **API Message** : This Community has been deleted.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class ChatFull(Exception):
    """
    - **API Code** : 1605
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UserNotJoined(Exception):
    """
    - **API Code** : 1613
    - **API Message** : Sorry, this user has not joined.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class API_ERR_CHAT_VVCHAT_NO_MORE_REPUTATIONS(Exception):
    """
    - **API Code** : 1627
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_CHAT_VVCHAT_NO_MORE_REPUTATIONS
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class LevelFiveRequiredToEnableProps(Exception):
    """
    - **API Code** : 1661
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class ChatViewOnly(Exception):
    """
    - **API Code** : 1663
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AlreadyRequestedJoinCommunity(Exception):
    """
    - **API Code** : 2001
    - **API Message** : Sorry, you have already submitted a membership request.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class API_ERR_PUSH_SERVER_LIMITATION_APART(Exception):
    """
    - **API Code** : 2501
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_PUSH_SERVER_LIMITATION_APART
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class API_ERR_PUSH_SERVER_LIMITATION_COUNT(Exception):
    """
    - **API Code** : 2502
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_PUSH_SERVER_LIMITATION_COUNT
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class API_ERR_PUSH_SERVER_LINK_NOT_IN_COMMUNITY(Exception):
    """
    - **API Code** : 2503
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_PUSH_SERVER_LINK_NOT_IN_COMMUNITY
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class API_ERR_PUSH_SERVER_LIMITATION_TIME(Exception):
    """
    - **API Code** : 2504
    - **API Message** : ``Unknown Message``
    - **API String** : API_ERR_PUSH_SERVER_LIMITATION_TIME
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AlreadyCheckedIn(Exception):
    """
    - **API Code** : 2601
    - **API Message** : Sorry, you can't check in any more.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AlreadyUsedMonthlyRepair(Exception):
    """
    - **API Code** : 2611
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AccountAlreadyRestored(Exception):
    """
    - **API Code** : 2800
    - **API Message** : Account already restored.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class IncorrectVerificationCode(Exception):
    """
    - **API Code** : 3102
    - **API Message** : Incorrect verification code.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NotOwnerOfChatBubble(Exception):
    """
    - **API Code** : 3905
    - **API Message** : You are not the owner of this chat bubble.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NotEnoughCoins(Exception):
    """
    - **API Code** : 4300
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AlreadyPlayedLottery(Exception):
    """
    - **API Code** : 4400
    - **API Message** : You have played the maximum number of lucky draws.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CannotSendCoins(Exception):
    """
    - **API Code** : 4500, 4501
    - **API Message** : ``Unknown Message``
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AminoIDAlreadyChanged(Exception):
    """
    - **API Code** : 6001
    - **API Message** : Amino ID cannot be changed after you set it.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidAminoID(Exception):
    """
    - **API Code** : 6002
    - **API Message** : Invalid Amino ID
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class InvalidName(Exception):
    """
    - **API Code** : 99001
    - **API Message** : Sorry, the name is invalid.
    - **API String** : ``Unknown String``
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class SpecifyType(Exception):
    """
    Raised when you need to specify the output of the command.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class WrongType(Exception):
    """
    Raised when you attribute the function the wrong type.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UnknownResponse(Exception):
    """
    Raised when an error occurs but the reason is unknown.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NotLoggedIn(Exception):
    """
    Raised when you try to make an action but you aren't logged in.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NoCommunity(Exception):
    """
    Raised when you try to make an action but no community was selected.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NoChatThread(Exception):
    """
    Raised when you try to make an action but no chat was selected.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class ChatRequestsBlocked(Exception):
    """
    Raised when you try to make an action but the end user has chat requests blocked.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class NoImageSource(Exception):
    """
    Raised when you try to make an action but no image source was selected.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CannotFetchImage(Exception):
    """
    Raised when an image cannot be fetched.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class FailedLogin(Exception):
    """
    Raised when you try to login but it fails.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class AgeTooLow(Exception):
    """
    Raised when you try to configure an account but the age is too low. Minimum is 13.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class UnsupportedLanguage(Exception):
    """
    Raised when you try to use a language that isn't supported or exists.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class CommunityNeeded(Exception):
    """
    Raised when you try to execute an command but a Community needs to be specified.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class FlagTypeNeeded(Exception):
    """
    Raised when you try to flag a community, blog or user but a Flag Type needs to be specified.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)

class ReasonNeeded(Exception):
    """
    Raised when you try to execute an command but a Reason needs to be specified.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)


class LibraryUpdateAvailable(Exception):
    """
    Raised when a new library update is available.
    """
    def __init__(*args, **kwargs):
        Exception.__init__(*args, **kwargs)