import json
import base64
import requests
from time import timezone
from time import time as timestamp
from locale import getdefaultlocale as locale
from typing import BinaryIO

from .lib.util import exceptions, headers, device, objects
from .socket import Callbacks, SocketHandler

device = device.DeviceGenerator()

class Client:
    def __init__(self, callback=Callbacks, socket_trace=False):
        self.api = "https://service.narvii.com/api/v1"
        self.authenticated = False
        self.configured = False
        self.user_agent = device.user_agent
        self.device_id = device.device_id
        self.device_id_sig = device.device_id_sig
        self.socket = SocketHandler(self, socket_trace=socket_trace)
        self.callbacks = callback(self)

        self.json = None
        self.sid = None
        self.userId = None
        self.account = None
        self.profile = None

        self.check_device(device.device_id)

    def login(self, email: str, password: str):
        """
        Login into an account.

        **Parameters**
            - **email** : Email of the account.
            - **password** : Password of the account.

        **Returns**
            - **200** (int) : **Success**

            - **200** (:meth:`InvalidAccountOrPassword <amino.lib.util.exceptions.InvalidAccountOrPassword>`) : ``Unknown Message``

            - **213** (:meth:`InvalidEmail <amino.lib.util.exceptions.InvalidEmail>`) : Invalid email address.

            - **214** (:meth:`InvalidPassword <amino.lib.util.exceptions.InvalidPassword>`) : Invalid password. Password must be 6 characters or more and contain no spaces.

            - **216** (:meth:`AccountDoesntExist <amino.lib.util.exceptions.AccountDoesntExist>`) : Account does not exist.

            - **246** (:meth:`AccountDeleted <amino.lib.util.exceptions.AccountDeleted>`) : ``Unknown Message``

            - **270** (:meth:`VerificationRequired <amino.lib.util.exceptions.VerificationRequired>`) : Verification Required.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "email": email,
            "v": 2,
            "secret": f"0 {password}",
            "deviceID": self.device_id,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/g/s/auth/login", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 200: raise exceptions.InvalidAccountOrPassword(response)
            elif response["api:statuscode"] == 213: raise exceptions.InvalidEmail(response)
            elif response["api:statuscode"] == 214: raise exceptions.InvalidPassword(response)
            elif response["api:statuscode"] == 216: raise exceptions.AccountDoesntExist(response)
            elif response["api:statuscode"] == 246: raise exceptions.AccountDeleted(response)
            elif response["api:statuscode"] == 270: raise exceptions.VerificationRequired(response)
            else: return response

        else:
            self.authenticated = True
            self.json = json.loads(response.text)
            self.sid = self.json["sid"]
            self.userId = self.json["account"]["uid"]
            self.account = objects.userProfile(self.json["account"]).userProfile
            self.profile = objects.userProfile(self.json["userProfile"]).userProfile
            headers.sid = self.sid
            self.socket.start()
            return response.status_code

    def register(self, nickname: str, email: str, password: str, deviceId: str = device.device_id):
        """
        Register an account.

        **Parameters**
            - **nickname** : Nickname of the account.
            - **email** : Email of the account.
            - **password** : Password of the account.
            - **deviceId** : The device id being registered to.

        **Returns**
            - **200** (int) : **Success**

            - **200** (:meth:`InvalidAccountOrPassword <amino.lib.util.exceptions.InvalidAccountOrPassword>`) : ``Unknown Message``

            - **213** (:meth:`InvalidEmail <amino.lib.util.exceptions.InvalidEmail>`) : Invalid email address.

            - **214** (:meth:`InvalidPassword <amino.lib.util.exceptions.InvalidPassword>`) : Invalid password. Password must be 6 characters or more and contain no spaces.

            - **215** (:meth:`EmailAlreadyTaken <amino.lib.util.exceptions.EmailAlreadyTaken>`) : Hey this email ``X`` has been registered already. You can try to log in with the email or edit the email.

            - **219** (:meth:`AccountLimitReached <amino.lib.util.exceptions.AccountLimitReached>`) : A maximum of 3 accounts can be created from this device. If you forget your password, please reset it.

            - **270** (:meth:`VerificationRequired <amino.lib.util.exceptions.VerificationRequired>`) : Verification Required.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "secret": f"0 {password}",
            "deviceID": deviceId,
            "email": email,
            "clientType": 100,
            "nickname": nickname,
            "latitude": 0,
            "longitude": 0,
            "address": None,
            "clientCallbackURL": "narviiapp://relogin",
            "type": 1,
            "identity": email,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/g/s/auth/register", data=data, headers=headers.Headers(data=data).headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 213: raise exceptions.InvalidEmail(response)
            elif response["api:statuscode"] == 214: raise exceptions.InvalidPassword(response)
            elif response["api:statuscode"] == 215: raise exceptions.EmailAlreadyTaken(response)
            elif response["api:statuscode"] == 219: raise exceptions.AccountLimitReached(response)
            elif response["api:statuscode"] == 270: raise exceptions.VerificationRequired(response)
            else: return response

        else: return response.status_code

    def restore(self, email: str, password: str):
        """
        Restore a deleted account.

        **Parameters**
            - **email** : Email of the account.
            - **password** : Password of the account.

        **Returns**
            - **200** (int) : **Success**

            - **200** (:meth:`InvalidAccountOrPassword <amino.lib.util.exceptions.InvalidAccountOrPassword>`) : ``Unknown Message``

            - **213** (:meth:`InvalidEmail <amino.lib.util.exceptions.InvalidEmail>`) : Invalid email address.

            - **214** (:meth:`InvalidPassword <amino.lib.util.exceptions.InvalidPassword>`) : Invalid password. Password must be 6 characters or more and contain no spaces.

            - **216** (:meth:`AccountDoesntExist <amino.lib.util.exceptions.AccountDoesntExist>`) : Account does not exist.

            - **270** (:meth:`VerificationRequired <amino.lib.util.exceptions.VerificationRequired>`) : Verification Required.

            - **2800** (:meth:`AccountAlreadyRestored <amino.lib.util.exceptions.AccountAlreadyRestored>`) : Account already restored.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "secret": f"0 {password}",
            "deviceID": device.device_id,
            "email": email,
            "timestamp": int(timestamp() * 1000)

        })

        response = requests.post(f"{self.api}/g/s/account/delete-request/cancel", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 200: raise exceptions.InvalidAccountOrPassword(response)
            elif response["api:statuscode"] == 213: raise exceptions.InvalidEmail(response)
            elif response["api:statuscode"] == 214: raise exceptions.InvalidPassword(response)
            elif response["api:statuscode"] == 216: raise exceptions.AccountDoesntExist(response)
            elif response["api:statuscode"] == 270: raise exceptions.VerificationRequired(response)
            elif response["api:statuscode"] == 2800: raise exceptions.AccountAlreadyRestored(response)
            else: return response

        else: return response.status_code

    def logout(self):
        """
        Logout from an account.

        **Parameters**
            - No parameters required.

        **Returns**
            - **200** (int) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "deviceID": self.device_id,
            "clientType": 100,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/g/s/auth/logout", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: self.authenticated = False; return response.status_code

    def configure(self, age: int, gender: str):
        """
        Configure the settings of an account.

        **Parameters**
            - **age** : Age of the account. Minimum is 13.
            - **gender** : Gender of the account.
                - ``Male``, ``Female`` or ``Non-Binary``

        **Returns**
            - **200** (int) : **Success**

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`AgeTooLow <amino.lib.util.exceptions.AgeTooLow>`, :meth:`JSON Object <JSONObject>`)
        """
        if gender.lower() == "male": gender = 1
        elif gender.lower() == "female": gender = 2
        elif gender.lower() == "non-binary": gender = 255
        else: raise exceptions.SpecifyType

        if age <= 12: raise exceptions.AgeTooLow

        data = json.dumps({
            "age": age,
            "gender": gender,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/g/s/persona/profile/basic", data=data, headers=headers.Headers(data=data).headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            else: return response

        else: return response.status_code

    def verify(self, email: str, code: str):
        """
        Verify an account.

        **Parameters**
            - **email** : Email of the account.
            - **code** : Verification code.

        **Returns**
            - **200** (int) : **Success**

            - **213** (:meth:`InvalidEmail <amino.lib.util.exceptions.InvalidEmail>`) : Invalid email address.

            - **219** (:meth:`TooManyRequests <amino.lib.util.exceptions.TooManyRequests>`) : Too many requests. Try again later.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "validationContext": {
                "type": 1,
                "identity": email,
                "data": {"code": code}},
            "deviceID": device.device_id,
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/g/s/auth/check-security-validation", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 213: raise exceptions.InvalidEmail(response)
            elif response["api:statuscode"] == 219: raise exceptions.TooManyRequests(response)
            elif response["api:statuscode"] == 3102: raise exceptions.IncorrectVerificationCode(response)
            else: return response

        else: return response.status_code

    def request_verify_code(self, email: str):
        """
        Request an verification code to the targeted email.

        **Parameters**
            - **email** : Email of the account.

        **Returns**
            - **200** (int) : **Success**

            - **213** (:meth:`InvalidEmail <amino.lib.util.exceptions.InvalidEmail>`) : Invalid email address.

            - **219** (:meth:`TooManyRequests <amino.lib.util.exceptions.TooManyRequests>`) : Too many requests. Try again later.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "identity": email,
            "type": 1,
            "deviceID": device.device_id
        })

        response = requests.post(f"{self.api}/g/s/auth/request-security-validation", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 213: raise exceptions.InvalidEmail(response)
            elif response["api:statuscode"] == 219: raise exceptions.TooManyRequests(response)
            else: return response

        else: return response.status_code

    def activate_account(self, email: str, code: str):
        """
        Activate an account.

        **Parameters**
            - **email** : Email of the account.
            - **code** : Verification code.

        **Returns**
            - **200** (int) : **Success**

            - **213** (:meth:`InvalidEmail <amino.lib.util.exceptions.InvalidEmail>`) : Invalid email address.

            - **219** (:meth:`TooManyRequests <amino.lib.util.exceptions.TooManyRequests>`) : Too many requests. Try again later.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "type": 1,
            "identity": email,
            "data": {"code": code},
            "deviceID": device.device_id
        })

        response = requests.post(f"{self.api}/g/s/auth/activate-email", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 213: raise exceptions.InvalidEmail(response)
            elif response["api:statuscode"] == 219: raise exceptions.TooManyRequests(response)
            else: return response

        else: return response.status_code

    def check_device(self, deviceId: str):
        """
        Check if the Device ID is valid.

        **Parameters**
            - **deviceId** : ID of the Device.

        **Returns**
            - **200** (int) : **Success**

            - **218** (:meth:`InvalidDevice <amino.lib.util.exceptions.InvalidDevice>`) : Error! Your device is currently not supported, or the app is out of date. Please update to the latest version.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "deviceID": deviceId,
            "bundleID": "com.narvii.amino.master",
            "clientType": 100,
            "timezone": -timezone // 1000,
            "systemPushEnabled": True,
            "locale": locale()[0],
            "timestamp": int(timestamp() * 1000)
        })

        response = requests.post(f"{self.api}/g/s/device", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 218: raise exceptions.InvalidDevice(response)
            else: return response

        else: self.configured = True; return response.status_code

    def upload_media(self, file: BinaryIO):
        """
        Upload file to the amino servers.

        **Parameters**
            - **file** : File to be uploaded.

        **Returns**
            - **200** (str) : **Success**, Url of the file uploaded to the server.

            - **300** (:meth:`BadImage <amino.lib.util.exceptions.BadImage>`) : ``Unknown Message``

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = file.read()
        response = requests.post(f"{self.api}/g/s/media/upload", data=data, headers=headers.Headers(type=f"image/jpg", data=data).headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 300: raise exceptions.BadImage(response)
            else: return response

        else: return json.loads(response.text)["mediaValue"]

    def handle_socket_message(self, data):
        return self.callbacks.resolve(data)

    def sub_clients(self, start: int = 0, size: int = 25):
        """
        List of Communities the account is in.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`Community List <amino.lib.util.objects.communityList>`) : **Success**

            - **Other** (:meth:`NotLoggedIn <amino.lib.util.exceptions.NotLoggedIn>`, :meth:`JSON Object <JSONObject>`)
        """
        if not self.authenticated: raise exceptions.NotLoggedIn
        response = requests.get(f"{self.api}/g/s/community/joined?v=1&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return objects.communityList(json.loads(response.text)["communityList"]).communityList

    def get_user_info(self, userId: str):
        """
        Information of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **200** (:meth:`User Object <amino.lib.util.objects.userProfile>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/user-profile/{userId}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return objects.userProfile(json.loads(response.text)["userProfile"]).userProfile

    def get_chat_threads(self, start: int = 0, size: int = 25):
        """
        List of Chats the account is in.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`Chat List <amino.lib.util.objects.threadList>`) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/chat/thread?type=joined-me&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.threadList(json.loads(response.text)["threadList"]).threadList

    def get_chat_thread(self, chatId: str):
        """
        Get the Chat Object from an Chat ID.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **200** (:meth:`Chat Object <amino.lib.util.objects.thread>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/chat/thread/{chatId}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            else: return response

        else: return objects.thread(json.loads(response.text)["thread"]).thread

    # TODO : The documentation of this
    def get_chat_users(self, chatId: str, start: int = 0, size: int = 25):
        response = requests.get(f"{self.api}/g/s/chat/thread/{chatId}/member?start={start}&size={size}&type=default&cv=1.2", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        return objects.userProfileList(json.loads(response.text)["memberList"]).userProfileList

    def join_chat(self, chatId: str):
        """
        Join an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **200** (int) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/member/{self.userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def leave_chat(self, chatId: str):
        """
        Leave an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.

        **Returns**
            - **200** (int) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.delete(f"{self.api}/g/s/chat/thread/{chatId}/member/{self.userId}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def get_chat_messages(self, chatId: str, size: int = 25):
        """
        List of Messages from an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`Message List <amino.lib.util.objects.messageList>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/chat/thread/{chatId}/message?v=2&pagingType=t&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            else: return response

        else: return objects.messageList(json.loads(response.text)["messageList"]).messageList

    def get_message_info(self, chatId: str, messageId: str):
        """
        Information of an Message from an Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - **message** : ID of the Message.

        **Returns**
            - **200** (:meth:`Message Object <amino.lib.util.objects.message>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/chat/thread/{chatId}/message/{messageId}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            else: return response

        else: return objects.message(json.loads(response.text)["message"]).message

    def get_community_info(self, comId: str):
        """
        Information of an Community.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **200** (:meth:`Community Object <amino.lib.util.objects.community>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **801** (:meth:`CommunityNoLongerExists <amino.lib.util.exceptions.CommunityNoLongerExists>`) : This Community no longer exists.

            - **833** (:meth:`CommunityDeleted <amino.lib.util.exceptions.CommunityDeleted>`) : This Community has been deleted.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s-x{comId}/community/info?withInfluencerList=1&withTopicList=true&influencerListOrderStrategy=fansCount", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 801: raise exceptions.CommunityNoLongerExists(response)
            elif response["api:statuscode"] == 833: raise exceptions.CommunityDeleted(response)
            else: return response

        else: return objects.community(json.loads(response.text)["community"]).community

    def get_user_following(self, userId: str, start: int = 0, size: int = 25):
        """
        List of Users that the User is Following.

        **Parameters**
            - **userId** : ID of the User.
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`User List <amino.lib.util.objects.userProfileList>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/user-profile/{userId}/joined?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return objects.userProfileList(json.loads(response.text)["userProfileList"]).userProfileList

    def get_user_followers(self, userId: str, start: int = 0, size: int = 25):
        """
        List of Users that are Following the User.

        **Parameters**
            - **userId** : ID of the User.
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`User List <amino.lib.util.objects.userProfileList>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/user-profile/{userId}/member?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return objects.userProfileList(json.loads(response.text)["userProfileList"]).userProfileList

    def get_user_visitors(self, userId: str, start: int = 0, size: int = 25):
        """
        List of Users that Visited the User.

        **Parameters**
            - **userId** : ID of the User.
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`Visitors List <amino.lib.util.objects.visitorsList>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/user-profile/{userId}/visitors?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return objects.visitorsList(json.loads(response.text)).visitorsList

    def get_blocked_users(self, start: int = 0, size: int = 25):
        """
        List of Users that the User Blocked.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`Users List <amino.lib.util.objects.userProfileList>`) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/block?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return objects.userProfileList(json.loads(response.text)["userProfileList"]).userProfileList

    def get_blocker_users(self, start: int = 0, size: int = 25):
        """
        List of Users that are Blocking the User.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (str) : **Success**, :meth:`List of User IDs <None>`

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/block/full-list?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return json.loads(response.text)["blockerUidList"]

    def get_wall_comments(self, userId: str, sorting: str, start: int = 0, size: int = 25):
        """
        List of Wall Comments of an User.

        **Parameters**
            - **userId** : ID of the User.
            - **sorting** : Order of the Comments.
                - ``newest``, ``oldest``, ``top``
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`Comments List <amino.lib.util.objects.commentList>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        if sorting.lower() == "newest": sorting = "newest"
        elif sorting.lower() == "oldest": sorting = "oldest"
        elif sorting.lower() == "top": sorting = "vote"
        else: raise exceptions.SpecifyType

        response = requests.get(f"{self.api}/g/s/user-profile/{userId}/g-comment?sort={sorting}&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return objects.commentList(json.loads(response.text)["commentList"]).commentList

    def flag(self, reason: str, flagType: int, userId: str = None, blogId: str = None, wikiId: str = None, asGuest: bool = False):
        """
        Flag a User, Blog or Wiki.

        **Parameters**
            - **reason** : Reason of the Flag.
            - **flagType** : Type of the Flag.
            - **userId** : ID of the User.
            - **blogId** : ID of the Blog.
            - **wikiId** : ID of the Wiki.
            - *asGuest* : Execute as a Guest.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **Other** (:meth:`ReasonNeeded <amino.lib.util.exceptions.ReasonNeeded>`, :meth:`FlagTypeNeeded <amino.lib.util.exceptions.FlagTypeNeeded>`, :meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        if reason is None: raise exceptions.ReasonNeeded
        if flagType is None: raise exceptions.FlagTypeNeeded

        data = {
            "flagType": flagType,
            "message": reason,
            "timestamp": int(timestamp() * 1000)
        }

        if userId:
            data["objectId"] = userId
            data["objectType"] = 0

        elif blogId:
            data["objectId"] = blogId
            data["objectType"] = 1

        elif wikiId:
            data["objectId"] = wikiId
            data["objectType"] = 2

        else: raise exceptions.SpecifyType

        if asGuest: flg = "g-flag"
        else: flg = "flag"

        data = json.dumps(data)
        response = requests.post(f"{self.api}/g/s/{flg}", data=data, headers=headers.Headers(data=data).headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            else: return response

        else: return response.status_code

    def send_message(self, chatId: str, message: str = None, file: BinaryIO = None, fileType: str = None, replyTo: str = None, mentionUserIds: list = None, stickerId: str = None):
        """
        Send a Message to a Chat.

        **Parameters**
            - **message** : Message to be sent
            - **chatId** : ID of the Chat.
            - **file** : File to be sent.
            - **fileType** : Type of the file.
                - ``audio``, ``image``, ``gif``
            - **mentionUserIds** : List of User IDS to mention. '@' needed in the Message.
            - **replyTo** : Message ID to reply to.
            - **stickerId** : Sticker ID to be sent.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **1605** (:meth:`ChatFull <amino.lib.util.exceptions.ChatFull>`) : ``Unknown Message``

            - **1663** (:meth:`ChatViewOnly <amino.lib.util.exceptions.ChatViewOnly>`) : ``Unknown Message``

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`DeveloperKeyRequired <amino.lib.util.exceptions.DeveloperKeyRequired>`, :meth:`InvalidDeveloperKey <amino.lib.util.exceptions.InvalidDeveloperKey>`, :meth:`JSON Object <JSONObject>`)
        """
        mentions = []
        if mentionUserIds:
            for mention_uid in mentionUserIds:
                mentions.append({"uid": mention_uid})

        data = {
            "type": 0,
            "content": message,
            "clientRefId": int(timestamp() / 10 % 1000000000),
            "extensions": {"mentionedArray": mentions},
            "timestamp": int(timestamp() * 1000)
        }

        if replyTo: data["replyMessageId"] = replyTo

        if stickerId:
            data["content"] = None
            data["stickerId"] = stickerId
            data["type"] = 3

        if file:
            data["content"] = None
            if fileType == "audio":
                data["type"] = 2
                data["mediaType"] = 110

            elif fileType == "image":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/jpg"
                data["mediaUhqEnabled"] = True

            elif fileType == "gif":
                data["mediaType"] = 100
                data["mediaUploadValueContentType"] = "image/gif"
                data["mediaUhqEnabled"] = True

            else: raise exceptions.SpecifyType

            data["mediaUploadValue"] = base64.b64encode(file.read()).decode()

        data = json.dumps(data)
        response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/message", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 106: raise exceptions.AccessDenied(response)
            elif response["api:statuscode"] == 1605: raise exceptions.ChatFull(response)
            elif response["api:statuscode"] == 1663: raise exceptions.ChatViewOnly(response)
            else: return response

        else: return response.status_code

    def delete_message(self, chatId: str, messageId: str, asStaff: bool = False, reason: str = None):
        """
        Delete a Message from a Chat.

        **Parameters**
            - **messageId** : ID of the Message.
            - **chatId** : ID of the Chat.
            - **asStaff** : If execute as a Staff member (Leader or Curator).
            - **reason** : Reason of the action to show on the Moderation History.

        **Returns**
            - **200** (int) : **Success**

            - **104** (:meth:`InvalidRequest <amino.lib.util.exceptions.InvalidRequest>`) : Invalid Request. Please update to the latest version. If the problem continues, please contact us.

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = {
            "adminOpName": 102,
            "adminOpNote": {"content": reason},
            "timestamp": int(timestamp() * 1000)
        }

        data = json.dumps(data)
        if not asStaff: response = requests.delete(f"{self.api}/g/s/chat/thread/{chatId}/message/{messageId}", headers=headers.Headers().headers)
        else: response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/message/{messageId}/admin", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            elif response["api:statuscode"] == 106: raise exceptions.AccessDenied(response)
            else: return response

        else: return response.status_code

    def mark_as_read(self, chatId: str, messageId: str):
        """
        Mark a Message from a Chat as Read.

        **Parameters**
            - **messageId** : ID of the Message.
            - **chatId** : ID of the Chat.

        **Returns**
            - **200** (int) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "messageId": messageId,
            "timestamp": int(timestamp() * 1000)
        })
        response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/mark-as-read", headers=headers.Headers().headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def edit_chat(self, chatId: str, doNotDisturb: bool = None, pinChat: bool = None, title: str = None, icon: str = None, backgroundImage: str = None, content: str = None, announcement: str = None, coHosts: list = None, keywords: list = None, pinAnnouncement: bool = None, publishToGlobal: bool = None, canTip: bool = None, viewOnly: bool = None, canInvite: bool = None, fansOnly: bool = None):
        """
        Send a Message to a Chat.

        **Parameters**
            - **chatId** : ID of the Chat.
            - **title** : Title of the Chat.
            - **content** : Content of the Chat.
            - **icon** : Icon of the Chat.
            - **backgroundImage** : Url of the Background Image of the Chat.
            - **announcement** : Announcement of the Chat.
            - **pinAnnouncement** : If the Chat Announcement should Pinned or not.
            - **coHosts** : List of User IDS to be Co-Host.
            - **keywords** : List of Keywords of the Chat.
            - **viewOnly** : If the Chat should be on View Only or not.
            - **canTip** : If the Chat should be Tippable or not.
            - **canInvite** : If the Chat should be Invitable or not.
            - **fansOnly** : If the Chat should be Fans Only or not.
            - **publishToGlobal** : If the Chat should show on Public Chats or not.
            - **doNotDisturb** : If the Chat should Do Not Disturb or not.
            - **pinChat** : If the Chat should Pinned or not.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **1600** (:meth:`RequestedNoLongerExists <amino.lib.util.exceptions.RequestedNoLongerExists>`) : Sorry, the requested data no longer exists. Try refreshing the view.

            - **1613** (:meth:`UserNotJoined <amino.lib.util.exceptions.UserNotJoined>`) : Sorry, this user has not joined.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = {"timestamp": int(timestamp() * 1000)}

        if title: data["title"] = title
        if content: data["content"] = content
        if icon: data["icon"] = icon
        if keywords: data["keywords"] = keywords
        if announcement: data["extensions"] = {"announcement": announcement}
        if pinAnnouncement: data["extensions"] = {"pinAnnouncement": pinAnnouncement}
        if fansOnly: data["extensions"] = {"fansOnly": fansOnly}

        if publishToGlobal: data["publishToGlobal"] = 0
        if not publishToGlobal: data["publishToGlobal"] = 1

        res = []

        if doNotDisturb:
            data = json.dumps({"alertOption": 2, "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/member/{self.userId}/alert", data=data, headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if not doNotDisturb:
            data = json.dumps({"alertOption": 1, "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/member/{self.userId}/alert", data=data, headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if pinChat:
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/pin", headers=headers.Headers().headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if not pinChat:
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/unpin", headers=headers.Headers().headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if backgroundImage:
            data = json.dumps({"media": [100, backgroundImage, None], "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/member/{self.userId}/background", data=data, headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if coHosts:
            data = json.dumps({"uidList": coHosts, "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/co-host", data=data, headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if not viewOnly:
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/view-only/disable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if viewOnly:
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/view-only/enable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if not canInvite:
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/members-can-invite/disable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if canInvite:
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/members-can-invite/enable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if not canTip:
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/tipping-perm-status/disable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        if canTip:
            response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}/tipping-perm-status/enable", headers=headers.Headers(data=data).headers)
            if response.status_code != 200:
                response = json.loads(response.text)
                if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
                elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
                elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
                elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
                else: res.append(response)

            else: res.append(response.status_code)

        data = json.dumps(data)
        response = requests.post(f"{self.api}/g/s/chat/thread/{chatId}", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: res.append(exceptions.UnsupportedService(response))
            elif response["api:statuscode"] == 106: res.append(exceptions.AccessDenied(response))
            elif response["api:statuscode"] == 1600: res.append(exceptions.RequestedNoLongerExists(response))
            elif response["api:statuscode"] == 1613: res.append(exceptions.UserNotJoined(response))
            else: res.append(response)

        else: res.append(response.status_code)

        return res

    def visit(self, userId: str):
        """
        Visit an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/user-profile/{userId}?action=visit", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return response.status_code

    def follow(self, userId: [str, list]):
        """
        Follow an User or Multiple Users.

        **Parameters**
            - **userId** : ID of the User or List of IDs of the Users.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        if isinstance(userId, str):
            response = requests.post(f"{self.api}/g/s/user-profile/{userId}/member", headers=headers.Headers().headers)

        elif isinstance(userId, list):
            data = json.dumps({"targetUidList": userId, "timestamp": int(timestamp() * 1000)})
            response = requests.post(f"{self.api}/g/s/user-profile/{self.userId}/joined", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.WrongType

        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return response.status_code

    def unfollow(self, userId: str):
        """
        Unfollow an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.delete(f"{self.api}/g/s/user-profile/{userId}/member/{self.userId}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return response.status_code

    def block(self, userId: str):
        """
        Block an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.post(f"{self.api}/g/s/block/{userId}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return response.status_code

    def unblock(self, userId: str):
        """
        Unblock an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.delete(f"{self.api}/g/s/block/{userId}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            else: return response

        else: return response.status_code

    def join_community(self, comId: str, invitationId: str = None):
        """
        Join a Community.

        **Parameters**
            - **comId** : ID of the Community.
            - **invitationId** : ID of the Invitation Code.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **104** (:meth:`InvalidRequest <amino.lib.util.exceptions.InvalidRequest>`) : Invalid Request. Please update to the latest version. If the problem continues, please contact us.

            - **229** (:meth:`YouAreBanned <amino.lib.util.exceptions.YouAreBanned>`) : You are banned.

            - **801** (:meth:`CommunityNoLongerExists <amino.lib.util.exceptions.CommunityNoLongerExists>`) : This Community no longer exists.

            - **802** (:meth:`InvalidCodeOrLink <amino.lib.util.exceptions.InvalidCodeOrLink>`) : Sorry, this code or link is invalid.

            - **833** (:meth:`CommunityDeleted <amino.lib.util.exceptions.CommunityDeleted>`) : This Community has been deleted.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = {"timestamp": int(timestamp() * 1000)}
        if invitationId: data["invitationId"] = invitationId

        data = json.dumps(data)
        response = requests.post(f"{self.api}/x{comId}/s/community/join", data=data, headers=headers.Headers(data=data).headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            elif response["api:statuscode"] == 229: raise exceptions.YouAreBanned(response)
            elif response["api:statuscode"] == 801: raise exceptions.CommunityNoLongerExists(response)
            elif response["api:statuscode"] == 802: raise exceptions.InvalidCodeOrLink(response)
            elif response["api:statuscode"] == 833: raise exceptions.CommunityDeleted(response)
            else: return response

        else: return response.status_code

    def request_join_community(self, comId: str, message: str = None):
        """
        Request to join a Community.

        **Parameters**
            - **comId** : ID of the Community.
            - **message** : Message to be sent.

        **Returns**
            - **200** (int) : **Success**

            - **801** (:meth:`CommunityNoLongerExists <amino.lib.util.exceptions.CommunityNoLongerExists>`) : This Community no longer exists.

            - **833** (:meth:`CommunityDeleted <amino.lib.util.exceptions.CommunityDeleted>`) : This Community has been deleted.

            - **2001** (:meth:`AlreadyRequestedJoinCommunity <amino.lib.util.exceptions.AlreadyRequestedJoinCommunity>`) : Sorry, you have already submitted a membership request.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({"message": message, "timestamp": int(timestamp() * 1000)})
        response = requests.post(f"{self.api}/x{comId}/s/community/membership-request", data=data, headers=headers.Headers(data=data).headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 801: raise exceptions.CommunityNoLongerExists(response)
            elif response["api:statuscode"] == 833: raise exceptions.CommunityDeleted(response)
            elif response["api:statuscode"] == 2001: raise exceptions.AlreadyRequestedJoinCommunity(response)
            else: return response
        else: return response.status_code

    def leave_community(self, comId: str):
        """
        Leave a Community.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **200** (int) : **Success**

            - **230** (:meth:`UserNotMemberOfCommunity <amino.lib.util.exceptions.UserNotMemberOfCommunity>`) : You are not a member of this Community.

            - **801** (:meth:`CommunityNoLongerExists <amino.lib.util.exceptions.CommunityNoLongerExists>`) : This Community no longer exists.

            - **833** (:meth:`CommunityDeleted <amino.lib.util.exceptions.CommunityDeleted>`) : This Community has been deleted.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.post(f"{self.api}/x{comId}/s/community/leave", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 230: raise exceptions.UserNotMemberOfCommunity(response)
            elif response["api:statuscode"] == 801: raise exceptions.CommunityNoLongerExists(response)
            elif response["api:statuscode"] == 833: raise exceptions.CommunityDeleted(response)
            else: return response
        else: return response.status_code

    def flag_community(self, comId: str, reason: str, flagType: int, isGuest: bool = False):
        """
        Flag a Community.

        **Parameters**
            - **comId** : ID of the Community.
            - **reason** : Reason of the Flag.
            - **flagType** : Type of Flag.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **113** (:meth:`MessageNeeded <amino.lib.util.exceptions.MessageNeeded>`) : Be more specific, please.

            - **801** (:meth:`CommunityNoLongerExists <amino.lib.util.exceptions.CommunityNoLongerExists>`) : This Community no longer exists.

            - **833** (:meth:`CommunityDeleted <amino.lib.util.exceptions.CommunityDeleted>`) : This Community has been deleted.

            - **Other** (:meth:`ReasonNeeded <amino.lib.util.exceptions.ReasonNeeded>`, :meth:`FlagTypeNeeded <amino.lib.util.exceptions.FlagTypeNeeded>`, :meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        if reason is None: raise exceptions.ReasonNeeded
        if flagType is None: raise exceptions.FlagTypeNeeded

        data = json.dumps({
            "objectId": comId,
            "objectType": 16,
            "flagType": flagType,
            "message": reason,
            "timestamp": int(timestamp() * 1000)
        })

        if isGuest: flg = "g-flag"
        else: flg = "flag"

        response = requests.post(f"{self.api}/x{comId}/s/{flg}", data=data, headers=headers.Headers(data=data).headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 113: raise exceptions.MessageNeeded(response)
            elif response["api:statuscode"] == 801: raise exceptions.CommunityNoLongerExists(response)
            elif response["api:statuscode"] == 833: raise exceptions.CommunityDeleted(response)
            else: return response
        else: return response.status_code

    def edit_profile(self, nickname: str = None, content: str = None, icon: str = None, backgroundColor: str = None, backgroundImage: str = None):
        """
        Edit account's Profile.

        **Parameters**
            - **nickname** : Nickname of the Profile.
            - **content** : Biography of the Profile.
            - **icon** : Url of the Icon of the Profile.
            - **backgroundImage** : Url of the Background Picture of the Profile.
            - **backgroundColor** : Hexadecimal Background Color of the Profile.

        **Returns**
            - **200** (int) : **Success**

            - **99001** (:meth:`InvalidName <amino.lib.util.exceptions.InvalidName>`) : Sorry, the name is invalid.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = {
            "address": None,
            "latitude": 0,
            "longitude": 0,
            "mediaList": None,
            "eventSource": "UserProfileView",
            "timestamp": int(timestamp() * 1000)
        }

        if nickname: data["nickname"] = nickname
        if icon: data["icon"] = icon
        if content: data["content"] = content
        if backgroundColor: data["extensions"] = {"style": {"backgroundColor": backgroundColor}}
        if backgroundImage: data["extensions"] = {"style": {"backgroundMediaList": [[100, backgroundImage, None, None, None]]}}

        data = json.dumps(data)
        response = requests.post(f"{self.api}/g/s/user-profile/{self.userId}", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 99001: raise exceptions.InvalidName(response)
            else: return response
        else: return response.status_code

    def set_privacy_status(self, isAnonymous: bool = False, getNotifications: bool = False):
        """
        Edit account's Privacy Status.

        **Parameters**
            - **isAnonymous** : If visibility should be Anonymous or not.
            - **getNotifications** : If account should get new Visitors Notifications.

        **Returns**
            - **200** (int) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """

        data = {"timestamp": int(timestamp() * 1000)}

        if not isAnonymous: data["privacyMode"] = 1
        if isAnonymous: data["privacyMode"] = 2
        if not getNotifications: data["notificationStatus"] = 2
        if getNotifications: data["privacyMode"] = 1

        data = json.dumps(data)
        response = requests.post(f"{self.api}/g/s/account/visit-settings", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def set_amino_id(self, aminoId: str):
        """
        Edit account's Amino ID.

        **Parameters**
            - **aminoId** : Amino ID of the Account.

        **Returns**
            - **200** (int) : **Success**

            - **6001** (:meth:`AminoIDAlreadyChanged <amino.lib.util.exceptions.AminoIDAlreadyChanged>`) : Amino ID cannot be changed after you set it.

            - **6002** (:meth:`InvalidAminoID <amino.lib.util.exceptions.InvalidAminoID>`) : Invalid Amino ID

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({"aminoId": aminoId, "timestamp": int(timestamp() * 1000)})
        response = requests.post(f"{self.api}/g/s/account/change-amino-id", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 6001: raise exceptions.AminoIDAlreadyChanged(response)
            elif response["api:statuscode"] == 6002: raise exceptions.InvalidAminoID(response)
            else: return response
        else: return response.status_code

    def get_linked_communities(self, userId: str):
        """
        Get a List of Linked Communities of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **200** (:meth:`Community List <amino.lib.util.objects.communityList>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/user-profile/{userId}/linked-community", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 106: raise exceptions.AccessDenied(response)
            else: return response
        else: return objects.communityList(json.loads(response.text)["linkedCommunityList"]).communityList

    def get_unlinked_communities(self, userId: str):
        """
        Get a List of Unlinked Communities of an User.

        **Parameters**
            - **userId** : ID of the User.

        **Returns**
            - **200** (:meth:`Community List <amino.lib.util.objects.communityList>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/user-profile/{userId}/linked-community", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 106: raise exceptions.AccessDenied(response)
            else: return response
        else: return objects.communityList(json.loads(response.text)["unlinkedCommunityList"]).communityList

    def reorder_linked_communities(self, comIds: list):
        """
        Reorder List of Linked Communities.

        **Parameters**
            - **comIds** : IDS of the Communities.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({"ndcIds": comIds, "timestamp": int(timestamp() * 1000)})
        response = requests.post(f"{self.api}/g/s/user-profile/{self.userId}/linked-community/reorder", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            else: return response
        else: return response.status_code

    def add_linked_community(self, comId: str):
        """
        Add a Linked Community on your profile.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **200** (int) : **Success**

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.post(f"{self.api}/g/s/user-profile/{self.userId}/linked-community/{comId}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 106: raise exceptions.AccessDenied(response)
            else: return response
        else: return response.status_code

    def remove_linked_community(self, comId: str):
        """
        Remove a Linked Community on your profile.

        **Parameters**
            - **comId** : ID of the Community.

        **Returns**
            - **200** (int) : **Success**

            - **104** (:meth:`InvalidRequest <amino.lib.util.exceptions.InvalidRequest>`) : Invalid Request. Please update to the latest version. If the problem continues, please contact us.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.delete(f"{self.api}/g/s/user-profile/{self.userId}/linked-community/{comId}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            else: return response
        else: return response.status_code

    def comment(self, message: str, userId: str = None, blogId: str = None, wikiId: str = None, replyTo: str = None):
        """
        Comment on a User's Wall, Blog or Wiki.

        **Parameters**
            - **message** : Message to be sent.
            - **userId** : ID of the User. (for Walls)
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)
            - **replyTo** : ID of the Comment to Reply to.

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **104** (:meth:`InvalidRequest <amino.lib.util.exceptions.InvalidRequest>`) : Invalid Request. Please update to the latest version. If the problem continues, please contact us.

            - **225** (:meth:`UserUnavailable <amino.lib.util.exceptions.UserUnavailable>`) : This user is unavailable.

            - **702** (:meth:`WallCommentingDisabled <amino.lib.util.exceptions.WallCommentingDisabled>`) : This member has disabled commenting on their wall.

            - **Other** (:meth:`MessageNeeded <amino.lib.util.exceptions.MessageNeeded>`, :meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        if message is None: raise exceptions.MessageNeeded

        data = {
            "content": message,
            "stickerId": None,
            "type": 0,
            "timestamp": int(timestamp() * 1000)
        }

        if replyTo: data["respondTo"] = replyTo

        if userId:
            data["eventSource"] = "UserProfileView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/g/s/user-profile/{userId}/g-comment", headers=headers.Headers(data=data).headers, data=data)

        elif blogId:
            data["eventSource"] = "PostDetailView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/g/s/blog/{blogId}/g-comment", headers=headers.Headers(data=data).headers, data=data)

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/g/s/item/{wikiId}/g-comment", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            elif response["api:statuscode"] == 225: raise exceptions.UserUnavailable(response)
            elif response["api:statuscode"] == 702: raise exceptions.WallCommentingDisabled(response)
            else: return response
        else: return response.status_code

    def delete_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        """
        Delete a Comment on a User's Wall, Blog or Wiki.

        **Parameters**
            - **commentId** : ID of the Comment.
            - **userId** : ID of the User. (for Walls)
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **104** (:meth:`InvalidRequest <amino.lib.util.exceptions.InvalidRequest>`) : Invalid Request. Please update to the latest version. If the problem continues, please contact us.

            - **106** (:meth:`AccessDenied <amino.lib.util.exceptions.AccessDenied>`) : Access denied.

            - **700** (:meth:`RequestedNoLongerExists <amino.lib.util.exceptions.RequestedNoLongerExists>`) : Sorry, the requested data no longer exists. Try refreshing the view.

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        if userId: response = requests.delete(f"{self.api}/g/s/user-profile/{userId}/g-comment/{commentId}", headers=headers.Headers().headers)
        elif blogId: response = requests.delete(f"{self.api}/g/s/blog/{blogId}/g-comment/{commentId}", headers=headers.Headers().headers)
        elif wikiId: response = requests.delete(f"{self.api}/g/s/item/{wikiId}/g-comment/{commentId}", headers=headers.Headers().headers)
        else: raise exceptions.SpecifyType

        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            elif response["api:statuscode"] == 106: raise exceptions.AccessDenied(response)
            elif response["api:statuscode"] == 700: raise exceptions.RequestedNoLongerExists(response)
            else: return response
        else: return response.status_code

    def like_blog(self, blogId: [str, list] = None, wikiId: str = None):
        """
        Like a Blog, Multiple Blogs or a Wiki.

        **Parameters**
            - **blogId** : ID of the Blog or List of IDs of the Blogs. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **104** (:meth:`InvalidRequest <amino.lib.util.exceptions.InvalidRequest>`) : Invalid Request. Please update to the latest version. If the problem continues, please contact us.

            - **700** (:meth:`RequestedNoLongerExists <amino.lib.util.exceptions.RequestedNoLongerExists>`) : Sorry, the requested data no longer exists. Try refreshing the view.

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        data = {
            "value": 4,
            "timestamp": int(timestamp() * 1000)
        }

        if blogId:
            if isinstance(blogId, str):
                data["eventSource"] = "UserProfileView"
                data = json.dumps(data)
                response = requests.post(f"{self.api}/g/s/blog/{blogId}/g-vote?cv=1.2", headers=headers.Headers(data=data).headers, data=data)

            elif isinstance(blogId, list):
                data["targetIdList"] = blogId
                data = json.dumps(data)
                response = requests.post(f"{self.api}/g/s/feed/g-vote", headers=headers.Headers(data=data).headers, data=data)

            else: raise exceptions.WrongType

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/g/s/item/{wikiId}/g-vote?cv=1.2", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType

        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            elif response["api:statuscode"] == 700: raise exceptions.RequestedNoLongerExists(response)
            else: return response
        else: return response.status_code

    def unlike_blog(self, blogId: str = None, wikiId: str = None):
        """
        Remove a like from a Blog or Wiki.

        **Parameters**
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **104** (:meth:`InvalidRequest <amino.lib.util.exceptions.InvalidRequest>`) : Invalid Request. Please update to the latest version. If the problem continues, please contact us.

            - **700** (:meth:`RequestedNoLongerExists <amino.lib.util.exceptions.RequestedNoLongerExists>`) : Sorry, the requested data no longer exists. Try refreshing the view.

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        if blogId: response = requests.delete(f"{self.api}/g/s/blog/{blogId}/g-vote?eventSource=UserProfileView", headers=headers.Headers().headers)
        elif wikiId: response = requests.delete(f"{self.api}/g/s/item/{wikiId}/g-vote?eventSource=PostDetailView", headers=headers.Headers().headers)
        else: raise exceptions.SpecifyType

        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            elif response["api:statuscode"] == 700: raise exceptions.RequestedNoLongerExists(response)
            else: return response
        else: return response.status_code

    def like_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        """
        Like a Comment on a User's Wall, Blog or Wiki.

        **Parameters**
            - **commentId** : ID of the Comment.
            - **userId** : ID of the User. (for Walls)
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **104** (:meth:`InvalidRequest <amino.lib.util.exceptions.InvalidRequest>`) : Invalid Request. Please update to the latest version. If the problem continues, please contact us.

            - **700** (:meth:`RequestedNoLongerExists <amino.lib.util.exceptions.RequestedNoLongerExists>`) : Sorry, the requested data no longer exists. Try refreshing the view.

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        data = {
            "value": 4,
            "timestamp": int(timestamp() * 1000)
        }

        if userId:
            data["eventSource"] = "UserProfileView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/g/s/user-profile/{userId}/comment/{commentId}/g-vote?cv=1.2&value=1", headers=headers.Headers(data=data).headers, data=data)

        elif blogId:
            data["eventSource"] = "PostDetailView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/g/s/blog/{blogId}/comment/{commentId}/g-vote?cv=1.2&value=1", headers=headers.Headers(data=data).headers, data=data)

        elif wikiId:
            data["eventSource"] = "PostDetailView"
            data = json.dumps(data)
            response = requests.post(f"{self.api}/g/s/item/{wikiId}/comment/{commentId}/g-vote?cv=1.2&value=1", headers=headers.Headers(data=data).headers, data=data)

        else: raise exceptions.SpecifyType

        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            elif response["api:statuscode"] == 700: raise exceptions.RequestedNoLongerExists(response)
            else: return response
        else: return response.status_code

    def unlike_comment(self, commentId: str, userId: str = None, blogId: str = None, wikiId: str = None):
        """
        Remove a like from a Comment on a User's Wall, Blog or Wiki.

        **Parameters**
            - **commentId** : ID of the Comment.
            - **userId** : ID of the User. (for Walls)
            - **blogId** : ID of the Blog. (for Blogs)
            - **wikiId** : ID of the Wiki. (for Wikis)

        **Returns**
            - **200** (int) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **104** (:meth:`InvalidRequest <amino.lib.util.exceptions.InvalidRequest>`) : Invalid Request. Please update to the latest version. If the problem continues, please contact us.

            - **700** (:meth:`RequestedNoLongerExists <amino.lib.util.exceptions.RequestedNoLongerExists>`) : Sorry, the requested data no longer exists. Try refreshing the view.

            - **Other** (:meth:`SpecifyType <amino.lib.util.exceptions.SpecifyType>`, :meth:`JSON Object <JSONObject>`)
        """
        if userId: response = requests.delete(f"{self.api}/g/s/user-profile/{userId}/comment/{commentId}/g-vote?eventSource=UserProfileView", headers=headers.Headers().headers)
        elif blogId: response = requests.delete(f"{self.api}/g/s/blog/{blogId}/comment/{commentId}/g-vote?eventSource=PostDetailView", headers=headers.Headers().headers)
        elif wikiId: response = requests.delete(f"{self.api}/g/s/item/{wikiId}/comment/{commentId}/g-vote?eventSource=PostDetailView", headers=headers.Headers().headers)
        else: raise exceptions.SpecifyType

        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 104: raise exceptions.InvalidRequest(response)
            elif response["api:statuscode"] == 700: raise exceptions.RequestedNoLongerExists(response)
            else: return response
        else: return response.status_code

    def get_membership_info(self):
        """
        Get Information about your Amino+ Membership.

        **Parameters**
            - No parameters required.

        **Returns**
            - **200** (:meth:`Membership Object <amino.lib.util.objects.membership>`) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/membership?force=true", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return objects.membership(json.loads(response.text)).membership

    def get_ta_announcements(self, language: str = "en", start: int = 0, size: int = 25):
        """
        Get the list of Team Amino's Announcement Blogs.

        **Parameters**
            - **language** : Language of the Blogs.
                - ``en``, ``es``, ``pt``, ``ar``, ``ru``, ``fr``, ``de``
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`Blogs List <amino.lib.util.objects.blogList>`) : **Success**

            - **Other** (:meth:`UnsupportedLanguage <amino.lib.util.exceptions.UnsupportedLanguage>`, :meth:`JSON Object <JSONObject>`)
        """
        if language not in self.get_supported_languages(): raise exceptions.UnsupportedLanguage
        response = requests.get(f"{self.api}/g/s/announcement?language={language}&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return objects.blogList(json.loads(response.text)["blogList"]).blogList

    def get_wallet_info(self):
        """
        Get Information about the account's Wallet.

        **Parameters**
            - No parameters required.

        **Returns**
            - **200** (:meth:`Wallet Object <amino.lib.util.objects.walletInfo>`) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/wallet", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return objects.walletInfo(json.loads(response.text)["wallet"]).walletInfo

    def get_wallet_history(self, start: int = 0, size: int = 25):
        """
        Get the Wallet's History Information.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`Wallet Object <amino.lib.util.objects.walletInfo>`) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/wallet/coin/history?start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return objects.walletHistory(json.loads(response.text)["coinHistoryList"]).walletHistory

    def get_from_deviceid(self, deviceId: str):
        """
        Get the User ID from an Device ID.

        **Parameters**
            - **deviceID** : ID of the Device.

        **Returns**
            - **200** (:meth:`User ID <amino.lib.util.objects.userProfile.userId>`) : **Success**

            - **218** (:meth:`InvalidDevice <amino.lib.util.exceptions.InvalidDevice>`) : Error! Your device is currently not supported, or the app is out of date. Please update to the latest version.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/auid?deviceId={deviceId}")
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 218: raise exceptions.InvalidDevice(response)
            else: return response
        else: return json.loads(response.text)["auid"]

    def get_from_code(self, code: str):
        """
        Get the Object Information from the Amino URL Code.

        **Parameters**
            - **code** : Code from the Amino URL.
                - ``http://aminoapps.com/p/EXAMPLE``, the ``code`` is 'EXAMPLE'.

        **Returns**
            - **200** (:meth:`From Code Object <amino.lib.util.objects.fromCode>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **107** (:meth:`UnexistentData <amino.lib.util.exceptions.UnexistentData>`) : The requested data does not exist.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/link-resolution?q={code}", headers=headers.Headers().headers)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 107: raise exceptions.UnexistentData(response)
            else: return response

        else: return objects.fromCode(json.loads(response.text)["linkInfoV2"]).fromCode

    def get_from_id(self, objectId: str, objectType: int, comId: str = None):
        """
        Get the Object Information from the Object ID and Type.

        **Parameters**
            - **objectID** : ID of the Object. User ID, Blog ID, etc.
            - **objectType** : Type of the Object.
            - *comId* : ID of the Community. Use if the Object is in a Community.

        **Returns**
            - **200** (:meth:`From Code Object <amino.lib.util.objects.fromCode>`) : **Success**

            - **100** (:meth:`UnsupportedService <amino.lib.util.exceptions.UnsupportedService>`) : Unsupported service. Your client may be out of date. Please update it to the latest version.

            - **107** (:meth:`UnexistentData <amino.lib.util.exceptions.UnexistentData>`) : The requested data does not exist.

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        data = json.dumps({
            "objectId": objectId,
            "targetCode": 1,
            "objectType": objectType,
            "timestamp": int(timestamp() * 1000)
        })

        if comId: response = requests.post(f"{self.api}/g/s-x{comId}/link-resolution", headers=headers.Headers(data=data).headers, data=data)
        else: response = requests.post(f"{self.api}/g/s/link-resolution", headers=headers.Headers(data=data).headers, data=data)
        if response.status_code != 200:
            response = json.loads(response.text)
            if response["api:statuscode"] == 100: raise exceptions.UnsupportedService(response)
            elif response["api:statuscode"] == 107: raise exceptions.UnexistentData(response)
            else: return response

        else: return objects.fromCode(json.loads(response.text)["linkInfoV2"]).fromCode

    def get_supported_languages(self):
        """
        Get the List of Supported Languages by Amino.

        **Parameters**
            - No parameters required.

        **Returns**
            - **200** (:meth:`List <List>`) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/community-collection/supported-languages?start=0&size=100", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return json.loads(response.text)["supportedLanguages"]

    def claim_new_user_coupon(self):
        """
        Claim the New User Coupon available when a new account is created.

        **Parameters**
            - No parameters required.

        **Returns**
            - **200** (int) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.post(f"{self.api}/g/s/coupon/new-user-coupon/claim", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return response.status_code

    def get_subscriptions(self, start: int = 0, size: int = 25):
        """
        Get Information about the account's Subscriptions.

        **Parameters**
            - *start* : Where to start the list.
            - *size* : Size of the list.

        **Returns**
            - **200** (:meth:`JSON List <JSON List>`) : **Success**

            - **Other** (:meth:`JSON Object <JSONObject>`)
        """
        response = requests.get(f"{self.api}/g/s/store/subscription?objectType=122&start={start}&size={size}", headers=headers.Headers().headers)
        if response.status_code != 200: return json.loads(response.text)
        else: return json.loads(response.text)["storeSubscriptionItemList"]

    @staticmethod
    def punishmentTypes():
        punishments = ["0 - Bullying",
                       "1 - Inappropriate Content"
                       "2 - Spam",
                       "3 - Art Theft",
                       "4 - Off-Topic",
                       "5 - Trolling",
                       "100 - Sexually Explicit",
                       "101 - Extreme Violence",
                       "102 - Inappropriate Requests",
                       "106 - Violence, Graphic Content or Dangerous Activity",
                       "107 - Hate Speech & Bigotry",
                       "108 - Self-Injury & Suicide",
                       "109 - Harassment & Trolling",
                       "110 - Nudity & Pornography",
                       "104, 105, 200 - Others"]

        return punishments
