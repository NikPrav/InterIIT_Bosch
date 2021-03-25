from auth0.v3.authentication import Users

domain = "dev-kqx4v2yr.jp.auth0.com"
myuser = Users(domain).userinfo(TOKEN)
