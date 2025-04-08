#!/usr/bin/env python3
import sys
import uuid
import os
from poster_api_tester import PosterAPITester

# global counter for total tests passed
tests_passed = 0

"""
there are 2 modes, get and set mode

get mode
	- allows us to talk to endpoints where data is not updated to changed
set mode
	- allows us to test endpoints where data is manipulated and uploaded using post/delete/ ...
"""

def check(response, test_name, expected_key=None):
    """
    assert that the response did not return error and optionally that it contains the
    expected key at the top level

    if successful
    	tests_passed += 1
    """
    global tests_passed
    assert "error" not in response, f"{test_name} FAILED: Response contains error: {response}"
    if expected_key:
        assert expected_key in response, f"{test_name} FAILED: Expected key '{expected_key}' not found in {response}"
    tests_passed += 1
    print(f"{test_name}: PASS")

# the main function for the get mode, we pass in the instance of our poster-api-tester
def test_get_mode(tester):
    print("\n========== GET MODE ==========")

    # login as test2, we know this account exists
    resp = tester.login_user("test2", "Hello@123")
    check(resp, "login (get mode)", expected_key="token")
    
    # 2. get profile for test 2 (response is { "message": "...", "user": { ... } } )
    profile = tester.get_profile("test2")

    assert "user" in profile, f"get profile (get mode) FAILED: expected key 'user' not found in {profile}"
    user_obj = profile["user"]
    assert "username" in user_obj, f"get profile (get mode) FAILED: expected key 'username' not found in user object {user_obj}"

    global tests_passed
    tests_passed += 1
    print("get profile (get mode): PASS")
    
    # 3. get first page of user feed (page 1)
    feed = tester.get_feed(page=1)
    check(feed, "get feed (get mode)")
    
    # 4. get notification feed (page 1)
    not_feed = tester.get_notification_feed(page_number=1)
    check(not_feed, "get notification feed (get mode)")
    
    # 5. get conversations
    convos = tester.get_conversations()
    check(convos, "get conversations (get mode)")
    
    # 6. get following list
    test2_id = user_obj.get("id", "test2")
    following = tester.get_following(test2_id)
    check(following, "get following (get mode)")
    
    # 7. get followers list
    followers = tester.get_followers(test2_id)
    check(followers, "get followers (get mode)")
    
    # 8. search posts with query
    search_result = tester.search_posts("litterally anything")
    check(search_result, "Search Posts (get mode)")
    
    # 9. get reports (admin endpoint)
    # TODO: test accounts should be promoted to admin if not already
    reports = tester.get_reports(page=1)
    # check(reports, "Get Reports (get mode)")

def test_set_mode(tester):
    print("\n========== SET MODE ==========")
    global tests_passed

    # 1. register new user with unique username and email
    unique_suffix = str(uuid.uuid4())[:8]
    new_username = f"testuser_{unique_suffix}"
    new_email = f"{new_username}@example.com"
    new_password = "Hello@123"

    # register response
    reg = tester.register_user(new_username, new_email, new_password)

    # check that user exists
    check(reg, "Register New User (set mode)", expected_key="user")
    user_obj = reg["user"]
    # check user.id exists too
    assert "id" in user_obj, f"register new user (set mode) FAILED: expected key 'id' in user object {user_obj}"
    tests_passed += 1

    print("register new user (set mode) nested id check: PASS")
    
    # 2. login as newly registered user
    login_new = tester.login_user(new_username, new_password)
    check(login_new, "login new user (set mode)", expected_key="token")
    
    # 3. update user info
    updated_username = f"{new_username}_updated"
    updated_email = f"{new_username}_updated@example.com"
    update = tester.update_user_info(updated_email, updated_username)
    check(update, "update info (set mode)", expected_key="token")
    
    # 4. upload profile image with temp file
    temp_img = "temp_profile.png"
    upload_profile = tester.upload_profile_image(temp_img)
    check(upload_profile, "upload profile image (set mode)")
    
    # 5. create post
    post_title = f"Test Post {uuid.uuid4()}"
    post_content = "test post tester on poster on test poster python tester post test post"
    created_post = tester.create_post(post_title, post_content, images=["http://nothing.com/no_image.jpg"]) # TODO
    check(created_post, "create post (set mode)", expected_key="postId")
    post_id = created_post.get("postId")
    
    # 6. add comment to post
    comment_content = "comment test on comment poster social comment post test python yes man"
    comment = tester.add_comment_to_post(post_id, comment_content)
    check(comment, "add comment (set mode)", expected_key="commentId")
    comment_id = comment.get("commentId")
    
    # 7. like comment
    liked = tester.like_comment(comment_id)
    check(liked, "like comment (set mode)")
    
    # 8. delete comment
    del_comment = tester.delete_comment(comment_id)
    check(del_comment, "delete comment (set mode)")
    
    # 9. delete post
    del_post = tester.delete_post(post_id)
    check(del_post, "delete post (set mode)")
    
    # no notif testing for now
    # TODO

#    # 10. create a test notification
#    notification = tester.test_create_notification("info", updated_username, "test notif message")
#    check(notification, "", expected_key="")
#    notification_id = notification.get("notifId") # broke
    
#    # 11. get the notification
#    notif = tester.get_notification(notification_id)
#    check(notif, "get notification (set mode)")
    
#    # 12. mark notif as read
#    read_notif = tester.read_notification(notification_id)
#    check(read_notif, "read notification (set mode)")
    
#    # 13. delete notif
#    del_notif = tester.delete_notification(notification_id)
#    check(del_notif, "Delete Notification (set mode)")
    
    # 14. follow user, (test2 userId here)
    follow = tester.follow_user("c68f1430-35ef-4ebf-a56e-b9d534492f24") # userId for test2 
    check(follow, "follow user (set mode)")
    
    # 15. start convo with test2
    convo = tester.start_conversation(["c68f1430-35ef-4ebf-a56e-b9d534492f24"]) # again userId for test2
    check(convo, "start convo (set mode)", expected_key="conversationId")
    convo_id = convo.get("conversationId")
    
    # 16. send message in convo
    msg = tester.send_message(convo_id, "python test message yup")
    check(msg, "send message (set mode)")
    
    # 17. retrieve message thread
    thread = tester.get_message_thread(convo_id)
    check(thread, "get message thread (set mode)")
    
    # 18. create post to report
    report_post = tester.create_post(f"repotrt test post {uuid.uuid4()}", "post created for reporting")
    check(report_post, "create post for report (set mode)", expected_key="postId")
    report_post_id = report_post.get("postId")
    
    # 19. create a report on the post
    rep_create = tester.report_create("post", report_post_id, "some test report")
    check(rep_create, "repotr create (set mode)", expected_key="reportId")
    report_id = rep_create.get("reportId")
    
    # TODO
    # 20. get reports again
    rep_get = tester.get_reports(page=1)
    # check(rep_get, "")
    
    # 21. process report
    rep_process = tester.process_report(report_id, "dismiss")
    # check(rep_process, "")
    
    # 22. cleanup, delete "reported" post
    del_report_post = tester.delete_post(report_post_id)
    check(del_report_post, "delete reported post (set mode)")
    
    # 23. upload general image
    temp_img_general = "temp_profile.png"
    upload_gen_img = tester.upload_general_image(temp_img_general)
    check(upload_gen_img, "upload general image (set mode)")
    
    # 24. delete registered account
    updated_profile = tester.get_profile(updated_username)

    # some assert
    assert "user" in updated_profile, f"get updated profile (set mode) FAILED: expected key 'user' not found in {updated_profile}"
    user_obj = updated_profile["user"]
    assert "id" in user_obj, f"get updated profile (set mode) FAILED: expected key 'id' not found in user object {user_obj}"
    tests_passed += 1

    print("get updated profile (set mode): PASS")
    user_id = user_obj.get("id")
    del_account = tester.delete_account(user_id, updated_username, new_password)
    check(del_account, "delete account (new user - set mode)")

def main():
    if len(sys.argv) < 2:
    	# some help
        print("Usage: python test_all_endpoints.py [get | set | get_set]")
        sys.exit(1)
    
    # mode is first arg (well second because arg1 is the proc name)
    mode = sys.argv[1].lower()
    tester = PosterAPITester(base_url="https://api.poster-social.com")
    # for local
    # tester = PosterAPITester(base_url="http://localhost:3000")
    
    try:
        if mode == "get":
            test_get_mode(tester)
        elif mode == "set":
            test_set_mode(tester)
        else:
            print("invalid mode. choose from: get or set")
            sys.exit(1)
    except AssertionError as e:
        print(f"\nTESTS FAILED after {tests_passed} tests")
        print(e)
        sys.exit(1)
        
    print(f"\nALL TESTS PASSED: {tests_passed} tests completed successfully")

if __name__ == "__main__":
    main()