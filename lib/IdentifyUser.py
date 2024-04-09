import hashlib, os, datetime,mysql.connector, requests
from flask import Flask, redirect, abort, render_template, make_response
from lib.PostgresMySQLLibrary import readSQL, writeSQL
from lib.ReadConfig import readConfig

initConfig = readConfig()

State = "a3d09c625ef90e908d81a55d7dd9c4a9826540d6c2826a9611cbc8b9d7b10d7c"
RedirectURI = initConfig['GoogleIDP']['RedirectURI']
GoogleClientID = initConfig['GoogleIDP']['GoogleClientID']
GoogleClientSecret = initConfig['GoogleIDP']['GoogleClientSecret']
GoogleAuthURL = 'https://accounts.google.com/o/oauth2/auth'
GoogleTokenURL = 'https://oauth2.googleapis.com/token'
GoogleUserInfoURL = 'https://openidconnect.googleapis.com/v1/userinfo'
RedirectURL = f"https://accounts.google.com/o/oauth2/auth?client_id={GoogleClientID}&redirect_uri={RedirectURI}&response_type=code&scope=email%20profile"
RedirectReturn = redirect(f"{RedirectURL}&state={State}", code=302)

def identifyUser(Request,SuccessCallback):
	Token = Request.cookies.get('portal_token')
	Email = Request.cookies.get('portal_user')
	User = readSQL("""SELECT token, timestamp FROM auth WHERE email=%s;""", (Email,))[0]
	if User == []:
		return abort(401)
	if User[0] == Token and datetime.datetime.now() < User[1]:
		if SuccessCallback:
			return SuccessCallback
		else:
			return User
	else:
		return RedirectReturn

def authUser(request):
    if request.args.get('code') and request.args.get('state') == State:
        # Exchange authorization code for access token
        token_response = requests.post(
            url=GoogleTokenURL,
            data={
                'code': request.args.get('code'),
                'client_id': GoogleClientID,
                'client_secret': GoogleClientSecret,
                'redirect_uri': RedirectURI,
                'grant_type': 'authorization_code'
            }
        ).json()
        
        if 'access_token' in token_response:
            # Get user info
            user_info_response = requests.get(
                url=GoogleUserInfoURL,
                headers={'Authorization': f'Bearer {token_response["access_token"]}'}
            ).json()
            # print(user_info_response)
            if user_info_response.get("sub"):  # Check if user info contains sub field
                writeSQL("""UPDATE auth SET token=%s, timestamp=%s, name=%s, picture=%s WHERE email=%s;""", (token_response["access_token"],(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"), user_info_response["name"], user_info_response["picture"],user_info_response["email"],))
                response = make_response(render_template('redirect.html'))
                CookieArray = {"portal_token": [token_response["access_token"],True], "portal_user": [user_info_response["email"],True], "portal_name": [user_info_response["name"],False], "portal_picture": [user_info_response["picture"],False]}
                for Cookie,CookieValue in CookieArray.items():
                    print(CookieValue[1])
                    response.set_cookie(Cookie, value=CookieValue[0], httponly=CookieValue[1], samesite="strict")
                return response
            else:
                return "User info does not contain sub field", 401
        else:
            return "Access token not found in token response", 401
    else:
        print(request.args.get('code'),request.args.get('state'),request.args.get('error'),request.args.get('error_description'))
        return abort(401)