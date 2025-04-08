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
        assert expected_key in response, f"{test_name} FAILED: expected key '{expected_key}' not found in {response}"
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

def test_equivalence_partitioning(tester):
    global tests_passed
    print("\n========== EQUIVALENCE PARTITIONING (EP) ==========")

    # EP1: valid login
    resp = tester.login_user("test2", "Hello@123")
    check(resp, "EP1: valid login", expected_key="token")

    # EP2: invalid username, valid password
    resp = tester.login_user("test3", "Hello@123")
    assert "error" in resp, f"EP2: expected login to fail with invalid username, got {resp}"
    print("EP2: invalid username login: PASS")
    tests_passed +=1

    # EP3: valid username, invalid password
    resp = tester.login_user("test2", "Hello@234")
    assert "error" in resp, f"EP3: expected login to fail with invalid password, got {resp}"
    print("EP3: invalid password login: PASS")
    tests_passed +=1

    # EP4: valid registration
    suffix = str(uuid.uuid4())[:8]
    username = f"epuser_{suffix}"
    email = f"{username}@example.com"
    password = "Hello@123"
    reg = tester.register_user(username, email, password)
    check(reg, "EP4: valid registration", expected_key="user")

    # EP5: registration with invalid email
    reg = tester.register_user(f"ep2_{suffix}", "bademail", password)
    assert "error" in reg, f"EP5: expected registration to fail with invalid email, got {reg}"
    print("EP5: invalid email registration: PASS")
    tests_passed +=1

    # EP6: registration with invalid password
    reg = tester.register_user(f"ep3_{suffix}", f"ep3_{suffix}@example.com", "weakpass")
    assert "error" in reg, f"EP6: expected registration to fail with invalid password, got {reg}"
    print("EP6: invalid password registration: PASS")
    tests_passed +=1

    # EP7: registration with invalid username
    reg = tester.register_user("A!", f"a_{suffix}@example.com", password)
    assert "error" in reg, f"EP7: expected registration to fail with invalid username, got {reg}"
    print("EP7: invalid username registration: PASS")
    tests_passed +=1

def test_boundary_value_analysis(tester):
    global tests_passed
    print("\n========== BOUNDARY VALUE ANALYSIS (BVA) ==========")

    suffix = str(uuid.uuid4())[:4]
    valid_password = "Aa1@aaaa"  # meets the minimum requirements
    valid_email = f"bva_{suffix}@example.com"

    # username BVA: exactly 4 characters (minimum valid)
    username_min = f"u{suffix}"  # 4 characters
    reg = tester.register_user(username_min, f"{username_min}@example.com", valid_password)
    check(reg, "BVA1: username length = 4", expected_key="user")

    # username BVA: 3 characters (invalid - too short)
    username_short = "a1_"
    reg = tester.register_user(username_short, f"{username_short}@example.com", valid_password)
    assert "error" in reg, f"BVA2: expected failure for username too short, got {reg}"
    print("BVA2: username too short: PASS")
    tests_passed += 1

    # password BVA: 8 characters (minimum valid)
    valid_min_pass = "Aa1@aaaa"
    reg = tester.register_user(f"bva_minpass_{suffix}", f"bva_minpass_{suffix}@example.com", valid_min_pass)
    check(reg, "BVA3: password length = 8", expected_key="user")

    # password BVA: 7 characters (invalid - too short)
    short_pass = "Aa1@aaa"
    reg = tester.register_user(f"bva_shortpass_{suffix}", f"bva_shortpass_{suffix}@example.com", short_pass)
    assert "error" in reg, f"BVA4: expected failure for password too short, got {reg}"
    print("BVA4: password too short: PASS")
    tests_passed += 1

    # email BVA: valid edge-case email format
    edge_email = f'"weird.but.valid"{suffix}@example.com'
    reg = tester.register_user(f"bva_edgeemail_{suffix}", edge_email, valid_password)
    check(reg, "BVA5: edge-case valid email", expected_key="user")


def main():
    if len(sys.argv) < 2:
        # some help
        print("Usage: python automated.py [get | set | ep | bva ]")
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
        elif mode == "ep":
            test_equivalence_partitioning(tester)
        elif mode == "bva":
            test_boundary_value_analysis(tester)
        else:
            print("invalid mode. choose from: get, set, ep or bva")
            sys.exit(1)
    except AssertionError as e:
        print(f"\nTESTS FAILED after {tests_passed} tests")
        print(e)
        sys.exit(1)
        
    print(f"\nALL TESTS PASSED: {tests_passed} tests completed successfully")

if __name__ == "__main__":
    main()