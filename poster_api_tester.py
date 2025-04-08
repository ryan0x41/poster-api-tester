#!/usr/bin/env python3
import requests
import os

class PosterAPITester:
    def __init__(self, base_url="https://api.poster-social.com"):
        self.base_url = base_url
        self.session = requests.Session()

    def register_user(self, username, email, password):
        """
        register new user
        """
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        try:
            response = self.session.post(f"{self.base_url}/user/register", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def login_user(self, identifier, password):
        """
        login using username or email
        """
        data = {
            "usernameOrEmail": identifier,
            "password": password
        }
        try:
            response = self.session.post(f"{self.base_url}/user/login", json=data)
            response.raise_for_status()
            result = response.json()
            token = result.get("token")
            if token:
                self.session.headers.update({"Authorization": f"Bearer {token}"})
                self.session.cookies.set("authToken", token)
                print("authToken stored in header")
            return result
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_profile(self, username):
        """
        retrieve a user by username
        """
        try:
            response = self.session.get(f"{self.base_url}/user/profile/{username}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def update_user_info(self, new_email, new_username):
        """
        update user email and or username
        """
        data = {
            "newEmail": new_email,
            "newUsername": new_username
        }
        try:
            response = self.session.post(f"{self.base_url}/user/update-info", json=data)
            response.raise_for_status()
            result = response.json()
            if "token" in result:
                self.session.cookies.set("authToken", result["token"])
            return result
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def delete_account(self, user_id, username_or_email, password):
        """
        delete user by providing credentials
        """
        data = {
            "userId": user_id,
            "usernameOrEmail": username_or_email,
            "password": password
        }
        try:
            response = self.session.post(f"{self.base_url}/user/delete-account", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def upload_profile_image(self, file_path):
        """
        upload profile image from local file
        """
        if not os.path.isfile(file_path):
            return {"error": "file does not exist"}
        try:
            with open(file_path, "rb") as img_file:
                files = {"image": img_file}
                response = self.session.post(f"{self.base_url}/user/profile-image", files=files)
                response.raise_for_status()
                return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def create_post(self, title, content, images=None):
        """
        create post with optional list of image urls
        """
        if images is None:
            images = []
        data = {
            "title": title,
            "content": content,
            "images": images
        }
        try:
            response = self.session.post(f"{self.base_url}/post/create", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def test_create_notification(self, notification_type, recipient_id, notification_message):
        """
        create test notification
        """
        data = {
            "notificationType": notification_type,
            "recipientId": recipient_id,
            "notificationMessage": notification_message
        }
        try:
            response = self.session.post(f"{self.base_url}/notification/test/create", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_notification(self, notification_id):
        """
        retrieve a specific notification given a notificationId
        """
        try:
            response = self.session.get(f"{self.base_url}/notification/{notification_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_notification_feed(self, page_number):
        """
        retrieve paginated feed of notifications
        """
        try:
            response = self.session.get(f"{self.base_url}/notification/all/{page_number}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def read_notification(self, notification_id):
        """
        mark notif as read
        """
        try:
            response = self.session.patch(f"{self.base_url}/notification/read/{notification_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def delete_notification(self, notification_id):
        """
        delete a notification
        """
        try:
            response = self.session.patch(f"{self.base_url}/notification/delete/{notification_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_posts_by_user(self, user_id):
        """
        retrieve all posts given userId
        """
        try:
            response = self.session.get(f"{self.base_url}/post/author/{user_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_post_by_id(self, post_id):
        """
        retrieve post by specific id
        """
        try:
            response = self.session.get(f"{self.base_url}/post/{post_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def search_posts(self, search_query):
        """
        search posts matching a query
        """
        data = {"searchQuery": search_query}
        try:
            response = self.session.post(f"{self.base_url}/post/search", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def add_comment_to_post(self, post_id, content):
        """
        add comment given a postId
        """
        data = {"postId": post_id, "content": content}
        try:
            response = self.session.post(f"{self.base_url}/comment/create", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def delete_comment(self, comment_id):
        """
        delete a comment given a commentId
        """
        try:
            response = self.session.delete(f"{self.base_url}/comment/delete/{comment_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_comment_by_id(self, comment_id):
        """
        retrieve a comment given commentId
        """
        try:
            response = self.session.get(f"{self.base_url}/comment/{comment_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_comments_by_post_id(self, post_id):
        """
        retrieve all comments given postId
        """
        try:
            response = self.session.get(f"{self.base_url}/comment/post/{post_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def like_comment(self, comment_id):
        """
        toggle like/unlike given commentId
        """
        data = {"commentId": comment_id}
        try:
            response = self.session.post(f"{self.base_url}/comment/like", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def delete_post(self, post_id):
        """
        delete a post given postId
        """
        try:
            response = self.session.delete(f"{self.base_url}/post/delete/{post_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def upload_general_image(self, file_path):
        """
        upload general purpose image (posts for now)
        """
        if not os.path.isfile(file_path):
            return {"error": "file does not exist"}
        try:
            with open(file_path, "rb") as img_file:
                files = {"image": img_file}
                response = self.session.post(f"{self.base_url}/upload/image", files=files)
                response.raise_for_status()
                return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def follow_user(self, user_id_to_follow):
        """
        toggle follow/unfollow given a userId
        """
        data = {"userIdToFollow": user_id_to_follow}
        try:
            response = self.session.post(f"{self.base_url}/user/follow", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_feed(self, page):
        """
        retrieve user feed given a page number
        TODO: this is silly i should not have to provide a page number
        """
        try:
            response = self.session.get(f"{self.base_url}/user/feed/{page}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_following(self, user_id):
        """
        retrieve list of users the given userId is following
        """
        try:
            response = self.session.get(f"{self.base_url}/user/following/{user_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_followers(self, user_id):
        """
        retrieve list of followers given a userId
        """
        try:
            response = self.session.get(f"{self.base_url}/user/followers/{user_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def report_create(self, content_type, id_to_report, user_message):
        """
        report post/comment given
            - idToReport (postId / commentId)
            - content type (post / comment)
            - userMessage ("uhh i dont like this post")
        """
        data = {
            "type": content_type,
            "idToReport": id_to_report,
            "userMessage": user_message
        }
        try:
            response = self.session.post(f"{self.base_url}/report/create", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_reports(self, page):
        """
        retrieve all reports (only works if user isAdmin)
        """
        try:
            response = self.session.get(f"{self.base_url}/report/all/{page}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def process_report(self, report_id, action):
        """
        process a report given an action and a reportId
        - actions
            - dismiss, ignore/delete report
            - ban, bans the user using userId associated with report that was created
            - warn, increases user warning count += 1
            - delete, deletes the content (idToReport)
        """
        data = {
            "reportId": report_id,
            "action": action
        }
        try:
            response = self.session.post(f"{self.base_url}/report/process", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def start_conversation(self, participants):
        """
        start a conversation with a list of participants [userId, userId, ...]
        """
        data = {"participants": participants}
        try:
            response = self.session.post(f"{self.base_url}/conversation/create", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def send_message(self, conversation_id, content):
        """
        send a message given a conversationId and some content
        """
        data = {
            "conversationId": conversation_id,
            "content": content
        }
        try:
            response = self.session.post(f"{self.base_url}/message/send", json=data)
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_conversations(self):
        """
        retrieve all conversations for the logged in user
        """
        try:
            response = self.session.get(f"{self.base_url}/conversation/all")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}

    def get_message_thread(self, conversation_id):
        """
        retrieve message thread given conversationId
        """
        try:
            response = self.session.get(f"{self.base_url}/message/thread/{conversation_id}")
            response.raise_for_status()
            return response.json()
        except Exception as err:
            return {"error": str(err), "response": response.text if response is not None else ""}
